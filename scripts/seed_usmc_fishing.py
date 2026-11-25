#!/usr/bin/env python3
"""Seeds 4 real pages from the USMC Winter Survival Course Handbook's
Survival Fishing chapter -- mined from the real text layer already
extracted in this session (/tmp/usmcwinter.txt, pages 10-1 through
10-10). Real food-procurement technique, genuinely applicable to any
extended disaster scenario near water, not just winter/mountain
settings.

Covers: real winter fishing challenges and bait-finding technique,
expedient hook construction, real ice-fishing tool construction (ice
spud, ice skimmer) and technique, real unattended set-line technique
(tippets, frozen-river set lines, standard set lines), and real
fish-cleaning/cooking technique.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_fishing.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Survival Fishing — Locations & Expedient Hooks",
        "section": "reference",
        "tags": ["fishing", "food-procurement", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Fish are usually an abundant real food source in mountainous terrain — and even the scraps left over after cleaning one make excellent lure material for your traps and snares** (see Trapping & Snaring — General Principles).

## Real Winter Fishing Challenges

- **Cold water carries less dissolved oxygen, which slows fish activity** — expect less aggressive bites.
- **Reaching water through deep snow or ice is itself a real hazard.**
- **Winter requires adapted technique**, not just the same summer approach in colder conditions.
- **Bait is genuinely harder to find in winter.** Real ways to locate it anyway:
  - Look for **galls** — abnormal swollen growths on plant tissue caused by insects living inside.
  - **Watch where birds are actively pecking at tree bark** — that often marks where insects are hiding underneath.
  - **Once you catch your first fish, its eye or first dorsal fin makes excellent bait for the next one** — a real way to bootstrap bait supply from a single catch.

## Real Fishing Locations in Mountain Streams

**A hand line is generally the best method for mountain-stream fishing.** As snow/ice conditions allow, prioritize real structural fishing spots: areas where current slows, pools below faster water, undercut banks, and similar natural holding spots where fish actually congregate rather than fighting current.

## Expedient Hooks — When You Don't Have Enough

**Always carry real hooks in a kit, but know how to make more if needed.** **One-piece hooks generally outperform two-piece designs.** Expedient hooks are shaped specifically to lodge in a fish's throat once swallowed, rather than simply piercing the lip — carved from bone, wood, or bent wire/metal depending on what's actually available.

## Detailed Version

**The real, repeated theme across bait-finding and hook design: a survival fisherman has to bootstrap resources from very little — the first fish caught supplies bait for the next, and a single hook design decision (barbed to lodge in the throat) maximizes the odds of actually landing each strike** rather than losing fish to a hook that slips free.
""",
    },
    {
        "title": "Ice Fishing — Tools & Technique",
        "section": "reference",
        "tags": ["ice-fishing", "food-procurement", "cold-weather"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Fish stay alive and active under ice all winter — the real challenge is simply getting through the ice to reach them**, safely.

## Building an Ice Spud (to chip through the ice)

**⚠️ This is one of the only situations where lashing a fixed-blade knife to a pole is appropriate — build it carefully to avoid accidentally losing the knife into the water.**

1. Cut a sturdy pole, about 4-5 feet long.
2. Cut a notch into the heavy end for the knife blade to seat into.
3. Fire-harden the notch if using green wood.
4. Lash the knife securely into the notch, and **dummy-cord the knife itself to the pole's upper third** — this keeps the blade attached to you even if the lashing fails or the pole breaks.
5. Attach a wrist loop to the pole's upper third as well.
6. **To use:** loop your wrist through the dummy cord, then chip at the ice until you reach water. **The knife's dummy cord prevents losing the blade if the lashing gives way; the wrist loop prevents losing the whole pole once you finally break through.**

## Building an Ice Skimmer (to clear ice chips from the hole)

1. Cut a small sapling shaft, about 2 feet long, smoothed of notches.
2. Cut a thin flat piece of wood (roughly 1-2 inches thick, 4-5 inches square).
3. **Coal-burn the flat piece** until about ½ inch of wood remains on the bottom.
4. Awl several holes through the coal-burned piece so water can drain through while it scoops out floating ice.
5. Bore a hole through one end and slide the shaft through it.

## Real Ice Fishing Technique

**⚠️ Confirm the ice is actually stable before moving onto it** — see Ice Safety — Formation, Strength & Crossing for how to judge this.

1. Chip a hole roughly 12-14 inches in diameter with the ice spud, making sure every component stays securely fastened as you work.
2. Clear floating ice from the hole with the skimmer.
3. **If hand-lining, reel the line in using two sticks rather than your bare hands or mittens** — this real technique avoids prolonged hand contact with wet/cold line, which is a genuine frostbite risk.

## Detailed Version

**The real engineering logic behind the ice spud's double-redundancy (knife dummy-cord plus wrist loop): losing either the knife or the pole through a freshly cut hole in the ice is a realistic, specific failure mode this design is built to prevent** — not a hypothetical worry, but the exact predictable way this tool fails if built without those two safeguards.
""",
    },
    {
        "title": "Fishing Set Lines — Catching Fish While You Work",
        "section": "reference",
        "tags": ["fishing", "set-lines", "food-procurement"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**A set line lets you keep "fishing" passively while doing other survival tasks or riding out bad weather** — a genuinely efficient way to conserve your own energy while still working toward food. Bait several hooks and leave them out overnight, positioned either on the bottom or suspended, until you learn where fish are actually feeding.

## Tippet Sets (multiple holes through ice)

**A tippet increases your odds by running several set lines through separate holes at once.**

1. Cut a green bough large enough that a fish can't pull it through the ice hole.
2. **Double-hook every line.**
3. **Position the bottom hook roughly 12 inches off the lake/river bottom.**
4. Place the tippet (the bough) into a small loose snow mound at the hole, anchoring the whole set.

## Frozen River Set Lines (for snow/ice-covered rivers)

1. **Confirm the snow/ice covering is actually stable** before working on it.
2. Cut a hole through with an ice spud.
3. Cut and sharpen one end of a long, sturdy pole.
4. Attach a line with several baited hooks to the pole.
5. **Submerge the baited line through the hole, then drive the pole's sharpened end into the riverbed** to anchor the whole set firmly in place.

## Standard Set Lines

A simpler baited-line set, anchored and left unattended, for open (non-iced) water.

## Detailed Version

**The real value of any set line, regardless of variant, is converting fishing from an active, time-consuming task into a passive, background one** — you can be building shelter, gathering firewood, or resting while a set line keeps working on your behalf, which matters enormously when your actual time and energy are the scarcest resources in a survival situation.
""",
    },
    {
        "title": "Preparing & Cooking Fish",
        "section": "reference",
        "tags": ["fishing", "food-safety", "food-procurement"],
        "risk_level": "high",
        "body_markdown": """## Cleaning Fish — Real Technique

1. **If the fish has scales**, scrape them off with a knife, working back and forth from tail to head.
2. Cut the fish open starting at the anus, working forward toward the gills.
3. **Push the guts out with your finger/thumb and wash thoroughly.** **Real, useful bonus step: check the intestines for undigested food — this tells you what the fish was actually eating, which you can then use as bait for your next catch.**
4. **Skin and head are usually left on.**

## ⚠️ Cooking Fish — a Real Parasite Safety Issue

**Fish meat commonly carries parasites — heat is what actually destroys them, so thorough cooking isn't optional.**

1. Cut the fish into pieces sized to fit your cooking container.
2. **Boil until thoroughly done** — this is the real preferred method.
3. **Roasting is possible, but wastes valuable fat that escapes into the fire** rather than being captured and consumed, same real trade-off as with game meat (see Cooking Game Safely).

## Detailed Version

**The real, easy-to-overlook value in checking a cleaned fish's gut contents: it's a free, real source of local intelligence about what bait is actually working in that specific water, right now** — information that's otherwise only discoverable through trial and error, extracted here as a genuine side benefit of a step you're already doing anyway.
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
