"""Guided Missions for History -- the third subject after Weather and
Earth Lab. Source is the same real, live, keyless Wikimedia "On This
Day" feed history_fact.py already uses, but pulling its `events`,
`births`, and `deaths` categories (all real, confirmed live before
writing this) instead of just one picked headline fact.

Reuses history_fact's own content-safety filter (`_score`, and the
`BLOCK_KEYWORDS` list behind it) rather than a second copy -- the raw
feed is a plain historical record, not curated for kids, and keeping
the block list in one place means a future edit to it protects every
history feature at once, not just the one it was made for.

Real per-item `year` fields (confirmed live: today's date alone spans
year 38 to the present) are what make an honest "how many years apart"
comparison possible -- every gap stated in these missions is computed
directly from that field, never estimated.
"""

import json
from datetime import date

import requests

import history_fact
from paths import DATA_DIR

CACHE_FILE = DATA_DIR / "history_missions_cache.json"
HEADERS = {"User-Agent": "Cloud9 History Guided Missions (kids learning dashboard)"}
API_BASE = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday"


def _load_cache():
    if not CACHE_FILE.exists():
        return None
    with open(CACHE_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _fetch_all_categories(month, day):
    """One real fetch per category, cached together for the whole day --
    all three barely change once Wikimedia's own daily feed is
    published, same reasoning as history_fact.py's own cache."""
    cache = _load_cache()
    today_key = f"{month:02d}-{day:02d}"
    if cache and cache.get("dateKey") == today_key:
        return cache["categories"]

    categories = {}
    for category in ("events", "births", "deaths"):
        resp = requests.get(f"{API_BASE}/{category}/{month:02d}/{day:02d}", headers=HEADERS, timeout=15)
        resp.raise_for_status()
        categories[category] = resp.json().get(category, [])

    _save_cache({"dateKey": today_key, "categories": categories})
    return categories


def _safe_items(items):
    """Reuses history_fact's own real safety filter directly -- never a
    second copy of BLOCK_KEYWORDS to fall out of sync."""
    return [item for item in items if item.get("text") and history_fact._score(item["text"]) is not None and item.get("year")]


def _page_url(item):
    page = (item.get("pages") or [{}])[0]
    return (page.get("content_urls") or {}).get("desktop", {}).get("page")


def _same_date_different_eras_mission(categories):
    safe_events = _safe_items(categories.get("events") or [])
    if len(safe_events) < 2:
        return None
    oldest = min(safe_events, key=lambda e: e["year"])
    newest = max(safe_events, key=lambda e: e["year"])
    if oldest is newest:
        return None
    gap = newest["year"] - oldest["year"]

    return {
        "missionType": "Guided",
        "concept": "same-date-different-eras",
        "title": "Same Calendar Date, Wildly Different Centuries",
        "briefing": (
            "A calendar date repeats every single year, so history piles up dozens of "
            "completely unrelated real events onto the exact same date -- today's real feed "
            "alone has events spanning many centuries."
        ),
        "observe": {
            "kind": "history-pair",
            "a": {"year": oldest["year"], "text": oldest["text"], "url": _page_url(oldest)},
            "b": {"year": newest["year"], "text": newest["text"], "url": _page_url(newest)},
        },
        "question": (
            f"In {oldest['year']}: {oldest['text']} In {newest['year']}: {newest['text']} Both real, both "
            f"documented on today's exact calendar date. About how many years apart do you think they are?"
        ),
        "reveal": (
            f"{gap:,} real years apart. The calendar date connecting them is a coincidence of how "
            f"we count days, not a real historical link -- {oldest['year']} and {newest['year']} share "
            f"nothing except that both happened to fall in late September. That's exactly why "
            f"historians study events by their real cause-and-effect connections to each other, not "
            f"by which day of the year they happened to land on."
        ),
        "investigateLink": "#history-block",
        "investigateLabel": "See today's featured This Day in History fact",
        "recap": f"{oldest['year']} and {newest['year']}: {gap:,} real years apart, same calendar date.",
        "source": "Wikimedia On This Day",
    }


def _births_and_deaths_mission(categories):
    safe_births = _safe_items(categories.get("births") or [])
    safe_deaths = _safe_items(categories.get("deaths") or [])
    if not safe_births or not safe_deaths:
        return None
    birth, death = safe_births[0], safe_deaths[0]

    return {
        "missionType": "Guided",
        "concept": "births-and-deaths",
        "title": "History Keeps Going Every Single Day",
        "briefing": (
            "This Day in History usually means wars, elections, and inventions -- but real "
            "people were also being born and dying on today's exact date throughout history, "
            "just like any other day."
        ),
        "observe": {
            "kind": "history-pair",
            "a": {"year": birth["year"], "text": birth["text"], "url": _page_url(birth)},
            "b": {"year": death["year"], "text": death["text"], "url": _page_url(death)},
        },
        "question": (
            f"Wikipedia's real record lists {len(safe_births)} notable births and "
            f"{len(safe_deaths)} notable deaths on today's exact date. Which do you think there "
            f"are usually more of?"
        ),
        "reveal": (
            f"Today it's {'births' if len(safe_births) >= len(safe_deaths) else 'deaths'} "
            f"({len(safe_births)} vs {len(safe_deaths)} in today's real record) -- though this real "
            f"number changes every day depending on who happens to be notable enough for Wikipedia "
            f"to record. Every single calendar date has real people on both lists; today's are "
            f"{birth['text']} ({birth['year']}) and {death['text']} ({death['year']})."
        ),
        "investigateLink": "#history-block",
        "investigateLabel": "See today's featured This Day in History fact",
        "recap": f"Real record for today: {len(safe_births)} notable births, {len(safe_deaths)} notable deaths.",
        "source": "Wikimedia On This Day",
    }


def _how_we_know_mission(categories):
    safe_events = _safe_items(categories.get("events") or [])
    if len(safe_events) < 2:
        return None
    oldest = min(safe_events, key=lambda e: e["year"])
    newest = max(safe_events, key=lambda e: e["year"])
    if oldest is newest:
        return None

    return {
        "missionType": "Guided",
        "concept": "how-we-know",
        "title": "How Do Historians Actually Know That?",
        "briefing": (
            "Historians don't have the same kind of evidence for every event -- how confident "
            "we can be, and how we know it happened at all, depends heavily on how long ago it was."
        ),
        "observe": {
            "kind": "history-pair",
            "a": {"year": oldest["year"], "text": oldest["text"], "url": _page_url(oldest)},
            "b": {"year": newest["year"], "text": newest["text"], "url": _page_url(newest)},
        },
        "question": (
            f"One real event happened in {oldest['year']}, another in {newest['year']}. Do you "
            f"think historians know about both of them the same way, or differently?"
        ),
        "reveal": (
            f"Differently, and by a lot. An event from {oldest['year']} is usually known through "
            f"a small number of surviving written records, coins, inscriptions, or archaeology -- "
            f"often written down well after the fact by someone with their own point of view. An "
            f"event from {newest['year']} usually has direct documentation: news reports, video, "
            f"official records, sometimes made within minutes of it happening. That real gap in "
            f"evidence is exactly why historians describe ancient history with more caution and "
            f"more competing versions than recent history."
        ),
        "investigateLink": "#history-block",
        "investigateLabel": "See today's featured This Day in History fact",
        "recap": f"{oldest['year']}: known through scarce ancient records. {newest['year']}: known through direct, real-time documentation.",
        "source": "Wikimedia On This Day",
    }


CONCEPTS = {
    "same-date-different-eras": ("Same Calendar Date, Wildly Different Centuries", _same_date_different_eras_mission),
    "births-and-deaths": ("History Keeps Going Every Single Day", _births_and_deaths_mission),
    "how-we-know": ("How Do Historians Actually Know That?", _how_we_know_mission),
}


def list_concepts():
    return [{"id": concept_id, "title": title} for concept_id, (title, _) in CONCEPTS.items()]


def get_history_mission(concept_id):
    entry = CONCEPTS.get(concept_id)
    if not entry:
        return {"status": "unavailable", "reason": f"Unknown concept '{concept_id}'."}
    _, builder = entry

    today = date.today()
    try:
        categories = _fetch_all_categories(today.month, today.day)
    except Exception:
        return {"status": "unavailable", "reason": "Couldn't reach Wikimedia's history archive right now."}

    result = builder(categories)
    if result is None:
        return {"status": "unavailable", "reason": "Not enough real, kid-safe history entries for today's date to build this lesson."}
    return result
