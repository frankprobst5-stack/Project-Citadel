#!/usr/bin/env python3
"""Seeds 2 more real pages covering 6 childhood infectious diseases
from Where There Is No Doctor's Chapter 21: Chickenpox, Measles,
German Measles, Mumps, Whooping Cough, and Diphtheria -- all mined
from the real text layer already extracted in this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_childhood_infectious_diseases.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Chickenpox, Measles & German Measles",
        "section": "reference",
        "tags": ["childhood-illness", "chickenpox", "measles"],
        "risk_level": "moderate",
        "body_markdown": """## Chickenpox

**Signs:** small, itchy red spots → pimples/blisters → scabs, often all three stages visible at once. Starts on the body, spreads to face/arms/legs. Usually mild fever.

**Treatment:** usually resolves in about a week on its own. Daily bath with soap and warm water; cool oatmeal-water compresses calm itching; keep fingernails short to limit scratching damage. If scabs become infected (real, visible infection — not just irritation), clean them, use warm wet compresses, and antibiotic ointment.

## Measles

**A genuinely severe illness, especially dangerous in malnourished children or those with TB.** Starts like a cold (fever, runny nose, red sore eyes, cough) about 10 days after exposure. Tiny white spots appear inside the mouth 2-3 days in, then the rash follows — starting behind the ears/neck, spreading to face, body, then limbs. The child usually starts improving once the rash appears; it lasts about 5 days.

**Scattered black spots in the rash (bleeding under the skin) means a severe attack — get medical help.**

**Treatment:** bed rest, plenty of fluids, nutritious food (liquids/soup if they can't manage solids). Vitamin A if available (helps prevent eye damage from measles specifically). Acetaminophen/ibuprofen for fever. Antibiotics if an earache develops. **Get medical help if signs of pneumonia, meningitis, or severe ear/stomach pain appear.**

**Prevention:** keep an infected child away from other children (including siblings) during the illness; unvaccinated children exposed in the household should avoid school/public places for 10 days. **Good nutrition and vaccination are the two real levers that prevent measles from becoming fatal.**

## German Measles (Rubella)

Milder than regular measles — mild rash, low fever, lasting 3-4 days, often with tender swollen lymph nodes at the back of the head/neck.

**The real reason this one matters beyond the illness itself: a woman who catches German measles in the first 3 months of pregnancy risks having a baby with a real birth disability.** Anyone who is pregnant and unsure whether they've already had German measles should stay away from children who currently have it. A vaccine exists (often as part of MMR) but isn't always available everywhere.
""",
    },
    {
        "title": "Mumps, Whooping Cough & Diphtheria",
        "section": "reference",
        "tags": ["childhood-illness", "mumps", "whooping-cough", "diphtheria"],
        "risk_level": "high",
        "body_markdown": """## Mumps

Fever and pain opening the mouth/eating, followed within 2 days by soft swelling below the ears at the jaw angle — often one side first, then the other.

**Treatment:** resolves on its own in about 10 days. Pain/fever relief (acetaminophen/ibuprofen), soft nourishing food, keep the mouth clean.

**Real complication to watch for in anyone over 11:** after the first week, belly pain or painful testicular swelling (in males) can occur — rest and cold compresses help. **Get medical help if signs of meningitis or hearing problems appear.**

## Whooping Cough

Starts like an ordinary cold (fever, runny nose, cough), then — about 2 weeks later — the real "whoop" begins: rapid coughing without a breath in between, until a plug of mucus clears and air rushes back in with a characteristic loud whoop sound. Lips/nails may turn blue during a coughing fit from lack of air. Often lasts 3+ months.

**Especially dangerous in babies under 1 year — and babies often don't show the classic whoop**, making it harder to recognize. If a baby has coughing fits and puffy/swollen eyes during a local whooping cough outbreak, treat it as whooping cough without waiting for confirmation.

**Treatment:** antibiotics only help in the early stage, *before* the whoop starts — erythromycin is the real priority for babies under 6 months at the very first sign. **If a baby stops breathing after a coughing fit:** turn her over, clear mucus from the mouth with your finger, then slap firmly between the shoulder blades with the flat of your hand. Keep feeding adequately between episodes to prevent malnutrition from the illness itself.

**Vaccination at 2, 4, 6, and 18 months is the real preventive lever here** — this illness is genuinely dangerous enough in infants that prevention matters more than treatment.

## Diphtheria

Starts like a cold with fever, sore throat, and a hoarse voice — but a distinctive yellow-gray membrane can form in the back of the throat (sometimes nose/lips too), with a very bad breath odor and neck swelling.

**If diphtheria is suspected: isolate the child from others immediately and get real medical help fast — a specific antitoxin exists and genuinely matters for outcome.** This is not a home-treatable illness; recognition and fast referral is the real first-aid value here.
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
