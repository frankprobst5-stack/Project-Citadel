"""Mission Mode's second real mission type: Guided (concept lessons --
fronts, thunderstorms, hurricanes, tornado environments, winter storms,
pressure). Unlike Live missions, a Guided mission's teaching content is
real, standard, textbook meteorology -- safe to state as fact the same
way event_explorer.py's Saffir-Simpson category boundaries are, not
something that needs a live API check.

But every "observe" step still reaches for a real, currently-live
number from an already-built lab wherever one genuinely illustrates the
concept, instead of a made-up example value -- same standing rule as
every other lab. Where no real live anchor fits honestly (no active
hurricane right now, no winter storm in September), the mission says so
plainly rather than pretending otherwise.
"""

import event_explorer
import storm_environment
import weather


def _safe(fn):
    try:
        return fn()
    except Exception:
        return None


def _pressure_mission():
    current = _safe(weather.get_current_conditions)
    pressure = current.get("pressureInHg") if current else None
    trend = current.get("pressureTrend") if current else None

    if pressure is not None and trend:
        observe = {"kind": "pressure", "pressureInHg": pressure, "trend": trend}
        trend_sentence = f"Right now it's reading {pressure} inHg and {trend}."
        question = (
            f"{trend_sentence} If pressure keeps {trend} over the next several hours, "
            f"what kind of weather would you expect -- clearing skies, or clouds and "
            f"possible rain?"
        )
    else:
        observe = {"kind": "pressure", "pressureInHg": None, "trend": None}
        question = (
            "No real pressure reading is available right now, but here's the real "
            "question meteorologists ask every day: if pressure is falling, what kind "
            "of weather usually follows?"
        )

    return {
        "missionType": "Guided",
        "concept": "pressure",
        "title": "What Pressure Tells You",
        "briefing": (
            "Air pressure is invisible, but it's one of the most useful real numbers in "
            "meteorology -- it's the reason wind blows at all, and it changes before the "
            "sky does."
        ),
        "observe": observe,
        "question": question,
        "reveal": (
            "Falling pressure means air is rising -- rising air cools, and cooling air "
            "can't hold as much moisture, so clouds and precipitation become more "
            "likely. Rising pressure means air is sinking, which generally clears skies. "
            "That's the real reason a falling barometer has meant \"storm coming\" to "
            "sailors and farmers for centuries -- it's real physics, not folklore."
        ),
        "investigateLink": "#wl-deck-current",
        "investigateLabel": "Open Current Conditions to see today's real pressure trend",
        "recap": "Pressure trend, not just pressure value, is the real clue: falling means rising air and a higher chance of clouds or storms; rising means sinking air and clearing skies.",
    }


def _thunderstorms_mission():
    cape = _safe(storm_environment.get_cape)
    lifted_index = _safe(storm_environment.get_lifted_index)
    cape_val = cape.get("value") if cape and cape.get("status") != "unavailable" else None
    li_val = lifted_index.get("value") if lifted_index and lifted_index.get("status") != "unavailable" else None

    observe = {"kind": "thunderstorm-ingredients", "capeJkg": cape_val, "liftedIndexC": li_val}
    if cape_val is not None:
        question = (
            f"CAPE here is {cape_val} J/kg right now. That's the real fuel available for "
            f"a thunderstorm. But fuel alone doesn't make a fire -- what else does a "
            f"thunderstorm need to actually form?"
        )
    else:
        question = "A thunderstorm needs fuel to grow -- but fuel alone doesn't make a fire. What else does it need to actually form?"

    return {
        "missionType": "Guided",
        "concept": "thunderstorms",
        "title": "The Recipe for a Thunderstorm",
        "briefing": (
            "Every real thunderstorm needs the same three real ingredients: moisture, "
            "instability, and a lift. Miss one, and the storm never forms, no matter how "
            "hot the day is."
        ),
        "observe": observe,
        "question": question,
        "reveal": (
            "A trigger to lift the air -- a front, a sea breeze, daytime heating over hot "
            "ground, or a mountain slope. CAPE (Convective Available Potential Energy) "
            "measures the real fuel; the Lifted Index measures how easily a parcel of air "
            "rises once triggered (negative values mean it rises easily). Meteorologists "
            "check both together, plus moisture, before calling thunderstorms likely -- "
            "exactly what the Storm Environment Lab's own instruments measure."
        ),
        "investigateLink": "#wl-deck-storm",
        "investigateLabel": "Open the Storm Environment Lab",
        "recap": "Moisture, instability (CAPE), and a lifting trigger -- a real thunderstorm needs all three, not just one.",
    }


def _tornado_mission():
    cape = _safe(storm_environment.get_cape)
    srh = _safe(storm_environment.get_storm_relative_helicity)
    cape_val = cape.get("value") if cape and cape.get("status") != "unavailable" else None
    srh_val = srh.get("value") if srh and srh.get("status") != "unavailable" else None

    observe = {"kind": "tornado-ingredients", "capeJkg": cape_val, "srhM2s2": srh_val}
    if cape_val is not None and srh_val is not None:
        question = (
            f"Right now, CAPE is {cape_val} J/kg and Storm Relative Helicity is "
            f"{srh_val} m²/s² here. SRH measures how much spin is available in the "
            f"lower atmosphere. Do you think today's real numbers suggest tornado "
            f"conditions, or not?"
        )
    else:
        question = "A thunderstorm can spin into a tornado only with one extra ingredient beyond fuel. What do you think that is?"

    return {
        "missionType": "Guided",
        "concept": "tornado-environments",
        "title": "What Makes a Storm Spin?",
        "briefing": (
            "Most thunderstorms never produce a tornado. The real difference is rotation "
            "-- and meteorologists have a specific number for measuring how much of it "
            "is available."
        ),
        "observe": observe,
        "question": question,
        "reveal": (
            "Storm Relative Helicity (SRH) measures how much spin is available in the "
            "lower few kilometers of the atmosphere -- real wind shear that a storm's "
            "updraft can tilt and stretch into rotation. High CAPE alone just makes a "
            "strong storm; high CAPE *and* high SRH together are what let a storm "
            "organize into a supercell capable of producing a tornado. Values low enough "
            "to feel unremarkable one day can be dramatically higher the next -- that's "
            "exactly why meteorologists watch SRH as its own real number, not just CAPE."
        ),
        "investigateLink": "#wl-deck-storm",
        "investigateLabel": "Open the Storm Environment Lab",
        "recap": "CAPE is the fuel; Storm Relative Helicity is the spin. A tornado-capable storm needs real amounts of both at once.",
    }


def _hurricanes_mission():
    storms_result = _safe(event_explorer.get_active_storms) or {}
    storms = storms_result.get("storms") or []

    if storms:
        strongest = max(storms, key=lambda s: (s["windMph"], -s["pressureMb"]))
        observe = {
            "kind": "storm", "name": strongest["name"], "windMph": strongest["windMph"],
            "pressureMb": strongest["pressureMb"], "classificationLabel": strongest["classificationLabel"],
            "category": strongest["category"], "lat": strongest["lat"], "lon": strongest["lon"],
        }
        question = (
            f"{strongest['name']} is real and active right now, with {strongest['windMph']} mph "
            f"winds and a central pressure of {strongest['pressureMb']} mb. Based on what you just "
            f"learned about pressure, does a *lower* central pressure mean a weaker hurricane, or a "
            f"stronger one?"
        )
        reveal_intro = f"A stronger one -- and {strongest['name']}'s real {strongest['pressureMb']} mb tells you that directly. "
    else:
        observe = {"kind": "hurricane-scale-only"}
        question = (
            "No tropical cyclones are active anywhere right now, so there's no live example to check -- "
            "but here's the real question anyway: does a *lower* central pressure mean a weaker "
            "hurricane, or a stronger one?"
        )
        reveal_intro = "A stronger one. "

    return {
        "missionType": "Guided",
        "concept": "hurricanes",
        "title": "Reading a Hurricane's Real Numbers",
        "briefing": (
            "A hurricane is a real heat engine -- warm ocean water evaporates, rises, and "
            "releases energy as it condenses, and that released energy is what powers the "
            "whole storm."
        ),
        "observe": observe,
        "question": question,
        "reveal": (
            reveal_intro +
            "Lower central pressure means air is being pulled upward and inward more "
            "forcefully, which drives faster spiraling winds -- pressure and wind speed "
            "move together. That's the real reason the National Hurricane Center reports "
            "both numbers on every single advisory, and why meteorologists watch pressure "
            "drop as the first real sign a storm is intensifying, sometimes before the "
            "wind speed estimate even updates."
        ),
        "investigateLink": "#wl-deck-events",
        "investigateLabel": "Open the Weather Event Explorer",
        "recap": "Lower central pressure means a stronger hurricane -- pressure and wind speed are two views of the same real engine.",
    }


def _winter_storms_mission():
    current = _safe(weather.get_current_conditions)
    temp_f = current.get("temperatureF") if current else None

    if temp_f is not None:
        observe = {"kind": "temperature", "temperatureF": temp_f}
        question = (
            f"It's {temp_f}°F here right now. If a storm dropped a lot of precipitation "
            f"at this exact surface temperature, would you expect snow, or rain?"
        )
    else:
        observe = {"kind": "temperature", "temperatureF": None}
        question = "If a storm drops a lot of precipitation and the surface temperature is below freezing, would you expect snow, or rain?"

    return {
        "missionType": "Guided",
        "concept": "winter-storms",
        "title": "Snow, Sleet, or Freezing Rain?",
        "briefing": (
            "Winter precipitation isn't just \"cold rain.\" The exact type that reaches "
            "the ground depends on the temperature all the way up through the "
            "atmosphere, not just the temperature where you're standing."
        ),
        "observe": observe,
        "question": question,
        "reveal": (
            "Surface temperature alone doesn't decide it. If the whole column of air is "
            "below freezing, you get snow. But if a layer of warmer-than-freezing air "
            "sits above a freezing layer near the ground, snow can partially melt and "
            "refreze into sleet, or melt completely and become freezing rain the instant "
            "it hits a surface below 32°F. That's exactly why meteorologists check a "
            "real vertical profile -- like the one on the Sounding Lab deck -- instead of "
            "just reading a single ground-level thermometer."
        ),
        "investigateLink": "#wl-deck-sounding",
        "investigateLabel": "Open the Sounding Lab to see a real vertical profile",
        "recap": "Snow, sleet, and freezing rain are all the same precipitation falling through different real temperature profiles on the way down.",
    }


def _fronts_mission():
    current = _safe(weather.get_current_conditions)
    trend = current.get("pressureTrend") if current else None
    temp_f = current.get("temperatureF") if current else None

    observe = {"kind": "front-clues", "temperatureF": temp_f, "pressureTrend": trend}
    if trend:
        question = (
            f"Pressure here is currently {trend}. Fronts are the boundaries between "
            f"different air masses -- based on what you learned about pressure, would "
            f"you expect pressure to be falling or rising as a front approaches, before "
            f"it arrives?"
        )
    else:
        question = "Fronts are boundaries between air masses. Would you expect pressure to be falling or rising as a front approaches, before it arrives?"

    return {
        "missionType": "Guided",
        "concept": "fronts",
        "title": "Reading the Boundary Between Air Masses",
        "briefing": (
            "A front is a real boundary between two different air masses -- and the "
            "weather usually changes fastest right at that line, not gradually."
        ),
        "observe": observe,
        "question": question,
        "reveal": (
            "Falling, generally -- a front is often tied to rising air and lower "
            "pressure moving in. A cold front (cold air replacing warm) usually passes "
            "quickly, with a sharp temperature drop, a wind shift, and sometimes a line "
            "of thunderstorms right along it. A warm front (warm air replacing cold) "
            "moves slower and brings a longer stretch of clouds and steady rain ahead of "
            "it. After either one passes, pressure typically starts rising again."
        ),
        "investigateLink": "#wl-deck-current",
        "investigateLabel": "Open Current Conditions to check today's real pressure trend",
        "recap": "A front is where two air masses meet -- cold fronts pass fast with sharp changes, warm fronts arrive slowly with longer-lasting clouds and rain.",
    }


CONCEPTS = {
    "pressure": ("What Pressure Tells You", _pressure_mission),
    "thunderstorms": ("The Recipe for a Thunderstorm", _thunderstorms_mission),
    "tornado-environments": ("What Makes a Storm Spin?", _tornado_mission),
    "hurricanes": ("Reading a Hurricane's Real Numbers", _hurricanes_mission),
    "winter-storms": ("Snow, Sleet, or Freezing Rain?", _winter_storms_mission),
    "fronts": ("Reading the Boundary Between Air Masses", _fronts_mission),
}


def list_concepts():
    return [{"id": concept_id, "title": title} for concept_id, (title, _) in CONCEPTS.items()]


def get_guided_mission(concept_id):
    entry = CONCEPTS.get(concept_id)
    if not entry:
        return {"status": "unavailable", "reason": f"Unknown concept '{concept_id}'."}
    _, builder = entry
    return builder()
