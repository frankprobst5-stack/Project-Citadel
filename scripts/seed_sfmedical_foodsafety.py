#!/usr/bin/env python3
"""Seeds 2 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 21 (Veterinary Medicine) --
mined from the OCR output cached at /tmp/sfmedical.txt (sections
21-1 Food Procurement/Inspection/Preparation and 21-3 Animal Health).

SCOPING NOTE: checked the existing wiki first. The existing "Safe
Home Food Storage" page already covers shelf-stable canned/dry
goods (USDA/CDC-sourced, genuinely better than this 1982 source for
that specific topic) -- so that ground is NOT re-seeded here. What
IS genuinely new: real handling/inspection rules for FRESH
perishables (produce, eggs, dairy, meat, seafood) and a real
antemortem exam checklist for evaluating a live animal before
slaughter, which directly extends this wiki's existing hunting/
butchering content (from ATP 3-50.21) with a step most of that
content doesn't cover -- deciding whether the animal is even safe
to butcher in the first place.

Also checked: maggot therapy and the "wet it/dry it" skin-infection
rule of thumb from this same handbook's Chapter 22 (Primitive
Medicine) were already seeded in an earlier session -- not
revisited here. That same chapter's worm/parasite "home remedies"
(eating tobacco, drinking kerosene) and its flame-based tick/leech
removal technique (now medically discredited -- heat can cause a
tick to regurgitate pathogens into the wound) are deliberately
never seeded, consistent with this project's standing rule against
publishing content that is actively dangerous or superseded by
current medical consensus.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_foodsafety.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Food Safety — Real Antemortem Inspection Before Butchering an Animal",
        "section": "reference",
        "tags": ["food-safety", "butchering", "livestock"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**Before butchering any animal (raised, traded for, or found already dead) for food, a real pre-slaughter inspection can catch disease that cooking might not fully protect against.** This extends this wiki's existing butchering guidance with a step that comes before the knife: deciding whether the animal is even safe to use at all.

## ⚠️ Real Reasons to Reject an Animal Before Butchering

**Examine the live (or very freshly dead) animal and reject it for food if you see any of these:**

- **Posture and gait:** reject if deformed, or if the animal is "down" (unable to rise/stand normally).
- **Nutritional state:** reject if very poor body condition — this can indicate chronic disease.
- **Reaction to its environment:** reject if very lethargic (possible serious illness) OR unusually hyperexcitable (**⚠️ real, important: this specific combination can indicate rabies or tetanus**).
- **Appetite, rumination, and feces:** reject if any of these suggest active disease.
- **Breathing:** reject if labored, or if coughing is severe.
- **Udder/genitals (vulva, mammary gland):** reject if there are visible signs of infection.
- **Hide, skin, and hair:** reject if there are widespread (diffuse) lesions.
- **Body temperature:** reject if elevated — though this specific sign is worth rechecking, since a single elevated reading isn't always conclusive on its own.

**⚠️ Real, important general rule: carcass (muscle) meat carries less contamination risk than visceral (organ) meat** — when in doubt about an animal's health, the muscle meat is the real safer choice, and organs are the first thing to discard if there's any uncertainty.

## Real Normal Vital Signs for Common Livestock

**Knowing what's normal is what makes "elevated temperature" or "abnormal breathing" actually meaningful.** Real reference ranges:

| Animal | Rectal Temp (°F) | Heart Rate (bpm) | Resp. Rate |
|---|---|---|---|
| Horse | 100.5 | 23-70 | 12 |
| Cow | 100.5 | 60-70 | 30 |
| Sheep | 103 | 60-120 | 19 |
| Goat | 104 | 70-135 | 10-14 |
| Pig | 102 | 54-86 | 11-16.5 |
| Dog | 101.5 | 100-130 | 22 |
| Cat | 101.5 | 110-140 | 26 |
| Rabbit | 102.5 | 123-304 | — |

## Detailed Version

**The real, most important idea on this page: a sick animal doesn't always look sick, but a few specific real red flags (abnormal gait, poor body condition, the lethargic-OR-hyperexcitable extremes, labored breathing, visible infection) are worth checking BEFORE the work of butchering begins** — finding one of these after the animal is already dressed out is a much worse position to discover a real problem from.
""",
    },
    {
        "title": "Perishable Food Safety — Real Produce, Dairy, Meat & Seafood Handling Rules",
        "section": "reference",
        "tags": ["food-safety", "food-handling", "foraging-safety"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**This page covers fresh/perishable food handling — produce, eggs, dairy, meat, and seafood.** For shelf-stable canned and dry goods, see the existing Safe Home Food Storage page; this is genuinely different ground.

## Real Framework: 3 Kinds of Food Contamination

1. **Physical** — arthropods, metal fragments, glass, and similar foreign material.
2. **Chemical** — contamination by chemical agents, industrial chemicals, pesticides, or toxic metals (zinc, copper, cadmium).
3. **Biological** — pathogenic microorganisms (bacteria, fungi, viruses) or excessive spoilage organisms.

## Real Produce Rules

**⚠️ Real, specific disinfection recipe: boiling for 30 minutes, cooking to 116°F+, or a 100ppm chlorine solution (1½ oz. of 5% bleach per 5 gallons of water) destroys most pathogenic organisms** on fresh fruits and vegetables. **Avoid vegetables grown using "night soil" (human waste as fertilizer) if at all possible** — always wash, peel, and disinfect (or cook) if there's any doubt about how produce was grown. **⚠️ Real, specific chemical hazard: don't store or serve acidic foods in galvanized containers** — this causes zinc toxicosis (zinc poisoning leaching from the galvanized coating into the acidic food).

## Real Eggs & Dairy Rules

**Eggs should always be cooked** (to prevent salmonella) — blood or meat spots inside an egg are harmless and don't make it unsafe, but a rotten or cracked egg should be discarded. **Unpasteurized dairy must be pasteurized or boiled for at least 15 seconds** — this real minimum time matters because it's what actually protects against tuberculosis, Q fever, brucellosis, and similar real risks (see Leptospirosis — Real Risk From Flood & Contaminated Water Exposure for a related real waterborne-disease concern).

## Real Seafood & Fish Rules

**Cooking is essential for all seafood** (hepatitis, bacteria) **and all freshwater fish** (tapeworm, fluke, and other parasites). **⚠️ Real, important exception to "cooking makes it safe": some shellfish toxins (for example, during a red tide) and some saltwater fish toxins are heat-stable** — cooking does NOT destroy them. The real safest approach where this is a possibility: judge local safety by what the native/local population actually eats, and when in doubt, avoid shellfish and unfamiliar saltwater fish entirely (see also Animals & Fish You Should Never Eat — Real Poisonous Species Warnings).

**Real seafood spoilage signs:** off-odors, sticky or pitting flesh, sunken eyes, or scales that come off easily — and remember that ice itself can be a real contamination source if it isn't from a clean supply.

## Real Meat Rules

**Thoroughly cooked meat from a healthy animal is safe** (cooking prevents trichinosis, tapeworms, and similar parasites) — see Food Safety — Real Antemortem Inspection Before Butchering an Animal for how to judge whether an animal was healthy in the first place. **Carcass (muscle) meat carries less real contamination risk than visceral (organ) meat.**

## Detailed Version

**The real, unifying idea across this whole page: "cook it and it's safe" is usually true, but has real, specific, worth-memorizing exceptions** — heat-stable shellfish/fish toxins, and the chemical (not biological) risk of zinc leaching from galvanized containers — where the usual cooking-based safety logic simply doesn't apply. Knowing those specific exceptions is what prevents a false sense of security in exactly the situations where it matters most.
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
