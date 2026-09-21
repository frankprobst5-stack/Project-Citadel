"""Storm Environment Lab -- the first real lab built on the Weather Data
Engine's GRIB2 pipeline. Scoped to CAPE for this first pass (the metric
the original plan named, and the one already verified end to end); the
same pattern extends to CIN/LI/K-index/SRH/PWAT later without changing
the engine underneath.

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


def get_cape():
    """Real CAPE (Convective Available Potential Energy) at the family's
    configured location, via the Weather Data Engine. Honestly returns
    `status: unavailable` (never a guessed number) if no location is set
    or every real GFS cycle attempt failed -- falls back to the last
    real cached value, clearly marked stale, if one exists."""
    config = settings.get_settings()
    lat, lon = config.get("lat"), config.get("lon")
    if lat is None or lon is None:
        return {"status": "unavailable", "reason": "No location set yet - add one in Settings."}

    cached = _get_cached("cape")
    if cached and (time.time() - cached["fetchedAt"]) < CACHE_TTL_SECONDS:
        return dict(cached["data"], stale=False)

    try:
        result = weather_data_engine.get_gridded_value(
            name="CAPE",
            variable="CAPE",
            var_key="cape",
            level_param="lev_surface",
            unit="J/kg",
            lat=lat,
            lon=lon,
            product_type="model",
        )
        _set_cached("cape", result)
        return dict(result, stale=False)
    except Exception:
        if cached:
            age_hours = (time.time() - cached["fetchedAt"]) / 3600
            return dict(cached["data"], stale=True, ageHours=round(age_hours, 1))
        return {"status": "unavailable", "reason": "Couldn't reach NOAA's model data right now."}
