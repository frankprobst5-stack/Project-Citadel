#!/usr/bin/env python3
"""Seeds 2 more real childbirth pages from Where There Is No Doctor's
Chapter 19: Care of the Newborn at Birth, and Delivery of the Placenta
-- mined from the real text layer already extracted in this session.
Complements the 3 childbirth pages seeded in an earlier batch (Labor &
Normal Childbirth, Danger Signs in Pregnancy, Postpartum Hemorrhage).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_newborn_placenta.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Care of the Newborn at Birth",
        "tags": ["childbirth", "newborn"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version — Immediately after birth

1. **Head down** so mucus drains from the mouth/throat — keep this position until the baby starts breathing on their own.
2. **Keep the baby below the mother's level until the cord is tied** — this lets more blood reach the baby, making them stronger.
3. **Dry the baby.** If breathing doesn't start right away, rub the back with a towel/cloth.
4. If still not breathing: clear mucus from the nose/mouth with a clean cloth around your finger.
5. **If no breathing within 1 minute of birth — start rescue breathing immediately.**
6. Wrap the baby in a clean, warm cloth right away — getting cold is a real danger, especially for a premature baby.

## Cutting the Cord

**Wait** — right after birth the cord is fat, blue, and pulsing. **Don't cut yet.** Only once it becomes thin, white, and stops pulsing: tie it in 2 places with clean, recently-ironed/heated cloth strips or string, then cut between the ties.

**Real safety rules, not optional steps:**
- Use a clean, unused razor blade (or freshly boiled scissors if no new blade is available).
- Wash your hands thoroughly first, or wear clean gloves.
- **Cut close to the baby's body — leave only about 2cm attached.** This specific detail is a real, documented tetanus-prevention measure (see Tetanus) — a cord cut long and left loosely covered is a real, confirmed cause of fatal newborn tetanus.

## Caring for the Cord Stump

Keep it clean and dry; wash your hands before touching it. If it gets dirty or has dried blood, clean gently with alcohol or gentian violet — **never put dirt, dung, or anything else on it** (a real, serious tetanus risk). Keep diapers folded below the stump.

**The stump normally falls off 5-7 days after birth** — a few drops of blood or clear mucus at that point is normal. **Significant bleeding or any pus is not normal — get medical help.** Similarly, if the cord area turns red, drains pus, or smells bad, that needs real medical attention too.

**Put the baby to the breast immediately after birth** — this isn't just about feeding; nursing helps bring the placenta out sooner and helps control bleeding afterward.

## Detailed Version

Don't bathe the newborn until after the cord stump has fallen off — until then, just gently wipe away blood/fluid with a warm damp cloth. Once the stump is gone, daily warm water + mild soap is fine.
""",
    },
    {
        "title": "Delivery of the Placenta",
        "tags": ["childbirth", "placenta"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

The placenta normally delivers 5 minutes to an hour after the baby — sometimes it takes longer.

**Once delivered, examine it.** If it looks torn or incomplete, **get medical help** — a retained piece of placenta inside the womb can cause ongoing bleeding or infection. Use gloves or a plastic bag to handle it, and wash your hands well afterward.

**If the placenta is delayed and the mother isn't losing much blood:** do nothing active — **don't pull on the cord**, which can cause dangerous bleeding. Having her squat and push gently can sometimes help it come on its own.

**If the placenta is delayed AND there's heavy bleeding:** feel the womb through the belly. If it's soft, massage it carefully until it firms up — this encourages it to contract and push the placenta out. If it still won't come out and bleeding continues, carefully support the lower womb while pushing down gently on the top of it (see Postpartum Hemorrhage for the full emergency escalation sequence), and get real medical help moving immediately.

## Detailed Version

**The real reason "don't pull the cord" is a hard rule, not a suggestion:** pulling can detach the placenta incompletely or invert the uterus — both genuinely dangerous complications that are worse than simply waiting, as long as the mother isn't actively losing significant blood. Patience is the correct default; active intervention is reserved specifically for when bleeding makes waiting itself the bigger risk.
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
                "section": "emergency",
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
