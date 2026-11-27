#!/usr/bin/env python3
"""Seeds 1 real page from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Appendix F (Field Sterilization and
Disinfection) -- mined from the OCR output cached at
/tmp/sfmedical.txt.

Not covered anywhere else in the wiki (the existing "Finding &
Disinfecting Water in Cold Environments" page is about drinking
water, a different topic entirely). This is genuinely novel,
directly actionable, home-equipment-compatible content -- a real
home pressure cooker can function as the autoclave method described
here.

SCOPING NOTE: the same appendix also includes diagram-dependent
step sequences for folding gauze pads, wrapping dry goods, and
making cotton balls/applicators (the OCR preserved only garbled
ASCII-art fragments of the actual diagrams) -- those are skipped,
consistent with this project's standing rule against reconstructing
figure-dependent technique from text alone. The real sterilization
METHODS themselves (temperatures, times, PSI, chemical ratios) are
plain prose/data in the source and are not figure-dependent, so
they are seeded here.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_sterilization.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Field Sterilization & Disinfection — Real Methods, Times & Temperatures",
        "section": "reference",
        "tags": ["sterilization", "disinfection", "medical-supplies"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**An item is either sterile or it isn't — there's no real in-between.** If there's any doubt, treat it as not sterile. This page covers real methods for sterilizing medical instruments and supplies at home, not drinking water (see the existing water-disinfection content for that).

## Real General Rules

**Everything being sterilized must first be clean, free of oil, and in working condition** — sterilization kills organisms, it doesn't clean dirt or oil off. **Wrappers for sterile goods must be double-thickness and free of holes.** Label and date packs when you make them. **⚠️ Real, important shelf-life rule: a sterilized pack is considered outdated after 4 weeks (only 2 weeks in high humidity)** — re-sterilize after that window rather than assuming it's still sterile.

## ⚠️ Real Method: Steam Under Pressure (Pressure Cooker)

**This is the real method of choice — a commercial home pressure cooker works if a real autoclave isn't available.** **It's the only method on this page that reliably kills everything, including spores.**

- **⚠️ Real, specific numbers: must reach at least 15 psi and 250°F (121°C), held for 15 minutes.** If using a home pressure cooker, **real, practical tip: run it at about 17 psi on the gauge** — this builds in margin to actually guarantee the 250°F minimum is reached.
- **Real timing by item type:** instrument packs and linen — 30 minutes, plus 15 minutes drying time. Rubber goods — 15 minutes, plus 15 minutes drying time.
- **Real practical limit: keep any pack to a maximum of 12 x 18 inches** so heat/steam can actually penetrate it fully.

## Real Method: Dry Heat (a Regular Oven)

**Good for ointments, oils, waxes, and powders — also works for glassware, instruments, and needles.** **⚠️ Destroys fabric, so don't use it for cloth items.** **Real timing: 120 minutes at 320°F for ointments/oils/waxes/powders; 60 minutes at 320°F for glassware/instruments/needles.**

## Real Method: Flame (Incineration)

**For anything that can simply be burned** (food scraps, paper, old dressings). **Real rule: burn until completely destroyed** — there's no fixed time, just a fixed end state.

## Real Method: Sunlight

**For clothing, bedding, and mattresses.** **Real timing: at least 6 hours of direct sunlight on EACH side.**

## Real Method: Boiling

**⚠️ Real, important limitation: boiling does NOT kill spores** — it's a real disinfection method, not true sterilization, and is the weakest option on this page.

- **Start timing only after the water is actually at a full boil.**
- **Real elevation adjustment: add 5 minutes for every 1,000 feet of elevation above sea level** (water boils at a lower temperature at altitude, so compensate with more time).
- **⚠️ Don't boil blades or scissors except as a real last resort — it dulls/rusts the edge.**
- **Adding sodium carbonate to make a 2% solution genuinely increases boiling's effectiveness.**
- **Real baseline time: 30 minutes at sea level** (before any elevation adjustment).

## Real Chemical Methods (If the Chemicals Are Available)

- **70% alcohol solution, 18 hours minimum** — real, important limitation: does not kill spores. **Real practical tip: add 0.5% sodium nitrite to prevent instruments from rusting in it.** Real advantage: once an item is sterilized by another method, storing it in alcohol afterward maintains that sterility.
- **Zephiran chloride, 1:750 solution, 18 hours minimum** — does not kill spores or tuberculosis bacteria.
- **⚠️ Formaldehyde-alcohol solution (99% ethyl/isopropyl alcohol 700ml + 37% formaldehyde solution 25ml + sodium nitrite 1g + sodium bicarbonate 1g + distilled water to 1,000ml total): the most powerful germicidal option here, and the only chemical method that genuinely kills spores.** Real timing: metal instruments, 3 hours; catheters/tubing, 18-24 hours. **This needs the actual lab chemicals on hand and careful handling — not something to improvise casually.**

## Detailed Version

**The real, most important idea across every method on this page: "disinfected" and "sterilized" are NOT the same real guarantee — several of the easiest real methods (boiling, alcohol, Zephiran chloride) explicitly do NOT kill bacterial spores, while only the pressure-cooker/autoclave method and the formaldehyde-alcohol solution genuinely do.** For routine cleaning, boiling or alcohol is a real, reasonable choice; for anything going into a deep wound or used for a serious procedure, the real, meaningfully safer choice is the pressure-cooker method specifically, precisely because spore-forming organisms (like the ones responsible for tetanus and gas gangrene) are exactly the ones the weaker methods can't touch.
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
