"""Mission Mode -- the capstone from CARD_REDESIGN_PLAN.md's nine-lab
reframe: "not a separate feature." It invents no new data of its own;
it picks whichever real thing already flowing through the other eight
labs is most worth a student's attention right now, and wraps it in the
locked briefing -> observe -> question -> reveal -> investigate-related
-> recap interaction pattern.

This first build is the **Live** mission type only (real weather
happening somewhere right now) -- Guided (concept lessons: fronts,
thunderstorms, hurricanes, tornado environments, winter storms,
pressure) and Historical (replaying a real archived event) are real,
named future work, not attempted here; they need real lesson-content
authoring and real NCEI/NOMADS archive integration respectively, both
substantially bigger builds than "orchestrate what already exists."

Real, standard meteorology (Saffir-Simpson category boundaries, CAPE
instability bands) is treated as safe textbook fact, same as the
Saffir-Simpson category already computed in event_explorer.py --
distinct from live numbers, which always come from the real, already-
cached lab data this module reads, never invented here.
"""

import event_explorer
import global_lab
import settings
import storm_environment

# Real, standard SPC/AMS Glossary CAPE instability bands (J/kg) -- safe
# textbook fact, not a per-request measurement.
CAPE_BANDS = (
    (2500, "extreme"),
    (1500, "strong"),
    (500, "moderate"),
)


def _cape_band(cape_jkg):
    for threshold, label in CAPE_BANDS:
        if cape_jkg >= threshold:
            return label
    return "weak or none"


def _storm_mission(storm):
    category_note = f" It's currently a Category {storm['category']} hurricane on the Saffir-Simpson scale." if storm["category"] else ""
    return {
        "missionType": "Live",
        "title": f"Is {storm['name']} a Threat?",
        "briefing": (
            f"Right now, {storm['classificationLabel']} {storm['name']} is active in the "
            f"{storm['basin']}. You're about to look at the same real numbers meteorologists "
            f"at the National Hurricane Center are watching."
        ),
        "observe": {
            "kind": "storm",
            "name": storm["name"],
            "windMph": storm["windMph"],
            "pressureMb": storm["pressureMb"],
            "classificationLabel": storm["classificationLabel"],
            "category": storm["category"],
            "lat": storm["lat"],
            "lon": storm["lon"],
        },
        "question": (
            f"{storm['name']}'s central pressure is {storm['pressureMb']} mb, and its winds are "
            f"{storm['windMph']} mph. Lower pressure generally means a stronger storm. Based on "
            f"just this one snapshot, can you tell whether {storm['name']} is getting stronger, "
            f"getting weaker, or holding steady?"
        ),
        "reveal": (
            f"Not from one snapshot alone -- and that's the real answer, not a trick question. "
            f"Meteorologists compare pressure and wind across *many* advisories over time to spot "
            f"a real trend, the same way the Model Lab compares one forecast across many hours "
            f"instead of trusting a single number.{category_note} A storm's real strength is a "
            f"pattern across time, not a single reading."
        ),
        "investigateLink": "#wl-deck-events",
        "investigateLabel": "Open the Weather Event Explorer for the full advisory",
        "recap": (
            f"{storm['name']} is a real, currently active {storm['classificationLabel']} with "
            f"{storm['windMph']} mph winds and {storm['pressureMb']} mb central pressure. Come "
            f"back later today and see how those two numbers have changed."
        ),
        "source": "NOAA/NHC",
        "product": f"NHC advisory for {storm['name']}",
    }


def _storm_potential_mission(cape_metric, location_label):
    cape_value = cape_metric["value"]
    band = _cape_band(cape_value)
    where = location_label or "your location"
    return {
        "missionType": "Live",
        "title": "Could a Storm Form Today?",
        "briefing": (
            f"Every thunderstorm needs fuel. Right now, the Weather Data Engine is measuring "
            f"that fuel directly above {where}."
        ),
        "observe": {
            "kind": "cape",
            "value": cape_value,
            "unit": cape_metric["unit"],
            "product": cape_metric["product"],
            "validTime": cape_metric.get("validTime"),
        },
        "question": (
            f"CAPE here is currently {cape_value} J/kg. Meteorologists consider 500 J/kg enough "
            f"for a thunderstorm to become possible if something triggers it. Based on that "
            f"number, do you think a storm could form today?"
        ),
        "reveal": (
            f"{cape_value} J/kg is real {band} instability. But CAPE only tells you whether the "
            f"fuel is there -- a storm still needs a real trigger, like a front or daytime "
            f"heating, to actually ignite it. That's exactly why meteorologists also check "
            f"Lifted Index and Storm Relative Helicity, both on the Storm Environment deck, "
            f"before deciding a storm is actually likely."
        ),
        "investigateLink": "#wl-deck-storm",
        "investigateLabel": "Open the Storm Environment Lab",
        "recap": f"CAPE is {cape_value} J/kg at {where} right now -- real {band} instability.",
        "source": cape_metric["source"],
        "product": cape_metric["product"],
    }


def _global_contrast_mission(points):
    usable = [p for p in points if p.get("status") != "unavailable"]
    if len(usable) < 2:
        return None
    warmest = max(usable, key=lambda p: p["temperatureC"])
    coolest = min(usable, key=lambda p: p["temperatureC"])
    if warmest["id"] == coolest["id"]:
        return None
    diff = round(warmest["temperatureC"] - coolest["temperatureC"], 1)
    return {
        "missionType": "Live",
        "title": "Same Planet, Different Weather",
        "briefing": (
            "The Global Weather Lab asks the same real weather model about several places on "
            "Earth at once. Two of them look very different right now."
        ),
        "observe": {
            "kind": "contrast",
            "warm": {"name": warmest["name"], "temperatureC": warmest["temperatureC"]},
            "cool": {"name": coolest["name"], "temperatureC": coolest["temperatureC"]},
        },
        "question": (
            f"Right now, {warmest['name']} is {warmest['temperatureC']}°C and {coolest['name']} "
            f"is {coolest['temperatureC']}°C -- a real {diff}°C difference, at the exact same "
            f"moment on the same planet. Why might that be?"
        ),
        "reveal": (
            "A few real reasons, all at once: latitude changes how directly sunlight hits the "
            "ground, the two hemispheres have opposite seasons, and elevation matters too -- a "
            "city high in the mountains can be much cooler than its latitude alone would suggest. "
            "Meteorology never has just one cause."
        ),
        "investigateLink": "#wl-deck-global",
        "investigateLabel": "Open the Global Weather Lab",
        "recap": (
            f"{warmest['name']} and {coolest['name']} are {diff}°C apart right now -- the same "
            f"real atmosphere, behaving very differently depending on where you look."
        ),
        "source": "NOAA/NCEP",
        "product": "GFS 0.25deg",
    }


def get_mission():
    """Picks one real, live mission: an active named storm first (most
    concrete and highest-stakes), then notable real local storm
    potential, then a real global contrast as the always-available
    fallback. Returns `status: unavailable` only if every real source
    it checked failed outright -- never a guessed or templated mission."""
    storms_result = event_explorer.get_active_storms()
    storms = storms_result.get("storms") or []
    if storms:
        strongest = max(storms, key=lambda s: (s["windMph"], -s["pressureMb"]))
        return _storm_mission(strongest)

    storm_env = storm_environment.get_all()
    cape = storm_env.get("cape") or {}
    if cape.get("status") != "unavailable" and cape.get("value") is not None and cape["value"] >= 500:
        location_label = settings.get_settings().get("location_label")
        return _storm_potential_mission(cape, location_label)

    global_result = global_lab.get_all()
    points = global_result.get("points") or []
    mission = _global_contrast_mission(points)
    if mission:
        return mission

    return {"status": "unavailable", "reason": "Couldn't reach any real weather data source right now."}
