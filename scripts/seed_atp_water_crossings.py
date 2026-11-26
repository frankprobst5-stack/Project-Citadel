#!/usr/bin/env python3
"""Seeds 3 real pages from ATP 3-50.21 (Survival), the current U.S.
Army survival doctrine manual (September 2018, superseding the older
FM 21-76) -- mined from the real text layer already extracted in
this session (/tmp/atp_survival.txt), Chapter 7 (Movement and
Navigation), Water Crossings section (pages 7-3 through 7-9).

This is genuinely new content for this wiki -- no prior source has
covered real river/stream crossing technique or field-expedient
rafts/flotation devices.

Covers: real site-selection and hazard-avoidance for river crossings,
real technique for swimming/fording in rapids (including the pole-
ford method for one or multiple people, with and without rope), 2
real field-expedient raft designs (brush raft, Australian poncho
raft) with full real construction steps, and real flotation device
options (log raft, trousers, containers, plastic bags/poncho rolls,
cattail bundles).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_atp_water_crossings.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
ATP_SURVIVAL_PDF_URL = "/files/pdfs/Military Manuals/ATP-3-50.21-Survival.pdf"

PAGES = [
    {
        "title": "Crossing Rivers & Streams — Site Selection & Rapids",
        "section": "reference",
        "tags": ["water-crossing", "navigation", "survival-skills"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Before crossing any river or stream, get to high ground first and actually scout the crossing — site selection is the single most important real decision, before any swimming or fording technique even comes into play.**

## Real Good Crossing Locations

- **A level stretch where the river splits into several channels** — 2-3 narrow channels are usually easier to cross than one wide river.
- **A shallow bank or sandbar** — pick a crossing point upstream of it, so if you lose your footing, the current carries you toward it rather than away.
- **A course angled downstream, crossing the current at roughly a 45-degree angle** rather than straight across.

## ⚠️ Real Hazards to Avoid

- **A rock ledge crossing the river** — often a real sign of dangerous rapids or a canyon downstream.
- **A river's estuary** — typically wide, strong-current, and tide-affected (sometimes for miles upstream of the actual coast) — go back upstream to find an easier site instead.
- **Eddies** — these can create a real, powerful backward pull just downstream of whatever obstruction caused them, strong enough to pull a person under.

## Swimming Through Rapids

- **In fast, deep water: swim WITH the current, never against it.** Keep your body horizontal in the water to reduce the real risk of being pulled under.
- **In fast, shallow rapids: float on your back, feet pointing downstream, finning your hands at your hips** — this increases buoyancy and helps you steer around obstacles while keeping your feet up and clear of rocks.
- **In deep rapids: float on your stomach, head pointing downstream, angling toward shore.** Watch for obstacles, and be especially wary of backwater eddies and converging currents (where a side channel joins the main river, or water diverts around an island) — these often hide dangerous swirls.

## Real Pole-Ford Technique (for a Swift, Treacherous Stream)

1. Find a sturdy pole, about 3 inches thick and 7-8 feet long.
2. **Plant the pole firmly on the upstream side of you to break the current.** Step firmly with each step, moving the pole slightly downstream of its previous position but still ahead of (upstream of) you.
3. **Step with each foot placed just below the pole, keeping the pole angled so the current's force holds it against your shoulder.** Cross at roughly a 45-degree angle to the downstream current — the same angle used for site selection above.

**Crossing as a group:** everyone crosses together, with **the heaviest person positioned at the downstream end of the shared pole and the lightest at the upstream end** — the upstream person breaks the current, and the real eddy this creates lets everyone below move more easily. If the upstream person briefly loses footing, the rest of the group can hold steady while they recover. **With 3+ people and a rope available, a rope-assisted crossing works too — the rope needs to be at least 3 times the width of the stream.**

## Detailed Version

**The real, repeated theme across every one of these techniques: fighting the current directly is almost always the wrong move — working with it (swimming with it, angling across it at 45°, using the upstream person to create a sheltering eddy for the group) is what actually gets a person across safely.** Site selection exists specifically to avoid situations where that's not possible at all (estuaries, eddies, rock-ledge rapids) in the first place.
""",
    },
    {
        "title": "Building a Field-Expedient Raft — Brush & Poncho Rafts",
        "section": "reference",
        "tags": ["water-crossing", "rafts", "survival-skills"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Neither of these 2 real raft designs is meant to carry a person's full body weight — both are built to float gear (and help a swimmer) across slow-moving water, not to be ridden like a boat.**

## Brush Raft (needs 2 ponchos, fresh green brush, 2 small saplings, rope/vine)

1. Tuck each poncho's hood to its inner side and tie the neck opening tightly shut with its drawstring.
2. Attach ropes/vines to the corner and side grommets of each poncho, long enough to reach and tie to the opposite corner/side.
3. Spread one poncho on the ground, inner side up. Pile fresh green brush (no thick branches) onto it until the pile is about 18 inches high, pulling the drawstring up through the center of the brush stack.
4. Build a simple X-frame from the 2 small saplings and lay it on top of the brush pile, tying it in place with the poncho's drawstring.
5. Pile another 18 inches of brush on top of the X-frame, then compress it slightly.
6. Pull the poncho's sides up around the brush bundle and tie them diagonally, corner-to-corner and side-to-side, using the attached ropes/vines.
7. Spread the second poncho nearby, inner side up.
8. Roll the tied brush bundle onto the second poncho (tied side down), then tie the second poncho around it the same way as the first.
9. Launch with the second poncho's tied side facing up.

## Australian Poncho Raft (faster to build, more waterproof, but only floats ~77 lbs of gear)

**Needed:** 2 ponchos, 2 rucksacks, 2 four-foot poles/branches, and rope/vine/bootlaces or similar.

1. Tuck each poncho's hood in and tie off the neck as above.
2. Spread one poncho, inner side up, and center the 2 poles on it, about 18 inches apart.
3. Place rucksacks/packs/gear (and anything that needs to stay dry) between the poles, then snap the poncho's sides together over them.
4. **With a second person's help**, lift the snapped seam into the air and roll it tightly down toward the equipment, rolling the poncho's full width.
5. Twist the roll's ends into "pigtails" in opposite directions, fold them over the bundle, and tie them securely.
6. Spread the second poncho, inner side up — **add fresh green brush here if you need more buoyancy.**
7. Place the tied bundle (tied side down) on the second poncho's center and wrap it the same way as the first.
8. Tie binding material around the raft about 12 inches from each pigtail's end, and secure any weapons/gear on top.
9. **Tie a rope from an empty canteen to the raft** — this gives you something to tow the raft by while swimming alongside it.

## Real Launch & Use Notes (both designs)

**Don't drag either raft on the ground when launching — this can puncture or tear it.** Let it float on the water for a few minutes first to confirm it's actually buoyant before committing gear to it. **If the water's too deep to ford, push the raft ahead of you while swimming — neither design is built to carry a rider's full weight**, only to float equipment and assist a swimmer.

## Detailed Version

**The real trade-off between these two designs: the brush raft takes more time and material to build but handles more weight and is genuinely more resistant to tearing, while the Australian poncho raft is faster when time is short but has a hard, real 77-pound capacity limit.** Picking the right one depends on how much time you actually have versus how much gear genuinely needs to cross dry.
""",
    },
    {
        "title": "Log Rafts & Flotation Devices",
        "section": "reference",
        "tags": ["water-crossing", "flotation", "survival-skills"],
        "risk_level": "moderate",
        "body_markdown": """## Log Raft

**Built from dry, dead, or standing trees — spruce makes an especially good raft in polar/subpolar regions.** A real, simple method: lash pressure bars securely across each end of a row of logs to hold them together as a unit.

## Real Flotation Device Options (for warm water, when there's no time/material for a raft)

- **Trousers:** knot each pant leg at the bottom and close the fly. Grasp the waistband at both sides and swing the trousers through the air to trap air in each leg, then quickly press the waistband sides together and hold it underwater so the trapped air can't escape — **this creates a real, functional pair of water wings.** **Wetting the trousers first helps trap air more effectively**, and may need repeating for a longer crossing.
- **Empty containers:** lash together gas cans, water jugs, ammo cans, or similar air-trapping containers as water wings — **this specific method is only reliable in slow-moving water.**
- **Plastic bags and ponchos:** fill 2+ plastic bags with air and tie them together at the openings. Separately, roll fresh green vegetation tightly inside a poncho to form a roll at least 8 inches thick, tying the ends securely — **wear it around the waist, or across one shoulder and under the opposite arm.**
- **Logs:** a stranded driftwood log, or one found near the water, works as a simple float — **test it before committing to cross; some wood (palm, for instance) sinks even when fully dead.** A real variant: **tie 2 logs about 24 inches apart and sit between them, back against one, legs over the other.**
- **Cattails:** gather stalks into a bundle at least 10 inches thick — **the many internal air cells in each stalk keep it floating until it eventually rots.** **Test the bundle's buoyancy before trusting your full weight to it.**

**⚠️ Whatever improvised device you build, test it in the water before actually relying on it to cross** — this single step applies to every option above without exception.

## Detailed Version

**The real, unifying principle across every flotation option here: none of them need to be purpose-built gear — ordinary clothing, trash, plant material, and deadwood all genuinely work, provided the real physics (trapped air, or air cells, or simple wood buoyancy) actually applies and gets tested before you depend on it.** The improvisation itself isn't the risky part; skipping the test before committing your full weight to an untested device is.
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
                "source_url": ATP_SURVIVAL_PDF_URL,
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
