#!/usr/bin/env python3
"""Seeds 6 real pages from the Canadian Military Basic Cold Weather
Training manual (B-GG-302-002/FP-001, Canadian Forces, 1982 stock
reprint) -- mined from the real text layer already extracted in this
session (/tmp/canadiancold.txt). This source is selectively mined:
much of its content is either obsolete-equipment-specific (named
sleeping bag/stove/tent models) or combat-tactics-specific (weapons,
field defences, camouflage from an enemy, patrolling) and is
deliberately skipped. What's mined here is genuinely new, civilian-
applicable content not already covered by the USMC Winter/Summer
Survival Handbooks earlier in this build-out.

Covers: a real windchill explanation with an actual wind-speed/
temperature freeze-time table (more specific than anything in the
USMC material), the real "COLD" acronym and layer-method clothing
principles, real cold-weather footwear care, real wooded-area shelter
construction (lean-to, double lean-to, wigwam -- timber-framed with
an internal heat fire, genuinely different from the USMC book's
all-snow shelters), real tree-pit/fallen-tree/open-country shelter
variants, and 2 genuinely new camp health topics (fume irritation/
"tent eye" and cold-weather constipation) plus a real CO-vs-fumes
distinction not previously captured.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_canadian_coldweather.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
CANADIAN_COLD_PDF_URL = "/files/pdfs/Military Manuals/Canadian-Military-Basic-Cold-Weather-Training.pdf"

PAGES = [
    {
        "title": "Understanding Cold — Wet vs. Dry Cold & the Windchill Table",
        "section": "reference",
        "tags": ["cold-weather", "windchill", "survival-skills"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Temperature alone doesn't tell you how dangerous cold conditions actually are — windchill (the combined effect of wind and temperature) is what actually determines real risk**, and a real table below shows exactly when that risk becomes "exposed flesh freezes within an hour."

## Wet Cold vs. Dry Cold — a Real, Practical Distinction

- **Wet cold:** temperatures near freezing, with real day/night swings causing alternating freeze-thaw, often with wet snow/rain turning the ground slushy. **Needs a waterproof/water-repellent, wind-resistant outer layer over an insulated inner layer** adequate for moderately cold conditions (above -10°C/14°F). **Waterproof footwear is essential here specifically.**
- **Dry cold:** average temperatures below -10°C/14°F, frozen ground, dry snow. **Needs insulation adequate for windchill as low as -62°C/-80°F**, still protected by a water-repellent, wind-resistant outer shell.

## The Real Windchill Concept

**Windchill measures how much heat a surface actually loses per hour from combined wind and cold — not temperature alone.** A real, concrete example from the source: 7°C (45°F) with a 48mph wind produces the *same* real heat-loss effect as -28°C (-18°F) with only a 5mph wind — **both lose about 1,400 kilocalories per hour, the same "windchill factor."** The real, practical lesson: **a mild-feeling temperature with high wind can be just as dangerous as a genuinely extreme temperature with light wind** — don't let the thermometer alone tell you how much protection you need.

## ⚠️ Real Table — When Exposed Flesh Freezes Within 1 Hour

| Wind speed | Temperature |
|---|---|
| 77 km/h (48 mph) | -7°C (20°F) |
| 42 km/h (26 mph) | -9°C (15°F) |
| 29 km/h (18 mph) | -12°C (10°F) |
| 22 km/h (14 mph) | -15°C (5°F) |
| 21 km/h (13 mph) | -18°C (0°F) |
| 14 km/h (9 mph) | -21°C (-5°F) |
| 11 km/h (7 mph) | -25°C (-10°F) |
| 9 km/h (6 mph) | -26°C (-15°F) |
| 8 km/h (5 mph) | -29°C (-20°F) |
| 6 km/h (4 mph) | -32°C (-25°F) |
| 5 km/h (3 mph) | -34°C (-30°F) |
| 3 km/h (2 mph) | -40°C (-35°F) |

**⚠️ Real caveat: windchill doesn't account for activity level, humidity, breath-related heat loss, sun radiation, or already-lowered skin temperature** — treat it as a simple, practical guide for when cold-weather travel becomes genuinely dangerous, not a precise biological measurement.

## Real Effects of Extreme Cold on the Body

**Below about -23°C (-9°F), real experience shows every other problem loses significance next to the personal battle against the cold itself.** Cold damages the body in 2 real categories: **general hypothermia** (whole-body cooling from immersion/exposure — fatal if prolonged) and **local hypothermia** (damage to specific body parts — frostbite, immersion foot — that can cause real tissue death/gangrene without proper care). **Any existing physical condition tends to get worse under cold exposure**, not better.

## The Real 4 Adjustment Rules

1. **Keep in shape** — cold-weather clothing is heavy and movement burns real extra energy; **a sleeping, exhausted person can freeze, while a healthy person will wake well before reaching that danger point.**
2. **Drink plenty of water** — people in cold climates tend to drink only when thirsty, which genuinely isn't enough; real dehydration and the fatigue it causes are a preventable risk.
3. **Eat to keep fit** — real, regular hot food matters for sustained performance, even without appetite.
4. **Maintain a healthy attitude** — staying alert and engaged is a real, practical defense against the psychological toll of harsh conditions.

## Detailed Version

**The single most important real idea on this page: the thermometer lies about danger when wind is involved.** A moderate temperature with strong wind can match or exceed the real risk of an extreme temperature in still air — which is exactly why the windchill table above exists as a practical field reference, not a theoretical curiosity.
""",
    },
    {
        "title": "The Layer Method & the COLD Acronym for Staying Warm",
        "section": "reference",
        "tags": ["cold-weather", "clothing", "survival-skills"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Clothing's real job in cold weather is insulation — trapping body-warmed air next to your skin rather than letting it escape.** Several real principles, summed up in the memorable acronym "COLD," make that insulation actually work.

## The Real Layer Method

**Several medium-weight layers genuinely insulate better than one heavy garment of the same total thickness** — the real mechanism is trapped dead-air pockets between each layer, not just bulk material. **Inner layers should be porous (holding air pockets); the outer layer should be windproof and water-repellent**, so outside cold air can't displace the warm air you've trapped. **The real practical payoff: layering lets you add or remove one piece at a time to match changing temperature or activity level**, rather than being stuck in one fixed insulation level all day.

**Ventilation matters just as much as insulation** — overheating causes sweat, which fills your clothing's air pockets with heat-conducting moisture (reducing its real insulating value) and then chills you further as it evaporates. **A partially open parka/jacket, or removing one layer, prevents this** without fully exposing you to the cold.

## The Real "COLD" Acronym

- **C — Clean clothing.** Dirt and grease mat the fabric and collapse its air pockets, letting heat escape faster. **Wash wool in lukewarm or cold water — never hot/boiled**, which damages it. Rinse soap completely out of outer garments — leftover soap residue reduces their water-shedding ability.
- **O — Overheating avoided.** **In cold weather, it's genuinely better to feel slightly chilly than too warm** — overheating causes the same moisture problem described above, both from sweat directly and from its evaporation afterward.
- **L — Loose and layered.** **Too-tight clothing or footwear restricts blood circulation, directly increasing frostbite risk.** But too-loose clothing lets the trapped air between layers actually move, which also causes real heat loss — the real goal is layered and snug, not tight and not baggy.
- **D — Dry clothing.** Moisture soaks in from both outside (snow/frost melting against your body heat) and inside (sweat). **Brush or shake off snow/frost before entering any heated shelter** — it will otherwise melt into your clothing immediately upon warming.

## Real Tips for Drying Clothes

**Drying wet clothes:** handle each piece separately; never hang items directly above a stove/heat source (they can fall and catch fire); keep anything away from direct contact with a hot stove/pipe (nylon melts, wool scorches quickly); don't hang clothes over steaming pots (adds moisture right back).

**Drying damp clothes:** hang them on your pack while marching, letting body heat and airflow do the work. **⚠️ Never put damp clothing inside your sleeping bag to dry** — this just transfers the moisture into your bag's insulation instead, degrading the one piece of gear you most need to stay dry and warm.

## Detailed Version

**The real, unifying idea behind every one of the COLD letters: moisture is the actual enemy, far more than cold air itself.** Dirty clothing traps less air; overheating creates moisture through sweat; tight clothing restricts the blood flow that keeps skin warm; and wet clothing loses its insulating value almost entirely. Every rule in "COLD" is really one rule — keep the insulating air pockets in your clothing dry and intact — applied from a different angle.
""",
    },
    {
        "title": "Cold Weather Footwear Care",
        "section": "reference",
        "tags": ["cold-weather", "footwear", "frostbite-prevention"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Feet are more vulnerable to cold than almost any other body part — they get wet easily, both from outside moisture and from their own sweat — which makes real footwear discipline one of the single most important cold-weather habits.**

## Real Principles

- **The same loose-and-layered rule applies to feet:** the boot itself plus sock/insole combinations form the real layers. **Avoid wearing too many socks too tightly, or lacing boots too tight** — either restricts circulation and genuinely increases frostbite risk, even though it feels like it should add warmth.
- **Carry a dry spare pair of socks at all times.** **Change socks as soon as they get wet** — don't wait. If wearing mukluks or similar footwear, change both socks AND insoles once they're wet.
- **Dry footwear at the first real opportunity, and keep it clean.** Wash both socks and feet frequently — this genuinely helps keep both in better condition over time.
- **Exercise your feet actively:** stamping, a few quick steps back and forth, flexing/wriggling toes inside boots — the real muscular activity this generates produces heat and keeps circulation going.
- **Massage feet when changing socks** — another real, simple way to support circulation.
- **⚠️ If using ski or snowshoe bindings, adjust them carefully.** Too tight restricts blood flow and causes cold feet; improperly adjusted bindings can also chafe the foot or cause excess wear on the boot itself.

## Detailed Version

**The real, counterintuitive point worth remembering: adding more socks or lacing tighter, which feels like it should help, can actually make feet colder by restricting the blood flow that keeps them warm in the first place.** The real fix isn't more insulation crammed on tighter — it's the right amount of loose, layered insulation plus active circulation (exercise, massage) and staying genuinely dry.
""",
    },
    {
        "title": "Wooded-Area Shelters — Lean-To, Double Lean-To & Wigwam",
        "section": "reference",
        "tags": ["shelter", "cold-weather", "bushcraft"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Unlike all-snow shelters (snow cave, snow trench, etc.), these designs use available timber as a structural frame and are warmed by an open fire built right beside or inside them — a genuinely different approach suited to forested terrain rather than deep open snowpack.**

## Real Site Selection (civilian-adapted)

**Consider the prevailing wind direction** — blowing snow always drifts in the lee (downwind side) of obstacles, which affects both comfort and how quickly your shelter gets buried. **Wooded areas are the best real location overall** — they provide building timber, firewood, windbreak, and natural cover, while open barren terrain offers only snow to build with.

## Single Lean-To — the Real Base Design

1. Select 2 live trees about 8 inches thick, spaced at least 2 feet per person who'll sleep there, as your uprights.
2. **Place a top crosspiece** (4-5 inches thick, about 4 feet longer than the gap between uprights) at roughly shoulder height — set in a tree crotch or propped up. **If the span exceeds 15 feet, brace the crosspiece's center** with a solid pole.
3. **Place a front bottom crosspiece** spanning the two uprights — this keeps sleeping bags from sliding toward the fire and holds insulating boughs in place.
4. **Place a rear bottom crosspiece** about 7 feet behind the front one, to help raise the back of the roof and hold boughs.
5. **Lay back pieces** (2-3 inches thick, 10-12 feet long) with their base ends on the ground against the rear crosspiece and their tops resting on the top crosspiece, spaced no more than 18 inches apart.
6. **Shingle boughs onto the roof** from the bottom up, to at least 6 inches thick — thick enough to walk on as you build it up.
7. **Close in the sides** with short trees or large tree-tips leaned against them, cut-end up.
8. **Line the floor with a bough bed**, at least 6 inches thick, tips pointing up (or laid flat if time/concealment needs don't allow the full version) — **check carefully for sharp points or small dead twigs that could puncture a sleeping pad.**
9. **Trim overhanging branch ends and bank the back/sides with snow.**
10. **If using canvas/poncho material for the roof**, weight it down against the backpieces with logs so wind can't lift it off.

## Heating It — a Real Log Fire

1. Lay short green logs on the ground first, to hold the fire up off the snow for better draft.
2. Lay two dry logs (at least the lean-to's length, 8-15 inches thick) across the green logs.
3. Lay a third green log on top, centered between the two dry ones.
4. **Light the fire in several spots along its length** to help it spread evenly — chipping the facing log surfaces helps it burn better.
5. **⚠️ On deep snow, a fire built directly on it will simply sink and go out — always build on a proper fire base** as long as the fire itself.
6. **Real rule of thumb for firewood: gather what you estimate you'll need for the night, then TRIPLE that amount** — new lean-to occupants consistently underestimate real consumption.

**A reflector wall** (green logs stacked like a short wall, about 3 feet from the fire's outer edge) bounces heat back into the lean-to and doubles as a small windbreak.

## Double Lean-To

**Simply two single lean-tos built facing each other** — the second lean-to's front occupies the spot where a reflector wall would normally go, letting the shared fire heat both sides at once.

## Wigwam (shelters up to 10 people in lightly wooded terrain)

1. Tie 3 poles (~10 feet, 3 inches thick) together about 1 foot from their small end; stand them up with the tied end on top, spread so the tie point sits roughly 8 feet up.
2. Lean several thinner side poles against the same tie point to support the covering.
3. Secure the pole bases with short poles laid flat on the ground between them.
4. **Cover the frame with ponchos/canvas (or woven boughs if that's all that's available)**, leaving an entrance gap, and **bank the base with snow to block drafts.**
5. Build a bough bed as with the lean-to.
6. **Hang an improvised firebox (a large tin can works) from the top by wire** — a draft channel under the wall and a smoke hole at the apex add real comfort. Alternatively, heat it the same way as a lean-to: an outside fire with a reflector wall by the entrance.

## Detailed Version

**The real, unifying design principle across all three shelters: they're built to be heated from an open fire that stays INSIDE the group's living space (or just at its entrance) rather than at a distance** — which is exactly why the bough-bed insulation, the fire-base (to stop sinking into snow), and the reflector wall all matter so much. None of this is optional decoration; each piece exists specifically to make sharing space with an open flame both survivable and actually warm.
""",
    },
    {
        "title": "Tree-Pit, Fallen-Tree & Open-Country Shelters",
        "section": "reference",
        "tags": ["shelter", "cold-weather", "bushcraft"],
        "risk_level": "moderate",
        "body_markdown": """## Tree-Pit Shelter — Using a Tree's Own Natural Gap

**Large trees often have a natural pit at their base where snow stays fairly shallow — a genuine shortcut to a usable shelter.** Enlarge that natural pit to your needed size, line the walls with boughs/branches, build a bough bed in the bottom, add an overhead covering of boughs/branches (or other material), and dig in an entrance.

## Chopped or Fallen Tree Shelter

**A low, tent-like shelter made from a tree with its main stem roughly 4 feet off the ground** — either a genuinely fallen tree, one you chop down into that position, or one whose butt end you lift and secure. **Make sure the butt end is held securely off the ground** regardless of which method you use. Trim the inside boughs off and use them to thicken the remaining ones along the sides; build a bough bed as usual; heat it with a small fire at the front (a log reflector behind the fire helps direct heat inward).

## Tent-Roof Shelter (open country/barren terrain, up to 10 people)

**The quickest, simplest shelter type overall, and genuinely the easiest to conceal** — built using a real tent (or salvaged parts of a damaged one).

1. Lay the tent on the ground and mark its outline in the snow for the first pitching phase.
2. Remove the tent and mark a second outline about 8 inches inside the first.
3. **Dig out the snow inside that inner mark to a depth of 4 feet.**
4. **Add roof supports:** about 10 logs laid across the hole, or — without logs — stand the tent pole upright in the center and run its guy ropes outward in a "wagon wheel" pattern around the hole's edge (keeping the pole top below the snow surface).
5. Lay the tent fabric over the supports, piling snow onto the outside edges and flaps to secure it. **If camouflage/visibility matters, keep the shelter's internal heat low enough that snow piled on the roof doesn't melt through** — melted-and-refrozen snow soaks and weakens the covering.
6. **If snow depth or concealment needs are lower-priority, a shallower 3-foot dig plus a ring of 1.5-foot snow blocks around the outline works as a simpler variant.**
7. **⚠️ Build the exit level with the floor, then angle it down so the tunnel's top sits about 18 inches below floor level** — this real design creates a genuine cold-air trap, keeping the coldest air from pooling where people actually are.

## Detailed Version

**The real engineering idea behind the tent-roof shelter's sunken-entrance design is worth generalizing: cold air is denser and sinks, so any shelter entrance built level with (or above) the living floor lets that cold air flow straight in and pool there.** A below-floor-level entrance tunnel traps it instead — the same real cold-air-trap principle that makes a snow cave's raised sleeping bench (see Building Snow Shelters — Snow Wall, Cave, Tree-Pit & More) work for the same underlying reason.
""",
    },
    {
        "title": "Tent Fumes, CO Poisoning & Cold-Weather Constipation",
        "section": "reference",
        "tags": ["camp-health", "carbon-monoxide", "cold-weather"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ A Real, Important Distinction: Carbon Monoxide Is NOT the Same as "Fumes"

**Carbon monoxide can be present with no detectable fumes at all, and strong fumes can exist with zero carbon monoxide — treating the two as the same thing is a real, dangerous mistake.** CO is produced by any combustion involving carbon — engine exhaust and coal stoves are the most common real sources, and even gasoline stoves/lamps (generally lower real risk) still require real, ongoing ventilation checks rather than assumed safety. **A real fatal dose is roughly 1 part carbon monoxide to 800 parts oxygen** — a genuinely small proportion.

**Real signs (often absent entirely before collapse):** headache, dizziness, impaired vision, confusion, yawning, weariness, nausea, ringing in the ears, and later a fluttering/throbbing heart. **⚠️ The gas frequently strikes with no warning at all — a person may have no idea anything is wrong until their legs give out.**

**Real treatment:** move the person into fresh air immediately, but keep them warm. **Do not let them exert themselves** — exercise increases oxygen demand at the worst possible time. If breathing stops or becomes gasping, start rescue breathing immediately. **A survivor needs to stay completely still and warm, in a well-ventilated space, for at least a full day afterward** — this is genuinely serious even once the immediate danger passes.

## Fume Irritation ("Tent Eye")

**A real, different (and less dangerous) problem: gasoline stove/lamp fumes building up in a poorly ventilated tent, causing eye irritation** — common when people first start living in tents. **Real prevention:** keep stoves/lamps clean and tents properly ventilated. **Fresh air is the only real, lasting fix** — holding snow against the eyes gives temporary relief but doesn't address the actual cause.

## Cold-Weather Constipation — a Real, Common, Preventable Problem

**A genuinely common pattern in cold conditions: people avoid relieving themselves to escape the discomfort of doing so in the cold, compounded by changed eating habits and not drinking enough fluids.** **Real symptoms if it persists:** mild to severe stomach cramps, headaches, dizziness, general fatigue/weakness.

**Real prevention/treatment:** adjust eating and drinking habits deliberately, and don't "put off" the normal process once the urge comes — delaying it specifically makes this worse over time. Mild laxatives can help restore normal function; **seek real medical help if severe constipation persists.**

## Detailed Version

**The real, practical value of separating these three topics clearly: CO poisoning is a genuine life-threatening emergency requiring immediate action, tent eye is an uncomfortable but low-risk ventilation problem with a simple fix, and constipation is a quietly common, entirely preventable discomfort that people routinely dismiss as unavoidable in cold conditions when it genuinely isn't.** Recognizing which of the three you're actually dealing with changes both the urgency and the real correct response.
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
                "source_url": CANADIAN_COLD_PDF_URL,
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
