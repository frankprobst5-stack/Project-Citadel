import json
import os
import time

import requests

import interactivity
import settings
import weather_cache
from paths import DATA_DIR

CLOUD_TYPES_FILE = DATA_DIR / "cloud_types.json"
HEADERS = {"User-Agent": "Cloud9 Weather Labs (kids learning dashboard)"}

# Cross-container call to media-vault's already-real, already-live NWS
# alerts client (news_nws_alerts.py, exposed at /api/news/active-alerts)
# instead of writing a second fetcher -- see CARD_REDESIGN_PLAN.md's
# "Real reuse found" note. Same `${VAR:-default}` container-name pattern
# ai.py already uses for citadel-ollama.
VAULT_API_BASE_URL = os.environ.get("VAULT_API_BASE_URL", "http://citadel-vault-brain:5000")


def get_cloud_types():
    with open(CLOUD_TYPES_FILE, encoding="utf-8") as f:
        return json.load(f)


def _grid_url(config, suffix=""):
    if not config.get("grid_office"):
        raise ValueError("No location set yet")
    return f"https://api.weather.gov/gridpoints/{config['grid_office']}/{config['grid_x']},{config['grid_y']}{suffix}"


def get_forecast():
    config = settings.get_settings()
    resp = requests.get(_grid_url(config, "/forecast"), headers=HEADERS, timeout=10)
    resp.raise_for_status()
    periods = resp.json()["properties"]["periods"]
    return [
        {
            "name": p["name"],
            "temperature": p["temperature"],
            "temperatureUnit": p["temperatureUnit"],
            "shortForecast": p["shortForecast"],
            "isDaytime": p["isDaytime"],
        }
        for p in periods[:7]
    ]


def get_hourly_forecast():
    config = settings.get_settings()
    resp = requests.get(_grid_url(config, "/forecast/hourly"), headers=HEADERS, timeout=10)
    resp.raise_for_status()
    periods = resp.json()["properties"]["periods"]
    return [
        {
            "startTime": p["startTime"],
            "temperature": p["temperature"],
            "temperatureUnit": p["temperatureUnit"],
            "shortForecast": p["shortForecast"],
            "isDaytime": p.get("isDaytime"),
            "windSpeed": p.get("windSpeed"),
            "windDirection": p.get("windDirection"),
            "probabilityOfPrecipitation": (p.get("probabilityOfPrecipitation") or {}).get("value"),
        }
        for p in periods[:12]
    ]


def _c_to_f(c):
    return round(c * 9 / 5 + 32, 1) if c is not None else None


def _kmh_to_mph(kmh):
    return round(kmh / 1.60934, 1) if kmh is not None else None


def _pa_to_inhg(pa):
    return round(pa / 3386.389, 2) if pa is not None else None


def _m_to_miles(m):
    return round(m / 1609.344, 1) if m is not None else None


def get_current_conditions():
    """Real surface observation from the nearest station to the saved
    grid, converted from NWS's raw SI units to the US units the rest of
    this app already shows. Every field is `None` (never a guessed
    number) when the station itself didn't report it -- see
    CARD_REDESIGN_PLAN.md's "populate a metric only when its real feed
    returns a valid value" rule. Every successful fetch is cached
    (weather_cache.py) both for the pressure-trend calculation below and
    as the offline fallback."""
    config = settings.get_settings()
    if not config.get("grid_office"):
        raise ValueError("No location set yet")

    stations_resp = requests.get(_grid_url(config, "/stations"), headers=HEADERS, timeout=10)
    stations_resp.raise_for_status()
    stations = stations_resp.json()["features"]
    if not stations:
        raise LookupError("No observation station found near this location")
    station_id = stations[0]["properties"]["stationIdentifier"]

    try:
        obs_resp = requests.get(
            f"https://api.weather.gov/stations/{station_id}/observations/latest",
            headers=HEADERS,
            timeout=10,
        )
        obs_resp.raise_for_status()
        props = obs_resp.json()["properties"]
    except requests.RequestException:
        cached = weather_cache.get_latest()
        if not cached:
            raise
        return dict(cached["payload"], stale=True, ageSeconds=time.time() - cached["fetched_at"])

    pressure_pa = (props.get("barometricPressure") or {}).get("value")
    current = {
        "stationId": station_id,
        "stationName": props.get("stationName"),
        "timestamp": props.get("timestamp"),
        "textDescription": props.get("textDescription"),
        "icon": props.get("icon"),
        "temperatureF": _c_to_f((props.get("temperature") or {}).get("value")),
        "dewpointF": _c_to_f((props.get("dewpoint") or {}).get("value")),
        "heatIndexF": _c_to_f((props.get("heatIndex") or {}).get("value")),
        "windChillF": _c_to_f((props.get("windChill") or {}).get("value")),
        "windSpeedMph": _kmh_to_mph((props.get("windSpeed") or {}).get("value")),
        "windGustMph": _kmh_to_mph((props.get("windGust") or {}).get("value")),
        "windDirectionDeg": (props.get("windDirection") or {}).get("value"),
        "pressureInHg": _pa_to_inhg(pressure_pa),
        "visibilityMiles": _m_to_miles((props.get("visibility") or {}).get("value")),
        "relativeHumidityPct": round(props["relativeHumidity"]["value"])
        if (props.get("relativeHumidity") or {}).get("value") is not None
        else None,
        "stale": False,
    }

    weather_cache.save_observation(station_id, current)

    older = weather_cache.get_near(weather_cache.TREND_WINDOW_SECONDS)
    if older and older["payload"].get("pressureInHg") is not None and current["pressureInHg"] is not None:
        diff = round(current["pressureInHg"] - older["payload"]["pressureInHg"], 2)
        current["pressureTrend"] = "rising" if diff > 0.02 else "falling" if diff < -0.02 else "steady"
        current["pressureTrendInHg"] = diff
    else:
        current["pressureTrend"] = None
        current["pressureTrendInHg"] = None

    interactivity.register_content("weather:current", ["weather", "science", "weather_labs"])
    interactivity.log_event("content_viewed", "weather:current", payload={"name": "Current weather conditions"})

    return current


def get_active_alerts():
    """Reuses media-vault's already-real, already-live NWS alerts client
    over its own HTTP API instead of a second fetcher -- see
    CARD_REDESIGN_PLAN.md's "Real reuse found" note. Returns an empty
    list (not an error) if media-vault is unreachable or genuinely has
    nothing active -- both are honest, valid states."""
    try:
        resp = requests.get(f"{VAULT_API_BASE_URL}/api/news/active-alerts", timeout=10)
        resp.raise_for_status()
        return resp.json().get("alerts", [])
    except requests.RequestException:
        return []
