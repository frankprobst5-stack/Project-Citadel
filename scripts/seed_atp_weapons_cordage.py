#!/usr/bin/env python3
"""Seeds 4 real pages from ATP 3-50.21 (Survival), Chapter 8
(Survival Equipment) -- mined from the real text layer already
extracted in this session (/tmp/atp_survival.txt, pages 8-1 through
8-10). This chapter's basic edged-weapon material content (stone/
bone/wood/metal blade-making, simple clubs) substantially duplicates
the USMC Field Expedient Materials content already in this wiki --
skipped here. Mined selectively for genuinely new real content: a
real walking staff, 2 more real club variants, real spear
construction, real throwing-stick throwing TECHNIQUE (not just the
stick itself), a complete real bow-and-arrow construction (including
a real double-bow trick for more pull), 3 more weapon types not
covered anywhere in this wiki (bola, sling, sapp), and real sinew/
inner-bark lashing material processing.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_atp_weapons_cordage.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Weighted Clubs, Spears & Throwing Sticks",
        "section": "reference",
        "tags": ["field-expedient-weapons", "bushcraft", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Before building anything, apply a real improvising discipline: is the item actually necessary, or just nice to have?** Inventory what you actually have, weigh every real alternative, and build only what genuinely earns its cost in material, time, and energy.

## A Walking Staff — the Real First Tool to Get

**Should be one of the very first tools obtained.** Real uses beyond walking support (ascending/descending slopes): real self-defense against snakes and dogs via thrusting, striking, and blocking, and genuine eye protection pushing through heavy brush/thorns in the dark. **Size it to your own height, or at least eyebrow height — and no larger than you could actually wield while exhausted and undernourished.**

## Weighted Club — a Real Upgrade Over a Simple Club

**A simple club (any straight-grained hardwood branch, sized to swing easily but strike hard) becomes a weighted club by lashing a stone to one end.** Find a stone with a natural hourglass shape for easy lashing — if none is available, peck a groove into a stone by repeatedly striking it with a smaller, harder stone. Match the handle's length to feel balanced against the stone's actual weight, then lash the stone securely to the handle.

## Sling Club — a Real Reach-and-Force Multiplier

**A weight hangs 3-4 inches from the handle on a strong, flexible lashing** (rather than being rigidly fixed) — this real design both extends your reach and genuinely multiplies the force of each blow compared to a simple weighted club.

## Real Spear Construction

**With a blade:** make the blade using the same real stone/bone/wood/metal technique as a knife blade, then attach it to a 4-5 foot straight sapling shaft. **The preferred real method: split the shaft's end, insert the blade, then wrap/lash it tightly** rather than just binding it to the outside.

**Without a blade:** select a 4-5 foot straight hardwood shaft, shave one end to a point, and fire-harden it if a fire is available. **Bamboo makes a genuinely excellent spear:** starting 3-4 inches back from the tip, shave the end at a 45-degree angle — **shave only the inner portion, since bamboo's outer layer is its hardest, strongest part and should be preserved.**

## Throwing Stick (Rabbit Stick) — Real Throwing Technique, Not Just Construction

**Genuinely effective against small game** (squirrels, chipmunks, rabbits) — but **real accuracy and speed require practiced technique, not just a good stick.**

**Construction:** select a heavy hardwood (oak works well) stick with a natural ~45-degree curve, then shave two opposite sides flat so it resembles a boomerang.

**Real throwing technique:**
1. Align your aim by extending your non-throwing arm toward the target's mid-to-lower section.
2. Slowly, repeatedly raise your throwing arm up and back until the stick crosses your back at roughly a 45-degree angle, or lines up with your non-throwing hip.
3. Bring the throwing arm forward until it's slightly above and parallel to your non-throwing arm — **this is the real release point.**
4. **Practice this motion repeatedly** — accuracy comes from the throwing mechanics, not the stick's shape alone.

## Detailed Version

**The real, repeated lesson across the sling club and throwing stick: real mechanical advantage (a flexible-mounted weight; a specific release-point throwing motion) often matters more than the raw material the weapon is made from.** A well-practiced throwing stick or a properly built sling club outperforms a cruder version of the same tool used without the real technique behind it.
""",
    },
    {
        "title": "Making a Bow & Arrows",
        "section": "reference",
        "tags": ["archery", "bushcraft", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Building a working bow and arrow is genuinely achievable with basic tools and dry hardwood — but real accuracy takes considerable practice beyond just building the equipment correctly.**

## Real Bow Construction

1. **Select a hardwood stick about 3 feet long, free of knots or limbs.** Dead, dry wood is genuinely preferable to green wood.
2. **Scrape the large end down until its pull matches the small end's pull** — examine the stick's natural curve carefully first. **⚠️ Always scrape from the side facing you** — scraping the wrong side causes the bow to break the first time it's drawn.
3. **Real trick to increase pull: lash a second bow to the first, front-to-front, forming an "X" shape when viewed from the side.** Attach both bows' tips together with cordage, but string only ONE of the two bows with the actual bowstring.

## Real Arrow Construction

1. **Select the straightest dry sticks available** — each arrow should be about half the bow's length.
2. Scrape each shaft smooth all around. **If a shaft isn't straight, heat it over hot coals to bend it true — being careful never to scorch or burn it — and hold it straight until it cools.**
3. **Real arrowhead materials: bone, glass, metal, or stone** — or simply sharpen and fire-harden the shaft's own end instead of adding a separate head.
4. **⚠️ "Fire hardening" is actually a real misnomer** — the true purpose is drying moisture OUT of the wood, not heat-treating it chemically. Hold the shaft over hot coals, or bury it in the ashes beneath them, taking care not to burn or scorch it.
5. **Notch the arrow's rear end for the bowstring by cutting or filing — never by splitting it**, which weakens the shaft.
6. **Fletching (feathers at the notched end) genuinely improves flight — recommended, though not strictly required** on a field-expedient arrow.

## Real Arrow Points (Beyond the Fire-Hardened Shaft Itself)

**Made with the same real technique as a stone knife blade** (see Field Expedient Materials — Stone, Bone, Wood & Metal). **Chert, obsidian, flint, and shell-type stones work best; broken glass also makes a genuinely effective point.** Bone can be shaped the same way as stone, by flaking.

## Detailed Version

**The real, clever engineering trick worth remembering from this whole page: the double-bow lashing technique lets a single, imperfect field-made bow stave gain real extra pull by borrowing a second stave's strength — without needing a longer, harder-to-source single piece of wood.** This is a genuinely field-practical workaround for the real limitation of improvised bow-making: finding one piece of wood strong enough on its own.
""",
    },
    {
        "title": "Bola, Sling, Slingshot & Sapp",
        "section": "reference",
        "tags": ["field-expedient-weapons", "hunting", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Bola — Real Technique for Catching Running Game or a Flock

**Especially effective against running game or low-flying birds in a flock.** Hold it by its center knot, twirl it overhead, then release toward the target. **As it flies, the weighted cords separate and wrap around whatever they strike, immobilizing the animal/bird.**

## Sling — a Different Real Tool From a Slingshot

**Needed:** 2 cords, each about 24 inches (60cm) long, tied to opposite ends of a palm-sized piece of leather or cloth.

**To use:** place a rock in the cloth cradle, wrap one cord around your middle finger and hold it in your palm, and hold the other cord between your forefinger and thumb. **Spin the sling in a circle several times, then release the cord held between thumb and forefinger** to launch the rock. **Genuinely effective against small game, but — like the throwing stick — needs real practice to use accurately.**

## Slingshot — the Familiar Y-Branch Design

**Find a Y-shaped green branch, tie surgical tubing to each tip of the Y, and tie a small piece of material (the ammo pouch) to the tubing's other ends.** Small rocks work as ammunition.

## Sapp — a Real Improvised Impact Weapon

**Fill a sock partway with rocks or other heavy material** (metal scraps, batteries, a lock — whatever's dense and available), then **use it exactly like a weighted club.**

## Detailed Version

**The real, easy-to-confuse distinction worth keeping straight: a "sling" (a cradle on two cords, thrown like David's weapon) and a "slingshot" (a Y-frame with elastic) are genuinely different tools with different real throwing mechanics — despite the similar name, mastering one doesn't transfer directly to the other.**
""",
    },
    {
        "title": "Natural Cordage — Sinew & Inner Bark Lashing",
        "section": "reference",
        "tags": ["cordage", "bushcraft", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Beyond spun plant fiber (already covered in Making Rope — Fiber Types, Twisting & Braiding), 2 more real, genuinely strong natural cordage sources are worth knowing: sinew and inner tree bark.**

## Real Cordage Strength Test (Before Trusting Any Material)

1. Pull on a length of the material to test raw strength.
2. Twist it between your fingers, rolling the fibers together — **if it survives this handling without snapping, continue.**
3. Tie an overhand knot in it and gently tighten. **If the knot holds without breaking, the material genuinely works as cordage.**

## Sinew — the Real Best Natural Material for Small Lashings

**Obtained from the tendons of large game** (deer and similar). **Real processing steps:**
1. Remove the tendons from the animal and dry them completely.
2. Smash the dried tendons to separate them into individual fibers.
3. Moisten the fibers and twist them into one continuous strand.
4. **For stronger lashing, braid multiple strands together.**

**⚠️ A real, genuinely useful property: moistened sinew is naturally sticky and hardens as it dries — small sinew lashings don't even need a knot**, since the material bonds and sets on its own.

## Inner Bark — a Real Alternative Cordage Source

**Real species that work well:** linden, elm, hickory, white oak, mulberry, chestnut, and red/white cedar. **Always run the real strength test above before trusting any batch** — inner bark cord quality can vary by species and individual tree. **Braiding multiple strands together increases real strength**, the same way it does for sinew or spun plant fiber.

## Detailed Version

**The real, practical reason sinew gets singled out as "the best" material for small lashings specifically: its self-bonding, no-knot-needed property is genuinely unique among natural cordage options** — every other material covered in this wiki (plant fiber, inner bark) still needs a real mechanical knot to hold, while dried sinew's own chemistry does that job instead.
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
