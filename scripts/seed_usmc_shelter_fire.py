#!/usr/bin/env python3
"""Seeds 4 real pages from the USMC Winter Survival Course Handbook's
Expedient Shelters and Fires chapter -- mined from the real text
layer already extracted in this session (/tmp/usmcwinter.txt, pages
04-1 through 04-17).

Covers: the real 6-criteria framework for any safe shelter, natural
shelter options and their real hazards, 7 real man-made snow shelter
construction techniques plus a real shelter-selection table (by snow
pack/depth), real fire-lay/fuel-gathering/fire-type technique, and
the complete real bow-and-drill primitive fire-starting method with
its own troubleshooting table.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_shelter_fire.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Expedient Shelter Basics — Criteria, Natural Hazards & Selection",
        "section": "reference",
        "tags": ["shelter", "survival-skills", "cold-weather"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Any shelter — a permanent building, a tent, or an improvised survival shelter — needs to meet the same 6 real criteria to actually be safe and effective.**

## The 6 Real Shelter Criteria

1. **Protection from the elements** — rain, snow, wind, sun.
2. **Free from natural hazards** — not built in avalanche-prone terrain, under rockfall paths, or under standing dead trees that could fall on it.
3. **Stable** — able to actually withstand real severe-weather forces, not just look adequate in calm conditions.
4. **Ventilated** — critical if burning fuel for heat (to prevent carbon monoxide buildup) and even just from normal breathing (carbon dioxide).
5. **Heat-retaining** — real insulation value that prevents wasting fuel trying to keep it warm.
6. **A drying capability** — somewhere to actually dry out wet clothing, which matters enormously for preventing cold-weather injury.

## Natural Shelters — Real Options and Real Hazards

**Caves/rock overhangs** and **hollow logs** take the least work — modify them by stacking rock/log/branch walls across open sides, or hanging a poncho/tarp/parachute panel across an opening.

**⚠️ Real hazards specific to natural shelters:**
- **Animals** — natural shelters may already be occupied (bears, coyotes, snakes, rodents), and animal scat/decaying carcasses carry real disease risk.
- **Poor ventilation** — a fire built inside for heat/cooking can become genuinely dangerous from smoke buildup in an enclosed natural space.
- **Gas pockets** — caves in mountainous terrain can contain natural gas pockets.
- **Instability** — a natural shelter can look solid and still be a real collapse risk.

## Choosing Which Shelter to Build — a Real Decision Table

| Snow condition | Snow depth | Est. hours to build | Recommended shelter |
|---|---|---|---|
| Loose | Under 2 feet | 2 | A-frame |
| Compacted | 4-6 feet | 2-3 | Snow coffin |
| Compacted | Over 6 feet | 3 | Snow cave |
| Iced | N/A | 2-3 | Snow trench |
| N/A | N/A | 1-2 | Fallen tree bivouac |
| N/A | Over 4 feet | 1-2 | Tree-pit shelter |
| N/A | Over 2 feet | 30 min | Snow wall |

## Real Construction Considerations (for any man-made shelter)

- **Group size** drives which shelter type is even practical.
- **A low silhouette and smaller interior volume improve heat retention** — bigger isn't better here.
- **Avoid** exposed hilltops, valley floors, moist ground, and avalanche paths.
- **Pack snow onto the roof/sides** where available — it adds real insulating value.
- **Build near firewood, water, and (if relevant) a good signaling location** — minimizing travel between your shelter and these resources matters over time.

## Detailed Version

**The real, easy-to-miss point tying all of this together: a shelter that fails even one of the 6 criteria can actively make a bad situation worse rather than better** — an unventilated shelter with a fire inside risks carbon monoxide poisoning, and an unstable one built on convenient-looking but hazardous ground risks collapse or avalanche burial. None of the 6 criteria is optional; a shelter that's warm but unventilated, or well-insulated but unstable, is not actually a safe shelter.
""",
    },
    {
        "title": "Building Snow Shelters — Snow Wall, Cave, Tree-Pit & More",
        "section": "reference",
        "tags": ["shelter", "snow-shelter", "cold-weather", "survival-skills"],
        "risk_level": "high",
        "body_markdown": """## Snow Wall (fastest, 1-2 people, ~30 min)

**The real go-to when weather won't allow time for anything more elaborate.** Determine wind direction, then build a horseshoe-shaped wall of compacted snow — at least 3 feet high and as long as your body — to block the wind. A poncho/tarp can be anchored along the top and staked to the ground for added cover; skis, poles, or branches add stability.

## Snow Cave (1-16 people, extended stays — needs 6+ feet of compacted snow)

1. **Dig down into the snow to your entrance depth, piling all excavated snow on top of the shelter** — this adds real structural strength.
2. Cut a roughly 3x3 foot entrance opening.
3. Continue excavating, shaping the roof into a dome. **⚠️ If the roof snow shows a bluish color when you look up through it, stop — that's a real sign there isn't enough snow left to support the roof safely.**
4. Carve a cooking/working shelf and a raised sleeping bench inside (sleeping above the entry level keeps you in warmer air, since cold air sinks).
5. **Dig a ventilation hole through the roof at a 45-degree angle, above the entrance** — leave a ski pole or branch in it so you can clear it if it clogs, and place a pine bough over the outside opening to keep falling snow from blocking it.
6. **Anyone digging will sweat from the exertion — dress in minimal layers with just a protective outer shell while digging**, to avoid soaking your insulating layers.
7. Once dug, pack the entrance shut with snow blocks and let it harden 2-3 hours before cutting a small entrance back open.
8. **A candle can raise the inside temperature roughly 2°F — but if left burning while people sleep, post a fire watch to prevent asphyxiation. Never use a burning stove to heat a snow cave — it melts the snow structure itself.**
9. **⚠️ Post a lookout/safety watch any time the cave is occupied, day or night, in case of collapse.**

## Tree-Pit Snow Shelter (1-3 people, short-term, needs 4+ feet of snow)

Find a tree with low, bushy branches for overhead cover, then dig out the snow around its trunk to your desired depth/diameter. **Cut evergreen boughs from OTHER trees (not the one you're sheltering under) to add over the top for extra concealment/cover**, and line the bottom of the pit with boughs for ground insulation.

## Fallen Tree Bivouac (fastest real-terrain option — most of the work is already done)

**Confirm the fallen tree is actually stable before using it.** Cut away branches on the underside to create a hollow space beneath, pile extra insulating material on top and sides, and build any fire outside the shelter, not under it.

## A-Frame Shelter (1-3 people)

Build a basic A-frame structure, weave pine boughs/tentage material onto the frame, then pack snow over the outside for insulation.

## Snow Trench (short-term, for hard-packed/iced terrain with no trees — e.g. alpine/glacier environments)

Built from cut blocks of snow or ice where loose snow or wood simply isn't available.

## Snow Coffin (1-4 people, extended stays, needs 4+ feet of compacted snow — a snow-trench/A-frame hybrid)

Dig a trench roughly 3 feet wide, 8-12 feet long, 4 feet deep; dig a "cold hole" in the trench floor (cold air sinks into it, away from where people sleep) plus sleeping platforms off the sides; cover the top with an A-frame structure or a poncho/tarp.

## Detailed Version

**The real pattern across every one of these: the amount of real time and material investment scales with how long you expect to stay, and the trade-off is explicit, not accidental** — a snow wall trades comfort/warmth for speed (30 minutes), while a snow cave trades significant build time (3+ hours, real exertion, real collapse risk during construction) for genuinely effective long-term insulation. Picking the wrong one for your actual timeline — over-investing when you need to move soon, or under-building when you're stuck for days — is itself a real risk, which is exactly what the shelter-selection table is for.
""",
    },
    {
        "title": "Building a Fire — Fire Lays, Fuel & Fire Types",
        "section": "reference",
        "tags": ["fire", "survival-skills", "cold-weather"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Fires split into two real categories — cooking fires and warmth/signaling fires — but the basic process is the same for both: prepare a fire lay, gather fuel in 3 real grades, build the fire, and extinguish it properly afterward.**

## Preparing the Fire Lay

**On snow, a fire needs a platform or it will simply sink and go out** — lay several green logs side by side under the fire area, or dig down to bare earth instead. Build a windbreak if you can. **⚠️ Avoid wet rocks in or near a fire** — heat acting on dampness trapped in sandstone, shale, or stream-rounded stones can cause them to explode.

**Dakota Hole (a lower-signature fire lay):** a below-ground fire pit design that reduces visible flame/light, burns with less smoke thanks to a strong air draft it creates, and is genuinely easier to light in high wind — a real, useful technique even outside any tactical context, anywhere you want a fire that's less visible or smoky.

## Gathering Fuel — 3 Real Grades, Each With a Job

1. **Tinder** — fine, dry material that catches the first spark/flame. Gather a double handful for the fire you're about to build, plus another double handful stored dry for the next morning (**dew alone can dampen tinder enough to ruin it overnight**). Real examples: shredded cedar/juniper bark, pine needles, fine shavings cut from a dry stick, natural fibers supplemented with pine pitch, or cotton balls with petroleum jelly.
2. **Kindling** — pencil-thick to thumb-thick dry sticks that catch from the tinder and burn long enough to ignite your real fuel wood. **Evergreen limbs often make excellent kindling** thanks to their high resin content — they burn hot and fast, though not for long.
3. **Fuel wood** — sustains the fire. **Dead limbs still attached to standing trees, or deadfall held up off the ground, have absorbed less moisture and burn more easily than wood lying directly on the ground.** **Never cut live, green trees for fuel** — it won't burn well anyway. **Softwoods (conifers) burn hot/fast with more smoke and spark but leave few coals; hardwoods burn slower with less smoke and leave a real bed of long-lasting coals** — know which species are actually available where you are.

**Stack your wood supply close enough to reach easily, but far enough from the flames to stay safe, and shelter it from further precipitation.**

## Building the Right Fire for the Job

- **Teepee fire** — a cooking fire, producing concentrated heat; once a solid bed of coals forms, collapse the teepee structure and push the embers into a compact pile for actual cooking.
- **Pyramid fire** — a heating fire, producing large amounts of light and heat, good for drying out wet wood and building up a coal supply for later cooking.

## Starting the Fire — Modern Methods (know their real limits)

- **Matches and lighters** — waterproof them; a modern method failing when you need it most is a real, common failure mode to plan around.
- **A convex lens** (binoculars, camera lens, magnifying glass) — works on bright sunny days to focus enough heat onto tinder to ignite it.
- **Flint and steel** — some designs include a magnesium block you shave onto tinder first, or have magnesium mixed directly into the flint for a hotter spark.

## Extinguishing a Fire — the Real "Drown, Stir, Feel" Method

1. **Drown** the fire lay with water.
2. **Stir** the ember bed thoroughly to make sure it's actually out underneath, not just on the surface.
3. **Feel** the bed with your hand for any remaining hot spots.
4. **If you find any hot spot at all, repeat the entire process from the start** — don't assume a single pass was enough.

## Detailed Version

**The real principle worth keeping from the fuel-gathering section: fire-building failure is overwhelmingly a fuel-preparation problem, not a lighting-technique problem.** Someone who skips gathering adequate dry tinder, or who tries to jump straight from tinder to full-size fuel wood without proper kindling in between, will struggle regardless of how good their ignition method is — the real fix for "my fire won't catch" is almost always more/better tinder and kindling, not a better lighter.
""",
    },
    {
        "title": "Starting a Fire — Bow & Drill Method",
        "section": "reference",
        "tags": ["fire", "bow-drill", "primitive-skills", "survival-skills"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**The bow and drill is a genuine, field-tested primitive fire-starting method requiring only cord and a knife from a basic survival kit — no modern ignition source at all.**

## The 6 Real Components

1. **Bow** — a resilient green stick, about ¾ inch diameter, 30-36 inches long, strung tight (no slack) with cord — 550 cord works best.
2. **Drill** — a straight, seasoned hardwood stick, ½-¾ inch diameter, 8-12 inches long. The top is tapered to a blunt point (reduces friction in the socket); the bottom is slightly rounded to seat into the fireboard.
3. **Socket** — an easily gripped stone, piece of hardwood, or bone with a slight depression on one side, used to hold the drill's top in place while you press down on it.
4. **Fire board** — a seasoned *softwood* piece, about ¾ inch thick, with a depression cut ¾ inch from one edge, plus a V-shaped notch cut from the board's edge into the center of that depression — this notch is what actually collects the forming ember.
5. **Ember patch** — any thin material (leather, foil, bark) placed under the notch to catch and later transfer the ember.
6. **Bird's nest** — a loosely woven, fist-sized ball of dry, finely shredded tinder (juniper/cedar/sagebrush outer bark, cottonwood/aspen inner bark, or dry grass/moss) with a small depression kneaded into its center to receive the ember.

## Producing the Fire

1. Position the ember patch directly under the fireboard's V-notch.
2. Kneel with your left foot anchoring the fireboard near the depression.
3. Load the bow: the drill goes between the bowstring and the bow itself. Set the drill's bottom into the fireboard's depression, and cap the top with the socket.
4. **Left hand holds the socket, applying steady downward pressure. Right hand saws the bow smoothly back and forth** to spin the drill.
5. **Once you see smoke, increase downward pressure and saw faster.**
6. **When a thick, steady column of smoke builds around the depression, stop all movement.** Carefully lift the bow, drill, and socket away without disturbing the fireboard, then lift your foot off it.
7. **Gently tap the fireboard** to make sure the ember has fully dropped out of the notch onto the ember patch, then remove the fireboard.
8. **Slowly fan the fine black powder** until it solidifies into a visibly glowing ember, then carefully tip it from the ember patch into the bird's nest's center depression.
9. **Hold the nest with the ember-filled cylinder facing you, parallel to the ground, and gently blow air into it.** As the smoke thickens, keep blowing steadily until it bursts into open flame.

## Real Troubleshooting

| Problem | Real fix |
|---|---|
| Drill won't stay in the depression | More downward pressure, and/or widen/deepen the depression |
| Drill won't spin | Less downward pressure, and/or tighten the bowstring |
| Socket is smoking | Less downward pressure; the socket wood may be too soft for the drill — add lubrication (animal fat, oil, grease) |
| No smoke at all | Wood may not be properly seasoned; check the drill is straight; keep your left hand locked against your shin while sawing |
| Smoke but no ember forms | The V-notch isn't cut into the center of the depression, or not enough heat is being generated |
| Bowstring rides up/down the drill | Keep your right arm locked while sawing; check the drill is straight; keep the bowstring running over the top of your left boot |
| Bird's nest won't ignite from the ember | Tinder isn't dry enough; the nest is woven too tightly; tinder wasn't kneaded/broken down enough; or you're blowing too hard and fracturing the ember |

## Detailed Version

**The real, most common beginner failure across this whole technique is treating each component as interchangeable rather than purpose-matched** — a fireboard that's too hard (not genuinely seasoned softwood) or a drill that's too soft produces smoke without ever forming a real ember, no matter how much effort goes into the sawing motion. Getting the wood selection right for each specific part matters as much as the physical technique itself.
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
