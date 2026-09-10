import json

import requests

import settings
from paths import DATA_DIR

CLOUD_TYPES_FILE = DATA_DIR / "cloud_types.json"
HEADERS = {"User-Agent": "Cloud9 Weather Labs (kids learning dashboard)"}


def get_cloud_types():
    with open(CLOUD_TYPES_FILE, encoding="utf-8") as f:
        return json.load(f)


def get_forecast():
    config = settings.get_settings()
    if not config.get("grid_office"):
        raise ValueError("No location set yet")
    url = f"https://api.weather.gov/gridpoints/{config['grid_office']}/{config['grid_x']},{config['grid_y']}/forecast"
    resp = requests.get(url, headers=HEADERS, timeout=10)
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
        for p in periods[:4]
    ]
