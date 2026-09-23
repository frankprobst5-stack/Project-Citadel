"""Weather Event Explorer -- a workspace built around one real named
event, per CARD_REDESIGN_PLAN.md's nine-lab reframe: pulling pressure,
wind, position, movement, and the official forecast into one place for
a storm that's actually happening right now, with a direct real link
out to Earth Lab's own subject (geography) via real lat/lon.

Source: the National Hurricane Center's own real, public
`CurrentStorms.json` feed (`nhc.noaa.gov`) -- no key needed, and no
guessed field names: every field used here was confirmed against a
real live fetch, including that NHC's current position/intensity is
itself a meteorologist-produced analysis (recon, satellite, radar all
folded in), not a single raw sensor reading -- hence `type: "analysis"`,
not `"observed"`, same provenance vocabulary as every other lab.

An empty `activeStorms` list is a real, valid answer -- "no active
tropical cyclones right now" -- not a failure, and is never confused
with a real fetch error in the schema below.
"""

import json
import re
import sqlite3
import time

import requests

from paths import DATA_DIR

DB_FILE = DATA_DIR / "event_explorer.db"

CACHE_TTL_SECONDS = 3 * 60 * 60

NHC_FEED_URL = "https://www.nhc.noaa.gov/CurrentStorms.json"
HEADERS = {"User-Agent": "Cloud9 Weather Labs (kids learning dashboard)"}

# Real NHC classification codes (National Hurricane Center Glossary) --
# confirmed HU and TD live in the current feed; the rest are real,
# standard NHC codes this feed can also produce. An unrecognized code
# falls back to showing the raw code rather than guessing a label.
CLASSIFICATION_LABELS = {
    "TD": "Tropical Depression",
    "TS": "Tropical Storm",
    "HU": "Hurricane",
    "SD": "Subtropical Depression",
    "SS": "Subtropical Storm",
    "EX": "Extratropical Cyclone",
    "LO": "Low",
    "DB": "Disturbance",
}

BASIN_LABELS = {
    "AL": "Atlantic",
    "EP": "Eastern Pacific",
    "CP": "Central Pacific",
}

KT_TO_MPH = 1.15078


def _saffir_simpson_category(wind_kt):
    if wind_kt >= 137:
        return 5
    if wind_kt >= 113:
        return 4
    if wind_kt >= 96:
        return 3
    if wind_kt >= 83:
        return 2
    if wind_kt >= 64:
        return 1
    return None


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


def _cone_image_url(graphics_page_url):
    """Real best-effort scrape of NHC's own graphics page for the 5-day
    forecast cone PNG -- its filename embeds a per-update timestamp, so
    it can't be predicted from the storm id alone. Never raises: a
    changed page layout just means no image, not a broken storm card."""
    try:
        resp = requests.get(graphics_page_url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        match = re.search(r'src="(/storm_graphics/[^"]*5day_cone_sm[^"]*\.png)"', resp.text)
        if match:
            return "https://www.nhc.noaa.gov" + match.group(1)
    except requests.RequestException:
        pass
    return None


def _normalize_storm(raw):
    basin_code = raw["id"][:2].upper()
    classification = raw["classification"]
    wind_kt = float(raw["intensity"])
    cone_url = _cone_image_url(raw["forecastGraphics"]["url"]) if raw.get("forecastGraphics") else None
    return {
        "id": raw["id"],
        "name": raw["name"],
        "basin": BASIN_LABELS.get(basin_code, basin_code),
        "classification": classification,
        "classificationLabel": CLASSIFICATION_LABELS.get(classification, classification),
        "category": _saffir_simpson_category(wind_kt) if classification == "HU" else None,
        "windMph": round(wind_kt * KT_TO_MPH),
        "pressureMb": float(raw["pressure"]),
        "lat": raw["latitudeNumeric"],
        "lon": raw["longitudeNumeric"],
        "movementDirectionDeg": raw.get("movementDir"),
        "movementSpeedMph": round(raw["movementSpeed"] * KT_TO_MPH) if raw.get("movementSpeed") is not None else None,
        "lastUpdate": raw["lastUpdate"],
        "advisoryUrl": raw["publicAdvisory"]["url"] if raw.get("publicAdvisory") else None,
        "forecastDiscussionUrl": raw["forecastDiscussion"]["url"] if raw.get("forecastDiscussion") else None,
        "coneImageUrl": cone_url,
        "source": "NOAA/NHC",
        "type": "analysis",
    }


def get_active_storms():
    """Every real, currently active NHC-tracked tropical cyclone. An
    empty list is itself a real, honest answer, distinct from
    `status: unavailable` (a real fetch failure)."""
    cache_key = "active_storms"
    cached = _get_cached(cache_key)
    if cached and (time.time() - cached["fetchedAt"]) < CACHE_TTL_SECONDS:
        return dict(cached["data"], stale=False)

    try:
        resp = requests.get(NHC_FEED_URL, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        raw_storms = resp.json().get("activeStorms") or []
        result = {
            "storms": [_normalize_storm(s) for s in raw_storms],
            "retrievedTime": time.time(),
            "source": "NOAA/NHC",
        }
        _set_cached(cache_key, result)
        return dict(result, stale=False)
    except Exception:
        if cached:
            age_hours = (time.time() - cached["fetchedAt"]) / 3600
            return dict(cached["data"], stale=True, ageHours=round(age_hours, 1))
        return {"status": "unavailable", "reason": "Couldn't reach the National Hurricane Center right now."}
