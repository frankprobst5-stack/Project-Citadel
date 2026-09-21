"""Storm Environment Lab -- built on the Weather Data Engine's GRIB2
pipeline. CAPE, CIN, Lifted Index, Precipitable Water, 0-3km Storm
Relative Helicity, and Storm Motion are all real, direct GFS output
fields (verified live against the real gfs.tXXz.pgrb2.0p25 index before
writing this). K-index/Total Totals/Showalter aren't direct GFS fields
-- confirmed absent from the real GRIB inventory -- so they're not
faked here; they genuinely belong to the Sounding Lab, computed from
real multi-level temperature/moisture profiles, per the locked
architecture doc.

Cached in SQLite: a GFS cycle only updates every 6 hours, and the real
decode pipeline (network fetch + cfgrib decode) is real work worth not
repeating on every page view -- same reasoning as weather_cache.py and
school_library.py's own caches.
"""

import json
import sqlite3
import time

import settings
import weather_data_engine
from paths import DATA_DIR

DB_FILE = DATA_DIR / "storm_environment.db"

# A GFS cycle is real for 6 hours; refresh a bit more often than that
# so a family opening this mid-cycle still sees the current one instead
# of an ever-slightly-stale cached read.
CACHE_TTL_SECONDS = 3 * 60 * 60


def _connect():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                name TEXT PRIMARY KEY,
                fetched_at REAL NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )


_init_db()


def _get_cached(name):
    with _connect() as conn:
        row = conn.execute(
            "SELECT fetched_at, payload FROM metrics WHERE name = ?", (name,)
        ).fetchone()
    if not row:
        return None
    return {"fetchedAt": row[0], "data": json.loads(row[1])}


def _set_cached(name, data):
    with _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO metrics (name, fetched_at, payload) VALUES (?, ?, ?)",
            (name, time.time(), json.dumps(data)),
        )


def _get_location():
    config = settings.get_settings()
    return config.get("lat"), config.get("lon")


def _get_metric(cache_key, fetch_fn):
    """Shared fetch/cache/fallback shape for every Storm Environment
    metric -- honestly returns `status: unavailable` (never a guessed
    number) if no location is set or every real GFS attempt failed,
    falling back to the last real cached value, clearly marked stale,
    if one exists."""
    lat, lon = _get_location()
    if lat is None or lon is None:
        return {"status": "unavailable", "reason": "No location set yet - add one in Settings."}

    cached = _get_cached(cache_key)
    if cached and (time.time() - cached["fetchedAt"]) < CACHE_TTL_SECONDS:
        return dict(cached["data"], stale=False)

    try:
        result = fetch_fn(lat, lon)
        _set_cached(cache_key, result)
        return dict(result, stale=False)
    except Exception:
        if cached:
            age_hours = (time.time() - cached["fetchedAt"]) / 3600
            return dict(cached["data"], stale=True, ageHours=round(age_hours, 1))
        return {"status": "unavailable", "reason": "Couldn't reach NOAA's model data right now."}


def get_cape():
    return _get_metric("cape", lambda lat, lon: weather_data_engine.get_gridded_value(
        name="CAPE", variable="CAPE", var_key="cape", level_param="lev_surface",
        unit="J/kg", lat=lat, lon=lon,
    ))


def get_cin():
    return _get_metric("cin", lambda lat, lon: weather_data_engine.get_gridded_value(
        name="CIN", variable="CIN", var_key="cin", level_param="lev_surface",
        unit="J/kg", lat=lat, lon=lon,
    ))


def get_lifted_index():
    return _get_metric("lifted_index", lambda lat, lon: weather_data_engine.get_gridded_value(
        name="Lifted Index", variable="LFTX", var_key="lftx", level_param="lev_surface",
        unit="°C", lat=lat, lon=lon,
    ))


def get_precipitable_water():
    return _get_metric("pwat", lambda lat, lon: weather_data_engine.get_gridded_value(
        name="Precipitable Water", variable="PWAT", var_key="pwat",
        level_param="lev_entire_atmosphere_(considered_as_a_single_layer)",
        unit="mm", lat=lat, lon=lon,
    ))


def get_storm_relative_helicity():
    return _get_metric("srh", lambda lat, lon: weather_data_engine.get_gridded_value(
        name="0-3km Storm Relative Helicity", variable="HLCY", var_key="hlcy",
        level_param="lev_3000-0_m_above_ground", unit="m²/s²", lat=lat, lon=lon,
    ))


def get_storm_motion():
    return _get_metric("storm_motion", lambda lat, lon: weather_data_engine.get_gridded_vector(
        name="Storm Motion", variable_u="USTM", variable_v="VSTM",
        var_key_u="ustm", var_key_v="vstm",
        level_param="lev_6000-0_m_above_ground", lat=lat, lon=lon,
    ))


def get_all():
    return {
        "cape": get_cape(),
        "cin": get_cin(),
        "liftedIndex": get_lifted_index(),
        "precipitableWater": get_precipitable_water(),
        "stormRelativeHelicity": get_storm_relative_helicity(),
        "stormMotion": get_storm_motion(),
    }
