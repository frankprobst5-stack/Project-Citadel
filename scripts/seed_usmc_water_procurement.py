#!/usr/bin/env python3
"""Seeds 3 real pages from the USMC Winter Survival Course Handbook's
Water Procurement chapter -- mined from the real text layer already
extracted in this session (/tmp/usmcwinter.txt, pages 03-1 to 03-8).

Covers: real dehydration percentages and water-intake guidance, real
water sourcing/disinfection technique in cold environments (including
the real iodination/chlorination dosing tables and contact times by
water temperature -- genuinely citable, specific numbers, not vague
guidance), and a real field-expedient snow/ice water generator build.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_water_procurement.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
USMC_WINTER_PDF_URL = "/files/pdfs/Military Manuals/USMC-Winter-Survival-Course-Handbook.pdf"

PAGES = [
    {
        "title": "Water Intake & Dehydration — The Real Numbers",
        "section": "reference",
        "tags": ["water", "dehydration", "survival-skills"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Thirst is not a reliable indicator of how much water you actually need — by the time you feel thirsty, you're already somewhat dehydrated.** The real guidance: drink plenty of water whenever it's available, especially with meals (the "over-drink" approach), rather than rationing based on how thirsty you feel in the moment.

## Real Dehydration Progression by Fluid Loss

- **5% body fluid loss:** thirst, irritability, nausea, weakness.
- **10% body fluid loss:** dizziness, headache, inability to walk normally, tingling in the limbs.
- **15% body fluid loss:** dim vision, painful urination, a swollen tongue, deafness, numbness in the skin.
- **Over 15% body fluid loss: can be fatal.**

## What Increases Your Real Water Needs

- A fever.
- Fear or anxiety (a real physiological effect, not just a mental one).
- Excess fluid evaporation — e.g., not using available shelter to reduce exposure.
- Improper clothing for the conditions.
- **Rationing water itself** — counterintuitively, trying to "save" water by drinking less increases your body's real need rather than reducing it.
- Overworking/overexertion.

## Detailed Version

**The real, actionable point: water rationing in anticipation of scarcity is usually the wrong strategy.** The body doesn't "save" the water you withhold from it — restricting intake just accelerates the dehydration curve above. The better real strategy is drinking adequately when water is available and focusing your actual effort on finding or producing more, rather than stretching a fixed supply by drinking less of it.
""",
    },
    {
        "title": "Finding & Disinfecting Water in Cold Environments",
        "section": "reference",
        "tags": ["water", "disinfection", "cold-weather", "survival-skills"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**In a cold-weather/mountain environment, real water sources include snow, ice, streams/rivers, and (eventually) sea ice — but each has a real catch, and getting those catches wrong is a genuine hazard.**

## Real Source Notes

- **Snow:** can be melted for drinking water, but **uses significantly more fuel** than melting the equivalent amount of ice. Uncontaminated snow itself doesn't need disinfecting.
- **Ice:** melting ice is actually preferable to snow — **ice has a much higher water content per volume**, meaning less fuel per cup of actual water produced. **But ice still needs disinfecting**, since it's just frozen water and can carry the same contamination.
- **Streams/rivers:** a real water source in mountainous terrain, but **use real caution approaching the edge** — accidental submersion in cold water is a genuine, serious risk in itself.
- **Sea ice:** loses its salt content over time — **look for rounded corners and a bluish color as the real sign it's desalinated enough to use; gray ice still has salt and should be avoided.**

**⚠️ Never melt snow or ice directly in your mouth** — this pulls real body heat away and increases your risk of cold-weather injury. **If you need to melt snow using body heat while moving, put it in a sealed bag between layers of clothing — never directly against bare skin.**

## ⚠️ Hazardous Fluids — Real Reasons Not to Substitute Them for Water

- **Seawater:** genuinely toxic beyond minimal amounts — its sodium/magnesium concentration is so high that your body must pull its own fluid to process and eliminate the excess salt, and enough of it can shut down kidney function entirely.
- **Alcohol:** dehydrates the body, lowers core body heat, and impairs judgment — in cold conditions, drinking a very cold alcoholic liquid can cause immediate frostbite of the throat, and in extreme cases death.
- **Blood:** counts as food, not water — digesting it actually costs your body additional fluid rather than supplying any.
- **Urine:** is body waste; drinking it returns that waste into your system and costs more fluid to re-expel it than it provides.

## Real Disinfection Methods

**Boiling is the single most preferred method.** Water brought to a rolling boil kills 99.9% of Giardia cysts (which die at 60°C) and Cryptosporidium (dies at 65°C). **Altitude barely matters for this** — water still boils at 86°C at 14,000ft and 90°C at 10,000ft, both comfortably above the kill temperatures, so don't assume high-altitude boiling is somehow insufficient.

**Chemical disinfection (halogens)** — real dosing, added per liter/quart of water:

| Method | Dose for 4ppm | Dose for 8ppm |
|---|---|---|
| Iodine tablets (tetraglycine hydroperiodide) | ½ tablet | 1 tablet |
| 2% iodine solution (tincture) | 0.2ml (5 drops) | 0.4ml (10 drops) |
| 10% povidone-iodine solution | 0.35ml (8 drops) | 0.70ml (16 drops) |

| Method | Dose for 5ppm | Dose for 10ppm |
|---|---|---|
| Household bleach (5% sodium hypochlorite) | 2 drops | 4 drops |

**⚠️ Real required contact time (minutes) before the water is safe, by halogen concentration and water temperature:**

| Concentration | 5°C / 40°F | 15°C / 60°F | 30°C / 85°F |
|---|---|---|---|
| 2ppm | 240 min | 180 min | 60 min |
| 4ppm | 180 min | 50 min | 45 min |
| 8ppm | 60 min | 30 min | 15 min |

**Colder water genuinely needs far longer contact time to kill Giardia — this is not a minor detail; using a warm-water contact time on cold water risks drinking still-contaminated water.** Also note: **chemical disinfection may not reliably destroy Cryptosporidium**, which has an unusually tough protective membrane — boiling is the more reliable method against it.

## Purification vs. Disinfection vs. "Potable" — a Real, Important Distinction

- **Disinfection** (the real goal) removes/destroys harmful microorganisms.
- **Purification** removes chemicals and particulate matter (including improving taste/smell/color) — **but doesn't necessarily kill all microorganisms.** A commercial filter with openings larger than 0.3 microns won't stop Cryptosporidium, and a filter that doesn't also release a disinfecting chemical may not kill everything it physically traps.
- **"Potable"** just means a source has, on average, a low enough microbial hazard that illness is statistically unlikely — it is the weakest of the three real categories, not a guarantee.
- **Sedimentation** (letting particles settle, about 1 hour undisturbed, then pouring off the clear water) **is not a real disinfection method** — it should be treated as a last resort, not a substitute for boiling or chemical treatment.

## Detailed Version

**The real, recurring theme across sourcing and disinfecting water here: assuming clear, cold, remote-looking water is automatically safe is a genuinely common and dangerous mistake.** Giardia cysts are described as an "ever-present danger in clear appearing mountain water throughout the world" — the water's appearance tells you nothing reliable about its actual safety, which is exactly why a real disinfection step, correctly timed for the water's actual temperature, matters even when the source looks pristine.
""",
    },
    {
        "title": "Building a Snow/Ice Water Generator",
        "section": "reference",
        "tags": ["water", "cold-weather", "shelter-building", "survival-skills"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**A simple field-expedient device lets you passively melt snow or ice into drinking water near a fire, without wasting fuel boiling it in a pot — ice is the better material to use, since it takes roughly 3-4 cups of snow to produce the same amount of water as a much smaller volume of ice.**

## What You Need

Any available fabric/container material — a parachute panel, plastic bag, or T-shirt work; bark is a real fallback if nothing else is available. Wood for a simple tripod, if available.

## Real Construction Steps

1. **If wood is available:** gather 3 poles, roughly 6 feet long and 3 inches in diameter, and tie them together into a tripod.
2. **Pack the material with snow:** fill your T-shirt/parachute/plastic bag with snow and tie it completely shut. **Repeatedly bang it against the ground to compact the snow densely** — this matters, since loosely packed snow melts less efficiently. Keep adding snow and compacting until the bag is completely full.
3. **Hang the packed bag from the tripod, positioned near the fire** — close enough to melt, but **far enough that the material itself won't catch fire or scorch.**
4. **Within about 30 minutes, the bag will begin dripping from one spot** — place any available container underneath that drip point to collect the water.
5. **Keep adding snow to the bag as it melts down** — never let the generator run completely empty, since restarting the melt from nothing wastes the heat you've already built up.
6. **No wood for a tripod?** A single pole tied to a tree works as a substitute, or snow packed directly onto bark angled toward the fire, with water collected as it melts and runs off.

**Once running, a single generator can reliably supply more than enough water for 2 people.**

## Detailed Version

**The real value of this device is passive efficiency: it converts heat that's already being generated for warmth (your fire) into drinking water production, with zero active fuel cost beyond what you're already burning to stay warm.** This is a meaningfully better strategy than melting snow directly in a pot over the fire, which consumes fuel specifically for water production rather than getting that production as a side effect of heat you need anyway.
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
                "source_url": USMC_WINTER_PDF_URL,
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
