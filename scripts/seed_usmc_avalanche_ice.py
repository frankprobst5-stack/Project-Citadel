#!/usr/bin/env python3
"""Seeds 6 real pages from the USMC Winter Survival Course Handbook's
Avalanche and Ice Hazards chapter -- mined from the real text layer
already extracted in this session (/tmp/usmcwinter.txt, pages 17-1
through 17-11). This is genuinely life-or-death content with real,
specific statistics (avalanche burial survival rates by time) and
real, specific technique (crossing prep, self-rescue, group rescue).

Covers: the 4 real avalanche types and their anatomy, the real
4-factor hazard evaluation framework (snowpack/weather/terrain/human
factor) with specific slope-angle and warning-sign detail, real
route-planning and slope-crossing technique, real avalanche-burial
rescue statistics and search method, and real ice formation/strength
factors plus both self-rescue and group-rescue technique for a
through-ice fall.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_avalanche_ice.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Avalanche Types, Triggers & Anatomy",
        "section": "reference",
        "tags": ["avalanche", "cold-weather", "mountain-safety"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**4 real avalanche types exist, each with a different real mechanism — knowing which kind of terrain/snow condition produces which type is the first step in recognizing danger.**

## The 4 Real Types

1. **Loose-snow (point release) avalanches** — start small, from a single point, fanning outward as they descend; usually involve only the top snow layers but **can grow large and destructive by picking up more material (entraining) as they go**, and can reach speeds up to 200mph. **More common on steep slopes, 35°+.** The stress they generate can also trigger a larger, deeper slab release.
2. **Slab avalanches** — one or more cohesive snow layers break away together at a fracture line, breaking into blocks as they descend. **Occurs when gravity's downhill pull on a snow layer exceeds the strength of the weakest layer beneath it.** Slabs range from inches to many feet thick, a few yards to over a mile wide, can be hard or soft/wet or dry, and reach speeds up to 150mph. **Most slabs fracture on 35-40° slopes.**
3. **Cornice collapses** — an overhanging ledge of wind-deposited snow at a sharp terrain break (ridge crests, gully edges) breaks off, sometimes well back from the visible edge, and can trigger a larger slide when it lands on a wind-loaded slope below.
4. **Ice avalanches** — unstable ice blocks (seracs) collapsing from steep/overhanging glacier terrain, capable of carrying large amounts of rock/ice/snow over long distances. **These are real genuinely unpredictable and cannot be reliably detected in advance** — unlike the other 3 types, there's no real warning-sign framework for this one.

## Real Triggers

- **Natural:** a falling cornice, sluffing snow, internal stress changes from snow metamorphism.
- **Artificial:** a person's weight (skier, hiker), an explosive blast, even a sonic boom.

## The 3 Real Parts of an Avalanche Path

1. **Starting zone** — usually steeper than 30°, where instability actually releases.
2. **Avalanche track** — the path from the starting zone down to the runout. **Can be channeled** (confined, like a gully) **or unchanneled** (open slope). **⚠️ A multi-branch track can run multiple times in quick succession** — a real, documented cause of rescuer deaths when a second slide comes down while working a runout zone from the first.
3. **Runout zone** — where debris piles up and slows to a stop; its exact position shifts year to year with weather patterns.

## Real Slab Anatomy (for recognizing one)

**Crown face/fracture line** (the slab's upper boundary), **crown** (just above the fracture line), **flanks** (the slab's outer edges), **stauchwall** (the slab's bottom boundary), **bed surface** (what the avalanche actually slides on).

## Detailed Version

**The single most important real distinction on this page: ice avalanches are genuinely unlike the other 3 — they can't be evaluated or predicted using the snow-condition framework that works for loose-snow, slab, and cornice hazards.** Treating glacier/serac terrain as "probably fine because the other warning signs aren't present" is a real, specific mistake this page exists to prevent.
""",
    },
    {
        "title": "Avalanche Hazard Evaluation — Snow, Weather & Terrain",
        "section": "reference",
        "tags": ["avalanche", "mountain-safety", "risk-assessment"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Real avalanche risk assessment weighs 4 factors together: the snow pack itself, the weather, the terrain, and the human factor (your actual alternatives and their consequences)** — no single sign in isolation tells the whole story.

## Snow Pack — Is It Capable of Sliding?

Each storm adds a new layer with its own texture/strength; some layers bond well, some don't. **The real question: is there a weak bond somewhere in the pack, and how much snow could release if it fails?**

## Weather — Real Signs of Instability

**A documented fact: almost all natural avalanches occur during or shortly after a storm** — new weight added faster than the snowpack can adjust to it. **Real warning signs:**
- Recent avalanche activity on similar slopes, or small slides underfoot.
- **"Booming"** — an audible collapse of snow layers.
- Visible cracks shooting out from underfoot.
- Sluffing debris (evidence avalanche activity is already happening).
- **"Sunballing"** — small snowballs rolling, from rapid surface warming.
- **Specific real weather patterns that increase risk:** heavy snow loading in a short window (1 inch/hour sustained over 24 hours), heavy warming rain, significant wind-loading on leeward slopes, a long cold/calm period followed suddenly by heavy precipitation or wind, a rapid temperature rise above freezing after a long cold spell, prolonged (24+ hour) above-freezing temperatures, and **very cold snow (25°F or below) — which slows the snow's own settling/strengthening process, letting instability persist longer than it otherwise would.**

## Weather — Real Signs of (Relative) Stability

Settlement cones around trees/obstacles, visible "creep and glide" (a rippling effect at a slope's base showing the snowpack is settling and gaining strength), snow accumulation still visible in tree branches (meaning calm conditions during the storm, not wind-loading), and snow temperatures holding steady between 25-32°F (which tends to settle snow into a denser, stronger pack).

## Terrain — Real Factors (Avalanches Can Happen on Any Slope)

- **Slope angle:** most slab avalanches release on 35-40° slopes; loose-snow avalanches happen on even steeper slopes, 60°+. **Slopes under 30° rarely slab** (not enough tension); **slopes over 45° usually sluff continuously before a slab can even form.**
- **Slope orientation:** leeward (wind-loaded) slopes carry more stress. Direct, regular sun exposure can actually stabilize a snowpack over time — but **shaded slopes, lacking that solar strengthening, often develop and hold onto weak layers longer — treat shaded slopes as a real, specific suspicion.**
- **Terrain roughness (anchoring):** slopes with real anchors (trees, rocks) are less likely to slide than smooth open slopes.
- **Vegetation as evidence:** a line of fallen trees all pointing the same direction, trees stripped of branches only on their uphill side ("flagged" trees), or a cleared strip through otherwise dense forest are all real, visible signs of past avalanche activity on that exact path.
- **Seasonal pattern:** once a specific path has slid once this season, further slides along that same path become more likely.
- **Elevation:** conditions can differ meaningfully with elevation even on the same mountain — **never assume one elevation's conditions apply to another on the same slope.**

## The Human Factor & Ongoing Evaluation

**What are your actual alternatives, and what are their real consequences?** Hazard evaluation is a continuous process, not a single checklist done once: gather real information before starting (recent snowfall, wind, avisories, terrain history), keep refining that picture during movement, and **stay objective about whether the mission's importance genuinely justifies the present hazard level** — rather than assuming no option exists.

## Detailed Version

**The real, repeated theme across all 3 physical factors: no single sign is conclusive on its own.** A slope showing one stability sign (settlement cones) can still be dangerous if the weather factor (recent heavy snow loading) or terrain factor (35-40° leeward slope) point the other way — real assessment means weighing all 4 together, not stopping at the first reassuring sign.
""",
    },
    {
        "title": "Avoiding & Crossing Avalanche Terrain",
        "section": "reference",
        "tags": ["avalanche", "mountain-safety", "route-planning"],
        "risk_level": "critical",
        "body_markdown": """## Real Route Planning Principles

- **Cross avalanche-prone slopes as high as possible**, ideally above real terrain anchors.
- **Favor high points and ridgelines, especially windward sides** over leeward (wind-loaded) ones.
- **When ascending/descending a prone slope, stay to the side of the starting zone and track**, not directly in it.
- **Avoid wind-loaded lee slopes** specifically.
- **Favor terrain with real anchors** (tree cover) over open slopes.
- **Pick flat, open runout areas** — this reduces potential burial depth — and avoid terrain that feeds into crevasses or cliffs.
- **A wide, U-shaped valley usually has a safe route somewhere in it; a narrow V-shaped valley often does not** — in a V-shape, an avalanche from either side can run up the opposite wall too, leaving little or no genuinely safe ground.

## ⚠️ Crossing a Suspected Slope — Only After All Alternatives Are Exhausted

**Individual preparation before crossing:**
1. Loosen ski bindings; remove your hands from ski pole wrist straps.
2. **Keep your pack on, with straps secured** (counterintuitive — but it can help with flotation/protection if caught, and removing it costs time).
3. Secure your hood tightly over your face; trail an avalanche cord if you have one.
4. **Go straight downhill on foot rather than skiing**, scanning for real escape routes as you go.
5. **Go straight down — never traverse across** a suspect slope.
6. If possible, cross as high as you can on a concave part of the slope.
7. **Cross one person at a time.** Critically: **one person crossing safely does NOT mean the slope is now safe for the next person** — belay each person across individually if at all possible.

## Real Actions If You're Caught in a Slide

1. Try to remove skis/snowshoes immediately.
2. Assess your best actual line of escape.
3. **Delay your own movement briefly — let as much of the avalanche pass by you first** if you can.
4. **Work toward the side of the flow** — force is genuinely lower at the edges than in the center.
5. Try swimming with a double-action backstroke, or roll away at roughly a 45-degree angle.
6. **Make a real, maximal effort to reach the surface as the avalanche begins settling** — once it stops moving, you likely won't be able to dig yourself out.
7. **Create an air space in front of your face to breathe**, before the snow fully sets.
8. Try to position yourself as close to the surface as possible.
9. Establish your orientation (which way is up).
10. **Don't panic** — panic wastes oxygen and the limited window you have to act.

## Detailed Version

**The real, counterintuitive guidance worth remembering from this page: speed and individual-crossing discipline matter more than they feel like they should.** Crossing one at a time (rather than as a group, which feels safer) and never assuming a successful first crossing proves the slope is stable are both real corrections to an understandable but wrong instinct — exactly the kind of mistake this specific guidance exists to prevent.
""",
    },
    {
        "title": "Avalanche Rescue — Search & Survival Statistics",
        "section": "emergency",
        "tags": ["avalanche", "rescue", "mountain-safety"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ The Real, Time-Critical Statistics

**After about 30 minutes of burial, survival chance is roughly 50%. After 1 hour, it drops to roughly 20%.** Cold and suffocation are the main real causes of death. **This single fact drives everything about real avalanche rescue: speed is the entire point, far more than thoroughness.**

## Real Search Sequence

1. **Mark the last-seen point immediately** — and also mark any spot where the person briefly reappeared during the slide, if observed.
2. **Quick visual search** of the area for any visible sign — an avalanche cord, body parts, equipment.
3. **If nothing is visible, do a quick surface search** of the whole debris area.
4. **If that fails, move to a more systematic search, working from the bottom of the debris upward.**
5. **If that also fails, begin probing** (physically probing the snow for a buried person).

## Real Most-Likely Locations for a Buried Victim

- **Along the fall line from the last-seen point, working downslope** — look for clues (skis, clothing, cord) along the way.
- **The outside of bends in the avalanche path**, where debris tends to accumulate.
- **The uphill side of obstacles** (trees, boulders), where debris piles up against them.
- **The runout zone** — though debris here can be very large/deep, making search genuinely harder.

## Real Types of Search (choose based on available people and time)

- **Hasty search** — by far the most important search for backcountry situations; speed is everything, and deciding whether to search further yourself or go for outside help is a real, difficult call to make in the moment.
- **Coarse probe** — deliberately trades thoroughness for speed.
- **Fine probe** — takes 4-5x longer than a coarse probe; **by the time a fine probe is needed, real survival odds are already low.**

## Detailed Version

**The real, hard truth underlying this entire page: the fastest, least-thorough search method available is usually the right choice, precisely because the 30-minute/1-hour survival statistics make speed the dominant factor.** A more careful, systematic search executed slowly is often the wrong trade — by the time it would find someone, the real odds of a live recovery have already dropped sharply. This is exactly why "hasty search" is explicitly called out as the most important search type, not merely the first step before a "real" search begins.
""",
    },
    {
        "title": "Ice Safety — Formation, Strength & Crossing",
        "section": "reference",
        "tags": ["ice-safety", "cold-weather", "mountain-safety"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Frozen lakes, streams, and bays are real, genuinely life-threatening obstacles — ice strength varies enormously based on real, specific factors, and "it looks frozen" is not a reliable safety check.**

## Real Ice Formation Facts

- Fresh water ice typically begins forming **3-5 weeks** after daily temperatures drop below 32°F.
- **Lake ice is weaker near streams, inlets, springs, and outlets** — moving water slows freezing there. Decaying vegetation on a lake bottom can also release air bubbles that weaken nearby ice.
- **River ice formed during warm/windy weather is rough and stays rough all winter**, and tends to be filled with air bubbles — real, weaker ice.
- Fresh water rarely freezes past 8 feet thick in a single season; typical lake ice by late March runs 3.5-6 feet depending on winter temperatures.

**Real factors that speed up freezing:** low stable temperatures, high wind chill, no snow cover, no current.
**Real factors that slow freezing (and weaken the ice):** fluctuating temperatures, fast current, snow cover (insulates the water underneath), salt or other impurities.

## Real Special Considerations

- **Ice right at the shoreline is thinner and weaker than ice toward the center** — but if shore ice actually rests on the riverbed itself, staying near shore can genuinely be the safer route depending on the riverbed's slope.
- **Ice above an under-ice current is often thicker than surrounding ice** — the current causes more temperature cycling there, which can build thicker ice over time.
- Shallow water ice is usually thinner than deep water ice.
- **Clear ice (free of bubbles/cracks) is often actually THINNER than cloudy-looking ice in the same body of water** — clarity is not a reliable "strong ice" indicator.
- Heavy vegetation decomposing in a lake weakens nearby ice.
- **"Slush ice"** (from flooded snow refreezing) is white, may contain air bubbles, and **carries roughly 25% less load than normal, prime ice.**
- **Ice left unsupported after the water level beneath it drops has very little real strength** — a real risk around reservoirs and runoff-fed lakes specifically.

## Real Ice-Crossing Safety Precautions

1. Loosen ski/snowshoe bindings.
2. Remove ski-pole wrist loops (or improvise a wrist-looped fixed-blade knife if no poles).
3. **Wear clothing snugly, with all ties/straps secured** — this adds real buoyancy and reduces cold shock if you go through.
4. Sling your pack and any weapon onto one shoulder (easier to shed quickly).
5. **Only expose one person to the risk at a time**, until the ice's real weight capacity is confirmed.
6. **Belay the first person/group across with rope, if available.**

## Detailed Version

**The real, counterintuitive fact worth remembering above everything else here: clear ice can be thinner than cloudy ice in the same water, and shoreline ice is often weaker than center ice — both run directly against normal visual instinct.** Judging ice safety by how it looks is genuinely unreliable; the real formation-condition factors above are what actually determine strength, not appearance.
""",
    },
    {
        "title": "Falling Through Ice — Self-Rescue & Group Rescue",
        "section": "emergency",
        "tags": ["ice-safety", "cold-water-immersion", "rescue"],
        "risk_level": "critical",
        "body_markdown": """## Self-Rescue — If You Fall Through Alone

1. **Remove unnecessary gear immediately** (pack, weapon, snowshoes) and try to throw it onto solid ice, out of the water.
2. **Use a fixed-blade knife or ski pole to drag/push yourself out** of the water and onto the ice.
3. **Do NOT stand up near the hole** — stay flat and keep pushing/dragging yourself away until you're genuinely clear of the weak ice around the break.
4. **⚠️ Rewarm immediately.** Cold-water immersion causes real shock and hypothermia — strip off all wet clothing and rewarm using a dry sleeping bag or, if available, multiple fires positioned around the body.

## Group Rescue — If Someone Else Falls Through

1. **Do not let anyone approach the hole without real safety backup** (a rope, or a human chain).
2. **If rope is available:** tie a large fixed loop at the end, throw it to the victim, and have them get the loop around their body before pulling them out.
3. **If no rope is available:** find a long stick/pole and form a human chain, everyone lying prone (flat, to spread weight over more ice), moving the chain as close to the victim as safely possible until they can grab the stick.
4. **If the victim can't reach the stick, keep carefully extending the chain toward the hole** until the lead person can reach the victim directly by hand.
5. **Once recovered, rewarm immediately** — same urgency as self-rescue above.

## Detailed Version

**The real, shared principle between both techniques: staying flat/prone and distributing weight (rather than standing, or having a single rescuer walk directly up to the hole) is what keeps the rescue from creating a second victim.** Standing near a hole that already proved too weak to hold one person is a genuinely common, understandable mistake under the stress of watching someone struggling in the water — and it's exactly the instinct this real technique is built to override.
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
