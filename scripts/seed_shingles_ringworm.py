#!/usr/bin/env python3
"""Seeds 2 more real pages from Where There Is No Doctor's Chapter 15
(Skin Problems): Shingles, and Ringworm & Fungal Skin Infections --
mined from the real text layer already extracted in this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_shingles_ringworm.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Shingles (Herpes Zoster)",
        "section": "reference",
        "tags": ["shingles", "skin"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**Signs:** a line or patch of painful blisters that suddenly appears on *one side* of the body — most common on the back, chest, neck, or face. Blisters typically last 2-3 weeks then clear on their own; pain can sometimes linger or return after the blisters are gone.

Shingles comes from the same virus that causes chickenpox, and generally only occurs in someone who's already had chickenpox in the past — the virus reactivates later in life rather than being a new infection. Not dangerous on its own, but genuinely painful, and **can sometimes be an early sign of a different, more serious underlying problem (a weakened immune system — cancer, HIV)**, especially if it occurs in someone younger or otherwise unexpected.

**Treatment:**
- Light bandaging over the rash so clothing doesn't rub against it.
- Aspirin for pain.
- **Acyclovir can help limit how much the blisters spread** — real antiviral treatment, not just symptom relief. Antibiotics do nothing against this (it's viral, not bacterial).

## Detailed Version

The one-sided pattern is the real distinguishing feature — shingles follows the path of a single nerve, which is why it stays confined to one side of the body rather than appearing symmetrically. If a case of shingles seems unusual for the person's age or health status, that's worth treating as a prompt to look for what else might be going on, not just treating the rash in isolation.
""",
    },
    {
        "title": "Ringworm & Fungal Skin Infections",
        "section": "reference",
        "tags": ["ringworm", "fungal-infection", "skin"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

Fungal infections show up most often on the scalp (tinea), hairless skin (ringworm, classically ring-shaped and itchy), between toes/fingers (athlete's foot), and the groin (jock itch). Infected nails become rough and thickened.

**Treatment:**
- Daily washing with soap and water may be all that's needed for mild cases.
- **Keep the area dry and exposed to air/sunlight** — fungus thrives in damp, covered skin, so this matters as much as any medication. Change sweaty socks/underwear often.
- Antifungal creams/powders (tolnaftate, salicylic or undecylenic acid) work well for infections between fingers/toes/groin.
- **Severe or widespread scalp fungus, or anything not responding to topical treatment**, may need oral griseofulvin — taken for weeks to months to fully clear it. **Pregnant women should not take griseofulvin.**

**It's contagious** — don't let an infected child share a bed, comb, towel, or clothing with others until treated; treat promptly to limit spread through the household.

## Detailed Version

**A separate, usually harmless look-alike worth distinguishing:** tinea versicolor causes small dark or light patches (not the classic itchy ring) on the neck/chest/back, often not itchy at all, and is of little medical importance beyond appearance — treated the same general way (antifungal cream, sulfur-lard paste, or sodium thiosulfate solution) but it's a cosmetic concern more than a health one, unlike ringworm proper.

Many childhood scalp fungal infections clear up naturally around puberty — a real, if slow, self-resolving pattern worth knowing so a lingering mild case in a younger child isn't automatically treated as a treatment failure.
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
