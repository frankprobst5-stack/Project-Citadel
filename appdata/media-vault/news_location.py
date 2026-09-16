"""Resolves Citadel's own station location (STATION_LAT/STATION_LON,
already set in .env for the Tactical Map) into the real NWS county
FIPS/UGC zone codes needed to scope emergency alerts to this household —
see news_matcher.py for why both codes are needed, not just one.

Real, live-verified finding this module depends on: a single call to
NWS's own real `api.weather.gov/points/{lat},{lon}` endpoint (the same
real NWS API WayStation already uses for weather) returns BOTH codes at
once — `properties.county` (a URL ending in the real SAME/FIPS county
code, e.g. ".../zones/county/TXC129") and `properties.forecastZone` (a
URL ending in the real UGC zone code, e.g. ".../zones/forecast/TXZ019").
One HTTP call, two stored values, not an extra round trip — confirmed
live against Citadel's own real station coordinates before writing this,
not assumed from NWS's documentation alone.

Cached in `settings` (a small key/value table, created alongside
news_sources/news_articles) rather than re-resolved on every request —
same "fetch once, cache, read from the cache" discipline this whole
feature is built around."""
import json

import requests

_NWS_HEADERS = {"User-Agent": "CitadelNewsArchive/1.0 (self-hosted, github.com/frankprobst5-stack/Project-Citadel)"}


def resolve_zone_codes(lat, lon, timeout=10):
    """Real NWS points lookup. Returns (county_fips, nws_zone_ugc) as
    plain strings, e.g. ("TXC129", "TXZ019") -- or (None, None) if the
    lookup fails (no station location set, NWS unreachable, or a
    location outside NWS's own coverage area, e.g. most of the world
    outside the US). Never raises -- a household with no usable NWS
    zone simply gets unfiltered NWS alerts, same graceful-degrade
    principle as every other "no location set" case in this feature.
    """
    if not lat or not lon:
        return None, None

    try:
        resp = requests.get(
            f"https://api.weather.gov/points/{lat},{lon}",
            headers=_NWS_HEADERS,
            timeout=timeout,
        )
        resp.raise_for_status()
        props = resp.json().get("properties", {})
    except (requests.RequestException, json.JSONDecodeError, ValueError):
        return None, None

    county_url = props.get("county") or ""
    zone_url = props.get("forecastZone") or ""

    county_fips = county_url.rstrip("/").rsplit("/", 1)[-1] or None
    nws_zone_ugc = zone_url.rstrip("/").rsplit("/", 1)[-1] or None

    return county_fips, nws_zone_ugc


def get_cached_zone_codes(db_conn):
    """Reads the cached (county_fips, nws_zone_ugc) from the settings
    table, or (None, None) if never resolved yet."""
    row = db_conn.execute(
        "SELECT value FROM settings WHERE key = 'news_zone_codes'"
    ).fetchone()
    if row is None:
        return None, None
    try:
        data = json.loads(row[0])
        return data.get("county_fips"), data.get("nws_zone_ugc")
    except (ValueError, TypeError):
        return None, None


def refresh_and_cache_zone_codes(db_conn, lat, lon):
    """Real, one-time (well, re-run whenever the scheduler decides to)
    refresh: resolves the real zone codes and writes them into
    `settings`, overwriting whatever was cached before. Called by
    news_scheduler.py, not on every request."""
    county_fips, nws_zone_ugc = resolve_zone_codes(lat, lon)
    if county_fips or nws_zone_ugc:
        db_conn.execute(
            "INSERT INTO settings (key, value) VALUES ('news_zone_codes', ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (json.dumps({"county_fips": county_fips, "nws_zone_ugc": nws_zone_ugc}),),
        )
        db_conn.commit()
    return county_fips, nws_zone_ugc
