"""Real current conditions + short forecast from NWS's own public API,
for the Master Situation Board (added 2026-10-09). Same real
api.weather.gov source and User-Agent convention as news_location.py/
news_nws_alerts.py -- no API key, no signup, a real US government data
source, consistent with this feature's other NWS integrations.

Three real calls, chained (NWS's own API shape, confirmed live against
Citadel's own real station coordinates, not assumed from docs alone):
  1. /points/{lat},{lon} -> properties.forecast (forecast URL) and
     properties.observationStations (a URL to the list of nearby
     stations, nearest first).
  2. GET that observationStations URL -> features[0].properties
     .stationIdentifier is the nearest station's real code (e.g.
     "KCDS" for Childress, TX, nearest to Citadel's own coordinates).
  3. /stations/{stationId}/observations/latest -> real current
     conditions (temperature, description, wind, humidity).
     /gridpoints/.../forecast (the URL from step 1) -> periods[], each
     a real short-term forecast chunk (today, tonight, tomorrow...).

Resolved URLs (station id, forecast url) are cached in the `settings`
table (same key/value table news_location.py already uses) since they
almost never change for a fixed station location -- re-resolved only
when missing, not on every fetch.
"""
import json

import requests

_NWS_HEADERS = {"User-Agent": "CitadelNewsArchive/1.0 (self-hosted, github.com/frankprobst5-stack/Project-Citadel)"}


def _resolve_station_info(lat, lon, timeout=10):
    """Returns (station_id, forecast_url) or (None, None) on any
    failure -- never raises, same graceful-degrade principle as every
    other NWS integration in this codebase."""
    try:
        points = requests.get(
            f"https://api.weather.gov/points/{lat},{lon}", headers=_NWS_HEADERS, timeout=timeout
        )
        points.raise_for_status()
        props = points.json().get("properties", {})
        forecast_url = props.get("forecast")
        stations_url = props.get("observationStations")
        if not stations_url:
            return None, forecast_url

        stations = requests.get(stations_url, headers=_NWS_HEADERS, timeout=timeout)
        stations.raise_for_status()
        features = stations.json().get("features", [])
        station_id = features[0]["properties"]["stationIdentifier"] if features else None
        return station_id, forecast_url
    except (requests.RequestException, json.JSONDecodeError, ValueError, KeyError, IndexError):
        return None, None


def _get_cached_station_info(db_conn):
    row = db_conn.execute("SELECT value FROM settings WHERE key = 'weather_station_info'").fetchone()
    if row is None:
        return None, None
    try:
        data = json.loads(row[0])
        return data.get("station_id"), data.get("forecast_url")
    except (ValueError, TypeError):
        return None, None


def _cache_station_info(db_conn, station_id, forecast_url):
    db_conn.execute(
        "INSERT INTO settings (key, value) VALUES ('weather_station_info', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (json.dumps({"station_id": station_id, "forecast_url": forecast_url}),),
    )


def fetch_conditions(db_conn, lat, lon, timeout=10):
    """Real current conditions + next 4 forecast periods. Returns a dict
    with "status": "ok" or "status": "error" (with a "detail" string) --
    callers store whichever comes back as-is, same honest-state pattern
    as every other daemon/fetch result in this codebase."""
    if not lat or not lon:
        return {"status": "error", "detail": "No station location configured (STATION_LAT/STATION_LON)."}

    station_id, forecast_url = _get_cached_station_info(db_conn)
    if not station_id or not forecast_url:
        station_id, forecast_url = _resolve_station_info(lat, lon, timeout=timeout)
        if station_id and forecast_url:
            _cache_station_info(db_conn, station_id, forecast_url)
            db_conn.commit()

    if not station_id or not forecast_url:
        return {"status": "error", "detail": "Could not resolve NWS station/forecast for this location."}

    result = {"status": "ok", "station_id": station_id}
    try:
        obs = requests.get(
            f"https://api.weather.gov/stations/{station_id}/observations/latest",
            headers=_NWS_HEADERS, timeout=timeout,
        )
        obs.raise_for_status()
        op = obs.json().get("properties", {})
        temp_c = (op.get("temperature") or {}).get("value")
        result["temperature_f"] = round(temp_c * 9 / 5 + 32, 1) if temp_c is not None else None
        result["description"] = op.get("textDescription")
        wind_kmh = (op.get("windSpeed") or {}).get("value")
        result["wind_mph"] = round(wind_kmh * 0.621371, 1) if wind_kmh is not None else None
        result["humidity_percent"] = (op.get("relativeHumidity") or {}).get("value")
    except (requests.RequestException, json.JSONDecodeError, ValueError, KeyError):
        result["status"] = "error"
        result["detail"] = "Current observation unreachable."

    try:
        fc = requests.get(forecast_url, headers=_NWS_HEADERS, timeout=timeout)
        fc.raise_for_status()
        periods = fc.json().get("properties", {}).get("periods", [])[:4]
        result["forecast"] = [{
            "name": p.get("name"),
            "temperature": p.get("temperature"),
            "temperature_unit": p.get("temperatureUnit"),
            "short_forecast": p.get("shortForecast"),
        } for p in periods]
    except (requests.RequestException, json.JSONDecodeError, ValueError, KeyError):
        result.setdefault("forecast", [])

    return result
