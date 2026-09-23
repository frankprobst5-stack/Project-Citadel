"""Mission Mode's third and last real mission type: Historical (replaying
a real archived event with real archived data). Source is the National
Hurricane Center's own real, public HURDAT2 best-track archive -- a
plain-text file, no key needed, confirmed live before writing any code,
same standing rule as every other lab.

The featured storm is picked dynamically, not hand-curated: every storm
in the whole 1851-present record is checked for a real entry on today's
real calendar month-day, and the most intense one (lowest real central
pressure) becomes today's Historical Mission -- genuinely new content
most days rather than a fixed, memorized list, and it means this module
never has to assert a fact (death toll, exact landfall town) that isn't
directly present in HURDAT2's own position/intensity/pressure columns.
Every claim in the mission text is computed from those real columns,
including "rapid intensification," which uses NHC's own real published
definition (>=35kt wind increase in 24 hours) rather than a vibe.
"""

import re
import sqlite3
import time
from datetime import datetime

import requests

from paths import DATA_DIR

DB_FILE = DATA_DIR / "historical_missions.db"

# The real archive only gets a new revision a handful of times a year --
# safe to cache the raw download for a week.
CACHE_TTL_SECONDS = 7 * 24 * 60 * 60

HURDAT_DIR_URL = "https://www.nhc.noaa.gov/data/hurdat/"
HEADERS = {"User-Agent": "Cloud9 Weather Labs (kids learning dashboard)"}

# Real NHC HURDAT2 status codes (same glossary event_explorer.py already
# uses for the live feed's classification field).
STATUS_LABELS = {
    "TD": "Tropical Depression", "TS": "Tropical Storm", "HU": "Hurricane",
    "SD": "Subtropical Depression", "SS": "Subtropical Storm",
    "EX": "Extratropical Cyclone", "LO": "Low", "WV": "Tropical Wave", "DB": "Disturbance",
}


def _connect():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, fetched_at REAL NOT NULL, payload TEXT NOT NULL)"
        )


_init_db()


def _get_cached(key):
    with _connect() as conn:
        row = conn.execute("SELECT fetched_at, payload FROM cache WHERE key = ?", (key,)).fetchone()
    if not row:
        return None
    return {"fetchedAt": row[0], "data": row[1]}


def _set_cached(key, text):
    with _connect() as conn:
        conn.execute("INSERT OR REPLACE INTO cache (key, fetched_at, payload) VALUES (?, ?, ?)", (key, time.time(), text))


def _latest_hurdat_filename():
    """Real filenames embed a revision date (e.g.
    hurdat2-1851-2025-091226.txt) that can't be hardcoded -- confirmed
    live that NHC's own directory listing is the real way to find the
    current one, same reasoning as scraping the forecast cone image in
    event_explorer.py. Picks the file with the newest end-year, then the
    newest revision suffix, restricted to the plain Atlantic series
    (hurdat2-1851-*) so a Pacific or one-off revision file never wins by
    accident."""
    resp = requests.get(HURDAT_DIR_URL, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    names = re.findall(r'hurdat2-1851-(\d{4})-(\d+)\.txt', resp.text)
    if not names:
        raise LookupError("No real HURDAT2 Atlantic file found in the NHC directory listing")
    end_year, revision = max(names, key=lambda t: (int(t[0]), t[1]))
    return f"hurdat2-1851-{end_year}-{revision}.txt"


def _fetch_hurdat_text():
    cache_key = "hurdat2_atlantic"
    cached = _get_cached(cache_key)
    if cached and (time.time() - cached["fetchedAt"]) < CACHE_TTL_SECONDS:
        return cached["data"]
    try:
        filename = _latest_hurdat_filename()
        resp = requests.get(HURDAT_DIR_URL + filename, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        text = resp.text
        _set_cached(cache_key, text)
        return text
    except Exception:
        if cached:
            return cached["data"]
        raise


def _parse_storms(text):
    lines = text.splitlines()
    storms = []
    i = 0
    header_re = re.compile(r"^(AL\d{6}),\s*([A-Z0-9\-]+),\s*(\d+),$")
    while i < len(lines):
        m = header_re.match(lines[i].strip())
        if not m:
            i += 1
            continue
        storm_id, name, count = m.group(1), m.group(2), int(m.group(3))
        entries = []
        for j in range(i + 1, i + 1 + count):
            parts = [p.strip() for p in lines[j].split(",")]
            wind_kt, pressure_mb = int(parts[6]), int(parts[7])
            entries.append({
                "date": parts[0], "time": parts[1],
                "status": parts[3], "lat": parts[4], "lon": parts[5],
                "windKt": wind_kt, "pressureMb": pressure_mb if pressure_mb != -999 else None,
            })
        storms.append({"id": storm_id, "name": name.title(), "entries": entries})
        i += 1 + count
    return storms


def _find_rapid_intensification(entries):
    """Real NHC definition: a >=35kt increase in maximum sustained wind
    within 24 hours. Entries are 6-hourly, so 24h later is 4 entries
    ahead -- checked directly, not assumed, since a storm's record can
    have gaps."""
    for i in range(len(entries) - 4):
        a, b = entries[i], entries[i + 4]
        try:
            t1 = datetime.strptime(a["date"] + a["time"], "%Y%m%d%H%M")
            t2 = datetime.strptime(b["date"] + b["time"], "%Y%m%d%H%M")
        except ValueError:
            continue
        if (t2 - t1).total_seconds() == 24 * 3600:
            gain = b["windKt"] - a["windKt"]
            if gain >= 35:
                return {"before": a, "after": b, "gainKt": gain}
    return None


def _format_date(entry):
    d = entry["date"]
    return f"{d[4:6]}/{d[6:8]}/{d[0:4]}"


def get_historical_mission(today_month, today_day):
    try:
        text = _fetch_hurdat_text()
    except Exception:
        return {"status": "unavailable", "reason": "Couldn't reach the National Hurricane Center's historical archive right now."}

    storms = _parse_storms(text)
    today_mmdd = f"{today_month:02d}{today_day:02d}"

    best = None
    for storm in storms:
        for entry in storm["entries"]:
            if entry["date"][4:8] == today_mmdd and entry["pressureMb"] is not None:
                if best is None or entry["pressureMb"] < best[1]["pressureMb"]:
                    best = (storm, entry)

    if best is None:
        return {"status": "unavailable", "reason": "No storm in the real archive had a documented entry on this calendar date."}

    storm, today_entry = best
    entries = storm["entries"]
    peak_entry = min((e for e in entries if e["pressureMb"] is not None), key=lambda e: e["pressureMb"])
    ri = _find_rapid_intensification(entries)
    year = storm["id"][4:8]

    observe = {
        "kind": "historical-storm",
        "name": storm["name"],
        "year": year,
        "formationDate": _format_date(entries[0]),
        "dissipationDate": _format_date(entries[-1]),
        "peakDate": _format_date(peak_entry),
        "peakWindKt": peak_entry["windKt"],
        "peakPressureMb": peak_entry["pressureMb"],
        "todayDate": _format_date(today_entry),
        "todayStatus": STATUS_LABELS.get(today_entry["status"], today_entry["status"]),
        "todayWindKt": today_entry["windKt"],
        "todayPressureMb": today_entry["pressureMb"],
    }

    if ri:
        question = (
            f"Between {_format_date(ri['before'])} and {_format_date(ri['after'])} -- exactly 24 real hours -- "
            f"{storm['name']}'s winds jumped from {ri['before']['windKt']} kt to {ri['after']['windKt']} kt, a real "
            f"{ri['gainKt']} kt gain. NHC has an official name for a wind jump that fast. Do you know what it's called?"
        )
        reveal = (
            f"Rapid intensification -- NHC's own real definition is a wind increase of 35 kt (40 mph) or more in "
            f"24 hours, and {storm['name']}'s real {ri['gainKt']} kt jump clears that bar. It happens when a storm "
            f"moves over unusually warm water with low wind shear -- ideal fuel, and nothing tearing the storm apart "
            f"while it uses it. It's exactly why the pressure/wind relationship from the Guided Hurricanes lesson "
            f"matters in practice: forecasters watch pressure drop in real time as the first sign this is happening."
        )
    else:
        question = (
            f"{storm['name']} ({year}) reached its real peak of {peak_entry['windKt']} kt on {_format_date(peak_entry)}, "
            f"with a minimum pressure of {peak_entry['pressureMb']} mb. Do you think every hurricane goes through a "
            f"sudden, rapid strengthening, or can a storm intensify gradually instead?"
        )
        reveal = (
            f"Gradually, sometimes -- {storm['name']}'s own real record doesn't show a documented 24-hour jump of "
            f"35 kt or more (NHC's real definition of \"rapid intensification\"), so this particular storm reached "
            f"its {peak_entry['windKt']} kt peak more steadily. Real storms don't all follow the same script -- some "
            f"explode in strength overnight, others build for days. That's exactly why forecasters track every real "
            f"6-hour advisory instead of assuming one pattern fits every storm."
        )

    return {
        "missionType": "Historical",
        "title": f"{storm['name']} ({year}): This Day in Hurricane History",
        "briefing": (
            f"On this exact calendar date in {year}, {storm['name']} was a real, documented "
            f"{STATUS_LABELS.get(today_entry['status'], today_entry['status'])} with {today_entry['windKt']} kt winds "
            f"-- the most intense storm on record for today's date in the whole 1851-present Atlantic archive."
        ),
        "observe": observe,
        "question": question,
        "reveal": reveal,
        "investigateLink": "#wl-deck-events",
        "investigateLabel": "Compare with a real storm active right now in the Weather Event Explorer",
        "recap": (
            f"{storm['name']} ({year}): formed {_format_date(entries[0])}, peaked at {peak_entry['windKt']} kt / "
            f"{peak_entry['pressureMb']} mb on {_format_date(peak_entry)}, dissipated {_format_date(entries[-1])} -- "
            f"a real, complete storm history, not a forecast."
        ),
        "source": "NOAA/NHC",
        "product": "HURDAT2 Atlantic hurricane database (1851-present)",
    }
