"""This Day in History -- real, live, keyless Wikimedia "On This Day"
feed (verified live 2026-09-20, see CARD_REDESIGN_PLAN.md): a real event
description, thumbnail, and Wikipedia link for the current date. Not
available offline (Kiwix's raw dumps don't carry this curated, live-
editorial feed), so today's fact is cached with its date and served
stale-but-labeled when the network is down -- same honest pattern
Weather Labs already uses.

Real, un-fun fact about the raw feed: Wikipedia's "On This Day" is a
plain historical record, not curated for kids -- a random pick can
surface a massacre, a terrorist attack, or similarly graphic content
next to something like a rocket launch, with nothing in the API to tell
them apart. BLOCK_KEYWORDS below is a real, best-effort filter for the
clearly graphic/traumatic categories, not a guarantee -- ordinary
history (wars, elections, notable deaths, stated plainly) stays
eligible, since that's normal, appropriate homeschool history content.
Worth a periodic human spot-check, not "solved."
"""

import json
from datetime import date

import requests

import interactivity
from paths import DATA_DIR

CACHE_FILE = DATA_DIR / "history_fact_cache.json"
HEADERS = {"User-Agent": "Cloud9 This Day in History (kids learning dashboard)"}

BLOCK_KEYWORDS = [
    "massacre", "genocide", "terroris", "mass shooting", "school shooting",
    "rape", "raped", "torture", "tortured", "beheading", "beheaded",
    "mutilat", "suicide bomb", "child abuse", "sexual assault",
    "ethnic cleansing", "concentration camp", "gas chamber",
    "lynch", "hostage", "hijack", "kidnap", "genital",
    "martyr", "burned at the stake", "stoned to death", "beaten to death",
    "hanged", "guillotine", "crucifi", "stabbed to death", "shot dead",
    "gunned down", "poisoned to death", "drowned by", "buried alive",
    "plague", "epidemic", "famine", "starvation",
]

PREFER_KEYWORDS = [
    "first", "discover", "launch", "invent", "founded", "opened",
    "record", "premiere", "publish", "born", "patent", "space",
    "moon", "flight", "explore", "award", "wins", "olympic",
]


def _score(text):
    t = text.lower()
    if any(k in t for k in BLOCK_KEYWORDS):
        return None
    return sum(1 for k in PREFER_KEYWORDS if k in t)


def _pick_event(events, seed):
    scored = [(i, e) for i, e in enumerate(events) if _score(e["text"]) is not None]
    if not scored:
        return events[0] if events else None
    best_score = max(_score(e["text"]) for _, e in scored)
    best = [(i, e) for i, e in scored if _score(e["text"]) == best_score]
    return best[seed % len(best)][1]


def _load_cache():
    if not CACHE_FILE.exists():
        return None
    with open(CACHE_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_today_fact():
    today = date.today()
    cache = _load_cache()
    if cache and cache.get("date") == today.isoformat():
        return dict(cache["fact"], stale=False)

    try:
        resp = requests.get(
            f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events/{today.month:02d}/{today.day:02d}",
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        events = resp.json().get("events", [])
        chosen = _pick_event(events, seed=today.toordinal())
        if not chosen:
            raise LookupError("No events returned for today")

        page = (chosen.get("pages") or [{}])[0]
        fact = {
            "year": chosen.get("year"),
            "text": chosen["text"],
            "thumbnail": (page.get("thumbnail") or {}).get("source"),
            "pageTitle": page.get("normalizedtitle"),
            "pageUrl": (page.get("content_urls") or {}).get("desktop", {}).get("page"),
        }
        _save_cache({"date": today.isoformat(), "fact": fact})

        interactivity.register_content("history:today", ["history", "this_day_in_history"])
        interactivity.log_event("content_viewed", "history:today", payload={"text": fact["text"][:120]})

        return dict(fact, stale=False)
    except (requests.RequestException, LookupError, KeyError, ValueError):
        if cache:
            age_days = (today - date.fromisoformat(cache["date"])).days
            return dict(cache["fact"], stale=True, ageDays=age_days, staleDate=cache["date"])
        raise
