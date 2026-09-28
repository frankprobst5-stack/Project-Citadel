"""Cloud9 2.0's six real Areas (My Day/Learn/Explore/Create/Tutor/Play) --
locked in CARD_REDESIGN_PLAN.md as the home screen's real information
architecture, replacing the old flat grid of same-sized cards.

Each Area is a destination hub: real hero art, a tagline, and a grid of
tiles pointing at the real features that already exist and belong there.
This orchestrates existing pages/panels rather than rebuilding anything --
same principle already applied to Kolibri (School Library) and Scratch
(Code Lab).

A destination's `kind` is either:
  - "page": a real, separate Cloud9 page -- `href` is that page's own URL.
  - "modal": a panel that lives on the home page itself -- `href` points
    back at `/` with `?open=<id>`, and `dashboard.js`'s `openPanelById()`
    is what actually opens it once the home page loads.
"""

import settings

AREAS = {
    "my-day": {
        "title": "My Day",
        "tagline": "Your daily homeschool command center.",
        "icon": "\U0001F31E",
        "hero_img": "img/areas/my-day.png",
        "destinations": [
            {"title": "Daily Planner", "subtitle": "Notes & calendar", "icon": "\U0001F4C5", "kind": "modal", "id": "planner"},
            {"title": "Science Journal", "subtitle": "Log what you noticed or built", "icon": "\U0001F52C", "kind": "modal", "id": "journal"},
        ],
    },
    "learn": {
        "title": "Learn",
        "tagline": "Structured learning and reference.",
        "icon": "\U0001F4DA",
        "hero_img": "img/areas/learn.png",
        "destinations": [
            {"title": "School Library", "subtitle": "Videos & exercises", "icon": "\U0001F4DA", "kind": "page", "href": "/school-library"},
            {"title": "Math Lab", "subtitle": "Times tables, challenges & a math sandbox", "icon": "\U0001F522", "kind": "page", "href": "/math-lab"},
            {"title": "Dictionary", "subtitle": "Look up a word", "icon": "\U0001F4D6", "kind": "modal", "id": "dictionary"},
        ],
    },
    "explore": {
        "title": "Explore",
        "tagline": "Curiosity-driven discovery.",
        "icon": "\U0001F30D",
        "hero_img": "img/areas/explore-geography.png",
        "destinations": [
            {"title": "Earth Lab", "subtitle": "Click a country, learn something new", "icon": "\U0001F30D", "kind": "page", "href": "/earth-lab"},
            {"title": "Weather Labs", "subtitle": "Learn to read the sky", "icon": "⛈️", "kind": "page", "href": "/weather-labs"},
        ],
    },
    "create": {
        "title": "Create",
        "tagline": "Make and build.",
        "icon": "\U0001F3A8",
        "hero_img": "img/areas/create.png",
        "destinations": [
            {"title": "Code Lab", "subtitle": "Build & run your own scripts", "icon": "\U0001F9E9", "kind": "modal", "id": "code_lab"},
            {"title": "STEM Lab", "subtitle": "Circuits, Bluetooth & how things work", "icon": "⚡", "kind": "modal", "id": "stem_lab"},
            {"title": "Writing Paper", "subtitle": "Practice a story or report", "icon": "✍️", "kind": "modal", "id": "writing"},
        ],
    },
    "tutor": {
        "title": "Tutor",
        "tagline": "Ollie, your local AI learning companion.",
        "icon": "\U0001F916",
        "hero_img": "img/mascot/ollie.png",
        "destinations": [
            {"title": "Ask Ollie", "subtitle": "Explain, quiz, hints, and help", "icon": "\U0001F916", "kind": "modal", "id": "ai_assist"},
            {"title": "Dictionary", "subtitle": "Look up a word", "icon": "\U0001F4D6", "kind": "modal", "id": "dictionary"},
        ],
    },
    "play": {
        "title": "Play",
        "tagline": "Healthy downtime.",
        "icon": "\U0001F3AE",
        "hero_img": "img/areas/play.png",
        "destinations": [
            {"title": "Arcade", "subtitle": "Simple games, just for fun", "icon": "\U0001F579️", "kind": "modal", "id": "arcade"},
            {"title": "Video Shelf", "subtitle": "Watch something good", "icon": "\U0001F3AC", "kind": "modal", "id": "video_shelf"},
            {"title": "Bible Study", "subtitle": "Stories, just for you", "icon": "\U0001F4D6", "kind": "modal", "id": "bible_study"},
        ],
    },
}

AREA_ORDER = ["my-day", "learn", "explore", "create", "tutor", "play"]


def get_area(area_id):
    """Real area data, with settings-dependent destinations resolved
    (My School's real configured link, Bible Study only when enabled) --
    same logic the old flat `cards.json` grid used to apply itself."""
    area = AREAS.get(area_id)
    if not area:
        return None

    current_settings = settings.get_settings()
    destinations = [dict(d) for d in area["destinations"]]

    if area_id == "learn" and current_settings.get("school_url"):
        destinations.insert(1, {
            "title": current_settings.get("school_name") or "My School",
            "subtitle": "Go to school",
            "icon": "\U0001F393",
            "kind": "external",
            "href": current_settings["school_url"],
        })

    if area_id == "play" and not current_settings.get("bible_study_enabled"):
        destinations = [d for d in destinations if d.get("id") != "bible_study"]

    result = dict(area)
    result["id"] = area_id
    result["destinations"] = destinations
    return result


def list_areas():
    return [get_area(area_id) for area_id in AREA_ORDER]
