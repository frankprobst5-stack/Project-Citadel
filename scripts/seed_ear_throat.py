#!/usr/bin/env python3
"""Seeds 2 more real pages from Where There Is No Doctor's Chapter 21
(Health and Sicknesses of Children): Earache & Ear Infections, and
Sore Throat/Strep Throat & Rheumatic Fever -- mined from the real text
layer already extracted in this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_ear_throat.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"

PAGES = [
    {
        "title": "Earache & Ear Infections",
        "section": "reference",
        "tags": ["ear-infection", "children"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

Common in small children, often starting a few days into a cold/stuffy nose. Fever, crying or rubbing the side of the head, sometimes visible pus in the ear. **In small children, an ear infection can cause vomiting or diarrhea with no other obvious sign — check the ears whenever a young child has unexplained fever and diarrhea together.**

**Treatment:**
- Real antibiotic treatment early matters (penicillin, cotrimoxazole, or ampicillin — ampicillin often works better under age 3). Pain relief with acetaminophen.
- Gently clean visible pus with cotton — **never insert cotton plugs, sticks, leaves, or anything else into the ear canal.**
- **No swimming/diving for at least 2 weeks** after a draining ear infection has cleared.

**Prevention:**
- Teach children to wipe, not blow, their nose during a cold.
- **Never bottle-feed a baby lying flat on their back** — milk can travel up into the nose and contribute to ear infections.
- Clear a blocked nose with saline drops and gentle suction rather than letting congestion sit.

**Ear canal infection (different from a middle-ear infection):** gently pull the outer ear — if that causes pain, the canal itself is infected. Treat with diluted vinegar-water drops (1:1 with boiled water) several times a day; add an antibiotic if fever or pus develops.

## Detailed Version

The diarrhea-plus-fever-plus-unexamined-ears pattern is worth remembering specifically because it's counterintuitive — a caregiver focused on GI symptoms can easily miss an ear infection that's actually driving the fever, especially in a child too young to clearly say their ear hurts.
""",
    },
    {
        "title": "Sore Throat, Strep Throat & Rheumatic Fever",
        "section": "reference",
        "tags": ["sore-throat", "strep-throat", "rheumatic-fever"],
        "risk_level": "high",
        "body_markdown": """## Ordinary Sore Throat

Usually comes with a cold — red throat, pain swallowing, sometimes swollen tonsils, fever. **Antibiotics don't help an ordinary cold-related sore throat and shouldn't be used for it.** Treat with warm salt water gargles, acetaminophen, and keep fluids up even if swallowing hurts.

## Strep Throat — the real exception that needs antibiotics

**Signs that distinguish it from an ordinary sore throat:** comes on suddenly with severe throat pain and high fever, often with NO cold symptoms (no runny nose, no cough) — the back of the throat/tonsils are very red, and the lymph nodes under the jaw/neck are swollen and tender.

**This specific kind of sore throat needs a full 10-day course of penicillin** — not because strep throat itself is dangerous, but because **treating it early and completely is what prevents rheumatic fever**, a real and serious complication. Keep an infected child away from others during treatment to limit spread.

## Rheumatic Fever — the real reason strep throat gets taken seriously

Develops 1-3 weeks after an (often untreated or incompletely treated) strep throat, mostly in children and young adults.

**Signs (usually only some present at once):** fever, painful/swollen/hot joints (wrists and ankles first, then knees and elbows), curved red lines or lumps under the skin, uncontrolled movements, and in serious cases weakness, shortness of breath, or chest pain.

**This can cause lasting heart damage — see a health worker if suspected.** Treatment is penicillin plus high-dose aspirin (under real medical guidance on amount — ringing in the ears is a sign to reduce the dose).

**Prevention is the real point:** treat every real strep throat fully with a 10-day penicillin course. Anyone who's already had rheumatic fever once needs penicillin at the very first sign of any future sore throat — and if there's already heart damage, ongoing regular penicillin (sometimes monthly injections, sometimes for life) under real medical supervision.

## Detailed Version

**The throat-to-heart connection is the single most important thing to carry from this page:** a sore throat is usually trivial, but the specific "strep throat" pattern (sudden onset, high fever, no cold symptoms, swollen tender neck nodes) is worth treating seriously precisely because the real danger isn't the throat itself — it's a preventable complication weeks later that can cause permanent heart damage. That's why this one specific kind of throat infection gets antibiotics when ordinary cold-related sore throats don't.
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
                "source_url": NO_DOCTOR_PDF_URL,
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
