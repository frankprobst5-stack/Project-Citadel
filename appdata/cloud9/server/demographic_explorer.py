"""Demographic Explorer -- ROADMAP.md Phase 3, item 6's second real
piece: "owns the *questions*; Earth Lab keeps owning the *geographic
data* it already has -- not a duplicate map." No new country database
here -- the real country list is read straight from the same GeoJSON
Earth Lab's own map already uses (server/static/data/world-countries.geojson,
177 real countries), and every population/area number comes from
earth_lab.get_country()'s own real, live countries.dev call, exactly
like a learner clicking that country on the map would get.
"""

import json

import earth_lab
from paths import STATIC_DIR

GEOJSON_FILE = STATIC_DIR / "data" / "world-countries.geojson"


def get_countries():
    """Real country list, straight from the map's own GeoJSON -- 2 of its
    177 features (N. Cyprus, Somaliland) have no real alpha3 code because
    they're outside the ISO 3166-1 standard the rest of the map is built
    on, so they're honestly skipped here rather than given a fabricated
    code."""
    with open(GEOJSON_FILE, encoding="utf-8") as f:
        data = json.load(f)
    countries = [
        {"name": feature["properties"]["name"], "alpha3": feature["properties"]["alpha3"]}
        for feature in data["features"]
        if feature["properties"].get("alpha3")
    ]
    return sorted(countries, key=lambda c: c["name"])


def compare(alpha3_a, alpha3_b):
    country_a = earth_lab.get_country(alpha3_a)
    country_b = earth_lab.get_country(alpha3_b)
    return {"countryA": country_a, "countryB": country_b}


def check_population_guess(alpha3_a, alpha3_b, guess):
    import learning_engine

    country_a = earth_lab.get_country(alpha3_a)
    country_b = earth_lab.get_country(alpha3_b)
    pop_a = country_a.get("population") or 0
    pop_b = country_b.get("population") or 0
    actual_winner = alpha3_a if pop_a >= pop_b else alpha3_b
    correct = guess == actual_winner

    learning_engine.record_activity(
        "demographics",
        "guess_population",
        f"{alpha3_a}-vs-{alpha3_b}",
        source="countries.dev (via Earth Lab)",
        correct=correct,
    )

    return {
        "correct": correct,
        "winner": actual_winner,
        "countryA": country_a,
        "countryB": country_b,
    }
