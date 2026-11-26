#!/usr/bin/env python3
"""Seeds 2 more real pages from ATP 3-50.21 (Survival), Chapter 7
(Movement and Navigation) -- mined from the real text layer already
extracted in this session (/tmp/atp_survival.txt, pages 7-10 through
7-13). Complements rather than duplicates the existing USMC-sourced
navigation pages: a more accurate real shadow-based method, 2 real
watch-based direction-finding methods not covered anywhere else in
this wiki, real moon-based direction-finding, and one genuinely new
specific detail about the North Star not previously captured.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_atp_navigation2.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
ATP_SURVIVAL_PDF_URL = "/files/pdfs/Military Manuals/ATP-3-50.21-Survival.pdf"

PAGES = [
    {
        "title": "Finding Direction With a Watch & the Equal-Shadow Method",
        "section": "reference",
        "tags": ["navigation", "sun-navigation", "survival-skills"],
        "risk_level": "low",
        "body_markdown": """## Equal-Shadow Method — a Real, More Accurate Shadow Technique

**More accurate than the basic shadow-stick method (see Daytime Navigation — Sun Movement, Shadow Stick & Pocket Navigator) and genuinely usable at any latitude under 66°, any time of year.**

1. **5-10 minutes before local noon (solar zenith)**, plant a stick vertically where it'll cast a shadow at least 12 inches long, and mark the shadow's tip.
2. **Trace an arc** using the shadow's current length as the radius and the stick's base as the center (a string, shoelace, or second stick works for tracing it).
3. **As noon approaches, the shadow shortens; after noon, it lengthens again until it crosses back over the arc you traced.** Mark that second crossing point the moment it touches.
4. **Draw a straight line through both marks — this is your real east-west line.**

## Watch Method — Using an Analog Watch's Hands

**Northern Temperate Zone:** point the hour hand toward the sun. **South lies midway between the hour hand and 12:00** (standard time) — or midway between the hour hand and 13:00 if on daylight saving time. If unsure which end of that line is actually north vs. south, remember: **the sun sits in the east before noon, west after noon.**

**Southern Temperate Zone:** point the 12:00 mark toward the sun instead. **North lies midway between 12:00 and the hour hand** (or between the hour hand and 13:00 on daylight saving time).

**⚠️ Real accuracy caveat: this method can be unreliable at lower latitudes and may cause you to walk in circles.** **Real fix: build a shadow clock (see Daytime Navigation — Sun Movement, Shadow Stick & Pocket Navigator's pocket navigator) and set your watch to match it. After an hour of travel, take a fresh shadow-clock reading and reset the watch if it's drifted.**

**No analog watch, only digital?** Draw a clock face on a paper circle with the current time marked, and use that paper "watch" the same way — or draw a full clock face on the ground, or simply lay your actual watch flat on the ground for a steadier reading.

## 24-Hour Clock Method — for Anyone Thinking in Military Time

1. **Take the local 24-hour time and divide by 2.**
2. **Northern Hemisphere:** point the resulting "hour" at the sun — **12 then points north.** (Example: 1400 hours ÷ 2 = 0700. Hold the watch flat, point "7" at the sun, and 12 points north.)
3. **Southern Hemisphere:** point 12 at the sun instead — **the resulting divided "hour" then points south.**

## Detailed Version

**The real, shared insight across the watch-based methods: an ordinary analog watch is a real, legitimate direction-finding tool, not just a backup for when "real" navigation gear fails** — but its real accuracy limit (especially near the equator) is exactly why pairing it with a periodic shadow-clock check matters, rather than trusting a single watch reading for an entire journey.
""",
    },
    {
        "title": "Finding Direction by Moon & the Real North Star Latitude Trick",
        "section": "reference",
        "tags": ["navigation", "night-navigation", "survival-skills"],
        "risk_level": "low",
        "body_markdown": """## Using the Moon for a Rough East-West Reference

**The moon has no light of its own — it only reflects the sun's, and which side is lit depends on where it sits in its 28-day orbit.** A real, simple rule for a rough east-west reference at night:

- **If the moon rises before the sun sets: the illuminated side faces WEST.**
- **If the moon rises after midnight: the illuminated side faces EAST.**

This gives a genuinely rough, but real and usable, directional reference during the night when stars might be obscured or hard to read.

## ⚠️ The Real North Star Latitude Trick — a Detail Worth Adding to Existing Star Navigation

**(Complements Nighttime Navigation — Finding North & South Without a Compass, which already covers the Big Dipper and Cassiopeia pointer-star methods for locating Polaris.)**

**The North Star sits at almost exactly the same vertical angle above the horizon as your actual latitude.** Real example: at 35°N latitude, Polaris sits roughly 35 degrees above the horizon. **Knowing this narrows your real search area in the sky dramatically** — rather than scanning the entire sky for the Big Dipper and Cassiopeia, you can focus specifically on the band of sky at roughly your own latitude's angle above the horizon.

**Real reminder on using Cassiopeia (the "Lazy W"):** it has 5 stars forming a "W" shape, with one side of the W appearing flattened ("lazy") — **bisect the angle on that lazy side and extend the resulting line** (about 5 times the distance across that angle) to find the North Star, the same general approach as the Big Dipper's pointer-star method.

## Detailed Version

**The real, practical value of the latitude trick: it converts "search the entire night sky for a specific faint star" into "look at one specific band of sky, at one specific height" — a genuinely large reduction in search effort, especially useful when haze, trees, or terrain limit how much sky is actually visible at once.**
""",
    },
]


def load_token(explicit_token):
    if explicit_token:
        return explicit_token
    env_token = os.environ.get("VAULT_API_TOKEN")
    if env_token:
        return env_token
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("VAULT_API_TOKEN="):
                return line.split("=", 1)[1].strip()
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:8085")
    parser.add_argument("--token", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    token = load_token(args.token)
    if not token:
        print("No VAULT_API_TOKEN found (env var or ../.env). Aborting.", file=sys.stderr)
        sys.exit(1)

    headers = {"X-Vault-Token": token, "Content-Type": "application/json"}
    existing = requests.get(f"{args.base_url}/api/wiki/pages", headers=headers, timeout=10)
    existing.raise_for_status()
    existing_titles = {p["title"] for p in existing.json()}

    created, skipped = 0, 0
    for page in PAGES:
        if page["title"] in existing_titles:
            print(f"SKIP  (already exists): {page['title']}")
            skipped += 1
            continue
        if args.dry_run:
            print(f"WOULD CREATE: {page['title']} (risk={page['risk_level']})")
            created += 1
            continue
        res = requests.post(
            f"{args.base_url}/api/wiki/pages",
            headers=headers,
            json={
                "section": page["section"],
                "title": page["title"],
                "body_markdown": page["body_markdown"],
                "tags": page["tags"],
                "source_url": ATP_SURVIVAL_PDF_URL,
                "verification_status": "verified",
                "risk_level": page["risk_level"],
            },
            timeout=10,
        )
        if res.ok:
            print(f"CREATED: {page['title']}")
            created += 1
        else:
            print(f"FAILED  ({res.status_code}): {page['title']} -- {res.text}", file=sys.stderr)

    print(f"\n{created} created, {skipped} skipped.")


if __name__ == "__main__":
    main()
