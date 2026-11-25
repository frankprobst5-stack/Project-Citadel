#!/usr/bin/env python3
"""Seeds 3 real pages from the USMC Winter Survival Course Handbook's
Expedient Snowshoes chapter -- mined from the real text layer already
extracted in this session (/tmp/usmcwinter.txt, pages 12-1 through
12-8). Real construction and technique for genuinely effective
no-equipment winter mobility.

Covers: real advantages/disadvantages and the real characteristics
that make an expedient snowshoe actually work, 2 real construction
methods (the standard lashed-frame design and the lower-cordage
Canadian emergency variant), and real snowshoeing technique --
walking, turning on steep terrain, and crossing obstacles safely.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_snowshoes.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Expedient Snowshoes — When & Why They Help",
        "section": "reference",
        "tags": ["snowshoes", "cold-weather", "bushcraft"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Expedient snowshoes exist to do one real job: provide flotation so you can move over snow without exhausting yourself "post-holing"** (sinking through the surface with every step) — but they come with real, specific trade-offs worth weighing before committing the material to build them.

## Real Advantages

- **Mobility** — real over-the-snow flotation.
- **Low maintenance** once built.
- **Genuinely good for hauling/carrying heavy loads on gentle terrain.**
- **Easy movement in confined areas**, around gear and obstacles.

## Real Disadvantages

- **Material-hungry** — building just one shoe takes roughly 70 feet of cordage. That's a real, meaningful resource cost in a survival kit.
- **Steep-to-moderate slopes are genuinely difficult** to navigate in them.
- **Dense forest or terrain with branches poking through snow is hard going.**
- **Green wood staves shrink as they dry** — expect to re-tie all the lashing after the frame dries out.

## Real Nomenclature

- **Tip/tail** — the front/rear of the frame.
- **Crossbars** — 3 lashed across the frame for structural reinforcement.
- **Webbing** — the cord/wire lattice that actually provides flotation and sheds snow when the shoe lifts.
- **Window** — the gap that lets your boot's toe pivot freely; without it, the boot drags the tip down into the snow with every forward step.
- **Frame** — built from resilient green saplings (willow, aspen).
- **Binding** — an 8-10 foot cord that attaches the boot to the shoe.

## The Real Critical Characteristic: Stability

**Stability matters more than any other design factor** — a snowshoe genuinely has to withstand real, repeated strain and pressure, which makes material selection the single most important decision. Real options beyond green saplings: aluminum aircraft skin/ribbed framing, cordage, wire, cargo strapping — **whatever's actually available and strong enough.**

## Detailed Version

**The real decision this page sets up: building expedient snowshoes is a genuine investment of scarce cordage, and the trade-off is explicit — real flotation and energy savings on moderate terrain, against real difficulty on steep slopes or dense forest, and the certainty that you'll need to retie everything once the green wood dries.** Deciding whether that trade-off is worth it for your actual terrain and situation is the first real question, before any construction begins.
""",
    },
    {
        "title": "Building Expedient Snowshoes — Construction",
        "section": "reference",
        "tags": ["snowshoes", "bushcraft", "cold-weather"],
        "risk_level": None,
        "body_markdown": """## Standard Construction (needs thick staves and real cordage)

1. **Select 3 straight, resilient green staves — 5 feet long, 1-1.5 inches diameter.** Cut one of the three into three 15-inch sections.
2. **Join the two 5-foot staves at both tip and tail using a shear lash** — this forms the snowshoe's main frame.
3. **Attach the three 15-inch sections as crossbars**, secured with a square lash: the first 12-14 inches from the tip, the second 4-6 inches below that, the third 15 inches below the second.
4. **Weave the latticework (webbing)** from the first crossbar toward the tip, and a second section from the second crossbar toward the tail. **If cord/wire is limited, space the lattice out and interweave branches or boughs to add flotation** instead of denser cordage.
5. **Attach the boot using the cord binding system** — secure all loose cord ends ("pigtails") with a square knot backed by two overhand knots.

## Canadian Emergency Snowshoe (works well with limited cordage, if saplings are available)

1. **Select 5 poles per shoe**, roughly your own height (~6 feet), about ¾ inch thick (thumb-sized) at the base, tapering to ¼ inch (little-finger-sized) at the tip.
2. **Cut 5 cross-sticks, about 10 inches long and ¾ inch wide, per shoe**, and lash them as follows:
   - One stick across the heavy (tail) end of the 5 poles.
   - 2 sticks positioned where the heel will rest.
   - 2 sticks positioned where the toe will rest.
3. **Secure all 5 pole tips together** at the front.
4. **Attach the boot with the same cord binding system** used on the standard design.

## Detailed Version

**The real trade-off between these two designs: the standard shear-lashed frame produces better real flotation but costs significantly more cordage, while the Canadian emergency design trades some flotation performance for a design that works when cordage — not wood — is your actual scarce resource.** Choosing between them is a real materials-availability decision, not a matter of one being universally "better."
""",
    },
    {
        "title": "Snowshoeing Technique — Walking, Turning & Crossing Obstacles",
        "section": "reference",
        "tags": ["snowshoes", "cold-weather", "survival-skills"],
        "risk_level": "moderate",
        "body_markdown": """## Real Walking Technique

**Snowshoeing is genuinely close to normal walking** — the real differences are an inconsistent walking surface and longer, wider, heavier footwear. **Walk relaxed, with a normal rolling-toe stride, lifting the snowshoe just high enough to clear the snow surface** — over-lifting wastes real energy over distance.

## Real Turning Technique

**Kick turn** (the easiest way to change direction on level ground): swing one snowshoe forward so its tail rests on the snow, then let it pivot toward the new direction; bring the other snowshoe around to match.

**⚠️ On steep terrain, the kick turn needs real care:**
- **Step off with your uphill foot** when turning. (Example, turning right: shift weight to your left foot, face downslope, swing the right snowshoe to point toward your next switchback direction, stamp it into the snow — making sure its tail doesn't land on your left snowshoe — then shift weight onto the right foot and bring the left snowshoe around parallel to it.)
- **When traveling as a group, each person should place their snowshoes exactly where the person ahead placed theirs.** A turn cut into a slope undermines the snow beneath it — each subsequent person sloughs more of it off, and people near the back of the line can find the turn genuinely degraded if everyone doesn't track precisely.

**Star turn** — a simpler alternative: a series of small half-facing pivots to change direction incrementally.

**Route choice while climbing:** plan turns for the gentlest spots on a slope, and don't hesitate to use short switchbacks rather than forcing a direct, steep line.

## Side Step & Herringbone

- **Side step** — for a critically steep slope angle.
- **Herringbone** — for a more gradual slope angle.

## Real Rules for Crossing Obstacles

1. **Always step over an obstacle** rather than around or through it — this protects the snowshoe frame and your own balance.
2. **⚠️ Never bridge a gap** (where only the shoe's tip and tail are supported, with its center suspended over open space) — this stresses and risks breaking the frame.
3. **Shallow snow risk:** webbing can catch and tear on stumps or snags that are only barely covered.
4. **Wet snow risk:** it tends to ball up under the feet, making walking genuinely uncomfortable — knock it off as soon as you notice it building up.
5. **Deep, loose, untracked snow is genuinely exhausting** — if traveling as a group, **rotate who's breaking trail frequently** rather than letting one person exhaust themselves the whole way.

## Detailed Version

**The real safety principle underlying the group-turn guidance and trail-breaking rotation: individual effort and individual technique aren't the whole story in a group setting — a turn's structural integrity and a group's collective energy both depend on everyone following the same disciplined pattern, not just on any one person's skill.**
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
