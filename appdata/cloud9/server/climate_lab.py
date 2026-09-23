"""Climate Lab -- "is today normal?" Real answer, not a vibe: NOAA/NCEI
publishes real 1991-2020 daily climate normals (30-year averages) per
station, queryable through NCEI's own real, public, keyless Search and
Data Access services -- confirmed live before writing any code, same
standing rule as every other lab this session. No API key needed,
unlike NCEI's older CDO v2 API.

Two very different real cadences live in one answer here: which
station is nearest and what its normal high/low/average is for today's
calendar date are both stable for the whole day, so they're cached;
today's actual observed temperature changes continuously through the
day, so it's always fetched fresh via the same real NWS current-
conditions call the Current Conditions deck already uses -- caching it
here would mean showing a kid a stale "right now" temperature next to a
live-looking comparison, which is exactly the kind of dishonesty this
project's reliability rules exist to prevent.
"""

import json
import math
import sqlite3
import time
from datetime import date

import requests

import settings
import weather
from paths import DATA_DIR

DB_FILE = DATA_DIR / "climate_lab.db"

# Real station/normal lookup barely changes day to day -- safe to cache
# for a full day, unlike anything GFS-cycle-dependent elsewhere in this
# engine.
CACHE_TTL_SECONDS = 24 * 60 * 60

SEARCH_URL = "https://www.ncei.noaa.gov/access/services/search/v1/data"
DATA_URL = "https://www.ncei.noaa.gov/access/services/data/v1"
HEADERS = {"User-Agent": "Cloud9 Weather Labs (kids learning dashboard)"}

# The daily normals dataset is keyed by month-day, not a real year --
# any leap year works as the placeholder; confirmed live against 2020.
NORMAL_YEAR = 2020


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


def _haversine_miles(lat1, lon1, lat2, lon2):
    r = 3958.8
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _fetch_daily_normal(station_id, month, day):
    """Raises KeyError if this particular station doesn't report
    temperature normals -- real and common for e.g. precipitation-only
    COOP stations, confirmed live (the first "nearest" station tried
    during development turned out to be exactly this case)."""
    date_str = f"{NORMAL_YEAR}-{month:02d}-{day:02d}"
    resp = requests.get(
        DATA_URL,
        params={"dataset": "normals-daily-1991-2020", "stations": station_id, "format": "json", "startDate": date_str, "endDate": date_str},
        headers=HEADERS, timeout=15,
    )
    resp.raise_for_status()
    rows = resp.json()
    if not rows:
        raise LookupError(f"No normal data for {station_id} on {month:02d}-{day:02d}")
    row = rows[0]
    return {
        "highF": round(float(row["DLY-TMAX-NORMAL"]), 1),
        "lowF": round(float(row["DLY-TMIN-NORMAL"]), 1),
        "avgF": round(float(row["DLY-TAVG-NORMAL"]), 1),
    }


def _find_normal(lat, lon, month, day):
    """Real search against NCEI's own station index -- confirmed live
    that `bbox` (not the more obvious `boundingBox`) is the real
    parameter name, and that widening the box is genuinely necessary:
    rural locations can have no normals station within even a full
    degree. Tries real candidates nearest-first, skipping any station
    that turns out not to report temperature normals (real and common
    for precipitation-only COOP stations) rather than trusting the
    single closest result blindly."""
    for radius in (0.5, 1.0, 2.0, 4.0):
        bbox = f"{lat + radius},{lon - radius},{lat - radius},{lon + radius}"
        resp = requests.get(
            SEARCH_URL,
            params={"dataset": "normals-daily-1991-2020", "bbox": bbox, "limit": 25},
            headers=HEADERS, timeout=15,
        )
        resp.raise_for_status()
        results = resp.json().get("results") or []
        candidates = sorted(results, key=lambda r: _haversine_miles(lat, lon, r["centroid"][1], r["centroid"][0]))
        for r in candidates:
            station_id = r["stations"][0]["id"]
            try:
                normal = _fetch_daily_normal(station_id, month, day)
            except (KeyError, LookupError):
                continue
            station = {
                "stationId": station_id,
                "lat": r["centroid"][1],
                "lon": r["centroid"][0],
                "distanceMiles": round(_haversine_miles(lat, lon, r["centroid"][1], r["centroid"][0]), 1),
            }
            return station, normal
    raise LookupError("No nearby station with real temperature normals found")


def _comparison_label(diff_f):
    if diff_f >= 10:
        return "much warmer than normal"
    if diff_f >= 3:
        return "warmer than normal"
    if diff_f <= -10:
        return "much cooler than normal"
    if diff_f <= -3:
        return "cooler than normal"
    return "close to normal"


def get_today_vs_normal():
    config = settings.get_settings()
    lat, lon = config.get("lat"), config.get("lon")
    if lat is None or lon is None:
        return {"status": "unavailable", "reason": "No location set yet - add one in Settings."}

    today = date.today()
    cache_key = f"normal:{round(lat, 2)}:{round(lon, 2)}:{today.month:02d}-{today.day:02d}"
    cached = _get_cached(cache_key)

    if cached and (time.time() - cached["fetchedAt"]) < CACHE_TTL_SECONDS:
        normal_data = cached["data"]
    else:
        try:
            station, normal = _find_normal(lat, lon, today.month, today.day)
            normal_data = {"station": station, "normal": normal}
            _set_cached(cache_key, normal_data)
        except Exception:
            if cached:
                normal_data = cached["data"]
            else:
                return {"status": "unavailable", "reason": "Couldn't reach NOAA's climate normals archive right now."}

    try:
        current = weather.get_current_conditions()
        observed_f = current.get("temperatureF")
    except Exception:
        observed_f = None

    if observed_f is None:
        return {
            "status": "unavailable",
            "reason": "Couldn't get today's real observed temperature to compare.",
            "normal": normal_data["normal"],
            "station": normal_data["station"],
        }

    diff_f = round(observed_f - normal_data["normal"]["avgF"], 1)
    return {
        "status": "valid",
        "date": today.isoformat(),
        "observedF": observed_f,
        "normal": normal_data["normal"],
        "diffF": diff_f,
        "comparisonLabel": _comparison_label(diff_f),
        "station": normal_data["station"],
        "source": "NOAA/NCEI",
        "product": "1991-2020 U.S. Climate Normals (daily)",
        "type": "analysis",
        "retrievedTime": time.time(),
    }
