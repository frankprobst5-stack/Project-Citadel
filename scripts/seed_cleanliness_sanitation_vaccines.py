#!/usr/bin/env python3
"""Seeds 3 more real pages from Where There Is No Doctor's Chapter 12
(Prevention): General Cleanliness & Hygiene, Sanitation & Latrines,
and Vaccinations -- all mined from the real text layer already
extracted in this session.

Vaccinations gets one real honest caveat the other pages in this
build-out haven't needed: the book's own schedule (ages/intervals) is
a general international one and real national schedules (the US CDC's
included) vary and are updated periodically -- the page says so
explicitly rather than presenting this book's specific ages as the
current literal schedule to follow.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_cleanliness_sanitation_vaccines.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "General Cleanliness & Hygiene",
        "section": "reference",
        "tags": ["hygiene", "disease-prevention"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Personal:** wash hands with soap on waking, after a bowel movement, before cooking/eating. Bathe daily, especially after sweating or hard work — this genuinely prevents skin infections, not just odor. In hookworm-prone areas, never go barefoot (hookworm larvae enter through bare feet and cause real anemia).

**In the home:** keep pigs/animals out of the house and away from where children play; don't let dogs lick children or get on beds; clean up any animal or child waste near the house immediately; sun bedding often; delouse the household regularly; never spit on the floor; cover coughs/sneezes; sweep/clean regularly and seal cracks where pests hide.

**Food and water:**
- Protect food from flies — cover it, don't leave scraps or dirty dishes out.
- Wash fallen fruit before eating; never let a child eat food picked up off the ground without washing it first.
- Cook meat and fish thoroughly — undercooked pork specifically carries real, dangerous parasites.
- **A real low-cost water purification method: put water in a clean, clear bottle or bag and leave it in direct sunlight at least 6 hours** (2+ days if the water is cloudy) — this is solar water disinfection, a genuine, documented technique, not folk wisdom. Complements but doesn't replace boiling/chemical treatment (see Making Water Safe in an Emergency) when a stronger method is needed.

## Detailed Version

**A real, practical tradeoff worth knowing:** boiling water takes real fuel and time, and for a family with limited resources, prioritizing *having enough water* over *having perfectly pure water* can sometimes be the safer overall choice — pushing a poor family to burn scarce firewood (or cut down more trees) to boil every drop can do more harm than the water's own real but smaller risk. This isn't an argument against purification — it's a reminder that purification is one tool among several, and having enough water matters too.
""",
    },
    {
        "title": "Sanitation & Latrines",
        "section": "reference",
        "tags": ["sanitation", "latrine"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Keep any shared water source (well, water hole, upstream river/creek) fenced off from animals and free of waste/garbage.** Never defecate or dump trash near a drinking water source, and take special care upstream of anywhere drinking water is drawn.

**Burn burnable garbage; bury the rest** in a pit well away from houses and water sources.

**Build a real latrine** so animals can't reach human waste — a deep hole with a simple structure over it works. **Deeper is better: less smell, fewer flies.** Throwing a little lime, dirt, or ash in after each use cuts smell and keeps flies down. **Site it at least 20 meters from any home or water source.**

**A closed latrine (with a lid over the hole) is a real upgrade** — keeps flies out and smell contained, versus an open pit that lets both through.

## Detailed Version — building a simple cement slab latrine

1. Dig a shallow pit, about 1m square and 7cm deep, level and smooth.
2. Cut a wire mesh grid 1m square (wires ¼-½cm thick, about 10cm apart), with a ~25cm hole in the center.
3. Set the grid in the pit, raised about 3cm off the ground (bend the wire ends down, or use small stones at the corners).
4. Place an old bucket in the grid's hole.
5. Pour a cement mix (1 part cement : 2 parts sand : 3 parts gravel) over the grid to about 5cm thick.
6. Remove the bucket once the cement starts hardening (roughly 3 hours), then keep the slab damp (wet cloths, sand, hay, or plastic) for 3 days before removing it from the pit.

This gives you a durable concrete slab with a proper hole — the core structural piece for a real closed latrine that won't rot or crack like a wood platform over time.
""",
    },
    {
        "title": "Vaccinations — Why Timing Matters",
        "section": "reference",
        "tags": ["vaccines", "immunization"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**Important caveat before anything else: this page describes a general international vaccine schedule. Real national schedules (the US CDC's included) differ in exact ages/intervals and are updated periodically — check your own country's current schedule rather than treating the ages below as current literal guidance.** What doesn't change: vaccinating on time, before a child is exposed to a dangerous disease, is dramatically safer than treating that disease after the fact.

**Core vaccines this book covers, and what each protects against:**
- **DPT/DTaP** — diphtheria, whooping cough (pertussis), tetanus. Several doses in infancy plus a booster.
- **Polio** — given as drops (or injections) in multiple doses.
- **BCG** — tuberculosis, one injection, especially important if a household member has TB.
- **Measles / MMR** — measles, mumps, rubella. Generally not given to a child with HIV.
- **Hepatitis B** — a 3-dose series, often starting at birth.
- **Hib** — protects against a bacteria that causes meningitis and pneumonia in young children.
- **Tetanus booster (Td/TT)** — repeated roughly every 10 years through adulthood; vaccinating during each pregnancy also protects the newborn from tetanus.
- **Rotavirus** — an oral vaccine protecting against a leading cause of severe childhood diarrhea.

## Detailed Version

**A real, practical vaccine storage note:** several vaccines (measles, polio, TB) need to stay frozen or very cold; others (Hepatitis B, tetanus, DPT) need to stay cold but must NEVER freeze — freezing ruins them just as surely as letting them get too warm does. A prepared-but-unused dose should be discarded, not saved for later. For anyone maintaining their own vaccine supply (a real homestead/off-grid consideration), a reliable cold chain matters as much as the vaccine itself — a vaccine that's been mishandled in storage may simply not work, with no obvious sign that it failed.
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
