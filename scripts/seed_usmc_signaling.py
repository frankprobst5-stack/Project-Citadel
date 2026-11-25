#!/usr/bin/env python3
"""Seeds 3 real pages from the USMC Winter Survival Course Handbook's
Survival Signaling and Recovery chapter -- mined from the real text
layer already extracted in this session (/tmp/usmcwinter.txt, pages
06-1 through 06-8). Filtered to genuinely civilian-accessible
technique: a whistle, a flashlight, a mirror, and improvised ground
signals are things anyone can actually carry or build. Military-
specific signaling hardware (M-186 pen flares, AN/PRC survival
radios, day/night flares) and the combat-evasion-specific "Recovery"
section (hostile-area signal placement, helicopter hoist devices,
border-crossing SOPs) are deliberately excluded as not practically
relevant to a civilian disaster-prep context.

Covers: the real international audio/visual distress signal patterns,
real smoke-generator and ground-symbol signal construction (including
the real international ground-to-air symbol set and shadow-signal
technique), and real signal-mirror technique plus the standard
aircraft acknowledgment signals.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_signaling.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Signaling for Rescue — Audio & Visual Distress Signals",
        "section": "emergency",
        "tags": ["signaling", "rescue", "survival-skills"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Visual signals are generally more effective than audio ones — they pinpoint your exact location and carry much farther in good weather — but both have a real, standardized international pattern worth knowing, since a rescuer trained to recognize that pattern will respond to it specifically.**

## Audio Signals — Real Limits and the Real Pattern

**Sound-based signaling has 2 genuine drawbacks:** limited range unless amplified somehow, and real difficulty for a rescuer to pinpoint your exact location from sound alone (echoes and wind distort direction). **The real international distress pattern: 6 blasts within one minute, repeated** — a rescuer who hears this should answer with **3 blasts within one minute** in return. A whistle is the simplest real tool for this.

## Visual Signals — the Real International Pattern

**The real international visual distress symbol is a series of 3 evenly spaced signals** (fires, panels, or any consistent marker) — three of anything, evenly spaced, is itself a globally recognized distress indicator independent of what the three objects actually are.

## A Flashlight as a Real Signaling Tool

**A real, simple Morse code distress call: 3 dots, 3 dashes, 3 dots (SOS)** — repeated continuously. A flashlight can send this at night across real distance, and doesn't require any specialized equipment beyond the light itself.

## Detailed Version

**The real reason the "3 of something, evenly spaced" pattern specifically matters: it's internationally recognized as meaning distress, independent of language, equipment, or context** — a rescuer trained anywhere in the world who sees 3 evenly spaced fires, panels, or markers should recognize it as a deliberate distress signal rather than a coincidence or ordinary human activity, which is exactly the point of using a standardized pattern instead of an improvised one.
""",
    },
    {
        "title": "Building a Smoke Generator & Ground Signals",
        "section": "emergency",
        "tags": ["signaling", "smoke-signal", "rescue"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**A smoke generator is a genuinely excellent improvised signal — it works for both day (visible smoke) and night (visible flame) with the same structure, and is worth building early, before you actually need it, then protecting until the moment you do.**

## Real Construction Steps

1. **Build it somewhere actually visible from the air** — a natural clearing or along a streambank. **A signal fire built under dense forest canopy will not be seen from above, no matter how well it's built.**
2. Lay two logs (6-10 inches diameter, ~5 feet long) parallel to each other, about 2 feet apart.
3. Lay smaller sticks (~2 inches diameter, ~2 feet long) across the two base logs — this forms the platform the fire actually sits on.
4. Fill the platform frame with completely dry kindling.
5. Place your tinder underneath the platform.
6. **Cover the whole structure with pine boughs** — this protects the fire and tinder from weather until you're ready to use it.
7. **To light it:** remove the pine bough cover and ignite the tinder (a torch helps speed this up, especially if lighting multiple signal fires at once).
8. **For daytime smoke:** once lit, pile fresh pine boughs back onto the burning fire — this is what actually produces visible smoke.
9. **On loose, deep snow:** build a bough platform underneath the two base logs first, or the whole structure will simply sink into the snow.

## Ground Symbols — Letters, Shapes & Shadows

**Arrange branches, twigs, or any contrasting material into letters/symbols on the ground** — real international ground-to-air symbols exist and are recognized by trained search personnel; using one of these standard symbols rather than an improvised message increases the odds it's correctly understood.

**Make the symbols as large as possible** — size is what actually makes them visible from altitude; a technically correct but small symbol may simply not be seen.

**Contrast matters more than shape:** bring material from elsewhere if needed (clothing, a space blanket, brightly colored panels) rather than using material that blends into the surrounding terrain. **On snow, pile pine boughs for contrast, or use sea dye (if you have a life vest) for real high-visibility color.**

**Shadow signals, if nothing else is available:** build mounds in the shape of a standard distress pattern and let the sun cast a shadow from them. **Orientation to the sun matters for this to actually work** — near the equator, a north-south line casts a usable shadow most of the day (except near noon); farther from the equator, an east-west orientation (or something in between) works better.

## Detailed Version

**The real principle tying ground signals and the smoke generator together: visibility from the air is the only thing that matters, and everything about both techniques is optimized for exactly that** — building in a clearing, maximizing size, maximizing contrast with the surroundings, and even orienting shadow-mounds to the sun's actual path. A technically well-built signal that's invisible from altitude (hidden under trees, blending into the terrain, too small) accomplishes nothing.
""",
    },
    {
        "title": "Signal Mirrors & Aircraft Acknowledgment Signals",
        "section": "emergency",
        "tags": ["signaling", "signal-mirror", "rescue"],
        "risk_level": "low",
        "body_markdown": """## Signal Mirror — the Real Best Tool for a Survivor

**A mirror (or any shiny object) can be reused indefinitely and is widely considered the single best signaling device a survivor can carry** — but it's only as effective as the person using it, which means **practicing the technique before you actually need it matters.**

**Real, documented fact: pilots have reported seeing mirror flashes from up to 160 kilometers (roughly 100 miles) away under ideal conditions** — a genuinely enormous range for something with no batteries or moving parts.

**Real technique notes:**
- Any shiny metallic object works as a substitute if you don't have a dedicated signal mirror.
- **Haze, ground fog, or a mirage can make a flash hard for a pilot to spot** — if conditions allow, move to the highest point available before flashing.
- **If you can't actually see the aircraft, flash toward the direction of the engine noise** rather than waiting until you have a visual.

## Aircraft Acknowledgment Signals — How to Tell If You've Been Seen

**Real, standardized signals an aircraft uses to tell you whether your ground signal was seen and understood:**

- **Seen AND understood:** the aircraft rocks side to side (day or bright moonlight), or flashes green with a signal lamp (full darkness).
- **Seen but NOT understood:** the aircraft flies a complete circle to the left (day or bright moonlight), or flashes red with a signal lamp (full darkness).

**Knowing these in advance matters practically: if you get the "seen but not understood" signal, that's real, actionable information — it means you should try a different, clearer signal rather than assuming help is already on the way.**

## Detailed Version

**The real, easy-to-miss value of the acknowledgment signals: without knowing them, a person has no way to distinguish "I was seen and help is coming" from "that aircraft is just passing by and never noticed me" — which can lead to either false relief or, worse, giving up on signaling just as a rescuer was actually trying to confirm understanding.** Recognizing the rock-vs-circle distinction turns an ambiguous moment into real, usable information.
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
