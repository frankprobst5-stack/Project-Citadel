#!/usr/bin/env python3
"""Seeds 2 real pages from the Navy Manual of Preventive Medicine,
Chapter 9 (Preventive Medicine for Ground Forces) -- mined from the
real text layer already extracted in this session (/tmp/navmed.txt).
This file is only Chapter 9 of the much larger multi-chapter Manual
of Naval Preventive Medicine; most of its other sections (water
treatment via ROWPU units, food service/galley equipment, military
water-requirement logistics tables) either require specialized
military equipment civilians won't have, or substantially duplicate
content already covered elsewhere in this wiki (water disinfection,
heat/cold injuries). Mined selectively for genuinely new,
civilian-actionable content: real field latrine engineering that
meaningfully extends the wiki's existing "Sanitation & Latrines"
page (which covers only a single cement-slab design from Where
There Is No Doctor).

Covers: real siting rules and 3 real latrine designs (cat hole,
straddle trench, deep pit) for different real durations of use, plus
3 more real designs (burn-barrel, mound, urine-specific disposal)
for difficult ground conditions -- all with real dimensions and
capacity figures.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_navmed_latrines.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NAVMED_PDF_URL = "/files/pdfs/Medical/NAVMED-P-5010-US-Navy-Manual-of-Preventive-Medicine.pdf"

PAGES = [
    {
        "title": "Field Latrines — Cat Hole, Straddle Trench & Deep Pit",
        "section": "reference",
        "tags": ["sanitation", "latrine", "field-hygiene"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Real latrine design should match how long you'll actually be using it — a quick one-time stop needs a different real solution than a shelter-in-place situation lasting weeks.** Real siting rules apply to every design below.

## Real Siting Rules (apply to every latrine type)

**Locate at least 100 feet from the nearest natural water source, at least 100 yards from any food storage/prep area, and 50 feet from where people actually sleep** — while still being reasonably convenient to reach. These distances exist specifically to keep waste from contaminating drinking water or food.

## Cat Hole — for a Single Use on the Move

**The real quick-stop solution** when no other latrine is available. Dig a hole 8-12 inches across and 6-12 inches deep. Deposit waste, then **immediately cover it with the same tightly compacted earth you removed** — this single step is what actually prevents it from becoming a health/odor hazard.

## Straddle Trench — Real Short-Term Group Solution

**Serves roughly 25 people, 2 at a time.** Dig a trench 1 foot wide, 2.5 feet deep, 4 feet long. **No seats** — boards placed along both sides improve footing. Space additional trenches at least 2 feet apart. **Each person covers their own waste and toilet paper immediately** using whatever digging tool is on hand (an entrenching tool, a shovel). **Close the trench once it's filled to within 1 foot of the top:** spray with insecticide if available, backfill in several compacted layers, and mound the final covering at least 1 foot above ground level. **Mark it clearly with the type of latrine and the date it was closed** — this real detail matters if the site is reused or if anyone digs there later.

## Deep Pit Latrine — Real Longer-Term Solution

**One standard 4-seat unit serves about 50 people.** The latrine box (built over the pit) is 8 feet long, 2.5 feet wide at the base, mounted on two 6-inch planks. **Seats need fly-proof, self-closing lids**, and any gaps in the wood should be sealed (strips of wood/metal, sandbagging, or oil-soaked burlap) to keep flies out. **A metal deflector on the inside front panel stops urine from soaking into the wood** — and surfaces that contact skin should be sanded smooth.

**Pit dimensions:** 2 feet wide, 7.5 feet long, up to 6 feet deep (or a 5-foot-square, 4-seat version over a 4-foot-square pit up to 6 feet deep). **A real, useful rule of thumb: allow 1 foot of pit depth for each week of planned use, plus 1 extra foot for final dirt cover.** **⚠️ The deeper the pit, the greater the real risk of it caving in** — don't dig deeper than your actual planned duration requires.

## Detailed Version

**The real principle tying all three designs together: the right latrine is the one sized to your actual real-world duration of use, not the most elaborate one you could build.** A cat hole over-engineered into a straddle trench wastes real time and material; a straddle trench under-sized for weeks of continuous use becomes a real health hazard well before you expect it to. Matching design to duration is the actual skill here, not memorizing one "best" design.
""",
    },
    {
        "title": "Field Latrines — Burn-Barrel, Mound & Urine Disposal",
        "section": "reference",
        "tags": ["sanitation", "latrine", "field-hygiene"],
        "risk_level": "high",
        "body_markdown": """## Burn-Barrel Latrine — Real Solution for Hard, Rocky, Frozen, or High-Water-Table Ground

**When digging a real pit genuinely isn't possible** (frozen ground, bedrock, or a water table too close to the surface), this design avoids digging almost entirely. Build a screened, insect-proof enclosure (plywood and framing lumber) with 2-4 toilet seats positioned over 55-gallon drums cut in half, **positioned precisely: the hole's forward edge set back 4-6 inches from the bench edge, the barrel's rim no more than 2 inches below the seat (further than that causes real splashing/spillage), pushed fully back against a stop to center it under the hole.**

**⚠️ Prime each barrel with 3 inches of diesel fuel before use** — this soaks the waste in oil, which both helps it burn completely later and genuinely acts as an insect repellent and odor suppressant in the meantime. **⚠️ Post "NO SMOKING" signs conspicuously inside and outside the structure** — this is a real, serious fire/explosion risk given the fuel involved.

**Real burn-out procedure, once a barrel is ½ to ⅔ full:** remove it from the structure. Mix 4 parts diesel to 1 part gasoline, enough to sufficiently cover the contents, and ignite with a stick/pole **at least 4 feet long** (shorter ones must be replaced — a real, specific safety margin from the flame). **Keep burning until the contents reduce to fine ash** — this can take more than one attempt. **Bury the resulting ash at least 12 inches deep; don't scatter it on the surface.** **A real way to reduce how often you need to do this at all: encourage people to use a separate urine-disposal method (see below) instead of urinating into the burn barrels** — urine adds fuel load without adding real benefit, making each burn-out slower and more fuel-intensive.

## Mound Latrine — for High Water Tables or Rock That Blocks Digging

**When the ground itself won't allow a deep pit, build UP instead of down.** Build the mound at least 6 feet wide and 12 feet long (enough to hold a standard 4-seat latrine box), in roughly 1-foot compacted layers. **Once the mound reaches the needed height, dig the actual pit down into the mound itself** — this keeps the pit's bottom above the real water table or rock layer, even though the ground beneath the mound couldn't support digging on its own. Reinforce the pit's side walls with timber or scrap wood.

## Urine Soakage Pit — Best in Sandy Soil

**A dedicated urine-only disposal method that reduces burn-barrel fuel load and odor.** Dig a 4-foot cube pit, fill to within 6 inches of ground level with coarse material (rocks, flattened cans, rubble, brick — anything that creates void space for drainage). **Insert ventilation shafts down to within 6 inches of the pit bottom, extending 6-12 inches above ground** — this lets air circulate through the pit and genuinely reduces odor. Insert 6 urine tubes (1-inch pipe, 36 inches long) at a slight angle, about 8 inches below ground level (leaving ~26 inches exposed above), each capped with a screened, moisture-proof funnel. Cover the pit with oil-soaked burlap, then 6 inches of compacted earth. **One pit serves about 20 men per pipe.**

## Urine Troughs — When Construction Material Is Available

**A simple 10-foot V- or U-shaped trough** (sheet metal, or wood lined with a moisture-proof material), with a splashboard in the middle and a drain trough/pipe at one end running to a soakage pit. **One trough design serves about 100 men** — build it with a slight slope toward the drain end to ensure real, reliable drainage rather than pooling.

## Detailed Version

**The real engineering principle shared by the burn-barrel and mound designs: both exist specifically to solve the same underlying problem — ground that physically won't accept a deep pit — through two different real workarounds (burning instead of burying, or building up instead of down).** Recognizing which constraint you're actually facing (frozen/rocky ground vs. a high water table) points you toward the design that genuinely fits your real site conditions, rather than forcing a standard deep-pit design onto ground that can't support it.
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
                "source_url": NAVMED_PDF_URL,
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
