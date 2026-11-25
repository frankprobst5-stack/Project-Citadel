#!/usr/bin/env python3
"""Seeds 4 real pages from the USMC Winter Survival Course Handbook's
Traps and Snares chapter -- mined from the real text layer already
extracted in this session (/tmp/usmcwinter.txt, pages 08-1 through
08-12 roughly). A genuinely detailed real food-procurement chapter,
civilian-applicable for food-security purposes in a prolonged
disaster scenario.

Covers: the real 8 general considerations for taking game, real
snare construction/sizing technique including a real species-specific
noose-size/ground-clearance table and a real by-species location
guide, real improvised trap trigger mechanisms, and a noise-producing
early-warning path guard for a shelter area.

The source's "casualty producing path guard" sub-section (an
anti-personnel deadfall trap explicitly designed to kill/injure a
human enemy combatant) is deliberately excluded -- it is a weaponized
device, not survival/food-procurement technique, and out of place in
a civilian disaster-prep wiki.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_traps_snares.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Trapping & Snaring — General Principles",
        "section": "reference",
        "tags": ["trapping", "snaring", "food-procurement", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**8 real, general considerations make trapping meaningfully more effective — most failures trace back to skipping one of these, not to the trap design itself.**

## The 8 Real Considerations

1. **Know your game.** Understanding when/where a specific animal moves, feeds, and drinks tells you where a set will actually work.
2. **Keep it simple.** A survival situation doesn't allow time for elaborate sets, and elaborate doesn't mean more effective anyway.
3. **Placement matters more than clever design.** Animals travel and pause in predictable locations — that's where sets belong.
4. **Control your scent.** Animals avoid a set that smells threatening or simply unfamiliar (human scent, equipment residue). **Human skin sheds scent continuously through sweat — an odorless glove while building a set helps; without one, your scent can take up to 3 days to fully dissipate from the area.** Boot soles and clothing can also leave a detectable scent — masking it with smoke from your fire can help if you notice it.
5. **Match the set type to the animal** — certain set designs genuinely work better for specific species than others.
6. **Use correctly sized equipment** — the lifting device's weight relative to the animal's weight, cordage/wire strength for that animal's actual strength, and correct trigger tension all matter.
7. **Check every set twice daily (morning and evening).** Checking less often risks the animal escaping, decomposing, or being taken by a predator before you get there.
8. **Use a lure appropriate to the season and target species** — real options include:
   - **Bait lures:** a food-packet spread (peanut butter, cheese, jelly), a dead carcass, or a dead rodent.
   - **Gland/territorial lures:** animal urine mixed with castor or gland secretions.
   - **Curiosity lures:** a single feather, bird wing, or piece of fur tied so it moves freely in the breeze under a tree limb — pure visual curiosity, no scent needed.

## Detailed Version

**The real, most commonly overlooked item on this list is scent control — it's easy to focus entirely on trap mechanism and placement while ignoring that your own presence while building the set can render an otherwise well-placed trap useless for days.** This is exactly why it gets its own dedicated consideration rather than being treated as a minor detail of placement.
""",
    },
    {
        "title": "Snare Construction & Species-Specific Sizing",
        "section": "reference",
        "tags": ["snaring", "food-procurement", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**A snare is simply a loop of wire, rope, or cord that tightens around an animal's neck — genuinely simpler and faster to build than a trap, while often producing better real results.** In a winter environment specifically, **snaring is considered the most effective overall method of taking game.**

## Wire Selection

**Wire outperforms rope/cord.** Look for wire with real "memory" (it resists kinking) — **aircraft cable, type 7x7, in 1/16 to 3/8 inch sizes, resists both chew-out and breakage.** Use the smallest diameter that can still actually hold your target animal — oversized cable wastes material and can be harder to set properly.

## The Locking Device

**A functioning locking device is essential — without one, the snare simply won't hold.** Real options include a commercial lock, a bent-washer lock, or a tied-knot lock, depending on what materials are actually available.

## The 3 Real Requirements for Effective Snaring

### 1. Location — By Species (a real field guide)

| Animal | Where to set |
|---|---|
| Coyotes, foxes, badger | Rarely-traveled roads, fire lanes, irrigation ditches, fence lines, saddles, ridge tops, meadow borders, near carcasses |
| Bobcat, lynx | Bases of cliffs/rock faces, ridge/saddle crossings, stream bottoms — cats stay close to cover |
| Raccoon, opossum, skunk, ring-tailed cat | Streambeds/banks, trails along water, areas combining water + mature trees + structures + a reliable food source |
| Weasel | Marshy, grassy meadows |
| Marten, fisher | Meadow edges, ridgelines, downfalls |
| Mink | Under bridges, around culverts/debris near streams/lakes/springs — mink investigate nearly every hole/cavity near water |
| Beaver, muskrat | Around the food cache, under the ice |
| Rabbits | Thick willow stands along their runs/trails |

### 2. Presentation (the real set type for the target animal)

**Cubbie sets** work well for bobcat, raccoon, marten, fisher, opossum, and skunk. **Trail sets** work well for coyote, fox, mink, and rabbit.

### 3. Construction

- **A split stick supports and fires the snare correctly** — green or seasoned wood both work, but the snare must not be able to slip through the split, and the locking device sits right next to the split stick. Secure the split stick firmly in the ground (a weighted-snare variant can position the lock at the 12 o'clock point instead).
- **Anchor the snare, or attach it to a drag** — an un-anchored snare the animal simply carries away defeats the purpose.
- **Load the snare so it fires quickly** once triggered.
- **Get the loop size and ground clearance right — this is the single most important sizing decision:**

| Animal | Noose size (loop diameter) | Ground clearance |
|---|---|---|
| Squirrel | 2.5–3 inches | 0.5–1.5 inches |
| Rabbit | 4–5.5 inches | 1.5–3 inches |
| Raccoon | 6 inches | 3–4 inches |
| Fox | 7–10 inches | 8–10 inches |
| Coyote | 12–14 inches | 12 inches |
| Bobcat | 9 inches | 8 inches |

**Too large a loop risks a body/leg catch (chew-out or breakage risk); too small lets the animal push the snare aside entirely and miss the catch.** The real target: the loop's bottom edge should hit the animal roughly chest-high — that exact point is the snare's real "trigger."

- **Fencing** (light brush/debris guiding the animal) should subtly funnel the animal along the path of least resistance — directly through the snare — without being obvious or overdone.
- **Lure helps, but isn't required for trail sets** — in a real survival situation, you likely can't maintain many snares at once, so luring the few you do set meaningfully improves your odds.

## Detailed Version

**The real, easy-to-get-wrong detail on this whole page is loop sizing — both too large and too small fail in different ways (chew-out vs. a clean miss), and the fix for each is opposite.** This is exactly why a real species-specific sizing table matters more than a generic "make it big enough" rule of thumb.
""",
    },
    {
        "title": "Improvised Traps — Triggers & Mechanisms",
        "section": "reference",
        "tags": ["trapping", "food-procurement", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**"SICK" is a real, useful way to remember the 4 real mechanisms by which a trap actually kills or holds an animal** — knowing which mechanism a given design uses tells you what it's actually suited for.

## SICK — the 4 Real Kill Mechanisms

- **S — Strangle** (a snare).
- **I — Impale** (a spiked deadfall that drives a stake through the animal).
- **C — Crush** (a deadfall sized for a small animal, like a chipmunk).
- **K — Knock** (a deadfall sized to knock a larger animal unconscious).

## 2 Real Basic Trigger Types (with real variations)

### Toggle / Spring Pole

**Needs:** a small sapling and cordage. **Designed to lift the animal off the ground once triggered — this specifically prevents predators from stealing your catch before you can retrieve it.** **⚠️ The trigger tension must be calibrated so the intended animal can actually set it off** — too tight and it never fires. **Real cold-weather caveat: a spring pole can freeze in position**, which defeats the whole mechanism — worth checking on in genuinely cold conditions.

### Inverted Figure-4

A different real trigger geometry, used both for standalone traps and (see the path-guard page) as an alarm trigger.

## Real Trap Constructions Using These Triggers

- **Weighted lift pole** — built the same way as the spring pole (sapling + cordage), using a toggle-style trigger, with the same real goal: lift the catch off the ground to protect it from predators, and the same real caution about trigger tension not being set too tight for the target animal to trip it.
- **Baited treble hook** — tie a large treble hook to a tree limb at a height that makes the animal jump for it but still lets it reach — then bait the hook itself.

## Detailed Version

**The real, shared design goal across both the spring pole and weighted lift pole: getting the catch physically off the ground isn't about the kill itself — it's protecting your food source from being taken by something else before you can check your set.** This is exactly why both constructions exist as lift variants rather than simple ground-level holds, and why checking sets twice daily (see Trapping & Snaring — General Principles) still matters even with a lift mechanism in place.
""",
    },
    {
        "title": "Noise-Producing Path Guards — Early Warning for a Camp",
        "section": "reference",
        "tags": ["camp-security", "early-warning", "survival-skills"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**A simple, field-expedient trip-alarm can give real early warning of an approaching predatory animal (or any unwanted visitor) near a shelter or camp area — no electronics required.**

## Real Construction

1. **Secure an inverted figure-4 trigger to a tree.**
2. **Attach several pieces of metal to a cord on the trigger's weighted end** — use whatever metal is actually available (cans, hardware, scrap).
3. **Run a trip cord from the trigger stick across the approach path**, anchored on the far side so it's taut enough to actually trip when disturbed.
4. **Place a solid object (wood, rocks) directly under the suspended metal.** When the trigger fires, the metal falls onto the solid object, **producing an audible noise** that alerts whoever's in camp.

## Detailed Version

**The real value of this device is that it converts an undetected approach into an audible event — giving people time to react before whatever triggered it is actually at the camp itself.** Positioning matters as much as construction: a trip line placed along the single most likely approach route is far more useful than one placed where nothing is likely to walk.
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
