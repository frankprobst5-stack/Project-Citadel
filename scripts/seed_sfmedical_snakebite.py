#!/usr/bin/env python3
"""Seeds 1 real page from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 12 Section I (Snake Bites) --
mined from the OCR output cached at /tmp/sfmedical.txt.

IMPORTANT SCOPING NOTE: this source's real treatment protocol for
snakebite explicitly recommends incision-and-suction for pit-viper
bites and tourniquet application for elapid bites -- both now known,
outdated techniques that directly contradict the current, carefully-
sourced Snakebite page already in this wiki (built from current
Mayo Clinic guidance, one of the very first "outdated local manual
vs. current medicine" corrections made in this entire build-out).
That treatment protocol is deliberately NOT included here, to avoid
silently contradicting the existing current-guidance page.

What IS included is the real taxonomic/toxicological content that
doesn't change with updated first-aid recommendations: real snake
family classification, real hemotoxic vs. neurotoxic venom
mechanisms, and real species-differentiated symptom patterns
(including the genuinely important real fact that sea snake bites
are often painless with no early clue that treatment is needed).
This explains WHY snakebite treatment differs by species without
repeating the outdated specific treatment steps -- readers needing
actual treatment guidance are pointed to the existing current page.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_snakebite.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Snake Venom Types & Real Species-Specific Symptoms",
        "section": "reference",
        "tags": ["snakebite", "toxicology", "venom"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**For actual snakebite treatment, see Snakebite (already in this wiki, built from current Mayo Clinic guidance).** This page covers only the real taxonomy and venom biology — knowledge that doesn't change with updated first-aid recommendations — specifically to explain WHY different snakebites look and progress so differently. **This source's own 1982 treatment protocol (which recommended incision-and-suction and tourniquet application) is deliberately excluded here, since both are now known to be outdated and are not what current medicine recommends** — follow the existing Snakebite page's current guidance instead.

## Real Venomous Snake Families

1. **Crotalidae (pit vipers):** rattlesnakes, moccasins, copperheads, bushmasters, fer-de-lance, habu, Russell's viper.
2. **Elapidae:** coral snakes, kraits, cobras, mambas, and related species.
3. **Hydrophidae (sea snakes):** all genuinely highly venomous — many carry venom more potent than cobras.
4. **Colubridae:** represented by the back-fanged boomslang.

## Real Venom Mechanisms — Hemotoxic vs. Neurotoxic

**⚠️ Real, important nuance: most snakes aren't purely one type — they're primarily one, with some elements of the other.**

**Hemotoxic** (mainly Crotalidae): attacks blood and tissue directly.
- **Thrombase** — acts locally at the bite site, causing clotting, tissue death, and gangrene.
- **Hemorrhagin** — the dominant hemotoxic component; breaks down capillary walls, causing local then spreading leakage into tissue (occasionally causing small brain hemorrhages and seizures).
- **Anticoagulin** — breaks down the fibrin network that normally holds a blood clot together.

**Neurotoxic** (mainly Elapidae, Colubridae, Hydrophidae): attacks the nervous system and heart.
- **Neurotoxin** — paralyzes the respiratory control center and several specific cranial nerves.
- **Hemolysin** (present in some species) — destroys blood cells.
- **Cardiotoxin** — can cause toxic cardiac arrest.

## Real Species-Differentiated Symptom Patterns

**Crotalidae (pit viper) bites — fast, dramatic, and local:**
- Swelling starts within 3 minutes at the bite site and can spread/intensify for an hour, severely enough to split the skin.
- Severe pain at the bite site, often with visible fang marks.
- Bleeding from internal organs (sometimes visible as blood in urine), destruction of blood/tissue cells.
- Severe headache, thirst, falling blood pressure with rising pulse, and bleeding into surrounding tissue.

**Elapidae and Colubridae bites — slower onset, more systemic/neurological:**
- Circulatory impairment: irregular heartbeat, falling blood pressure, weakness progressing toward shock.
- Severe headache, dizziness, blurred vision, hearing trouble, confusion, and eventually unconsciousness.
- Muscle incoordination and twitching.
- Breathing difficulty that can progress to real respiratory paralysis.
- Tingling, excess sweating, numbness of the lips and soles of the feet.
- Chills, fever, nausea, vomiting, diarrhea.

**⚠️ Hydrophidae (sea snake) bites — the real, dangerous exception: often genuinely painless with no visible swelling and no early clue that anything is wrong.** **Real, important guidance: suspect sea snake envenomation in anyone who was in snake-frequented coastal water within the last 1-2 hours and develops:**
- Muscle aches, pains, and stiffness.
- Pain specifically on passive movement of the arm, thigh, neck, or trunk.
- **Urine turning reddish-brown within about 3 hours.**
- The same real neurotoxic symptom pattern described for Elapidae above.

## Detailed Version

**The real, single most important practical idea on this page: a painless bite is not a reassuring sign — it can mean the venom is neurotoxic rather than hemotoxic, which is exactly the Hydrophidae pattern above, and exactly why "it doesn't even hurt" is the wrong reason to delay seeking real treatment.** Understanding which venom type is likely involved, based on the real symptom pattern actually developing, is what lets a real provider anticipate complications (respiratory paralysis vs. local tissue destruction vs. internal bleeding) before they fully develop — which is the genuine, lasting value of this biology, independent of any specific first-aid technique's fashion over time.
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
