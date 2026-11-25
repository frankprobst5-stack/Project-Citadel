#!/usr/bin/env python3
"""Seeds 4 real pages from the USMC Winter Survival Course Handbook's
Mountain Weather chapter -- mined from the real text layer already
extracted in this session (/tmp/usmcwinter.txt, pages 15-1 through
15-11). Real, substantive field meteorology -- genuinely useful for
anyone trying to forecast weather without instruments, not specific
to combat or military operations.

Covers: real atmospheric pressure/humidity/wind fundamentals
(including real adiabatic lapse rates and real mountain-specific
anabatic/katabatic winds), the 3 real ways air gets lifted/cooled
into precipitation and the real cloud types/subtypes this produces,
real cloud-progression signatures for warm/cold/occluded fronts, and
a real, extensive list of natural weather-prediction signs.

This chapter's companion chapter in the source (Chapter 16,
Introduction to Evasion) is entirely military/combat-evasion-specific
(SAFE areas, Evasion Plans of Action, enemy intelligence) and is
deliberately NOT mined -- it has no real civilian survival
application.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_weather.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Mountain Weather Basics — Pressure, Humidity & Wind",
        "section": "reference",
        "tags": ["weather", "meteorology", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Real weather comes down to a few interacting factors: air pressure, moisture content, and wind** — understanding how they relate makes field weather prediction genuinely possible without instruments.

## Pressure — the Real Driver

**Air behaves much like a liquid in the atmosphere.** A "high" has more of this atmospheric liquid pressing down (a ridge); a "low" has less (a trough). **High pressure flows outward to equalize; low pressure draws air inward and, once it reaches equal pressure, keeps building vertically — and that vertical buildup is what actually creates the turbulence behind bad weather.** **Real reference points:** average sea-level pressure is 29.92 inches of mercury / 1,013 millibars; pressure drops substantially with altitude (roughly 500 millibars at 18,000 feet). **Lower pressure generally means a higher real chance of rain and strong wind.**

## Humidity & Condensation

**Warmer air can hold more water vapor.** Air holding all the vapor it can is "saturated" (100% relative humidity) — cool it further and the excess vapor condenses into visible droplets. **The exact condensation temperature depends on how much moisture is already present** — very humid air can condense around 68°F, while dry air might not condense until near or below freezing.

**Real adiabatic lapse rate (how air cools as it rises, warms as it descends):** saturated (moist) air cools about 2.2°F per 1,000 feet of altitude gained; dry air cools roughly 5.5°F per 1,000 feet — **a real, meaningful difference that explains why moist and dry air masses behave so differently as they rise.**

## Wind — Real Patterns

**Winds are named for the direction they blow FROM.** Real global surface patterns: Polar Easterlies (cold air settling and flowing from the poles), Prevailing Westerlies (from ~30°N, moving from the west), Northeast Tradewinds (from ~30°N, moving from the northeast). **The jet stream** — a fast-moving (often 250+ mph), meandering high-altitude current near the tropopause — drives real day-to-week weather changes through its long waves, while smaller short waves within it drive hourly changes.

**Real mountain-specific winds (don't necessarily signal incoming weather on their own):**
- **Anabatic wind** — blows UP a mountain valley, replacing rising warm air; usually light.
- **Katabatic wind** — blows DOWN a valley slope as air cools; can occasionally be strong.

## Air Masses — the Real Building Blocks

Named by where they form: **maritime** (over water) vs. **continental** (over land); **polar** (above 60°N) vs. **tropical** (below 60°N). Combined, this gives 4 real types: **Continental Polar** (cold, dry), **Maritime Polar** (cold, wet), **Continental Tropical** (warm, dry), **Maritime Tropical** (warm, wet). **⚠️ Different air masses genuinely don't mix — when two different masses collide, that collision is what creates a front** (see Reading Weather Fronts — Warm, Cold & Occluded).

## Detailed Version

**The real, unifying idea tying pressure, humidity, and wind together: weather isn't random — it's the predictable result of air moving between high and low pressure while carrying a specific moisture load, and the adiabatic lapse rate is the real physical mechanism connecting elevation change to actual precipitation.** Every later topic in this chapter (clouds, fronts, nature signs) is really just visible evidence of these same underlying mechanics playing out.
""",
    },
    {
        "title": "Lifting, Cooling & Cloud Types",
        "section": "reference",
        "tags": ["weather", "clouds", "meteorology"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Air releases its moisture (as rain, snow, fog, or dew) once it's cooled past its saturation point — and there are 3 real ways that cooling happens.**

## The 3 Real Lifting Mechanisms

1. **Orographic uplift** — air is pushed up and over higher ground (a mountain). The real adiabatic cooling this causes (see Mountain Weather Basics) can push it past saturation, producing real precipitation on the windward side.
2. **Convection** — typically a summer effect: the sun heats the surface, which heats air directly above it, pushing it straight upward until it saturates.
3. **Frontal lifting — the real source of most precipitation.** When two air masses of different temperature/moisture meet, they don't mix; the warmer, less dense air gets forced upward, cools, and saturates.

**Real combinations of more than one mechanism at once are common** — they're not mutually exclusive.

## Cloud Types — Real Forecasting Value in Each

### Cirrus
**Thin, feathery, high-altitude (20,000-35,000ft) ice-crystal clouds** — genuinely useful because they can give **up to 24 hours of warning** of approaching bad weather, sometimes hundreds of miles ahead of a real warm front. Scattered wisps ("mare's tails") or light cirrus layers often mean fair weather for now, **but can be an early signal that lower clouds, precipitation, and a front are still on the way.**

### Cumulus — 3 Real Subtypes Worth Distinguishing
1. **Cotton-puff cumulus** — fair weather for now, but **watch for growth into the next two stages.**
2. **Towering cumulus** — cauliflower-shaped, driven by real vertical lift (convection, orographic lift, or frontal lifting).
3. **Cumulonimbus** — the real "thunderhead." Violent updrafts carry the cloud top to extreme altitude; **this is the real source of thunderstorms, hail, heavy rain, and tornadoes.** A flat anvil shape at the top signals the storm beginning to dissipate.

### Stratus
**Flat, layered, fog-like clouds** with a uniform gray base — genuinely resistant to vertical development. They often produce light drizzle, light snow, or fog, **but rarely heavy rain/snow**, since they lack the real vertical lift that drives those.

## Detailed Version

**The real, practical payoff of distinguishing cumulus subtypes specifically: a cotton-puff cumulus and a cumulonimbus look related at a glance, but one is fair weather and the other is a genuine severe-weather threat.** Watching for the real progression from puffy to towering to anvil-topped is exactly how a cloud-watcher gets real advance warning rather than being surprised by a storm that "appeared out of nowhere."
""",
    },
    {
        "title": "Reading Weather Fronts — Warm, Cold & Occluded",
        "section": "reference",
        "tags": ["weather", "fronts", "meteorology"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**You can't see a front directly, but you CAN see its real cloud progression — learning that progression is a real, practical way to forecast incoming weather hours to a day in advance.**

## Warm Front — Real Cloud Progression

**Happens when warm air advances over slower-moving or stationary cold air.** Since warm air is less dense, it rises and slides up over the cooler air. **The real sequence to watch for: cirrus clouds first → stratus as the warm air continues rising and cooling → progressively darkening nimbostratus (literally "rain cloud") as moisture builds → precipitation.**

## Cold Front — Real Cloud Progression

**Happens when a colder, denser air mass overtakes a slower/stationary warmer one**, sliding underneath and forcing the warm air upward. **The real sequence: cirrus → cirrocumulus → cumulus → cumulonimbus** — a cold front's arrival is often marked by this faster, more abrupt progression than a warm front's.

## Occluded Front

**Cold fronts move faster than warm fronts, so a cold front eventually catches up to and overtakes a warm one** — progressively lifting the warm air entirely off the surface. The dividing zone is called a **cold occlusion** if the air behind is colder than the air ahead, or a **warm occlusion** if the air behind is actually warmer. **Occlusions are real the most common front type experienced over most land areas.** **⚠️ Real complicating factor: orographic uplift (mountain terrain) can add its own cumulus clouds into the mix, making a front's actual type harder to read from clouds alone** — an occlusion's cloud progression is genuinely a blend of both the warm-front and cold-front sequences.

## Detailed Version

**The real, most useful single skill from this page: recognizing which direction the cloud progression is running (cirrus-to-stratus-to-nimbostratus vs. cirrus-to-cumulus-to-cumulonimbus) tells you which kind of front is approaching before it arrives** — and that distinction matters because a warm front's precipitation tends to arrive more gradually, while a cold front's arrival is often faster and more abrupt.
""",
    },
    {
        "title": "Natural Signs of Incoming Weather",
        "section": "reference",
        "tags": ["weather", "nature-signs", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**No single natural sign is 100% reliable on its own — but combining several together, along with real local experience, gives genuinely better-than-chance predictions.** The real signs below have been field-tested for reasonable accuracy; treat them as real, weighted evidence, not certainty.

## Real Sky & Atmospheric Signs

- **Jet contrails that don't dissipate within 2 hours** indicate a low-pressure area — often about 24 hours ahead of an approaching front.
- **Lenticular clouds** (lens-shaped, wind-sculpted) indicate real moisture and high winds aloft — ahead of a cold front, expect the clouds and wind to lower from there.
- **A gray, overcast evening sky** means atmospheric dust has become overloaded with moisture — favors rain.
- **A gray morning sky** (from dust collecting moisture in the lower atmosphere, with dry air above) favors a fair day.
- **A green tint atop the setting sun against a clear horizon** signals probable fair weather for roughly the next 24 hours.
- **A late-afternoon rainbow** signals fair weather ahead; **a morning rainbow signals prolonged bad weather instead** — timing of day meaningfully changes what the same sign means.
- **A corona (a ring around the sun or moon) growing larger over time** means water droplets are evaporating — clearing weather. **A corona shrinking over time** means droplets are growing into real cloud/rain — precipitation likely.
- **In the Northern Hemisphere, wind from the south often signals a low-pressure system and real incoming rain** — "winds from the south bring rain in its mouth."

## Real Animal & Insect Signs

- **Spider behavior:** on a calm, fair day, spiders spin long filaments and actively patrol them; **when precipitation is imminent, they shorten/tighten their webs and sit still near the center.**
- **Insects become noticeably more irritating 2-4 hours before a storm.**
- **Bees swarming** signals fair weather for at least the next half day.
- **Large game (deer, elk) feeding unusually heavily 4-6 hours before a storm** — real anticipatory behavior.
- **A quiet period where distant sounds carry unusually clearly** often precedes a storm by a couple of hours, as wildlife activity drops off.

## Real Fire, Water & Dew Signs

- **Campfire smoke that rises briefly, then beats back downward,** signals an approaching storm; **steadily rising smoke indicates continuing fair weather.**
- **Natural springs flowing at a noticeably higher rate** often precede a storm — driven by dropping barometric pressure. **Real side effect: ponds with decaying vegetation at the bottom can become momentarily more polluted** as this happens.
- **Heavy dew or frost in the morning** signals fair weather for the rest of the day (the atmosphere's moisture settled onto the ground rather than falling as precipitation) — can indicate up to 12 hours of continued good conditions.

## Detailed Version

**The real, repeated instruction worth following literally: use multiple signs together, not any single one alone.** A single spider's web or one rainbow might be coincidence; several of these signs agreeing (a shrinking corona, south wind, irritable insects, and a smoky campfire beating downward, say) is real, meaningfully stronger evidence that weather is actually about to change.
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
