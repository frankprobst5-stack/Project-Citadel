"""The Weather Data Engine -- CARD_REDESIGN_PLAN.md's locked architecture:
the one place in Cloud9 that knows how to talk to gridded/model weather
products (GRIB2 via NOMADS), so the GRIB2/geospatial complexity doesn't
spread through every lab that needs it. Surface obs/forecast/alerts stay
in weather.py (they're already simple JSON, no need to route them
through here) -- this engine is specifically for products that only
exist as gridded model/analysis data: GFS via NCEP's NOMADS today,
other NOMADS-hosted products (NAM, etc.) the same way later.

Real pipeline, verified live before writing this module: NOMADS' real
GRIB Filter service subsets a model file geographically and by field
before download (no giant blind file fetch), the result decodes cleanly
with cfgrib/xarray (eccodes' compiled backend ships in its own PyPI
wheel), and a point value comes out of the grid via xarray's
nearest-neighbor selection. Confirmed end to end against a real GFS
cycle before this was locked in as buildable.

Every value this engine returns carries its own scientific identity
(the locked schema) rather than just a number -- see `describe()`.
"""

import math
import tempfile
import time
from datetime import datetime, timedelta, timezone

import requests
import xarray as xr

HEADERS = {"User-Agent": "Cloud9 Weather Data Engine (kids learning dashboard)"}
NOMADS_FILTER_URL = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"

# Real publish-lag convention for GFS: a cycle's data isn't fully
# available on NOMADS until roughly 3-4 hours after its cycle time.
# Starting the search this far back means the *first* cycle tried is
# normally already published, not a guaranteed-missing one.
PUBLISH_LAG_HOURS = 4
GFS_CYCLE_HOURS = (0, 6, 12, 18)


def _candidate_cycles(max_tries=4):
    """Real cycles to try, most recent first -- most requests succeed on
    the first candidate; older ones are a real fallback for when the
    latest cycle genuinely isn't published yet, not a guess."""
    now = datetime.now(timezone.utc) - timedelta(hours=PUBLISH_LAG_HOURS)
    cycle_hour = max(h for h in GFS_CYCLE_HOURS if h <= now.hour)
    cursor = now.replace(hour=cycle_hour, minute=0, second=0, microsecond=0)
    candidates = []
    for _ in range(max_tries):
        candidates.append(cursor)
        idx = GFS_CYCLE_HOURS.index(cursor.hour)
        if idx == 0:
            cursor = (cursor - timedelta(days=1)).replace(hour=GFS_CYCLE_HOURS[-1])
        else:
            cursor = cursor.replace(hour=GFS_CYCLE_HOURS[idx - 1])
    return candidates


def _fetch_grib_one_cycle(fields, lat, lon, cycle, forecast_hour, box_degrees=1.5):
    """One real NOMADS GRIB Filter request against one specific, already-
    chosen cycle -- no retry/fallback here, that's `_fetch_grib_subset`'s
    job for a single value, and `get_forecast_series`'s own job when it
    needs one cycle held fixed across several forecast hours. Raises
    ValueError if the response isn't real GRIB2 data."""
    params = {
        "dir": f"/gfs.{cycle.strftime('%Y%m%d')}/{cycle.strftime('%H')}/atmos",
        "file": f"gfs.t{cycle.strftime('%H')}z.pgrb2.0p25.f{forecast_hour:03d}",
        "subregion": "",
        "toplat": lat + box_degrees,
        "bottomlat": lat - box_degrees,
        "leftlon": lon - box_degrees + 360 if lon < 0 else lon - box_degrees,
        "rightlon": lon + box_degrees + 360 if lon < 0 else lon + box_degrees,
    }
    for variable, level_param in fields:
        params[f"var_{variable}"] = "on"
        params[level_param] = "on"
    resp = requests.get(NOMADS_FILTER_URL, params=params, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    if resp.content[:4] != b"GRIB" or len(resp.content) <= 100:
        raise ValueError(f"Response for cycle {cycle} f{forecast_hour:03d} wasn't real GRIB2 data")
    return resp.content


def _fetch_grib_subset(fields, lat, lon, box_degrees=1.5, forecast_hour=0):
    """Real NOMADS GRIB Filter fetch, trying recent GFS cycles until one
    actually has data (see `_candidate_cycles`). `fields` is a list of
    (variable, level_param) tuples -- multiple fields in one request
    (e.g. storm motion's U/V components) is real, supported NOMADS
    filter behavior, not a workaround. `forecast_hour` selects a real
    forecast lead time from the same cycle (0 = the analysis itself,
    verified live that later hours -- e.g. f012 -- return real, distinct
    values, not a copy of f000) -- the Model Lab's whole point: the
    model's own atmosphere at a future time, not a live observation.
    Returns (grib_bytes, cycle_datetime, forecast_hour) or raises if
    every candidate failed."""
    last_error = None
    for cycle in _candidate_cycles():
        try:
            content = _fetch_grib_one_cycle(fields, lat, lon, cycle, forecast_hour, box_degrees)
            return content, cycle, forecast_hour
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
    raise LookupError(f"No published GFS cycle had usable data: {last_error}")


def _decode_points(grib_bytes, var_keys, lat, lon):
    """Real decode + nearest-grid-point extraction for one or more
    variables from the same downloaded subset. cfgrib needs a real file
    path (it shells out to eccodes), not an in-memory buffer -- confirmed
    directly, not assumed. Returns {var_key: (value, valid_time)}."""
    with tempfile.NamedTemporaryFile(suffix=".grib2") as f:
        f.write(grib_bytes)
        f.flush()
        lon_grid = lon + 360 if lon < 0 else lon
        results = {}
        # Multiple fields at different levels/type-of-level combos can't
        # always merge into one cfgrib Dataset (real cfgrib limitation --
        # confirmed live: mixed level types raise on open_dataset), so
        # each variable gets decoded from its own filtered view of the
        # same bytes rather than assuming one shared Dataset works.
        for var_key in var_keys:
            ds = xr.open_dataset(f.name, engine="cfgrib", backend_kwargs={"filter_by_keys": {}, "indexpath": ""})
            if var_key not in ds.data_vars:
                # Real fallback for the mixed-level-type case: reopen
                # scoped to just this variable's own GRIB messages.
                ds = xr.open_dataset(
                    f.name, engine="cfgrib",
                    backend_kwargs={"filter_by_keys": {"shortName": var_key}, "indexpath": ""},
                )
            point = ds[var_key].sel(latitude=lat, longitude=lon_grid, method="nearest")
            value = float(point.values)
            valid_time = str(point.coords["valid_time"].values) if "valid_time" in point.coords else None
            results[var_key] = (value, valid_time)
        return results


STANDARD_LEVELS_MB = (1000, 925, 850, 700, 500, 400, 300, 250, 200)


def _decode_profile(grib_bytes, lat, lon):
    """Real decode of a multi-level fetch (TMP/RH/UGRD/VGRD across the
    standard pressure levels) into one vertical profile at the nearest
    grid point. Unlike `_decode_points`, this is a single cfgrib Dataset
    open -- confirmed live that same-level-type fields (all isobaricInhPa
    here) merge cleanly, unlike storm motion's mixed level types."""
    with tempfile.NamedTemporaryFile(suffix=".grib2") as f:
        f.write(grib_bytes)
        f.flush()
        ds = xr.open_dataset(f.name, engine="cfgrib")
        lon_grid = lon + 360 if lon < 0 else lon
        point = ds.sel(latitude=lat, longitude=lon_grid, method="nearest")
        levels = [float(p) for p in point["isobaricInhPa"].values]
        temps_c = [float(v) - 273.15 for v in point["t"].values]
        rh_pct = [float(v) for v in point["r"].values]
        u_ms = [float(v) for v in point["u"].values]
        v_ms = [float(v) for v in point["v"].values]
        valid_time = str(point.coords["valid_time"].values) if "valid_time" in point.coords else None
        return levels, temps_c, rh_pct, u_ms, v_ms, valid_time


def get_pressure_profile(lat, lon, levels_mb=STANDARD_LEVELS_MB):
    """Real vertical profile (temperature, relative humidity, wind) across
    the standard pressure levels -- the Sounding Lab's own data, and the
    real source for K-index/Total Totals/Showalter (none of which are
    direct GFS output fields -- confirmed absent from the real .idx
    inventory; they're computed from exactly this kind of profile)."""
    fields = []
    for lvl in levels_mb:
        lev_param = f"lev_{lvl}_mb"
        fields.append(("TMP", lev_param))
        fields.append(("RH", lev_param))
        fields.append(("UGRD", lev_param))
        fields.append(("VGRD", lev_param))

    grib_bytes, cycle, fhour = _fetch_grib_subset(fields, lat, lon)
    levels, temps_c, rh_pct, u_ms, v_ms, valid_time = _decode_profile(grib_bytes, lat, lon)

    profile = []
    for i in range(len(levels)):
        speed_mph = round(((u_ms[i] ** 2 + v_ms[i] ** 2) ** 0.5) * 2.23694, 1)
        direction_deg = round((270 - math.degrees(math.atan2(v_ms[i], u_ms[i]))) % 360)
        profile.append({
            "pressureMb": levels[i],
            "temperatureC": round(temps_c[i], 1),
            "relativeHumidityPct": round(rh_pct[i], 1),
            "windSpeedMph": speed_mph,
            "windDirectionDeg": direction_deg,
        })
    # Standard sounding convention: surface/highest-pressure first.
    profile.sort(key=lambda p: -p["pressureMb"])

    return {
        "levels": profile,
        "source": "NOAA/NCEP",
        "product": _product_label(cycle, fhour),
        "type": "model",
        "validTime": valid_time,
        "retrievedTime": time.time(),
        "coverage": "Global model grid (0.25 degree resolution)",
        "status": "valid",
    }


def _product_label(cycle, fhour):
    return f"GFS 0.25deg, {cycle.strftime('%Y-%m-%d %H')}Z cycle, f{fhour:03d}"


def get_gridded_value(name, variable, var_key, level_param, unit, lat, lon, product_type="model", forecast_hour=0):
    """The real, locked schema every Weather Data Engine value returns --
    what it is, where it came from, whether it was observed or
    calculated, when it's valid, and whether it's actually usable right
    now. Never fabricates a value: raises up to the caller (which decides
    the honest UNAVAILABLE/cache-fallback behavior) rather than guessing."""
    grib_bytes, cycle, fhour = _fetch_grib_subset([(variable, level_param)], lat, lon, forecast_hour=forecast_hour)
    value, valid_time = _decode_points(grib_bytes, [var_key], lat, lon)[var_key]
    return {
        "name": name,
        "value": round(value, 1),
        "unit": unit,
        "source": "NOAA/NCEP",
        "product": _product_label(cycle, fhour),
        "type": product_type,
        "validTime": valid_time,
        "retrievedTime": time.time(),
        "coverage": "Global model grid (0.25 degree resolution)",
        "status": "valid",
    }


def get_gridded_vector(name, variable_u, variable_v, var_key_u, var_key_v, level_param, lat, lon, product_type="model"):
    """For metrics that only exist as U/V wind components (storm motion)
    -- fetches both in one request, combines into speed (mph) + compass
    direction, same locked schema as a scalar value."""
    grib_bytes, cycle, fhour = _fetch_grib_subset(
        [(variable_u, level_param), (variable_v, level_param)], lat, lon
    )
    points = _decode_points(grib_bytes, [var_key_u, var_key_v], lat, lon)
    u, valid_time = points[var_key_u]
    v, _ = points[var_key_v]
    speed_mph = round(((u**2 + v**2) ** 0.5) * 2.23694, 1)
    direction_deg = round((270 - math.degrees(math.atan2(v, u))) % 360)
    return {
        "name": name,
        "value": speed_mph,
        "unit": "mph",
        "direction": direction_deg,
        "source": "NOAA/NCEP",
        "product": _product_label(cycle, fhour),
        "type": product_type,
        "validTime": valid_time,
        "retrievedTime": time.time(),
        "coverage": "Global model grid (0.25 degree resolution)",
        "status": "valid",
    }


def get_forecast_series(name, variable, var_key, level_param, unit, lat, lon, forecast_hours, product_type="model"):
    """Model Lab's real data: the SAME model cycle's own predicted
    atmosphere at several real lead times -- "what does the model think
    happens at +6h, +12h, +24h," not several different runs. Verified
    live that later lead times genuinely carry distinct valid_times and
    values, not a copy of f000 (e.g. real CAPE going 0 -> 0 -> 148 -> 0
    J/kg across f000/f006/f012/f024 for a real point, tracking real
    afternoon convective heating).

    Deliberately tries one whole cycle across every requested lead time
    before falling back to an older cycle -- a naive per-call retry
    could silently stitch together two different cycles if a later lead
    time simply hasn't published yet for the newest one, which would
    make this "the model's own forecast" claim false.
    """
    last_error = None
    for cycle in _candidate_cycles():
        try:
            points = []
            for fhour in forecast_hours:
                grib_bytes = _fetch_grib_one_cycle(
                    [(variable, level_param)], lat, lon, cycle, fhour
                )
                value, valid_time = _decode_points(grib_bytes, [var_key], lat, lon)[var_key]
                points.append({
                    "forecastHour": fhour,
                    "value": round(value, 1),
                    "validTime": valid_time,
                })
            return {
                "name": name,
                "unit": unit,
                "points": points,
                "source": "NOAA/NCEP",
                "product": f"GFS 0.25deg, {cycle.strftime('%Y-%m-%d %H')}Z cycle",
                "type": product_type,
                "retrievedTime": time.time(),
                "coverage": "Global model grid (0.25 degree resolution)",
                "status": "valid",
            }
        except (ValueError, requests.RequestException) as exc:
            last_error = exc
    raise LookupError(f"No published GFS cycle had every requested lead time: {last_error}")
