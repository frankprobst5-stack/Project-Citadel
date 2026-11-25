#!/usr/bin/env python3
"""Seeds 4 real pages from the USMC Winter Survival Course Handbook's
Winter Tracking chapter -- mined from the real text layer already
extracted in this session (/tmp/usmcwinter.txt, pages 13-1 through
13-9 roughly). Real, detailed tracking technique -- genuinely useful
for locating game (food procurement) or understanding animal activity
near a camp, beyond its original military reconnaissance framing.

Covers: real tracking terminology (trails/runs, beds/lays, rubs,
scratches, transference, compression, disturbance, sign, spoor), real
gait-based and family-based animal track identification, real track-
age determination including a specific real snow-track erosion
timetable, and real tracking/direction-finding technique.

The source's "Size Estimation" section (estimating enemy military
unit size -- squad/platoon/company -- from ski/snowshoe track
patterns) is deliberately excluded as a combat-reconnaissance-
specific application with no real civilian survival use.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_tracking.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Tracking Terminology — Trails, Beds, Signs & Spoor",
        "section": "reference",
        "tags": ["tracking", "survival-skills", "bushcraft"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Real tracking starts with a shared vocabulary — each term below describes a genuinely distinct type of evidence, and conflating them leads to real misreadings.**

## Trails and Runs

**Trails are like highways** — the main thoroughfares an area's animals (sometimes multiple species) use regularly, some seasonally. **Runs are like side streets** — less-used paths connecting a main trail to a specific feeding, bedding, or watering spot.

## Beds and Lays

**A bed is a frequently reused sleeping spot** (a den, burrow — found in hollow logs, rock piles, brush, grass, thickets, even open ground). **A lay is a one-off resting spot**, rarely used more than once.

## Rubs and Scratches

**Rubs** can be accidental (brushing against a burrow entrance, trail-side branches, a fallen tree) or deliberate (an animal scratching an itch, or a deer rubbing antler velvet off against a tree). **Scratches** follow the same accidental/deliberate split — accidental ones from climbing or a belly-drag over a log; deliberate ones at a tree base where claws raked downward, or in the ground where a cat buried scat, a squirrel cached nuts, or something dug at a scent.

## Transference, Compression & Disturbance

- **Transference** — material physically carried from one spot to another (mud tracked onto a log from a muddy bank).
- **Compression** — the actual flattening of soil/snow/debris under body weight. **More visible in hard, dry, sandy conditions** where there's no moisture to hold a crisp impression.
- **Disturbance** — an unnatural visual pattern, especially noticeable in snow. **Real example: forward movement always kicks snow forward (transference) — once that tossed snow melts, it leaves a visibly disturbed pattern on the surface behind it**, distinct from the original transference itself.

## Gnawing, Scat, Sign & Spoor

- **Gnawing** — chew marks on bark/vegetation, either from feeding or (in predators) seeking specific nutrients.
- **Scat** — actual droppings.
- **Sign** — any disturbance revealing a presence: a displaced stone, an overturned leaf showing its darker underside, sand on a rock, drag/scuff marks, a displaced twig.
- **Spoor** — the actual track/trail itself, identifiable by size, shape, type, and pattern (often used interchangeably with "track"). **Splits into aerial sign (above ground level) and ground sign.**

## Detailed Version

**The real, practical reason this vocabulary matters: "I see something" is not the same observation as "I see a rub" versus "I see a scratch" versus "I see disturbance"** — each term points to a different real cause, and misidentifying which one you're looking at leads directly to a wrong conclusion about what actually happened at that spot.
""",
    },
    {
        "title": "Identifying Animal Tracks by Gait & Family",
        "section": "reference",
        "tags": ["tracking", "animal-identification", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Real track identification works in 2 real steps: first narrow by gait (how the animal moves), then narrow further by family-level track features (toe/claw pattern).**

## The 4 Real Gait Types

- **Diagonal walker** — the normal pattern for predators broadly: dogs, cats, hoofed animals, and humans.
- **Pacer** — the normal pattern for wide-bodied animals (bears, raccoon, opossum, skunk, wolverine, badger, beaver, porcupine, muskrat, marmot) — they move both limbs on one side together rather than alternating sides.
- **Bounder** — the normal pattern for long-bodied, short-legged weasel-family animals (marten, fisher, mink) — front feet reach out, back feet land just behind them.
- **Galloper** — the normal pattern for rabbits, hares, and most rodents (except the wide-bodied beaver, muskrat, marmot, porcupine) — push off with the back feet, land front feet first, bring the back feet forward into position. **Tree-dwelling gallopers land with front feet side by side; ground-dwelling gallopers land with front feet at a diagonal.**

**⚠️ Real caveat: an animal can modify its normal gait depending on circumstances** — treat gait as a strong clue, not an absolute rule.

## Real Family-Level Track Features

| Family | Real members | Key real features |
|---|---|---|
| Cat | Bobcat, lynx, mountain lion | 4 toe pads, **no visible claw print**, moves with purpose, direct-registers paws, well-defined heel pad |
| Dog | Fox, coyote, wolf | **Visible claw print**, 4 toe pads, generally no sense of purpose (fox is an exception — steps cat-like, favors depressions), rounder heel pad |
| Rabbit | Rabbits, hares/jackrabbits | 4 toes, disproportionately large hind feet |
| Rodent | Voles, mice, rats, chipmunks, squirrels, woodchucks, muskrats, beaver | **5 toe prints on rear feet, 4 on front feet** — a consistent rule despite huge size variation between species |
| Weasel | Weasel, mink, marten, fisher, skunk, otter, badger, porcupine, wolverine | **5 toe prints on all feet** |
| Raccoon/opossum/bear | Raccoon, opossum, bear | **5 toe prints, resembling a baby's handprint** |

## A Real Worked Example — Narrowing to Species

**Real scenario from the source:** tracks along a creek bank show 5 toe prints on both front and back feet, with visible claws — **this places it in the weasel family.** The gait is bounding, which **rules out the wide-bodied weasel-family members** (badger, skunk, porcupine, wolverine, which pace instead). The tracks are roughly dime-sized, **ruling out marten and fisher** (larger). They follow the stream bank, stopping at small holes along the edge — and **knowing mink favor exactly this kind of habitat, the tracks are most likely mink.**

## Detailed Version

**The real skill demonstrated by that worked example isn't memorizing a single identifying feature — it's successively eliminating candidates by combining gait, family-level anatomy, size, and known habitat/behavior together.** No single clue was conclusive on its own; the real identification came from stacking several real, individually-ambiguous clues until only one species remained consistent with all of them.
""",
    },
    {
        "title": "Determining Track Age",
        "section": "reference",
        "tags": ["tracking", "survival-skills", "bushcraft"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Track age determination genuinely varies by climate and terrain — real skill here comes from practice and local experience, not a universal formula.** That said, several real factors consistently degrade tracks everywhere, and a real snow-specific timetable gives a workable general guide.

## Real Degrading Factors (any terrain)

Weather (the most recent snow/rain, fog, dew), sun exposure, wind, and soil type (hard/sandy/firm/moist all erode tracks differently).

## A Real Snow Track Erosion Timetable

**The real driving factors for snow-track aging: sunlight exposure and temperature.**

| Time since track made | Real appearance |
|---|---|
| Minutes to 1 hour | Transference visible around the track's outer edges, on top of the snow pack; edges sharp and clean |
| 1-3 hours | Transferred snow has melted, leaving small pockmarks on the surface; track edges slightly rounded |
| 4-24 hours | Surface pockmarks have disappeared; track edges rounded, inside walls still firm |
| 24-72 hours | The top snow layer has begun angling down into the track; the track is filling in and develops an "S" curve shape |

## Real Scat Aging

**Scat dries from the inside first** — meaning relatively wet-looking scat on the outside can actually still be old underneath. **The only reliable way to judge real age is examining the interior**, not the surface. **⚠️ Handle with real caution — assessing scat carries a real disease exposure risk** (see Wildlife & Food-Borne Diseases in a Survival Situation).

## Detailed Version

**The real, most counterintuitive point on this page: a scat's outer appearance can actively mislead you about its age, since the drying process runs opposite to visual intuition (dry outside ≠ necessarily old; wet outside ≠ necessarily fresh).** The same caution — trusting the actual physical evidence over a quick visual impression — applies to the snow-track timetable too: the "S" curve and pockmark details are the real signal, not a guess based on how long ago you think it snowed.
""",
    },
    {
        "title": "Tracking Technique & Direction-Finding",
        "section": "reference",
        "tags": ["tracking", "survival-skills", "navigation"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Real tracking success depends as much on when and how you look as on recognizing the track itself.**

## Real Timing & Positioning

**Early morning or late afternoon is the real best time to track** — the low sun angle casts longer shadows that make tracks far more visible. **When reading a track, position it between yourself and the sun** so the shadow contrast actually works in your favor.

## "Sign Cutting" — Don't Skip Ahead

**Don't move past the last confirmed sign until you've actually found the next one.** In practice, this means working methodically between confirmed points rather than jumping forward on assumption — skipping ahead risks losing the trail entirely if the animal/person changed direction between signs.

## Document Each Track as You Find It

**Sketch and record the initial track in enough detail to recognize it again later** — this real discipline prevents accidentally switching onto a different, similar-looking track partway through a trail and not noticing.

## Real Direction-Finding — by Mover Type

- **A person/animal on foot:** forward movement always pushes snow forward ("fluffing") — **as that pushed snow melts, it leaves pockmarks that reveal the direction of travel.**
- **⚠️ Walking backward in snowshoes does NOT fool an experienced tracker** — it's also genuinely exhausting for the person attempting it, for very little real benefit.
- **A skier:** as a ski pole plants and the ski moves forward, the pole's basket angles forward too, digging an indent on the forward edge — **and the pole tip touches snow just before the pole plants, leaving a short line pointing away from the direction of travel.** Both details reveal direction even without a clear footprint.
- **Snowmobiles/tracked vehicles:** direction is genuinely harder to read here. **Look at the compressed snow "plates" formed inside the track impressions** — the large majority of these plates face the actual direction of travel, though a smaller number will face the opposite way, so look for the dominant pattern rather than any single plate.

## Tracking as a Team ("Sign Cutting" at Scale)

**With at least 2 tracking teams, the process can speed up significantly:** both teams document and sketch the same initial track together; one team continues tracking while the other works ahead until it positively re-confirms the same track further along the trail — marking that confirmed point for reference as the search continues.

## Detailed Version

**The real, shared insight across every direction-finding method here: a moving body or object leaves subtle secondary evidence (melting fluffed snow, a pole-basket indent, compressed-snow plates) that persists even when the obvious footprint itself becomes ambiguous or absent.** Learning to read that secondary evidence, rather than relying only on a clear footprint, is what separates reliable tracking from guessing.
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
