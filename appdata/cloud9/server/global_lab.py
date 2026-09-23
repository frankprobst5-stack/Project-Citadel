"""Global Weather Lab -- the "Planet" rung of the scale ladder from
CARD_REDESIGN_PLAN.md's nine-lab reframe: My Location -> Region ->
United States -> Hemisphere -> Planet. Every other lab in Weather Labs
only ever asks the Weather Data Engine about one point (the family's
own home). GFS is a real whole-Earth model, so the SAME engine already
works anywhere on the planet -- this lab is the first one to actually
ask it to.

Six real preset points, deliberately chosen to span both hemispheres
and the equator so the lesson is a real, current fact rather than a
map decoration: on 2026-09-23 (the real autumnal equinox), the Northern
Hemisphere locations are entering fall while the Southern Hemisphere
ones are entering spring -- same planet, same physics, opposite
seasons, visible directly in the real numbers below.
"""

import json
import sqlite3
import time

import settings
import weather_data_engine
from paths import DATA_DIR

DB_FILE = DATA_DIR / "global_lab.db"

CACHE_TTL_SECONDS = 3 * 60 * 60

GLOBAL_LOCATIONS = (
    {"id": "fairbanks", "name": "Fairbanks, Alaska, USA", "hemisphere": "Northern — high latitude", "lat": 64.8378, "lon": -147.7164},
    {"id": "miami", "name": "Miami, Florida, USA", "hemisphere": "Northern — subtropical", "lat": 25.7617, "lon": -80.1918},
    {"id": "quito", "name": "Quito, Ecuador", "hemisphere": "Equatorial", "lat": -0.1807, "lon": -78.4678},
    {"id": "nairobi", "name": "Nairobi, Kenya", "hemisphere": "Southern — near equator", "lat": -1.2921, "lon": 36.8219},
    {"id": "sydney", "name": "Sydney, Australia", "hemisphere": "Southern — mid-latitude", "lat": -33.8688, "lon": 151.2093},
    {"id": "ushuaia", "name": "Ushuaia, Argentina", "hemisphere": "Southern — high latitude", "lat": -54.8019, "lon": -68.3030},
)


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


def _fetch_point(location):
    try:
        snapshot = weather_data_engine.get_global_snapshot(location["lat"], location["lon"])
        return dict(location, **snapshot)
    except Exception as exc:
        return dict(location, status="unavailable", reason=f"Couldn't reach NOAA's model data for this point: {exc}")


def get_all():
    """Every real preset point, plus the family's own home location
    (labeled from Settings) as the ladder's first rung when one is
    configured. Each point succeeds or fails independently -- one
    unreachable point never blanks out the rest."""
    cache_key = "global_snapshot"
    cached = _get_cached(cache_key)
    if cached and (time.time() - cached["fetchedAt"]) < CACHE_TTL_SECONDS:
        return dict(cached["data"], stale=False)

    try:
        config = settings.get_settings()
        locations = list(GLOBAL_LOCATIONS)
        if config.get("lat") is not None and config.get("lon") is not None:
            locations = [{
                "id": "home",
                "name": config.get("location_label") or "My Location",
                "hemisphere": "My Location",
                "lat": config["lat"],
                "lon": config["lon"],
            }] + locations

        result = {"points": [_fetch_point(loc) for loc in locations]}
        _set_cached(cache_key, result)
        return dict(result, stale=False)
    except Exception:
        if cached:
            age_hours = (time.time() - cached["fetchedAt"]) / 3600
            return dict(cached["data"], stale=True, ageHours=round(age_hours, 1))
        return {"status": "unavailable", "reason": "Couldn't reach NOAA's model data right now."}
