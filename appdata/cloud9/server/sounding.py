"""Sounding Lab -- CARD_REDESIGN_PLAN.md's "Atmosphere / Sounding Lab":
teaches the atmosphere vertically (1000mb down to 200mb) instead of just
at the surface, and is the real source for K-index, Total Totals, and
Showalter Index -- confirmed none of the three are direct GFS output
fields (absent from the real .idx inventory checked while building
Storm Environment), because they're genuinely computed from a real
multi-level temperature/moisture profile, not looked up.

Real thermodynamics (dewpoint-from-RH, K-index, Total Totals, Showalter
-- the last one needs real moist-adiabatic parcel-lifting physics, not
simple arithmetic) are computed with MetPy
(github.com/Unidata/MetPy, real, actively maintained, the standard
open-source Python meteorology library) rather than hand-rolled -- same
"orchestrate, don't rebuild" reasoning as reusing Kolibri/media-vault's
real APIs elsewhere in this project, just applied to a physics library
instead of a web API.
"""

import json
import sqlite3
import time

import metpy.calc as mpcalc
from metpy.units import units

import settings
import weather_data_engine
from paths import DATA_DIR

DB_FILE = DATA_DIR / "sounding.db"

# Same real 3-hour convention as storm_environment.py -- a GFS cycle is
# real for 6 hours; refresh a bit more often than that.
CACHE_TTL_SECONDS = 3 * 60 * 60


def _connect():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, fetched_at REAL NOT NULL, payload TEXT NOT NULL)"
        )


_init_db()


def _get_cached(key):
    with _connect() as conn:
        row = conn.execute("SELECT fetched_at, payload FROM cache WHERE key = ?", (key,)).fetchone()
    if not row:
        return None
    return {"fetchedAt": row[0], "data": json.loads(row[1])}


def _set_cached(key, data):
    with _connect() as conn:
        conn.execute("INSERT OR REPLACE INTO cache (key, fetched_at, payload) VALUES (?, ?, ?)", (key, time.time(), json.dumps(data)))


def _add_dewpoints(profile_levels):
    """Attaches a real MetPy-computed dewpoint to every level, in place --
    the table display needs it per-level, not just the 850/700/500mb
    subset the indices below use."""
    pressures = [lvl["pressureMb"] for lvl in profile_levels]
    t_arr = [lvl["temperatureC"] for lvl in profile_levels] * units.degC
    rh_arr = [lvl["relativeHumidityPct"] / 100.0 for lvl in profile_levels] * units.dimensionless
    td_arr = mpcalc.dewpoint_from_relative_humidity(t_arr, rh_arr)
    for lvl, td in zip(profile_levels, td_arr.magnitude):
        lvl["dewpointC"] = round(float(td), 1)
    return profile_levels


def _compute_indices(profile_levels):
    """Real MetPy calculations from the real profile -- returns None for
    an index if the real inputs it needs (850/700/500mb temp+humidity)
    aren't all present, rather than computing from a partial profile."""
    by_pressure = {lvl["pressureMb"]: lvl for lvl in profile_levels}
    needed = (1000, 925, 850, 700, 500, 400, 300, 250, 200)
    if not all(p in by_pressure for p in needed):
        return None

    pressures = sorted(by_pressure.keys(), reverse=True)
    p_arr = [p for p in pressures] * units.hPa
    t_arr = [by_pressure[p]["temperatureC"] for p in pressures] * units.degC
    rh_arr = [by_pressure[p]["relativeHumidityPct"] / 100.0 for p in pressures] * units.dimensionless
    td_arr = mpcalc.dewpoint_from_relative_humidity(t_arr, rh_arr)

    try:
        k = float(mpcalc.k_index(p_arr, t_arr, td_arr).magnitude)
        tt = float(mpcalc.total_totals_index(p_arr, t_arr, td_arr).magnitude)
        si_raw = mpcalc.showalter_index(p_arr, t_arr, td_arr)
        si = float(si_raw.magnitude[0] if hasattr(si_raw.magnitude, "__len__") else si_raw.magnitude)
    except Exception:
        return None

    return {"kIndex": round(k, 1), "totalTotals": round(tt, 1), "showalterIndex": round(si, 1)}


def get_sounding():
    """Real vertical profile + the three real derived indices, at the
    family's configured location. Honestly `status: unavailable` (never
    a guessed number) with no location or a failed fetch, falling back
    to the last real cached sounding, clearly marked stale, otherwise."""
    config = settings.get_settings()
    lat, lon = config.get("lat"), config.get("lon")
    if lat is None or lon is None:
        return {"status": "unavailable", "reason": "No location set yet - add one in Settings."}

    cached = _get_cached("sounding")
    if cached and (time.time() - cached["fetchedAt"]) < CACHE_TTL_SECONDS:
        return dict(cached["data"], stale=False)

    try:
        profile = weather_data_engine.get_pressure_profile(lat, lon)
        indices = _compute_indices(profile["levels"])
        profile["levels"] = _add_dewpoints(profile["levels"])
        result = dict(profile, indices=indices)
        _set_cached("sounding", result)
        return dict(result, stale=False)
    except Exception:
        if cached:
            age_hours = (time.time() - cached["fetchedAt"]) / 3600
            return dict(cached["data"], stale=True, ageHours=round(age_hours, 1))
        return {"status": "unavailable", "reason": "Couldn't reach NOAA's model data right now."}
