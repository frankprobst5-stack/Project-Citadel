"""Earth Lab's own Guided Missions -- the same real briefing -> observe
-> question -> reveal -> investigate-related -> recap pattern Weather
Labs' Mission Mode already uses, applied to geography instead. Every
"observe" step uses real, live data from earth_lab.get_country() (the
same real countries.dev API Earth Lab's map already calls) comparing
two real, named countries -- never invented example numbers.

Countries were chosen deliberately for real, dramatic, honest contrast
(verified live before writing this file, same standing rule as every
other lab): Bangladesh vs. Australia for population density, Canada vs.
Argentina for hemispheres, China vs. Iceland for land borders, and the
USA vs. China for time zones (a real, genuinely interesting case since
China's single time zone is a political choice, not a physical
necessity -- despite spanning nearly as much longitude as the
continental US).
"""

import earth_lab


def _safe_country(alpha3):
    try:
        return earth_lab.get_country(alpha3)
    except Exception:
        return None


def _population_density_mission():
    a, b = _safe_country("BGD"), _safe_country("AUS")
    if not a or not b:
        return None
    return {
        "missionType": "Guided",
        "concept": "population-density",
        "title": "How Crowded Is a Country, Really?",
        "briefing": (
            "Two countries can have very different populations but the number that really "
            "describes what living there feels like is population density -- how many people "
            "share each square kilometer of land."
        ),
        "observe": {
            "kind": "country-pair",
            "metric": "populationDensity", "unit": "people per km²",
            "a": {"name": a["name"], "population": a["population"], "area": a["area"], "value": a["populationDensity"]},
            "b": {"name": b["name"], "population": b["population"], "area": b["area"], "value": b["populationDensity"]},
        },
        "question": (
            f"{a['name']} has about {a['population']:,} people in {a['area']:,} km². "
            f"{b['name']} has about {b['population']:,} people in {b['area']:,} km² -- a much bigger "
            f"country. Which one do you think has more people packed into each square kilometer?"
        ),
        "reveal": (
            f"{a['name']} -- by a huge margin. {a['name']}'s real population density is "
            f"{a['populationDensity']} people per km², while {b['name']}'s is only "
            f"{b['populationDensity']} people per km². {b['name']} actually has fewer total people "
            f"living across a much larger area, much of it desert interior that very few people "
            f"call home -- total population alone doesn't tell you how crowded a place really is."
        ),
        "investigateLink": "#earth-lab-map",
        "investigateLabel": "Click around the map to compare more real countries",
        "recap": f"{a['name']}: {a['populationDensity']} people/km². {b['name']}: {b['populationDensity']} people/km² -- same planet, very different crowding.",
        "source": "countries.dev",
    }


def _hemispheres_mission():
    a, b = _safe_country("CAN"), _safe_country("ARG")
    if not a or not b:
        return None
    a_lat, b_lat = a["latlng"][0], b["latlng"][0]
    return {
        "missionType": "Guided",
        "concept": "hemispheres",
        "title": "Which Half of the Planet?",
        "briefing": (
            "A country's latitude -- how far north or south of the equator it sits -- decides "
            "which hemisphere it's in, and that decides its whole rhythm of seasons."
        ),
        "observe": {
            "kind": "country-pair", "metric": "latitude", "unit": "°",
            "a": {"name": a["name"], "value": a_lat},
            "b": {"name": b["name"], "value": b_lat},
        },
        "question": (
            f"{a['name']}'s real latitude is {a_lat}°, and {b['name']}'s is {b_lat}°. A positive "
            f"latitude means north of the equator; negative means south. Which hemisphere is each "
            f"country in?"
        ),
        "reveal": (
            f"{a['name']} ({a_lat}°) is in the Northern Hemisphere; {b['name']} ({b_lat}°) is in "
            f"the Southern Hemisphere. That real difference means their seasons run opposite each "
            f"other all year -- when it's real winter in {a['name']}, it's real summer in "
            f"{b['name']}, exactly the same reasoning the Global Weather Lab uses to compare real "
            f"temperatures at Northern and Southern Hemisphere cities on the same day."
        ),
        "investigateLink": "#earth-lab-map",
        "investigateLabel": "Find a country in each hemisphere on the map",
        "recap": f"{a['name']}: {a_lat}° (Northern Hemisphere). {b['name']}: {b_lat}° (Southern Hemisphere) -- opposite seasons, same moment in time.",
        "source": "countries.dev",
    }


def _borders_mission():
    a, b = _safe_country("CHN"), _safe_country("ISL")
    if not a or not b:
        return None
    return {
        "missionType": "Guided",
        "concept": "borders",
        "title": "How Many Neighbors Does a Country Have?",
        "briefing": (
            "Some countries share a border with more than a dozen others. Some share a border "
            "with none at all -- and it's not always about how big the country is."
        ),
        "observe": {
            "kind": "country-pair", "metric": "borders", "unit": "neighboring countries",
            "a": {"name": a["name"], "value": len(a["borders"]), "list": a["borders"]},
            "b": {"name": b["name"], "value": len(b["borders"]), "list": b["borders"]},
        },
        "question": f"How many other countries do you think share a real land border with {a['name']}? What about {b['name']}?",
        "reveal": (
            f"{a['name']} shares a real land border with {len(a['borders'])} other countries "
            f"({', '.join(a['borders'])}) -- among the most of any country on Earth. {b['name']} "
            f"shares a border with {len(b['borders'])}: it's an island, so there's simply no land "
            f"edge for a border to exist on. Geography, not size alone, decides how many neighbors "
            f"a country has."
        ),
        "investigateLink": "#earth-lab-map",
        "investigateLabel": "Find an island country and a country with many neighbors",
        "recap": f"{a['name']}: {len(a['borders'])} real land borders. {b['name']}: {len(b['borders'])} -- an island nation with none.",
        "source": "countries.dev",
    }


def _time_zones_mission():
    a, b = _safe_country("USA"), _safe_country("CHN")
    if not a or not b:
        return None
    return {
        "missionType": "Guided",
        "concept": "time-zones",
        "title": "Why Doesn't Every Country Have One Clock?",
        "briefing": (
            "Earth turns 360° every 24 hours, so the sun rises at different real times depending "
            "on how far east or west you are -- that's the whole reason time zones exist."
        ),
        "observe": {
            "kind": "country-pair", "metric": "timezones", "unit": "time zones",
            "a": {"name": a["name"], "value": len(a["timezones"])},
            "b": {"name": b["name"], "value": len(b["timezones"])},
        },
        "question": (
            f"The USA spans real {len(a['timezones'])} time zones. China covers almost as much "
            f"east-west distance but uses just {len(b['timezones'])}. Both are physically huge -- "
            f"so why would one country choose to use only one clock for the whole country?"
        ),
        "reveal": (
            f"It's a real political choice, not a physical requirement -- China decided in 1949 "
            f"to run the entire country on a single official time zone for national unity, even "
            f"though the sun physically rises hours apart at its eastern and western edges. The "
            f"USA's real {len(a['timezones'])} instead follow the physical sun closely, matching "
            f"local time to where the sun actually is. Time zones are drawn by people, not just "
            f"by geography."
        ),
        "investigateLink": "#earth-lab-map",
        "investigateLabel": "Compare more real countries on the map",
        "recap": f"{a['name']}: {len(a['timezones'])} real time zones. {b['name']}: {len(b['timezones'])} -- geography sets the range, but people draw the lines.",
        "source": "countries.dev",
    }


def _currencies_mission():
    a, b = _safe_country("ECU"), _safe_country("USA")
    if not a or not b:
        return None
    a_currency, b_currency = a["currencies"][0], b["currencies"][0]
    return {
        "missionType": "Guided",
        "concept": "currencies",
        "title": "Whose Money Is It, Really?",
        "briefing": (
            "Most countries have their own currency, printed and controlled by their own "
            "government. But that's not actually a rule -- some countries use someone else's "
            "money entirely."
        ),
        "observe": {
            "kind": "country-pair", "metric": "currency", "unit": "",
            "a": {"name": a["name"], "value": a_currency},
            "b": {"name": b["name"], "value": b_currency},
        },
        "question": f"{a['name']}'s official real currency is the {a_currency}. The real currency of {b['name']} is the exact same one. Since {a['name']} isn't part of {b['name']}, why do you think they share the exact same money?",
        "reveal": (
            f"{a['name']} made a real, deliberate choice in 2000 to adopt the {b_currency} as its "
            f"own official currency (a real process called \"dollarization\") after its own "
            f"previous currency lost most of its value -- it gave up printing its own money in "
            f"exchange for real economic stability. A shared currency doesn't always mean shared "
            f"government; sometimes it means one country decided another country's money was more "
            f"trustworthy than its own."
        ),
        "investigateLink": "#earth-lab-map",
        "investigateLabel": "Find other countries that share a currency",
        "recap": f"{a['name']} and {b['name']} both use the real {a_currency} -- one printed it, the other adopted it.",
        "source": "countries.dev",
    }


def _languages_mission():
    a, b = _safe_country("CHE"), _safe_country("JPN")
    if not a or not b:
        return None
    return {
        "missionType": "Guided",
        "concept": "languages",
        "title": "How Many Languages Does One Country Speak?",
        "briefing": (
            "Some countries run entirely on one shared language. Others officially operate in "
            "several at once -- government documents, road signs, and schools all in more than "
            "one real language."
        ),
        "observe": {
            "kind": "country-pair", "metric": "languages", "unit": "official languages",
            "a": {"name": a["name"], "value": len(a["languages"]), "list": a["languages"]},
            "b": {"name": b["name"], "value": len(b["languages"]), "list": b["languages"]},
        },
        "question": f"{a['name']} has {len(a['languages'])} real official languages ({', '.join(a['languages'])}). {b['name']} has {len(b['languages'])} ({', '.join(b['languages'])}). Why might one small country need so many official languages while another gets by with just one?",
        "reveal": (
            f"{a['name']}'s real {len(a['languages'])} languages reflect its actual regions -- "
            f"different areas of the country have spoken German, French, Italian, or Romansh for "
            f"centuries, and the country's government recognizes all of them rather than forcing "
            f"one on everyone. {b['name']}'s single official language reflects a much more "
            f"linguistically uniform population. Neither approach is more \"normal\" -- it just "
            f"depends on a country's real history of who settled where."
        ),
        "investigateLink": "#earth-lab-map",
        "investigateLabel": "Find a country with several official languages",
        "recap": f"{a['name']}: {len(a['languages'])} real official languages. {b['name']}: {len(b['languages'])}.",
        "source": "countries.dev",
    }


CONCEPTS = {
    "population-density": ("How Crowded Is a Country, Really?", _population_density_mission),
    "hemispheres": ("Which Half of the Planet?", _hemispheres_mission),
    "borders": ("How Many Neighbors Does a Country Have?", _borders_mission),
    "time-zones": ("Why Doesn't Every Country Have One Clock?", _time_zones_mission),
    "currencies": ("Whose Money Is It, Really?", _currencies_mission),
    "languages": ("How Many Languages Does One Country Speak?", _languages_mission),
}


def list_concepts():
    return [{"id": concept_id, "title": title} for concept_id, (title, _) in CONCEPTS.items()]


def get_geography_mission(concept_id):
    entry = CONCEPTS.get(concept_id)
    if not entry:
        return {"status": "unavailable", "reason": f"Unknown concept '{concept_id}'."}
    _, builder = entry
    result = builder()
    if result is None:
        return {"status": "unavailable", "reason": "Couldn't reach the real country data source right now."}
    return result
