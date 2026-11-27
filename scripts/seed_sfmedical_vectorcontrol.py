#!/usr/bin/env python3
"""Seeds 1 real page from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 20 Section 20-10 (Arthropod and
Rodent Control) -- mined from the OCR output cached at
/tmp/sfmedical.txt.

SCOPING NOTE: checked the existing wiki first. Field latrines/waste
disposal are already thoroughly covered (from the Navy Manual of
Preventive Medicine). This same chapter's washing-device section
(20-8) is skipped -- its only non-trivial content (solar-heated and
oil-water-flash-burner shower rigs) depends entirely on diagrams
("see diagram on next page") that didn't survive OCR as anything
reconstructable, consistent with this project's standing rule
against publishing figure-dependent technical builds from text
alone. Section 20-11 (a 1982 military immunization schedule
including smallpox and plague vaccination) is also skipped --
smallpox vaccination is no longer administered to the general
population and plague/cholera vaccines aren't standard civilian
practice; professionally-administered vaccination schedules are
outside this wiki's real scope.

What IS seeded: the real arthropod life-cycle/breeding-habitat
reference chart, which directly explains WHERE and HOW the vectors
behind this wiki's existing rickettsial/relapsing-fever/typhus
content (ticks, lice, fleas, mosquitoes) actually breed -- genuinely
new, actionable prevention content this wiki didn't have before,
plus the basic real rodent-control principles from the same section.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_vectorcontrol.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
SFMEDICAL_PDF_URL = "/files/pdfs/Medical/ST-31-91B-US-Army-Special-Forces-Medical-Handbook.pdf"

PAGES = [
    {
        "title": "Rodent & Arthropod Control — Breaking the Disease-Vector Life Cycle",
        "section": "reference",
        "tags": ["vector-control", "pest-control", "disease-prevention"],
        "risk_level": "moderate",
        "body_markdown": """## ⚠️ Read This First

**This page explains WHERE and HOW the disease vectors behind Tick, Lice & Mite-Borne Fevers — Recognizing the Rickettsial Diseases and Tick & Louse-Borne Relapsing Fever actually breed** — real, practical prevention works by denying them exactly these conditions, rather than only treating bites after they happen.

## Real Rodent Control

**The real key to rodent control is simply good area cleanup — denying rodents a place to live and breed.** Keep ditches and depressions free of standing water. **Never leave garbage unburied** — it attracts both flies and rats. **⚠️ Real, specific technique: if you must trap rats, live-trap and then burn them** — this real detail matters because it also kills the fleas and mites living in their fur, rather than just relocating the disease risk.

## Real Arthropod Breeding Conditions — By Vector

**⚠️ Real, practical idea: effective vector control means understanding each pest's specific breeding habitat, then denying exactly that** — rather than generic "pest control" effort spread evenly across everything.

| Vector | Where It Actually Breeds | Approx. Life Cycle |
|---|---|---|
| Flies (housefly) | Animal or human waste, garbage, grass, decomposing animal matter, mud contaminated with organic material | ~30 days egg to adult |
| Mosquitoes (yellow fever mosquito) | **Standing water** — ponds, tin cans, old tires, tree holes (a genuinely wide variety of small water-holding containers/depressions) | ~14 days egg to adult |
| Fleas (oriental rat flea) | Nests or beds of animals | ~365 days egg to adult |
| Lice (human body louse) | **Head hair and clothing of humans — real, important fact: lice cannot survive on a genuinely clean human** | ~30 days egg to adult |
| Cockroaches (German cockroach) | Cracks and crevices with warmth, moisture, and food — around water, garbage, and food facilities | ~200 days to adult |
| Ticks and mites | Tall grass, underbrush, animal watering places, shady animal rest areas | 6 weeks to 2 years |

## Detailed Version

**The real, most actionable idea on this page: mosquitoes need standing water specifically, lice need an unwashed human specifically, and fleas need an animal's nest/bedding specifically** — each vector's real breeding requirement is a specific, controllable thing. **Eliminating standing water around a camp or home, maintaining basic personal cleanliness, and keeping animal bedding areas clean are each targeted at exactly one of these vectors' real breeding needs** — understanding which action targets which pest is what turns "pest control" from a vague chore into a specific, effective real strategy.
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
                "source_url": SFMEDICAL_PDF_URL,
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
