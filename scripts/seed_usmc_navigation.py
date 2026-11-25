#!/usr/bin/env python3
"""Seeds 5 real pages from the USMC Winter Survival Course Handbook's
Survival Navigation chapter -- mined from the real text layer already
extracted in this session (/tmp/usmcwinter.txt, pages 07-1 through
07-13). A genuinely rich, broadly civilian-applicable chapter: real
no-compass direction-finding technique (shadow stick, pocket
navigator, North Star, Southern Cross, improvised compasses, natural
signs) and real decision-making/log-keeping guidance for navigating
without a map.

Covers: the real stay-or-travel decision framework, real sun-based
daytime navigation technique (shadow stick, pocket navigator, local
apparent noon), real night-sky direction-finding (Big Dipper/
Cassiopeia to the North Star, the Southern Cross), 3 real improvised
compass techniques ranked by reliability plus real natural navigation
signs, and real field-sketch/log-keeping technique for not getting
lost without a map.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_navigation.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
USMC_WINTER_PDF_URL = "/files/pdfs/Military Manuals/USMC-Winter-Survival-Course-Handbook.pdf"

PAGES = [
    {
        "title": "Deciding Whether to Stay or Travel — Survival Decision Points",
        "section": "reference",
        "tags": ["survival-skills", "navigation", "decision-making"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Staying put is usually the safer default — a vehicle or known location is both a real shelter and a known point rescuers can search toward.** Only leave it when specific, real conditions are met.

## Real Reasons to Stay

**Stay with a vehicle/aircraft/known location if at all possible** — someone likely knows roughly where it was headed, and it's already a ready-made shelter.

## Real Conditions That Justify Leaving

1. You're certain of your present location, have a known destination, and genuinely have the ability to reach it.
2. Water, food, shelter, or real help can actually be reached by traveling.
3. You're genuinely convinced rescue isn't coming.

## If You Decide to Travel — Real Things to Plan First

- Which direction, and why that direction specifically.
- What the actual travel plan is.
- What equipment to bring.
- How you'll mark your trail as you go.
- The predicted weather for your travel window.

## Real Information to Leave Behind at Your Departure Point

Departure time, destination, your planned route/direction, your physical condition, and what supplies you're taking with you — **all of this is exactly what a search party needs to actually find you if you leave before they arrive.**

## Detailed Version

**The real principle underlying this whole page: the decision to travel should be driven by genuine necessity and real information, not by restlessness or assumption that rescue has already given up.** Leaving a known, already-locatable position to travel toward an uncertain destination is a real, serious trade-off — and the information you leave behind at your original position is what preserves a rescuer's ability to still find you even after you've gone.
""",
    },
    {
        "title": "Daytime Navigation — Sun Movement, Shadow Stick & Pocket Navigator",
        "section": "reference",
        "tags": ["navigation", "sun-navigation", "survival-skills"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**"The sun rises in the east and sets in the west" is a real oversimplification — depending on latitude and season, the sun can rise/set up to 50 degrees off true east/west.** Real sun-based navigation accounts for this rather than assuming a fixed direction.

## The Real Pattern

**Solstices** (around June 21 and December 21) are the two points in the year when the sun has no apparent north/south drift. **Equinoxes** (around March 20 and September 23) are when the sun crosses the celestial equator and day/night length are roughly equal. Across a single day, the sun moves in a uniform arc — and **at exactly the midpoint of that arc, the sun sits due south of an observer in the Northern Hemisphere** (due north if you're in the Southern Hemisphere). This moment — when shadows are shortest — is called **"local apparent noon."**

**⚠️ This south/north rule doesn't reliably apply in the tropics (within 23.5° of the equator) or near the poles (above ~60° latitude).**

## Finding Local Apparent Noon

- **If you know sunrise and sunset times:** take the total daylight hours, divide by 2, and add that to sunrise. (Example: sunrise 0630, sunset 1930 = 13 hours daylight ÷ 2 = 6h30m; 0630 + 6h30m = local apparent noon at 1300.)
- **The string method:** mark two points where a shadow falls at equal lengths before and after your estimate of solar noon; the midpoint between those two marks is the real local apparent noon.

## Shadow Stick Method — Real Accuracy Within 10°, But Time-Limited

**Only works within about 2 hours of local apparent noon** (and is impractical very near the poles, where shadows run extremely long, or deep in the tropics, where they're very short).

1. Find a straight, branch-free stick (3-6 feet) with pointed ends, plus 3-5 small markers (pebbles, twigs).
2. Plant the stick upright in the ground and mark the current tip of its shadow.
3. Wait 10-15 minutes, then mark the new shadow-tip position. Repeat until you're out of markers.
4. **The resulting markers form a real, usable west-to-east line.**
5. **Stand with your left foot on the first marker and your right foot on the last marker — you are now facing north.**

## Pocket Navigator — a Real, All-Day, Week-Long-Accurate Sundial

**What you need:** a flat piece of cardboard, a watch, a pen/pencil, and a 1-2 inch pin or nail.

1. Set the pin upright on the flat material where sunlight will cast a shadow from it; mark its base position so you can replace it exactly later. Weight the card down against wind.
2. **Every 15 minutes, mark the current tip of the pin's shadow and write down the time next to each mark.**
3. By end of day, connect the marks — they'll form a curved line (flatter near the equinoxes, more pronounced otherwise). **If you can't finish in one day, resume the next day by realigning the shadow to a previously plotted point.**
4. **The mark made at the sun's highest point (solar noon) is your real north-south line** — draw an arrow from the pin's base through that mark; this is the shortest line from the base to the shadow curve.
5. **To use it later: hold the navigator so the current shadow aligns with the plotted point for the current time** — this both re-levels the device and confirms your drawn arrow is still pointing true north.
6. **The same pocket navigator stays accurate for about a week** before needing to be rebuilt.

## Detailed Version

**The real, shared insight behind both the shadow stick and pocket navigator: the sun's shadow movement is predictable enough to extract a genuinely accurate compass bearing from it, without any magnetic equipment at all** — the shadow stick trades setup simplicity for a narrow 2-hour usable window around solar noon, while the pocket navigator trades more setup effort for all-day, multi-day reusable accuracy. Picking between them is a real trade-off based on how much time and attention you can actually give it.
""",
    },
    {
        "title": "Nighttime Navigation — Finding North & South Without a Compass",
        "section": "reference",
        "tags": ["navigation", "night-navigation", "survival-skills"],
        "risk_level": "low",
        "body_markdown": """## Finding the North Star (Northern Hemisphere) — 2 Real Methods

1. **Using the Big Dipper:** the two lowest stars of the Big Dipper's "cup" act as real pointers — draw an imaginary straight line through them, extended outward, and **the North Star sits along that line at a distance roughly 5 times the gap between the two pointer stars.** (The North Star is technically the end star in the Little Dipper's handle, but the Little Dipper itself is much harder to spot directly — this is why the Big Dipper method is the real practical approach.)
2. **Using Cassiopeia** (the "Big M" or "W" shaped constellation): draw a line straight out from its center star, roughly half the distance you'd travel to reach the Big Dipper — **the North Star sits at that point.**

**⚠️ Real caveat: both the Big Dipper and Cassiopeia rotate around the North Star through the night, so their own position in the sky changes — don't expect them to always appear in the same spot.** Also, **at very high latitudes, the North Star sits high overhead rather than near the horizon, which makes it a genuinely less useful directional reference there** — at the center of the Arctic Circle, it would be directly overhead, where every direction from you leads south.

## Finding South (Southern Hemisphere) — the Southern Cross

**Polaris isn't visible in the Southern Hemisphere — the Southern Cross is the real equivalent reference.** An imaginary line extended through its long axis points toward a real, star-free dark patch roughly 3° offset from the actual South Pole.

**⚠️ Don't confuse the real "True Cross" with the larger, nearby "False Cross"** — the False Cross is dimmer, more widely spaced, and has 5 stars rather than 4. **A reliable way to confirm you've found the True Cross: look for two closely-spaced, very bright stars trailing behind its crosspiece — these two stars are often easier to spot than the cross shape itself**, and their presence confirms you're looking at the real True Cross. Two of the True Cross's own stars (on its southern and eastern arms) are notably brighter than the other two.

## Moon Navigation

**The moon rises in the east and sets in the west, just like the sun** — the same shadow-stick technique used in daylight works with moonlight too. **Real limitation: moonlight is far less consistent than sunlight and is easily obscured by clouds**, making this method meaningfully less reliable than sun-based methods.

## Detailed Version

**The real, most valuable single fact on this page for anyone without a dedicated star chart: the "pointer stars" technique (Big Dipper → North Star, Southern Cross's bright trailing stars → confirmation) works precisely because it turns "find one specific, sometimes-hard-to-spot star" into "find an easier, more prominent pattern and follow a simple rule from there."** This is the same practical principle behind most real field navigation technique in this chapter — use the more visible, more reliable reference to find the less visible, more useful one.
""",
    },
    {
        "title": "Improvised Compasses & Natural Navigation Signs",
        "section": "reference",
        "tags": ["navigation", "improvised-compass", "survival-skills"],
        "risk_level": "low",
        "body_markdown": """## 3 Real Improvised Compass Techniques — Ranked Most to Least Reliable

### 1. Magnet Technique (most reliable)

**Needed:** a magnet (a radio speaker or headphone magnet works well) and a small, thin, light piece of ferrous metal — **it must actually rust** (steel/iron); aluminum or other non-ferrous "yellow metals" will not work. A needle, pin, straightened paper clip, or thin steel wire all work; smaller is better.

1. Hold the metal against the magnet (or a battery, per the source — at least 2 minutes minimum, longer is fine) to magnetize it.
2. **Float it on still water** using a small non-magnetic support (a wood chip, leaf, bit of foam) in a non-magnetic container or depression (⚠️ not a steel "tin can" — an aluminum can is fine). Place the magnetized metal on the float; it will slowly rotate to align itself.
3. **Repeat the process a few times to confirm consistency** before trusting the reading.
4. **Alternative: hang the needle from a thread in a draft-free space** — this works but is real meaningfully less reliable than the floating method.

### 2. Magnetization Through a Battery

A battery (2+ volts) with a length of wire tightly coiled around the needle (wrap the needle in paper/cardboard first if the wire isn't insulated), connected to the battery terminals for about 5 minutes. **Needs a tight coil and a battery with real remaining charge** — a weak battery produces the same unreliable result as the technique below.

### 3. Synthetic Technique (least reliable — use only if nothing else is available)

**Doesn't magnetize the metal strongly enough to give a consistently true reading**, especially in any wind — real accuracy here can be as poor as 1-in-5 correct readings, off by up to 45°.

## Real Problems With Any Improvised Compass

- **Soft steel loses its magnetism fairly quickly** — expect to re-magnetize the needle up to 2-3 times a day.
- **Test it by disturbing the needle after it settles, then watching if it returns to the same alignment** — repeat this check a few times. A consistent return means it's working, though you'll still need the sun/stars/other natural signs to determine which end is actually north versus south.

## Real Natural Navigation Signs (Northern Hemisphere)

**Find the prevailing wind direction first** — it informs several of the signs below. **The sun's apparent daily path runs roughly SE-to-SW** in the Northern Hemisphere, which drives these real, visible effects:

- **Trees bent by prevailing wind** — a consistent lean indicates the wind's habitual direction.
- **Sapling bark coloration:** the side facing the sun (roughly SW-to-SE) often turns whitish as a natural sunscreen response — **pick a sapling standing in the open, exposed all day, for a reliable read.**
- **Vegetation density on a slope:** the side that gets the most sun exposure (roughly SW) tends to grow thicker vegetation.
- **Snow melt patterns on a tree or slope:** the side that melts/refreezes repeatedly tends to be the sun-facing (south) side.
- **"Bleached" rock:** prolonged sun exposure can visibly lighten one face of a rock — the lighter face tends to face south. (Obviously, a rock that's simply white-colored naturally isn't a useful sign here.)

**⚠️ Always look for more than one confirming sign before trusting a direction** — any single natural sign alone can be misleading in specific local conditions.

## Detailed Version

**The real, repeated lesson across both the compass techniques and the natural signs: every one of these methods is probabilistic, not certain, which is exactly why the source repeatedly emphasizes re-testing and cross-confirming with a second method.** Treating any single improvised compass reading or natural sign as definitive, rather than as one data point to confirm against another, is the real, most common way these techniques lead someone astray.
""",
    },
    {
        "title": "Navigating Without a Map — Log-Keeping & Getting Un-Lost",
        "section": "reference",
        "tags": ["navigation", "wayfinding", "survival-skills"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Without a map, a real, continuously updated field sketch is what actually prevents walking in circles** — memory alone is genuinely unreliable for this over any real distance or time.

## Real Navigator Basics

1. Settle on one navigation method (sun, stars, compass — whatever's actually reliable in your conditions) and stick with it consistently.
2. Determine your cardinal direction using that method.
3. **Pick a visible "steering mark"** — a tree, rock formation, ridge line — in your intended direction of travel, and walk toward it rather than trying to hold an abstract compass bearing the whole way.

## Building and Maintaining a Real Field Log

**Use whatever material is available** — paper, a flattened box, even fabric. Draw a simple field sketch marking north, prominent terrain features, and the distance/direction you've actually traveled. **Note anything genuinely useful you observe along the way** — water sources, game trails, trails/roads, notable vegetation.

**Keep updating it as you move** — a log that isn't maintained loses its value quickly. **Keep it simple and legible** — a cluttered sketch that only you (and only in the moment) can read defeats the purpose; aim for something anyone could interpret later.

**While moving, continuously refer back to both your log and your current steering mark** — don't treat either as a one-time setup step.

## Real Actions If You Realize You're Lost

1. **Immediate action: re-orient your sketch** — stop and establish where you actually are relative to what you've recorded, before doing anything else.
2. **Corrective action:** backtrack using your own recorded steering marks until you can identify where the error actually happened, re-orient your sketch at that confirmed point, then re-select a direction and continue.

## Detailed Version

**The real, most important discipline underlying all of this: a steering mark converts an abstract compass bearing into a concrete, walkable target, and a maintained log converts "I think I'm going the right way" into an actually checkable record.** Both exist specifically to catch drift — the slow, easy-to-miss process by which someone without a map gradually veers off their intended line without ever feeling like they've made a single wrong turn.
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
                "source_url": USMC_WINTER_PDF_URL,
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
