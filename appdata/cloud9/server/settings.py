import json

import requests

from paths import DATA_DIR

SETTINGS_FILE = DATA_DIR / "settings.json"
HEADERS = {"User-Agent": "Cloud9 Weather Labs (kids learning dashboard)"}

DEFAULTS = {
    "school_name": "",
    "school_url": "",
    "zip_code": "",
    "location_label": "",
    "grid_office": "",
    "grid_x": None,
    "grid_y": None,
    "radar_station": "",
    "weather_radio_url": "",
    "weather_radio_label": "",
    "bible_study_enabled": False,
}


def get_settings():
    if not SETTINGS_FILE.exists():
        return dict(DEFAULTS)
    with open(SETTINGS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    merged = dict(DEFAULTS)
    merged.update(data)
    return merged


def save_settings(updates):
    settings = get_settings()
    settings.update(updates)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
    return settings


def resolve_zip(zip_code):
    """Look up a US ZIP code -> lat/long -> NWS grid + radar station info."""
    geo_resp = requests.get(f"http://api.zippopotam.us/us/{zip_code}", timeout=10)
    geo_resp.raise_for_status()
    place = geo_resp.json()["places"][0]
    lat = place["latitude"]
    lon = place["longitude"]
    label = f"{place['place name']}, {place['state abbreviation']}"

    points_resp = requests.get(
        f"https://api.weather.gov/points/{lat},{lon}",
        headers=HEADERS,
        timeout=10,
    )
    points_resp.raise_for_status()
    props = points_resp.json()["properties"]

    return {
        "zip_code": zip_code,
        "location_label": label,
        "grid_office": props["gridId"],
        "grid_x": props["gridX"],
        "grid_y": props["gridY"],
        "radar_station": props["radarStation"],
    }
