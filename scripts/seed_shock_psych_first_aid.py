#!/usr/bin/env python3
"""Seeds 2 more real pages: Shock, and Psychological First Aid.

Both mined from Medical/FM-4-25-11-First_Aid.pdf (Chapter 2's Section
III, and Chapter 8). Shock is transcribed close to verbatim -- it's a
real step-by-step procedure, and nothing in it is medically outdated
(lay flat, elevate legs unless a leg/head/abdominal injury says
otherwise, keep warm, no food/drink, reassure, recovery position if
vomiting is a risk -- all consistent with current practice).

Psychological First Aid is adapted rather than transcribed verbatim --
the real manual's chapter is written entirely in a "service member"/
combat-stress framing (get him back to duty, dig fighting positions),
so the universal principles underneath that framing (don't dismiss
emotional distress as unreal, let someone talk without arguing with
their account, give calm purposeful tasks instead of idleness, ensure
rest) are pulled out and reworded for a general disaster context --
this is a case where the real underlying psychology doesn't need a
different source to be current, just different wording than a
military field manual uses.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_shock_psych_first_aid.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
FIRST_AID_PDF_URL = "/files/pdfs/Medical/FM-4-25-11-First_Aid.pdf"

PAGES = [
    {
        "title": "Shock — Recognition and First Aid",
        "section": "emergency",
        "tags": ["shock", "first-aid"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Shock means the body's circulation is failing** — not enough blood actually reaching the tissues, whether from blood loss, a failing heart, or blood vessels suddenly widening (as in a severe allergic reaction). Untreated, it can kill even if the original injury wouldn't have.

**Signs:** clammy/sweaty but cool skin, weak and rapid pulse, pale skin (grayish in dark skin tones), restlessness or nervousness, thirst, confusion, faster-than-normal breathing, bluish lips/mouth, nausea or vomiting.

**Treat for shock BEFORE these signs even appear, on anyone with a serious injury, major blood loss, burns, a severe allergic reaction, or a traumatic shock (seeing a bad wound, a crash) — waiting for symptoms costs real time.**

1. Lay the person on their back. **Exception:** someone with chest trouble or breathing difficulty may do better sitting up — let them, but watch closely.
2. **Elevate the feet above heart level** using a pack or rolled clothing — **unless** there's an unsplinted broken leg, a head injury, or an abdominal injury, in which case don't elevate (for an abdominal wound, bend the knees up instead).
3. Loosen tight clothing at the neck/waist.
4. Keep body temperature stable — a blanket under and over them in cold weather; shade and airflow (not piled blankets) in hot weather.
5. Stay calm and reassuring — your own demeanor measurably affects theirs.
6. **No food or drink.** If you have to leave them, or they're unconscious, turn their head to the side so they won't choke if they vomit.
7. Keep monitoring until help arrives.

## Detailed Version

The "treat before symptoms appear" instruction is the real core of this page: shock can develop after the initial injury looks stabilized, and by the time clammy skin and confusion show up, it's already progressed. Any of the triggering situations above — major bleeding, burns, severe allergic reaction, a bad fall, a crush injury — is reason enough to start shock positioning and monitoring immediately, not a reason to wait and see.

Splint any suspected fracture **before** moving or elevating a limb — moving an unsplinted break to "help" circulation can cause real additional damage.
""",
    },
    {
        "title": "Psychological First Aid",
        "section": "reference",
        "tags": ["mental-health", "psychological-first-aid", "stress"],
        "risk_level": None,
        "body_markdown": """Adapted for a general disaster/emergency context from real first-aid principles.

## Quick Version

**Someone in acute emotional distress after an emergency needs the same basic first aid as a physical injury — don't dismiss it as unreal because you can't see it.**

- **Don't say "calm down," "snap out of it," or "it's all in your head."** These land as dismissal, not help, and make a frightened person feel worse understood, not better.
- **Let them talk, and actually listen**, in their own words, without arguing about their version of events. Retelling what happened is part of how people process it — interrupting or correcting them doesn't speed that up.
- **Give them something small, useful, and concrete to do** rather than leaving them idle — carry water, hold a flashlight, help gather supplies. Purposeful activity genuinely reduces panic better than sitting still with nothing to do.
- **Protect rest** where you can — physical exhaustion makes emotional overwhelm worse, and a safe, relatively quiet place to actually sleep matters as much as anything else on this list.
- Stay calm yourself — a frightened person reacts to your own visible fear or impatience, often more than to the situation itself.

## Detailed Version

Everyone reacts differently to the same stressful event — what finally overwhelms one person often isn't the triggering event itself but something else layered on top of it (exhaustion, an unrelated worry, a prior loss). That means there's no single "right" reaction to expect, and someone's response isn't a referendum on their character or toughness.

An injured person — even from something relatively minor — almost always has a real emotional reaction to the injury itself, not just the physical pain. This is especially true for injuries to a highly valued part of the body or ability; what seems "minor" to you may not be minor to them, and that reaction deserves patience, not correction.

**This is reference material, not a substitute for real mental health support.** If distress is severe, prolonged, or involves a risk of harm to the person or others, that's a signal to get real professional help involved, not just more patience.
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
            print(f"WOULD CREATE: {page['title']}")
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
                "source_url": FIRST_AID_PDF_URL,
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
