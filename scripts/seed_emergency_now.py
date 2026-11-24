#!/usr/bin/env python3
"""Seeds the first real batch of "Emergency Now" quick-reference pages --
the start of the Survival & Emergency Reference Library build-out
(2026-11-24). Every page below was drafted against a real, fetched,
cited government source (CDC, Indiana DHS/Stop the Bleed) -- not
written from memory -- which is why verification_status='verified' is
honestly earned here, not just applied. See wiki.py's own
VERIFICATION_STATUSES docstring for what that status is supposed to
mean: a real provenance record, not decoration.

Each page follows the Quick/Detailed split: a short "act now" version
first, a fuller explanation after, matching the Emergency Now design
(the single feature most worth getting right, since someone reading
this is often mid-emergency, not browsing).

Idempotent by title, same pattern as scripts/migrate_manual_to_wiki.py.
This is phase 1 of many -- see the chat history for the full proposed
structure (26 sections). Starting narrow and real beats starting broad
and fabricated.

Usage:
    python3 scripts/seed_emergency_now.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    {
        "title": "Severe Bleeding — Stop the Bleed",
        "tags": ["bleeding", "trauma", "first-aid"],
        "risk_level": "critical",
        "source_url": "https://www.in.gov/dhs/get-prepared/emergencies/stop-the-bleed-bleeding-control-for-the-injured/",
        "body_markdown": """## Quick Version

1. **Call 911** — have someone else call while you start working.
2. **Expose the wound.** Find exactly where the bleeding is coming from.
3. **Pack the wound** with gauze, a clean cloth, clothing — even your bare hands — stuffing it directly into the wound, not just laid on top.
4. **Apply firm, continuous pressure with both hands** directly on the packed wound. Keep holding for at least 5 minutes before you check it.
5. **If blood soaks through, add more bandages on top** — don't remove what's already there.
6. **If bleeding is life-threatening and pressure isn't controlling it, apply a tourniquet** 2-3 inches above the wound (never directly over a joint). Tighten until bleeding stops or is significantly reduced.
7. **Tell first responders how long the tourniquet has been on** the moment they arrive. Do not loosen or remove it yourself.

**Do not:** stop pressing to "check" the wound repeatedly — that's what lets bleeding restart. Do not remove a tourniquet once applied.

## Detailed Version

Life-threatening external bleeding is one of the few true seconds-matter emergencies a bystander can directly affect the outcome of — it's the whole premise behind the national "Stop the Bleed" campaign. The sequence above (call → expose → pack → pressure → tourniquet if needed) is the real, current guidance from Indiana's Department of Homeland Security's own Stop the Bleed program, cross-checked against the broader Stop the Bleed campaign's own published steps.

A tourniquet is not a last resort to fear — properly applied, it is safe for several hours and is explicitly part of the first-line response when direct pressure and wound packing aren't enough, not something to only attempt after everything else has failed.

**What this page doesn't cover:** actual tourniquet application technique (exact device use, windlass mechanics) and hands-on practice — that genuinely requires real training, not a wiki page. If you own a trauma kit, take a real Bleeding Control Basic course (many fire departments and hospitals offer these free); this page is a memory-jogger for a real emergency, not a substitute for that training.
""",
    },
    {
        "title": "Power Outage — Food, Medication & Carbon Monoxide Safety",
        "tags": ["power-outage", "food-safety", "carbon-monoxide", "generator"],
        "risk_level": "critical",
        "source_url": "https://www.cdc.gov/natural-disasters/response/what-to-do-protect-yourself-during-a-power-outage.html",
        "body_markdown": """## Quick Version

- **Refrigerator:** safe up to **4 hours** without power, unopened. Don't open the door to check.
- **Freezer:** a full freezer stays safe **48 hours** unopened (**24 hours** if only half-full).
- **After that, or if anything thawed:** throw out perishables — meat, poultry, fish, eggs, leftovers. When genuinely unsure, throw it out.
- **Refrigerated medication:** if the power's been out a day or more, throw away any medication that needed refrigeration *unless its own label says otherwise* — replace it as soon as you can.
- **Never run a generator, pressure washer, or any gasoline engine indoors, in a garage, or within 20 feet of any window, door, or vent** — even with the garage door open. Carbon monoxide from these kills quickly and has no smell.
- **Run a battery-powered or battery-backup CO detector** any time a generator is running.
- **CO poisoning symptoms:** headache, dizziness, weakness, nausea, vomiting, chest pain, confusion. If suspected, get outside immediately and call 911 or Poison Control (1-800-222-1222).

## Detailed Version

This is drawn directly from the CDC's own power-outage guidance. The 4-hour/48-hour figures assume the door stays shut the whole time — every door-opening lets warm air in and shortens that window for real, not just in theory.

Generator placement is the single biggest preventable cause of death in outages with portable generators: 20 feet is the CDC's own minimum distance from any opening into the home, not a rough guideline — carbon monoxide can still reach a house through a door or window even with the generator "outside." Use an extension cord rated for the load rather than moving the generator closer for convenience.

If someone shows CO poisoning symptoms, don't wait to see if it passes — get them into fresh air immediately and call for help. CO poisoning can be fatal within hours.
""",
    },
    {
        "title": "Hypothermia — Recognizing and Responding",
        "tags": ["cold-weather", "hypothermia", "first-aid"],
        "risk_level": "high",
        "source_url": "https://www.cdc.gov/natural-disasters/psa-toolkit/recognizing-hypothermia.html",
        "body_markdown": """## Quick Version

**Warning signs in adults:** shivering, exhaustion, confusion, fumbling hands, memory loss, slurred speech, drowsiness.

**Warning signs in babies:** bright red, cold skin, and very low energy.

**If you see these signs: seek immediate medical attention.** If you can't get help right away:
1. Move the person into a warm room or shelter.
2. Remove any wet clothing.
3. Warm them with an electric blanket, or skin-to-skin contact if nothing else is available.
4. Give warm beverages **only if the person is fully conscious** — never to someone confused or drowsy.
5. **Never give alcohol.**

## Detailed Version

Shivering stopping is not a good sign — it can mean the body has moved past the point where it can generate its own heat, not that the person is recovering. Confusion, slurred speech, and fumbling hands are the signs that distinguish hypothermia from just being cold; they mean the body's core temperature has actually dropped, and this needs real medical attention, not just a blanket and time.

This is drawn directly from CDC guidance (Recognizing Hypothermia). The "Rule of Threes" sometimes cited for cold survival (a rough "3 hours without shelter in harsh conditions" type mnemonic) is a teaching tool, not a measured countdown — real survival time varies enormously with wind, wetness, body size, health, and exertion, so don't treat any fixed number as a real deadline.
""",
    },
    {
        "title": "Heat Exhaustion & Heat Stroke",
        "tags": ["heat", "heatstroke", "first-aid"],
        "risk_level": "critical",
        "source_url": "https://www.cdc.gov/extreme-heat/signs-symptoms/",
        "body_markdown": """## Quick Version

**Heat stroke (medical emergency — call 911 immediately):** body temperature 103°F+, hot/red/dry or damp skin, fast strong pulse, headache, dizziness, nausea, confusion, loss of consciousness.
- Call 911. Move the person to a cooler place. Cool them with cool cloths or a cool bath. **Do not give them anything to drink.**

**Heat exhaustion:** heavy sweating, cold/pale/clammy skin, fast weak pulse, nausea/vomiting, muscle cramps, tiredness, dizziness, headache, fainting.
- Move to a cool place, loosen clothing, apply cool wet cloths or a cool bath, sip water.
- **Get medical help if:** vomiting, symptoms worsen, or symptoms last longer than 1 hour. Untreated heat exhaustion can progress to heat stroke.

## Detailed Version

The key distinction: heat stroke is a 911 emergency with altered mental state and very high body temperature — you do NOT give fluids to someone that confused, since they may not be able to swallow safely. Heat exhaustion is the earlier, less severe stage where the person is still clear-headed enough to safely sip water themselves.

Both conditions are CDC-documented (Signs and Symptoms of Heat-Related Illness). Heat stroke risk rises sharply in situations preparedness docs specifically flag: a vehicle stranded in heat, physical exertion in extreme temperatures, or extended power outages without cooling — treat any of those as real risk multipliers, not just discomfort.
""",
    },
    {
        "title": "Making Water Safe in an Emergency",
        "tags": ["water", "water-treatment", "boil-water"],
        "risk_level": "critical",
        "source_url": "https://www.cdc.gov/water-emergency/about/index.html",
        "body_markdown": """## Quick Version

**Boiling (most effective, no equipment needed beyond heat):**
- Bring clear water to a rolling boil for **1 minute**.
- Above 6,500 feet elevation, boil for **3 minutes**.

**If you can't boil — unscented household bleach (5-9% sodium hypochlorite):**
- 1 quart/liter: 2 drops
- 1 gallon: 8 drops
- 5 gallons: 40 drops
- Stir, then **let stand at least 30 minutes** before drinking. If it doesn't smell faintly of chlorine afterward, repeat the dose and wait another 15 minutes.

**For 1% concentration bleach:** 10 drops/quart, 40 drops/gallon, 200 drops/5 gallons — same 30-minute wait.

## Detailed Version

**What boiling and bleach CANNOT do, per CDC's own guidance:** you cannot make water containing fuel, toxic chemicals, or radioactive materials safe by boiling or disinfecting it — no amount of either fixes chemical contamination. If you suspect chemical or fuel contamination (a flood that passed through an industrial area, a known spill), don't drink that water at all regardless of treatment.

Chemical disinfectants (bleach, tablets) are also weaker than boiling against two specific parasites, *Cryptosporidium* and *Giardia* — they may survive chemical treatment that would be killed by boiling.

**Filters:** a portable filter needs roughly a 1-micron pore size to remove parasites and 0.3-micron to remove bacteria — many consumer filters will NOT remove viruses at all. Check what your specific filter is actually rated for; don't assume "filtered" means "safe from everything."

Only use plain, unscented household bleach — scented bleach, color-safe bleach, and bleach with added cleaners contain other chemicals you don't want in drinking water.
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
            print(f"WOULD CREATE: {page['title']} (risk={page['risk_level']}, source={page['source_url']})")
            created += 1
            continue
        res = requests.post(
            f"{args.base_url}/api/wiki/pages",
            headers=headers,
            json={
                "section": "emergency",
                "title": page["title"],
                "body_markdown": page["body_markdown"],
                "tags": page["tags"],
                "source_url": page["source_url"],
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
