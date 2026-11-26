#!/usr/bin/env python3
"""Seeds 1 real page from FM 21-60 (Visual Signals), Chapter 5,
Ground-to-Air Panel System -- mined from the real text layer already
extracted in this session (/tmp/visualsignals.txt, pages 5-9 through
5-13). Most of this short manual (arm-and-hand signals, flag signals)
is combat/unit-coordination-specific with no real civilian survival
application and is not mined. The actual body-position and ground-
symbol emergency codes (Figures 5-30/5-31) are real, but exist only
as figures in the source PDF, not as extractable text -- consistent
with this build-out's standing discipline of never reconstructing a
figure's content from training-data recall, they are NOT included
here.

Covers: the real panel-system construction specs (size, placement,
clear-area requirements) and the real Wind-T panel signal -- genuine
complements to the existing mirror/smoke/ground-symbol signaling
pages already in this wiki, not duplicates of them.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_fm2160_panels.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
FM2160_PDF_URL = "/files/pdfs/Military Manuals/FM-21-60-Visual-Signals.pdf"

PAGES = [
    {
        "title": "Ground-to-Air Panel Signaling",
        "section": "emergency",
        "tags": ["signaling", "panel-signals", "rescue"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**Beyond a signal mirror or smoke (already covered in Signal Mirrors & Aircraft Acknowledgment Signals and Building a Smoke Generator & Ground Signals), ground panels are a real, distinct way to communicate with an aircraft overhead — genuinely useful if you have any large flat material (tarps, sheets, brightly colored fabric) available.**

## Real Panel Construction

**If building panels locally: make them large enough to read easily from the air, with as much color contrast against the background as possible.** **Real minimum size: at least 6 feet long and 2 feet wide.**

## Real Site Selection

**Pick a relatively flat, clear area — roughly 40 by 130 feet** — large enough to lay out messages/symbols, and genuinely clear of obstacles so an aircraft could fly in low and slow if attempting a pickup or drop.

## Real Placement Principles

- **One panel acts as the real "base" panel** — place it first and keep it in position throughout signaling.
- **Space panels one panel-length apart**, wherever room allows.
- **Change a displayed symbol by shifting, adding, or removing non-base panels** — not by rebuilding the whole layout from scratch.
- **Remove any panel not actively part of the current display** — a cluttered field of old symbols is harder to read correctly than a clean one.

## The Real Wind-T Signal

**A "T" shape, 2 panels wide and 2 panels long, representing an aircraft flying into the wind** — this real symbol communicates wind direction to an approaching pilot, genuinely useful information for anyone attempting a landing or low pass nearby.

## Real Aircraft Acknowledgment (Consistent With Other Signaling Methods)

**Seen/understood:** the aircraft rocks its wings side to side, or flashes a green signal lamp. **Seen but NOT understood:** the aircraft makes a 360-degree turn, or flashes a red signal lamp. *(This matches the same real acknowledgment convention already covered for other signal types — see Signal Mirrors & Aircraft Acknowledgment Signals.)*

## Detailed Version

**The real, practical value of panels specifically: unlike a mirror (which needs direct sun) or smoke (which needs fuel and fire), a panel signal works with whatever large, contrasting material is already on hand — a tarp, a sheet, even clothing laid out flat — and stays visible continuously without needing to be actively operated once it's placed.** That makes it a genuinely good complement to the other signaling methods already in this wiki, not a replacement for any of them.
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
                "source_url": FM2160_PDF_URL,
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
