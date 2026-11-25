#!/usr/bin/env python3
"""Seeds 3 real pages from the USMC Winter Survival Course Handbook
(Mountain Warfare Training Center, 2002) -- mined from the real text
layer already extracted in this session (/tmp/usmcwinter.txt),
Chapters 1-2 (pages 1-1 through 02-4). This is the first batch from a
new source: unlike the combat-focused TCCC handbook, this is a real
survival-skills training manual (water, shelter, fire, signaling,
food procurement, survival medicine, navigation) that is broadly
civilian-applicable once combat/evasion-specific sub-points are
filtered out, which is exactly what these pages do.

Covers: the real psychological stressors/reactions framework (a
civilian-adapted version of the SURVIVAL acronym's mental-attitude
points, stress signs, and group-survival factors), the real
priorities-of-work sequencing for the first 24-72 hours, and a real,
itemized survival kit component list.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_survival_mindset_kit.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Survival Mindset — Psychology & Stressors",
        "section": "reference",
        "tags": ["survival-skills", "psychology", "mindset"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**The "will to survive" is a real, trainable mental discipline, not just an innate trait — and understanding the specific psychological stressors a survival situation creates is what makes that discipline possible to maintain.**

## The Real Mental-Attitude Principles

- **Size up your situation, surroundings, physical condition, and equipment** before acting — check yourself for injuries and treat them, note the area's terrain/weather/wildlife patterns, and realistically assess what you actually have available.
- **Undue haste makes waste** — plan moves deliberately rather than rushing, which causes avoidable mistakes and injuries.
- **Always know where you are** — orient yourself continuously relative to water sources, shelter options, and terrain that offers protection, not just once at the start.
- **Vanquish fear and panic** — these feelings will be present; the real skill is controlling them, not eliminating them entirely.
- **Improvise and improve** — use tools and objects for purposes beyond their original design (a rock as a hammer, for instance).
- **Value living** — consciously place a high value on continuing, and refuse to give in to obstacles; draw strength from others who are holding up well.
- **Learn basic skills before you need them** — the real moment to practice survival skills is during calm, low-stakes conditions, not for the first time during an actual emergency.

## Stress — a Real, Double-Edged Factor

**Stress itself isn't purely bad** — it provides real challenges that teach you about your own values and strengths. The problem is *too much* stress, which becomes distress. **Real signs of distress to watch for in yourself and others:** difficulty making decisions (don't mistake this for a hypothermia symptom — they can look similar), angry outbursts, forgetfulness, low energy, constant worrying, increased mistakes, thoughts about death, trouble getting along with others, withdrawing, avoiding responsibilities, and carelessness.

## The Real Survival Stressors

- **Injury, illness, or the real possibility of death** — being alone in an unfamiliar environment facing these risks is genuinely one of the most stressful experiences a person can have.
- **Uncertainty and lack of control** — the only real guarantee in a survival situation is that nothing is guaranteed.
- **The environment itself** — weather, terrain, and local wildlife are all real, ongoing stressors.
- **Hunger and thirst** — these get more serious the longer a situation continues; real diarrhea risk during food/water scarcity makes replacing lost electrolytes genuinely important, not optional.
- **Fatigue** — protecting sleep deliberately, even when food/water are scarce, is one of the few genuinely controllable factors — and sleep deprivation directly worsens fear.
- **Isolation** — being with others provides a real sense of security; being alone removes that.

## The Real Psychological Reactions

- **Fear** — a normal response to real danger; it has a genuinely useful function when it makes you appropriately cautious.
- **Anxiety** — an uneasy, apprehensive feeling; reduced by actually doing the tasks that move you toward getting through the situation.
- **Anger and frustration** — arises from repeatedly being blocked from a goal (lost gear, bad weather, physical limits); left unmanaged, it drives poor decisions.
- **Depression** — often follows unmanaged anger/frustration, shifting a person's focus from "what can I do" to "there's nothing I can do" — recognizing this shift is the first step back out of it.
- **Loneliness and boredom** — genuinely compounds depression; deliberately keeping your mind occupied with productive tasks counters this.
- **Guilt** — if others were lost in the same event that led to your survival, feeling both relief and grief at once is normal — don't let guilt stop you from continuing to live.

## Real Group Survival Factors

**A group's survival depends on its ability to organize, not just on having more people.** An emergency does not automatically bring people together effectively — a disorganized group under stress often becomes more dysfunctional, not more cooperative, without deliberate leadership. **Real factors that improve group survival odds:** organizing who does what, matching tasks to people's actual skills, a designated leader who still genuinely accepts input and criticism, making time-sensitive decisions promptly, regularly checking shared equipment, and building real survival knowledge/skill within the group (confidence comes from actual competence, not just optimism).

## Detailed Version

**The single most load-bearing idea across all of this: naming a feeling or stressor correctly is itself a real coping tool.** Recognizing "this is frustration turning into anger" or "this is the isolation-driven boredom the manual warned about" gives you something concrete to act on, rather than just an undifferentiated sense that things feel bad — which is exactly why this framework exists as a checklist to actively run through, not background theory to read once.
""",
    },
    {
        "title": "Priorities of Work in a Survival Situation",
        "section": "reference",
        "tags": ["survival-skills", "priorities", "shelter", "fire"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**A survival situation's real task order changes in blocks of time — what matters most in the first 24 hours is different from what matters in the days after, and getting that order right is as important as doing each task well.**

## First 24 Hours — the Real Critical Window

**Make an initial honest assessment of your actual situation** — weather, terrain, time of day, and what resources you genuinely have — before committing to a plan. **The real task order for this window:**

1. **Shelter** — protection from the elements comes first; exposure can kill faster than almost anything else on this list.
2. **Fire** — warmth, a way to purify water, signaling, and psychological comfort all depend on it.
3. **Water** — the body can survive without food far longer than without water.
4. **Signaling** — once the above are addressed, improve your chances of being found.

## Second 24 Hours — Expanding Your Situation

**Once you know you can actually survive the immediate term, shift to building out knowledge of your surroundings:**

- **Tools and resources:** short trips from your shelter to locate what's actually around you — edible food sources, usable materials, and (in the source's framing) travel routes through the area.
- **Traps/snares for food, placed further from camp:** moving farther out to set these also lets you view your own shelter location from different vantage points, which helps you understand how approachable/visible it actually is.
- **Awareness of approaches to your shelter:** once you understand likely paths into your area, you can position early-warning measures accordingly — in a civilian context, this is the same logic as understanding sightlines and approach routes to a shelter-in-place location.

## Remainder of the Situation

**This entire remaining period is spent continuously improving your situation** — strengthening shelter, expanding food/water security, maintaining signaling readiness — until rescue or self-extraction actually happens, not just "waiting."

## Detailed Version

**The real principle behind block-of-time thinking: the first 24 hours is about not dying, and everything after that is about not merely surviving but steadily improving your odds and your conditions.** Treating every hour with first-24-hour urgency burns out a person's limited energy and decision-making capacity; treating the whole situation with "remainder of the situation" patience during the first critical hours gets people killed by exposure or dehydration before they even get the chance to improve anything. Getting the phase right matters as much as doing the right task within it.
""",
    },
    {
        "title": "Building a Survival Kit — Real Components",
        "section": "reference",
        "tags": ["survival-skills", "gear", "survival-kit"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**A real survival kit is built around 6 functional categories, not a specific brand-name product list** — the goal is picking items that are durable, weather-resistant, easy to carry, and ideally multi-purpose, layered so the most critical items stay directly on your body rather than in a pack you might lose.

## Fire Starting

Matches, a magnifying glass, flint and steel, a lighter, potassium permanganate (paired with sugar or antifreeze — a real improvised fire-starting chemical reaction), and pre-packaged tinder (commercial tinder, or a simple cotton-balls-soaked-in-petroleum-jelly improvised version).

## Water Procurement

- **Disinfecting:** iodine tablets, betadine solution, iodine solution, or household bleach.
- **Boiling container:** a metal cup or any can that never held petroleum products (petroleum residue can leach into water and food).
- **Carrying:** a canteen, a plastic bag, or any plastic/metal/glass container that never held petroleum products.

## Food Procurement

- **Fishing:** assorted hook and sinker sizes, metal leaders/swivels, small weighted jigs, fishing line — **size your gear to the actual fish in your specific environment.**
- **Trapping game:** snares (commercial, aircraft cable, or tie/communication wire), bait (a cheese/jelly/peanut-butter food packet, or fishing bait), strong cord for building gill nets or traps, marking tape, slingshot material, large treble hooks.

## Signaling

- **Daytime:** a signal mirror, a whistle, smoke/pen-flare pyrotechnics, brightly colored panels or fabric.
- **Nighttime:** pen flares/star-cluster pyrotechnics, a flashlight/strobe/chemical glow stick, a whistle.

## Shelter

Strong cordage (paracord, wire, communication wire, tie wire), a small folding saw, a basic sewing kit (for repairing clothing/gear), tentage (a poncho or space blanket doubles well here), and a candle (real, practical heat/light/fire-starting value in one small item).

## First Aid

Adhesive bandages/steri-strips/tape, non-stick pads, gauze, a muslin bandage, improvised butterfly closures, burn and antiseptic ointment, salt and sugar (for a real improvised oral rehydration mix — see Dehydration & Oral Rehydration Drink), eye wash, alcohol prep pads.

## Miscellaneous (genuinely useful extras)

Fingernail clippers, a compass, a notebook with pen or pencil, small wood screws and nails, and surgical tubing (useful for everything from a tourniquet substitute to a water siphon).

## Detailed Version

**The real organizing principle worth keeping, even if you never use this exact item list: layer your kit by how catastrophic losing it would be.** The smallest, most critical items (fire starter, water disinfectant, signal mirror) go directly on your body; a larger, more complete kit can live in a pack — because a pack can be lost, dropped, or left behind in an emergency, while whatever's on your person generally isn't.
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
