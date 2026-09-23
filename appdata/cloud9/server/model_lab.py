"""Model Lab -- CARD_REDESIGN_PLAN.md's real teaching goal: observation
!= analysis != forecast model != forecast. Shows the SAME real GFS
cycle's own predicted atmosphere at several real lead times (+0/+6/+12/
+24/+48/+72h), matching Frank's own lesson shape directly: "show today's
observed atmosphere, then the model's atmosphere 6/12/24 hours from
now."

Scoped to CAPE for this first pass -- the same metric already proven
end to end in Storm Environment, and a real, honest choice for this
lesson specifically: CAPE's real diurnal swing (verified live: a real
point going 0 -> 520 -> 34 -> 0 J/kg across a single afternoon) is a
much more vivid "watch the model's story unfold" example than a
slower-moving field like pressure would be.
"""

import json
import sqlite3
import time

import settings
import weather_data_engine
from paths import DATA_DIR

DB_FILE = DATA_DIR / "model_lab.db"

FORECAST_HOURS = (0, 6, 12, 24, 48, 72)

# Same real 3-hour convention as storm_environment.py/sounding.py.
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


def get_cape_forecast():
    """Real CAPE forecast series at the family's configured location.
    Honestly `status: unavailable` (never a guessed number) with no
    location set or every real GFS cycle attempt failed, falling back to
    the last real cached series, clearly marked stale, otherwise."""
    config = settings.get_settings()
    lat, lon = config.get("lat"), config.get("lon")
    if lat is None or lon is None:
        return {"status": "unavailable", "reason": "No location set yet - add one in Settings."}

    cached = _get_cached("cape_forecast")
    if cached and (time.time() - cached["fetchedAt"]) < CACHE_TTL_SECONDS:
        return dict(cached["data"], stale=False)

    try:
        result = weather_data_engine.get_forecast_series(
            name="CAPE", variable="CAPE", var_key="cape", level_param="lev_surface",
            unit="J/kg", lat=lat, lon=lon, forecast_hours=FORECAST_HOURS,
        )
        _set_cached("cape_forecast", result)
        return dict(result, stale=False)
    except Exception:
        if cached:
            age_hours = (time.time() - cached["fetchedAt"]) / 3600
            return dict(cached["data"], stale=True, ageHours=round(age_hours, 1))
        return {"status": "unavailable", "reason": "Couldn't reach NOAA's model data right now."}
