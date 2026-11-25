#!/usr/bin/env python3
"""Seeds 3 real pages from the USMC Winter Survival Course Handbook's
Field Expedient Tools, Weapons, and Equipment chapter -- mined from
the real text layer already extracted in this session
(/tmp/usmcwinter.txt, pages 11-1 through 11-6). Real bushcraft
technique for making tools, simple hunting implements, a pack, and
camp utensils entirely from field materials.

Covers: the 5 real material categories (stone, bone, wood, metal,
other improvised materials) with real fire-hardening and coal-burning
technique and real pine-pitch glue construction, 3 real survival
sticks (noose stick, slingshot, throwing stick) plus a basic club,
and real expedient pack and camp-utensil (bowl, spork, tongs)
construction.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_expedient_tools.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Field Expedient Materials — Stone, Bone, Wood & Metal",
        "section": "reference",
        "tags": ["bushcraft", "tool-making", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Every field-expedient tool is built from one of 5 real material categories, each with its own real working technique.**

## Stone

**Good for striking, puncturing, or chopping — but won't hold a fine edge**, except for specific stones (chert, flint, obsidian), which are genuinely hard to find in winter conditions.

**Chipping & flaking** produces a sharp edge: a chipping tool (blunt, made from wood/bone/metal) breaks off small pieces; a flaking tool (pointed, made from bone/antler tine/soft iron) breaks off thin, flat pieces. **Test a candidate stone's hardness before relying on it as a weapon head** — some shatter unpredictably under force.

## Bone

Real uses: hooks, shaft tips, scrapers, awls, sockets, handles. **Shatter raw bone with a heavy object (a rock)**, then select a suitably pointed splinter from the pieces and refine its point/edge by rubbing it against a rough stone or metal file.

## Wood — the Most Versatile Real Material

- **Hardwood is preferred for nearly everything.** Real field test: press a fingernail into the grain — **if it leaves a visible print, the wood is soft** and less durable for tool use.
- **Sharpen points off to the side of the shaft, not through the center** — wood is structurally weakest at its center and won't hold a point there.
- **⚠️ Fire-harden all green wood before use:** hold the point a few inches above hot coals, slowly rotating it, until it hisses/steams. This swells the wood's cells and thickens its sap, making it genuinely more resistant to abrasion and impact. **Harden only to a light brown — avoid actually charring it.**
- **Coal-burning** creates a hollow depression that's otherwise very hard to carve: hold a hot coal (with tongs) over the spot to be hollowed, blow a thin steady air stream onto it (a hollow reed or bone works well for directing airflow), let it burn down, then scrape out the charred wood with a knife or sharp rock. **Repeat with fresh coals until the depression reaches the depth you need.**

## Metal — the Best Real Material for an Edged Tool

**Metal can fulfill all 3 of a knife's real jobs — puncturing, slicing/chopping, and cutting — when properly shaped.** Pick a piece of metal already close to your intended final shape. Refine a point/edge by rubbing it against a rough stone or metal file; **if the metal is soft enough, you can cold-hammer an edge** using a flat hard surface as an anvil and a harder stone/metal object as a hammer.

## Other Real Improvised Materials

- **Load-bearing equipment clips** — a sliding retaining clip can be removed and sharpened to a point.
- **Plastic/Plexiglas/glass** (e.g., salvaged from wreckage) can be shaped into a point; plastic can also be melted as an adhesive.
- **Paracord** — genuinely unlimited real construction uses.
- **Pine pitch glue** — a real, functional field adhesive, essentially an improvised epoxy:
  1. Harvest pine sap/pitch — fresh sap works best, though old hardened sap still works, just less effectively.
  2. Melt it on an elevated platform (a smooth rock works) and let it run down.
  3. Coat a 6-8 inch stick repeatedly in the pooling pitch until it resembles a large wooden match.
  4. **To use: light the pitch end and let it drip onto the area being glued**, then sprinkle on an activator (finely ground eggshell or wood ash) once the pitch has coated the surface.

## Detailed Version

**The real, shared discipline across every material here: match the material to the job rather than forcing one material to do everything.** Stone chops but won't hold a fine edge; bone makes a fine point but isn't structural; wood is endlessly shapeable but needs fire-hardening to actually hold up; metal does everything a knife needs but requires more processing to shape. Picking the right material for a specific tool, rather than defaulting to whatever's easiest to grab, is the real skill underneath all of this.
""",
    },
    {
        "title": "Survival Sticks & Simple Weapons",
        "section": "reference",
        "tags": ["bushcraft", "survival-skills", "tool-making"],
        "risk_level": None,
        "body_markdown": """## Simple Club

**A held (never thrown) weapon that extends your reach beyond your own fingertips and lets you hit harder without injuring your own hand.** Use a staff or branch **short enough to swing easily, but long and strong enough to actually damage whatever it hits** — diameter should sit comfortably in your palm without being so thin it snaps on impact.

## 3 Real Survival Sticks

### Noose Stick

**Used to safely control or finish off an animal that's still alive in an improperly set snare.** Find a pole as long as you can handle effectively, attach a noose of wire or stiff cord at the small end, then slip the noose over the animal's neck and pull tight.

### Slingshot

**A genuinely effective and accurate weapon, built from a Y-shaped hardwood stick** with slingshot rubber and a pouch (carried in a survival kit) attached to the two prongs.

### Throwing Stick

**One of the simplest real survival tools — doubles as both a weapon and a practical tool for knocking dead branches out of a tree for firewood** that would otherwise be out of reach.

1. Find a stick as straight as possible, 2.5-3 feet long, 1.5-2 inches in diameter.
2. Remove the bark.
3. Taper both ends.
4. Fire-harden the whole stick if it's green wood.
5. **Throwing technique depends on terrain:** an overhand throw works best in forested areas (more vertical clearance); a sidearm throw extends your effective range in open terrain.

## Detailed Version

**The real, shared value across these 4 implements: each is built from minimal, commonly-available material (a branch, a Y-stick, a straight stick) and solves a specific, real problem — extending reach safely, controlling a live catch, ranged accuracy, or reaching unreachable firewood — rather than trying to be a single do-everything tool.**
""",
    },
    {
        "title": "Making an Expedient Pack & Camp Utensils",
        "section": "reference",
        "tags": ["bushcraft", "survival-skills", "camp-gear"],
        "risk_level": None,
        "body_markdown": """## The Horseshoe Pack — Simple, Comfortable to Carry

1. Lay a square piece of material flat (a poncho or tarp works well).
2. Arrange your gear along one edge — **put frequently-used items (canteens, etc.) toward the outside**, and pad anything hard against your back.
3. Roll the material (with gear inside) toward the opposite edge, then tie both ends securely.
4. Tie additional lines along the bundle's length for stability.
5. Fold the whole bundle in half and secure a long rope to the fold's apex.
6. Attach the completed pack across one shoulder.

## Camp Utensils — Real, Simple Builds

### Bowl or Container

**Made from bone or wood.** To make a wooden one: find or split a piece of wood, then **coal-burn it to the desired depth** (see Field Expedient Materials — Stone, Bone, Wood & Metal for the real coal-burning technique).

### Spork

A simple carved eating utensil — shape a piece of wood into the desired spoon/fork combination with a knife.

### Tongs (for handling hot coals/embers safely)

1. Cut a green sapling.
2. Split it in half lengthwise and shave off the bark; flatten both ends of each half.
3. **Fire-harden each half** before use.

## Detailed Version

**The real principle tying the pack and utensils together: none of this requires purchased gear — a tarp, a knife, and basic woodworking technique (splitting, coal-burning, fire-hardening) are genuinely enough to produce a functional pack, bowl, eating utensil, and fire tool from scratch**, which matters specifically when store-bought replacements for lost or broken gear simply aren't available.
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
