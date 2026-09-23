"""Earth Lab's Country Explorer -- real data from countries.dev (verified
live 2026-09-20; the older, commonly-known restcountries.com is deprecated
and now requires a paid v5 API key, see CARD_REDESIGN_PLAN.md). Only
`/alpha/{code}` and `/name/{name}` are real endpoints on countries.dev --
there's no bulk "all countries" or "by numeric code" route, so the map's
own GeoJSON (server/static/data/world-countries.geojson) carries a
pre-computed `alpha3` property per country, generated once from the ISO
3166-1 standard so every click can look the country up by its unambiguous
alpha-3 code instead of a fuzzy name match.
"""

import requests

import interactivity

HEADERS = {"User-Agent": "Cloud9 Earth Lab (kids learning dashboard)"}
API_BASE = "https://countries.dev"


def get_country(alpha3):
    alpha3 = alpha3.strip().upper()
    resp = requests.get(f"{API_BASE}/alpha/{alpha3}", headers=HEADERS, timeout=10)
    if resp.status_code == 404 or resp.text.strip() == "Country not found":
        raise LookupError(f"No country found for code {alpha3}")
    resp.raise_for_status()
    data = resp.json()

    country = {
        "name": data.get("name"),
        "capital": data.get("capital"),
        "region": data.get("region"),
        "subregion": data.get("subregion"),
        "population": data.get("population"),
        "area": data.get("area"),
        "flagEmoji": data.get("flag"),
        "flagImage": (data.get("flags") or {}).get("png"),
        "languages": [lang.get("name") for lang in data.get("languages", []) if lang.get("name")],
        "currencies": [
            f"{c.get('name')} ({c.get('symbol')})" if c.get("symbol") else c.get("name")
            for c in data.get("currencies", [])
            if c.get("name")
        ],
        "latlng": data.get("latlng"),
        "alpha3": data.get("alpha3Code") or alpha3,
        "borders": data.get("borders") or [],
        "timezones": data.get("timezones") or [],
        "populationDensity": data.get("populationDensity"),
    }

    tags = ["geography", "earth_lab"]
    if country["region"]:
        tags.append(country["region"].lower())
    interactivity.register_content(f"country:{country['alpha3']}", tags)
    interactivity.log_event(
        "content_viewed",
        f"country:{country['alpha3']}",
        payload={"name": country["name"], "region": country["region"]},
    )

    return country
