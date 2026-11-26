#!/usr/bin/env python3
"""Seeds 1 real page from FM 21-10 (Field Hygiene and Sanitation),
Chapter 2, Section VIII (Toxic Industrial Chemicals/Materials) --
mined from the real text layer already extracted in this session
(/tmp/fieldhygiene.txt, pages 2-38 through 2-43). Genuinely new
content for this wiki: real recognition and protection guidance for
chemical/industrial hazards a household could realistically
encounter during a disaster (vehicle exhaust, cleaning solvents,
biological waste, nearby industrial/radiological sources).

The source's brief "Noise" section (hearing protection) is thin,
mostly covering military-specific equipment (crew helmets), and is
not mined as a standalone page.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_fm2110_toxic_hazards.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
FM2110_PDF_URL = "/files/pdfs/Military Manuals/FM-21-10-Field-Hygiene-and-Sanitation.pdf"

PAGES = [
    {
        "title": "Recognizing & Protecting Against Toxic Industrial Hazards",
        "section": "reference",
        "tags": ["chemical-hazards", "carbon-monoxide", "safety"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Real toxic exposure risk doesn't require a dedicated hazmat scenario — ordinary vehicle exhaust, cleaning solvents, and nearby industrial activity are all genuine, common sources, and each has its own real recognition signs and protective measures.**

## Real Occupational & Industrial Sources

- **Engine exhaust and fuel-burning space heaters.**
- **Weapons-firing/combustion gases** (a real hazard in any enclosed space where something is burning or firing, not just military-specific).
- **Cleaning solvents, greases, and oils** from equipment/vehicle maintenance.
- **Detergents** used for equipment cleaning.
- **Compressed gases, industrial solvents, hazardous chemical waste.**
- **Materials from water/sewage treatment facilities.**
- **Medical waste, materials from medical research facilities, radioactive isotopes, nuclear power plant substances, depleted uranium** — real biological/radiological hazard categories, relevant if a disaster disrupts normal containment of any of these nearby.

## Real Signs of Exposure, by Hazard

- **⚠️ Carbon monoxide:** colorless, odorless, tasteless. **Causes headache, sleepiness, coma, and death** — with frequently no earlier warning sign at all (see Carbon Monoxide Poisoning in Shelters and Tent Fumes, CO Poisoning & Cold-Weather Constipation for more on this specific hazard).
- **Hydrogen chloride gas:** reacts with body fluids to form hydrochloric acid in the throat/lungs/eyes — causes coughing, tissue acid burns, and flu-like lung illness.
- **Irritant smoke (from combustion/munitions):** severe coughing, wheezing, and real lung damage if inhaled.
- **Bore/combustion gases generally:** cause the same real effects as carbon monoxide and hydrogen chloride.
- **Solvents, greases, oils:** skin rashes, burns, drying, infections — and real internal damage to liver, blood, and brain with repeated exposure; **many are also real carcinogens.**
- **Medical waste:** real disease transmission risk.
- **Radioactive material:** radiation illness.

## ⚠️ Real Protective Measures

**Carbon monoxide:**
- Run engines outdoors, or with doors/windows open if indoors.
- **Keep a sleeping area's windows slightly open for ventilation and air movement.**
- **⚠️ Never sleep in a vehicle with the engine running, and never use engine exhaust as a heat source.**
- **⚠️ Never park a vehicle near an air intake** for a tent, trailer, or any environmental control unit.

**Combustion/bore gases:** use any available vehicle ventilation system; keep exhaust/evacuation systems well maintained; try to maintain real air movement in any enclosed space where something is being fired or burned.

**Solvents, greases, oils:**
- **Never substitute an unknown or "stronger" solvent for the recommended one** — a real, specific danger (e.g., never substitute benzene or raw fuel for a proper safety solvent).
- Wear coveralls and rubber gloves if available.
- Wash or change clothing often, especially once soiled by chemicals or fuel.
- Follow real label instructions and safety precautions exactly.
- Use ventilation wherever fumes are present.

**Biological waste:** disposable rubber gloves, coveralls/rubberized apron, goggles/safety glasses, and an appropriate air-filtered mask when handling it — **dispose of it according to real label instructions**, not by improvisation.

## Real Documentation Reference

**Material Safety Data Sheets (MSDS/SDS) accompany any stored toxic chemical/material and serve as the real, immediate reference for exposure or injury** — if a household stores any hazardous chemical in quantity, keeping its real SDS accessible is a genuine, practical safety step.

## Detailed Version

**The real, most important single fact on this page, worth repeating because it's so often missed: carbon monoxide has absolutely no smell, color, or taste — which is exactly why the real protective measures (ventilation, never running an engine indoors, never parking near an air intake) have to be followed as fixed rules, not as responses to a warning sign that will never actually appear in time.**
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
                "source_url": FM2110_PDF_URL,
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
