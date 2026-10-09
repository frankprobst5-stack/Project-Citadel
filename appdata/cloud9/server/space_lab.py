"""Space Lab's real landing experience -- ROADMAP.md Phase 3, item 5:
Tonight's Sky (moon phase, sunrise/sunset, ISS passes only when a
trustworthy source is actually available).

Real sourcing, checked live before building anything:
- Moon phase: a standard, widely-published deterministic calculation
  (days since the known 2000-01-06 18:14 UTC new moon, modulo the real
  synodic month length) -- no API, no uptime risk, accurate to within
  about an hour for any date.
- Sunrise/sunset: sunrise-sunset.org's real v1 API (free, no key,
  documented as "supported indefinitely"). Confirmed live before use.
  Returns UTC -- converted to local time client-side, which is exactly
  correct here since the browser viewing this page is physically at the
  real configured location.
- ISS passes: iss-api.polluxlabs.io -- a real rebuild of the retired
  open-notify.org API, using actual CelesTrak TLE data and the
  industry-standard SGP4 propagator (via Skyfield), confirmed live
  before use. It's a small, community-run service (not NASA/NOAA), so
  this module degrades honestly (empty list, not fabricated passes) if
  it's unreachable -- matching the roadmap's own "only when trustworthy"
  rule.
- Visible planets: real candidate (api.visibleplanets.dev, a legitimate
  wrapper around Don Cross's JS Astronomy Engine) was checked live and
  found returning 503 on every request, including its root path --
  not reliable enough to build on right now. Left out honestly rather
  than faked; real, named work once a working source exists.

Reuses settings.py's existing real lat/lon (already populated by Weather
Labs' own location setup) rather than asking for location twice.
"""

import datetime
import math

import requests
import settings

HEADERS = {"User-Agent": "Cloud9 Space Lab (kids learning dashboard)"}

_SYNODIC_MONTH_DAYS = 29.53058867
_KNOWN_NEW_MOON = datetime.datetime(2000, 1, 6, 18, 14)

_PHASE_NAMES = [
    (0.03, "New Moon"),
    (0.22, "Waxing Crescent"),
    (0.28, "First Quarter"),
    (0.47, "Waxing Gibbous"),
    (0.53, "Full Moon"),
    (0.72, "Waning Gibbous"),
    (0.78, "Last Quarter"),
    (0.97, "Waning Crescent"),
    (1.01, "New Moon"),
]


def get_moon_phase(date=None):
    if date is None:
        date = datetime.date.today()
    moment = datetime.datetime.combine(date, datetime.time(12, 0))
    days_since = (moment - _KNOWN_NEW_MOON).total_seconds() / 86400
    fraction = (days_since % _SYNODIC_MONTH_DAYS) / _SYNODIC_MONTH_DAYS

    phase_name = next(name for threshold, name in _PHASE_NAMES if fraction < threshold)
    illumination_pct = round((1 - math.cos(2 * math.pi * fraction)) / 2 * 100)

    return {
        "date": date.isoformat(),
        "phaseName": phase_name,
        "illuminationPct": illumination_pct,
        "fraction": round(fraction, 4),
    }


def get_sun_times():
    current_settings = settings.get_settings()
    lat, lon = current_settings.get("lat"), current_settings.get("lon")
    if lat is None or lon is None:
        return None
    try:
        resp = requests.get(
            "https://api.sunrise-sunset.org/json",
            params={"lat": lat, "lng": lon, "formatted": 0},
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("status") != "OK":
            return None
        results = data["results"]
        return {
            "sunrise": results["sunrise"],
            "sunset": results["sunset"],
            "civilTwilightBegin": results["civil_twilight_begin"],
            "civilTwilightEnd": results["civil_twilight_end"],
            "dayLengthSeconds": results["day_length"],
            "source": "sunrise-sunset.org",
        }
    except requests.RequestException:
        return None


def get_iss_passes():
    current_settings = settings.get_settings()
    lat, lon = current_settings.get("lat"), current_settings.get("lon")
    if lat is None or lon is None:
        return {"available": False, "passes": []}
    try:
        resp = requests.get(
            "https://iss-api.polluxlabs.io/iss-pass",
            params={"lat": lat, "lon": lon, "visible_only": "true", "n": 5},
            headers=HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
        passes = [
            {
                "riseTime": p["rise"]["time"],
                "setTime": p["set"]["time"],
                "maxElevationDeg": p["culmination"]["elevation_deg"],
                "compass": p["rise"]["compass"],
                "durationSec": p["visible_duration_sec"],
            }
            for p in data.get("passes", [])
        ]
        return {"available": True, "passes": passes, "source": "iss-api.polluxlabs.io (community-run, not NASA/NOAA)"}
    except (requests.RequestException, KeyError):
        return {"available": False, "passes": []}


def get_tonight():
    current_settings = settings.get_settings()
    return {
        "locationLabel": current_settings.get("location_label") or None,
        "moonPhase": get_moon_phase(),
        "sunTimes": get_sun_times(),
        "iss": get_iss_passes(),
    }


# Long Missions -- ROADMAP.md's own instruction: "feeding directly into
# Project Workshop (already built -- this is real reuse, not new
# storage, same pattern as Learning Journal)." No new DB table here;
# "starting" one of these just calls Project Workshop's own real
# create_project() with real, pre-filled content, same as a parent would
# do by hand -- these two both reuse data this Lab already computed for
# real (Tonight's Sky's real moon-phase names, Solar System Explorer's
# real relative sizes) rather than inventing separate content.
LONG_MISSIONS = [
    {
        "id": "moon-journal",
        "title": "Moon Journal",
        "blurb": "Watch the real Moon every night for one full lunar cycle (about 29 days) and see the real pattern for yourself.",
        "goal": "Watch and record the real Moon's phase every night for one full lunar cycle (about 29 days) to see the real pattern for yourself, using Tonight's Sky to check the real phase each night.",
        "materials": ["A notebook or the Learning Journal", "Tonight's Sky page, checked each night"],
        "checklist": [
            "Record a night you saw a New Moon",
            "Record a night you saw a Waxing Crescent",
            "Record a night you saw a First Quarter",
            "Record a night you saw a Waxing Gibbous",
            "Record a night you saw a Full Moon",
            "Record a night you saw a Waning Gibbous",
            "Record a night you saw a Last Quarter",
            "Record a night you saw a Waning Crescent",
            "Write a Learning Journal entry about the real pattern you noticed",
        ],
    },
    {
        "id": "solar-system-model",
        "title": "Build a Scale Model of the Solar System",
        "blurb": "Use Solar System Explorer's real relative sizes to build your own model with things from around the house.",
        "goal": "Use Solar System Explorer's real relative sizes to build a scale model of the solar system with real household objects, in the real order from the Sun.",
        "materials": ["Solar System Explorer's real size numbers", "Household objects of different sizes (balls, fruit, beads, coins, etc.)", "A camera to photograph the finished model"],
        "checklist": [
            "Pick a real object to represent Earth",
            "Find objects for Mercury, Venus, and Mars using the real relative sizes",
            "Find objects for Jupiter, Saturn, Uranus, and Neptune using the real relative sizes",
            "Lay them out in the real order from the Sun",
            "Take a photo of the finished model",
            "Write a Learning Journal entry about what surprised you",
        ],
    },
]


def get_long_missions():
    return LONG_MISSIONS


def start_long_mission(mission_id):
    import learning_engine
    import project_workshop

    mission = next((m for m in LONG_MISSIONS if m["id"] == mission_id), None)
    if not mission:
        return None

    project = project_workshop.create_project(
        mission["title"], mission["goal"], mission["materials"], mission["checklist"]
    )
    learning_engine.record_activity(
        "space",
        "start_long_mission",
        mission_id,
        source="cloud9-space-lab",
        correct=None,
        artifact=mission["title"],
    )
    return project
