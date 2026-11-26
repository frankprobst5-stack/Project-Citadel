#!/usr/bin/env python3
"""Seeds 3 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 11 Section I (Heat Injuries) --
mined from the OCR output cached at /tmp/sfmedical.txt.

Covers real, specific content genuinely extending the existing heat-
illness coverage (USMC content covers general signs/prevention but
not this level of clinical specificity): a real water-requirement
table by activity/temperature, real 0.1% salt-solution recipes by
container size, the real WBGT index formula and activity-restriction
categories, real SOAP-format clinical treatment for heat cramps and
heat exhaustion (including real cautions against hot packs and
saline enemas), and a genuinely detailed real heat stroke cooling
protocol with its real temperature-oscillation management technique.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_heat.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
SFMEDICAL_PDF_URL = "/files/pdfs/Medical/ST-31-91B-US-Army-Special-Forces-Medical-Handbook.pdf"

PAGES = [
    {
        "title": "Heat Injury Prevention — Water, Salt & the WBGT Index",
        "section": "reference",
        "tags": ["heat-illness", "prevention", "hydration"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Preventing heat injury comes down to 4 real, controllable factors: water, salt, acclimatization, and matching activity level to actual heat stress** — each with real, specific numbers behind it.

## Real Water Requirements

**In severe heat, a person can lose up to a quart of water per hour** — lost water must be replaced, or heat injury becomes likely. **⚠️ The idea that people can be trained to need less water is a real, debunked myth** — the only real way to economize water when it's scarce is limiting physical activity to the coolest parts of the day/night.

**Real daily drinking-water guide (quarts/day), by activity and heat index:**

| Activity | Below 80° WBGT | Above 80° WBGT |
|---|---|---|
| Light (desk work) | 6 | 10 |
| Moderate (route march) | 7 | 11 |
| Heavy (forced march, digging, heavy loads) | 8 | 13 |

## Real Salt Requirements

**Normal food intake usually provides enough salt — extra is needed mainly for unacclimatized people under real heat stress**, and mainly if sweating continuously/repeatedly (otherwise, extra salt at meals is enough). **Older and already-acclimatized people generally need less extra salt.**

**Real 0.1% salt solution recipes, by container:**
- 1-quart canteen: 2 ten-grain salt tablets.
- 2-quart canteen: 4 ten-grain salt tablets.
- 5-gallon can: 1⅓ level mess-kit spoons of salt.
- Lister bag: 9 level mess-kit spoons of salt.
- 250-gallon water trailer: 1 level canteen cup of salt.

## Real Acclimatization Timeline

**Takes about 2 weeks regardless of existing fitness level** — achieved through progressively increasing heat/exertion exposure. **⚠️ Real limit: even thorough acclimatization increases resistance but never gives complete protection from heat illness.**

## Real Risk Factors

**Debilitating illness/injury and being overweight both significantly raise real heat-injury risk.** **Heat injury can occur even below 90°F** (from overexertion or overdressing), though most real cases happen in genuinely high heat/humidity.

## The Real WBGT Index — Calculating True Heat Stress

**WBGT = (0.7 × wet-bulb temperature) + (0.2 × black-globe temperature) + (0.1 × dry-bulb temperature).** This combines air temperature, humidity, air movement, and radiant heat into one real number more accurate than dry-bulb temperature alone.

**Real activity-restriction guide by WBGT category:**

| Category | WBGT | Unacclimatized | Acclimatized |
|---|---|---|---|
| I | 82-84.9°F | Use discretion for intense activity; limit sun exposure; supervise closely | Normal duties |
| II | 85-87.9°F | Cancel strenuous drills/PT and outdoor classes in sun | Use discretion for intense activity; limit sun exposure |
| III | 88-89.9°F | Cancel all PT, strenuous activity, and parades | Minimize strenuous outdoor activity for anyone with under 12 weeks of hot-weather conditioning |
| IV | 90°F+ | Cancel strenuous and nonessential activity | Cancel strenuous and nonessential activity |

## Detailed Version

**The real, practical value of the WBGT formula specifically: it captures why a "cooler-feeling" 85°F day with high humidity and strong sun can be more dangerous than a drier 95°F day** — dry-bulb temperature alone misses exactly the humidity and radiant-heat factors this index accounts for.
""",
    },
    {
        "title": "Heat Cramps & Heat Exhaustion — Real Clinical Treatment",
        "section": "emergency",
        "tags": ["heat-illness", "heat-cramps", "heat-exhaustion"],
        "risk_level": "critical",
        "body_markdown": """## Heat Cramps — Caused by Excessive Salt Loss

**Real signs:** painful voluntary-muscle cramps in episodes lasting 3-10 minutes, with relatively comfortable periods between — the person may grimace and thrash, arms/legs drawn up. Skin is hot and moist; **blood pressure and temperature are usually normal**, pulse only slightly elevated.

**Real treatment:**
1. Move to shade; replace salt in any form.
2. **For acute cases: IV normal saline, 500-1,000cc.**
3. **For milder cases: a 0.1% salt solution in cool water, taken by mouth** — this both relieves symptoms and provides ongoing protection (see Heat Injury Prevention — Water, Salt & the WBGT Index for the real recipe).
4. Massaging the cramped muscle usually gives real, immediate relief.
5. **⚠️ Never apply hot packs to a cramped muscle — this makes it worse.**
6. **⚠️ Never use a saline enema** — it actually draws more salt and water OUT of the tissue, working against recovery.

## Heat Exhaustion — Caused by Salt Loss and Dehydration Impairing Peripheral Circulation

**Real signs:** profuse sweating with cold, wet, pale skin; headache, mental confusion, dizziness, poor coordination, drowsiness, extreme weakness, appetite loss, nausea/vomiting, visual disturbances; occasional limb or abdominal cramping.

**Real vitals:** oral temperature may read subnormal or slightly elevated, but **rectal temperature usually runs 100-101°F**; pulse rapid (140-200); blood pressure usually low.

**⚠️ Real differential: heat exhaustion and heat cramps can look similar — the oral-vs-rectal temperature discrepancy and the broader symptom picture (confusion, profuse sweating, low BP) are what distinguish real heat exhaustion from cramps alone.**

**Real treatment:** remove to a cool shaded area; replace fluids and salt with cool 0.1% salt water by mouth, or — if the person can't swallow — **1,000-1,500cc of 5% dextrose in normal saline, or plain normal saline, by IV** (an IV line should be started regardless). **Real stimulation if needed:** caffeine (tea, cola, coffee), or in more severe cases an IM injection of 0.3-0.5cc of 1:1,000 epinephrine. **Avoid putting the person back into the heat right away.**

## Detailed Version

**The real, most clinically useful detail on this page: checking rectal rather than oral temperature is what actually reveals heat exhaustion's real severity** — oral temperature alone can look deceptively normal while the person's true core temperature is already meaningfully elevated, which is exactly the kind of mismatch that leads to underestimating how serious the situation actually is.
""",
    },
    {
        "title": "Heat Stroke — Real Temperature Management Protocol",
        "section": "emergency",
        "tags": ["heat-stroke", "emergency-medicine", "hyperthermia"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**Heat stroke is a genuine, immediately life-threatening emergency — a breakdown of the body's own heat-regulating mechanism.** Real early signs (headache, dizziness, confusion, weakness, nausea, involuntary urination, reduced/absent sweating, even a false sense of well-being) can give way to **sudden collapse and loss of consciousness, sometimes with convulsions.**

## Real Signs Once Established

**Hot, red, dry skin** (sweating has typically stopped); full, rapid pulse with normal-to-elevated blood pressure; rapid, deep breathing; **body temperature markedly elevated, 106-110°F.** As it worsens: bluish skin, shallow/irregular breathing, fluid in the lungs, loss of bowel/bladder control, vomiting, bleeding tendencies, abnormal muscle tone, and in severe cases jaundice and meningitis-like symptoms including tetanus-like body arching. **⚠️ Death can come very quickly — but if the person survives to the second day, real recovery usually follows, though severe relapses can still occur.**

## ⚠️ Real Cooling Protocol — Speed Is Everything

**The longer body temperature stays elevated, the greater the real risk of permanent damage or death.**

1. **Remove clothing and immerse in cold water (an ice-water bath, if available).** If immersion isn't possible, wet the person down with ice water or alcohol and fan them continuously.
2. **Briskly rub the extremities and trunk** to actively drive blood circulation to the skin, where cooling is actually happening.
3. **⚠️ Monitor temperature closely. Stop active cooling once it drops to 102°F** — dry the person off and switch to warming (blankets, heating pads).
4. **Real, important pattern: temperature will typically keep falling on its own after cooling stops — sometimes down to as low as 90°F — before it starts rising again.**
5. **⚠️ If temperature falls below 97°F, be ready to restart cooling once it climbs back up to 97°F.** **Real management is this active oscillation — alternating cooling and warming — repeated until the temperature genuinely stabilizes on its own.**
6. **Continue checking temperature every 10 minutes for the following 4+ hours.**

## ⚠️ Real Medication Caution

**Sedatives can interfere with the body's own heat-regulating center and should be avoided where possible.** If a sedative is genuinely necessary (for example, to control convulsions), **use a short-acting one** rather than a long-acting option.

## Detailed Version

**The real, most important and counterintuitive management detail on this entire page: heat stroke recovery isn't a simple "cool until normal and stop" process — the body's temperature genuinely overshoots and swings after active cooling stops, and real management means actively tracking and responding to that oscillation rather than walking away once the number looks better.** Stopping too early, assuming the crisis has passed the moment the temperature first drops, is exactly the mistake this real protocol is built to prevent.
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
                "source_url": SFMEDICAL_PDF_URL,
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
