#!/usr/bin/env python3
"""Seeds 5 final real pages from the USMC Winter Survival Course
Handbook's Survival Medicine chapter -- mined from the real text
layer already extracted in this session (/tmp/usmcwinter.txt, pages
14-11 through 14-17). This closes out Chapter 14.

Covers: dehydration and heat illness in a survival context, altitude
sickness (AMS/HACE/HAPE) with real altitude thresholds and ascent-
rate prevention numbers, carbon monoxide poisoning near a shelter
fire, real survival wound care (including the real "open treatment"
method and the 4 life-saving steps), casualty evacuation planning
(the real APASSNGG acronym), and real wildlife/food-borne disease
prevention.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_survival_medicine2.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Dehydration & Heat Illness in Survival Situations",
        "section": "reference",
        "tags": ["dehydration", "heat-illness", "survival-skills"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Dehydration is the #2 leading cause of death in survival situations** (after hypothermia) — and it compounds nearly every other problem a survival situation creates.

## Real Signs of Dehydration

Headache and nausea, dizziness and fainting, cramps (both abdominal and in the limbs), weakness and lethargy, and dark, strong-smelling urine.

## Real Prevention

- **Drink water when eating** — digestion itself uses water. **If you have food but no water source, don't eat until you find water** — eating without enough water to digest it makes things worse, not better.
- Conserve energy — pace yourself rather than overexerting.
- **Drink 6-8 quarts per day when water is available — continuously through the day, not just when thirsty.**
- Monitor your own urine color as a real ongoing check.
- **Don't rely on thirst as your indicator** — by the time you're thirsty, you're already somewhat behind.

## Real Heat-Related Illnesses (all driven by dehydration)

- **Heat syncope:** fainting from heat-driven blood vessel dilation.
- **Heat exhaustion:** body salt loss plus dehydration from sweating becomes severe enough that blood pressure can't be maintained — **this can progress into heat stroke if not addressed.** Signs: headache, nausea, dizziness, fatigue, fainting.
- **Heat stroke:** the body's cooling mechanism fails outright. Signs: everything from heat exhaustion, plus possible delirium or coma, pinpoint pupils, flushed skin — **sweating may be present or may have stopped entirely, which is itself a bad sign, not a reassuring one.**
- **Heat cramps:** painful muscle spasms from salt loss.

**Real prevention for all of these:** dress appropriately, rest adequately, and maintain real water intake — the same core actions address every heat-illness category above.

## Detailed Version

**The real, easy-to-miss connection: dehydration isn't just its own standalone problem — it's the shared root cause behind an entire cluster of heat-related illnesses that can otherwise look like separate, unrelated conditions.** Fixing hydration genuinely addresses most of this cluster at once, which is why it gets treated as the first and most important prevention step rather than one tip among many.
""",
    },
    {
        "title": "Altitude Sickness — AMS, HACE & HAPE",
        "section": "emergency",
        "tags": ["altitude-sickness", "ams", "hace", "hape"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Rapid ascent to high altitude without time to acclimatize causes a real, predictable spectrum of illness — from mild and self-limiting (AMS) to genuinely fatal (HACE, HAPE).** The real statistics: roughly 25% of people who rapidly ascend to 8,000-9,000ft develop AMS; **virtually everyone unacclimatized who rapidly reaches 11,000-12,000ft does.**

## Acute Mountain Sickness (AMS)

**Signs:** apathy, dizziness, easy fatigue, nausea, decreased appetite, headache. **This can be mistaken for dehydration** — the real way to tell them apart: if fluid intake has genuinely been adequate and the headache still persists, that points toward AMS rather than simple dehydration.

## HACE — High Altitude Cerebral Edema (swelling of the brain)

**Signs are similar to AMS, but with real additions: bizarre behavior, hallucinations, confusion, and in severe cases coma.** This is a real escalation beyond AMS, not just "worse AMS."

## HAPE — High Altitude Pulmonary Edema (fluid filling the lungs)

**Signs:** a persistent cough, sometimes with pink, frothy sputum, shortness of breath, disorientation, fainting, cool/clammy skin, blue-tinted lips.

## ⚠️ Treatment for HACE and HAPE

**Descend. Descend. Descend.** Both conditions can be fatal, and the real, primary treatment is getting to lower altitude as quickly as safely possible — not waiting to see if symptoms resolve in place.

## Real Prevention — Ascent Rate Limits

**Gain elevation slowly.** Below 10,000ft: no faster than 1,000ft per day. **Above 14,000ft: no faster than 500-1,000ft per day.** Build in real rest/acclimatization time rather than pushing straight through.

## Detailed Version

**The real relationship between these three conditions worth keeping: AMS, HACE, and HAPE are not three unrelated diseases — they're a real severity spectrum of the same underlying problem (the body failing to adapt fast enough to reduced oxygen at altitude).** Treating early AMS symptoms seriously, rather than pushing on and hoping they pass, is the real way to avoid the far more dangerous HACE/HAPE stages — and the single most effective intervention at any point on that spectrum is the same: stop ascending, and descend if symptoms are already present.
""",
    },
    {
        "title": "Carbon Monoxide Poisoning in Shelters",
        "section": "emergency",
        "tags": ["carbon-monoxide", "shelter", "fire-safety"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Carbon monoxide (CO) is a heavy, odorless, colorless, tasteless gas from incomplete combustion — and it's lethal even when there's still adequate oxygen in the air, because hemoglobin binds CO roughly 210 times more readily than it binds oxygen.** CO effectively displaces oxygen from your blood's actual transport system, not from the air itself.

## Real Signs

**Mild cases:** dizziness, headache, confusion. **Severe cases:** deep coma, and sudden respiratory arrest can occur. **⚠️ The textbook "cherry-red lips" sign is real but is a very late and severe indicator — by the time it appears, skin is more commonly found pale or blue instead.** Don't wait for cherry-red lips to suspect CO poisoning.

**⚠️ Suspect CO poisoning whenever someone in a poorly ventilated space suddenly collapses** — and recognize that if everyone present is affected simultaneously, the condition can be very easy to miss, since there's no unaffected person left to notice the pattern.

## Real Treatment

1. **Immediately remove the person from the contaminated area.**
2. **Mild cases (person never lost consciousness):** fresh air and light activity for a minimum of 4 hours; give supplemental oxygen if available.
3. **More severe cases may require rescue breathing.**
4. **The lungs clear CO within a few hours** once removed from the source — recovery is generally real and fast once exposure stops.

## Real Prevention

**Ensure adequate ventilation whenever using a fire near your shelter** — this single step prevents the entire problem; see Expedient Shelter Basics — Criteria, Natural Hazards & Selection's ventilation criterion.

## Detailed Version

**The real, counterintuitive danger worth remembering: CO poisoning doesn't require a smoky, obviously unsafe-feeling fire — it can build up from a well-behaved fire in an enclosed, poorly ventilated space, with no smell or visible warning sign at all.** This is exactly why ventilation is treated as a mandatory shelter criterion rather than a nice-to-have, and why "the fire looks fine" is not a reliable safety check on its own.
""",
    },
    {
        "title": "Survival Wound Care & Casualty Evacuation",
        "section": "emergency",
        "tags": ["wound-care", "casevac", "first-aid", "survival-skills"],
        "risk_level": "high",
        "body_markdown": """## The Real 4 Life-Saving Steps (in order)

1. Start the breathing.
2. Stop the bleeding.
3. Treat the wound.
4. Check for shock.

## Real Wound Care Principles

**Wounds are dangerous in a survival situation for 3 real reasons together: tissue damage, blood loss, and infection risk** — proper wound care addresses all three, not just the visible bleeding.

**Animal bites specifically:** prevention comes from understanding animal behavior — most animals give real warning before attacking, intending to scare off an intruder rather than actually engage. **An animal that approaches a human without that normal caution/avoidance behavior should be treated as possibly rabid and avoided.** Animal bites combine tearing, cutting, and crushing injury together — always check for additional, less obvious injuries beyond the obvious bite wound.

**Early, thorough cleansing** (irrigation) reduces bacterial infection risk and is genuinely effective at physically removing rabies virus and other pathogens before they can establish infection — a wound that bleeds a bit during this process actually helps the irrigation along.

**⚠️ Real "open treatment" method: do NOT suture or otherwise close a wound in a survival context.** Closing a wound seals in any dirt or infection that's already present. **A wound that can continue to drain is usually not life-threatening** — keeping it open and draining is the safer real choice without access to real surgical cleaning. (The source notes maggots, superglue, and a shunt as techniques associated with open wound management, without further detail in this text.)

## Real Tourniquet Guidance in THIS Source — and a Note on a Real Conflict

**This source states:** if no rescue/medical aid is likely for over 2 hours, you may attempt to SLOWLY loosen a tourniquet about 20 minutes after applying it — provided a pressure dressing is in place and bleeding has actually stopped, loosen slowly to test if circulation can be restored, and leave it loosened-but-in-place in case bleeding resumes.

**⚠️ This is meaningfully less conservative than the TCCC Prolonged Field Care appendix's real tourniquet-conversion guidance already in this wiki** (under 2hr: safe to attempt; 2-6hr: likely safe, upper limit not established; over 6hr: field conversion not advised — see Prolonged Field Care — Sustaining a Casualty Without Evacuation). **Given TCCC is the more current, medically-specific doctrine, treat its timing as the more authoritative guidance** — this source's 20-minute figure is presented here for completeness and real sourcing transparency, not as a recommendation to follow over TCCC's.

**Bandaging exists to protect a wound from dirt/debris, not just to stop bleeding.** Any significant injury — but especially an open wound — increases real water needs; increase fluid intake accordingly.

**On herbal medicine:** only consider it with real prior training and when conventional supplies are genuinely unavailable — **some herbal remedies are dangerous and can cause real additional harm or death.**

## Real Casualty Evacuation Planning — APASSNGG

A poorly planned evacuation risks creating additional casualties, not just delay. Real considerations, in the acronym APASSNGG:

- **Apply** essential first aid first (splints, pressure bandages) before moving the person.
- **Protect** the patient from the elements — real insulation, keeping them warm and dry throughout transport.
- **Avoid** unnecessary handling/movement of the patient.
- **Select** the easiest actual route — send scouts ahead to break trail if possible.
- **Set up** relay points and warming stations on a long or difficult route, to rotate litter-bearers and reassess the patient along the way.
- **Normal** litter teams need extra people in difficult terrain — don't assume the standard team size is enough.
- **Give** litter teams specific, concrete goals — this work is both physically and mentally exhausting, and clear short-term targets help sustain it.
- **Gear** — keep all of the patient's own equipment with them throughout the evacuation.

## Detailed Version

**The real thread tying wound care and evacuation together: both sections push against an intuitive-but-wrong instinct — closing a wound to "fix" it, or rushing a patient out quickly without proper planning.** In each case, the source's real guidance is to resist the urge to do the seemingly obvious thing (seal the wound, move fast) in favor of the less intuitive but genuinely safer approach (leave it open and draining, plan the evacuation deliberately).
""",
    },
    {
        "title": "Wildlife & Food-Borne Diseases in a Survival Situation",
        "section": "reference",
        "tags": ["wildlife-disease", "food-safety", "survival-skills"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Handling wild animals, their meat, or their waste carries real, specific disease risks — each with its own transmission route and prevention, worth knowing individually rather than relying on generic caution.**

## Hantavirus Pulmonary Syndrome (HPS)

Carried by the common deer mouse, **spread when dried droppings/urine/saliva become airborne and are inhaled** — not through a bite. **Signs:** flu-like symptoms 3-45 days after exposure, which can rapidly progress to a life-threatening lung illness (lungs flooding with fluid). **No cure or vaccine exists** — earlier medical treatment improves real odds. **Prevention: never handle mice, don't disturb rodent dens, package food so rodents can't crawl on it, and don't occupy a shelter that shows signs of prior rodent occupation.**

## Plague

Caused by a bacterium maintained through a flea-rodent cycle. **Spread by flea bites, or direct contact with infected rodents or other hosts (rabbits, hares, cats).** **Fatality rate over 50% if untreated** — a swollen lymph node is a real characteristic sign. **Prevention:** avoid any animal visibly carrying fleas; **if you must handle a killed animal, submerge it in cool water immediately until the fleas have drowned or left.**

## Tick-Borne Diseases

- **Lyme disease** — most common May-September; a real, sometimes-present sign is an expanding skin rash (5+ inches across) at the bite site with flu-like illness. **Left untreated, it can become chronic**, with neurological, cardiac, or joint problems.
- **Rocky Mountain Spotted Fever** — 2-14 day incubation; flu-like onset (fever, headache, muscle/joint pain, nausea), sometimes a rash. **Fatality is about 5% if treated with antibiotics, up to 25% if untreated** — a real, large difference that makes seeking treatment genuinely worthwhile.
- **Real prevention for both: daily full-body tick checks**, removing any found promptly.

## Food-Borne Diseases

- **Botulism** — typically from improperly stored meat. Starts with vomiting/diarrhea, progresses to impaired vision and descending paralysis. **Can be fatal.**
- **Salmonella** — carried in the intestines/feces of many animals (poultry, swine, cattle, pets). **Can be fatal.**
- **Trichinosis** — a parasite in muscle tissue, most common in wild swine and bear. **Thorough cooking destroys it.**
- **Tularemia** — found in 45+ species, most often tied to ticks, rabbits, and rodents; spread through undercooked meat or handling contaminated meat with any open skin wound. **Treatable only with antibiotics.**

**Real prevention across all of these:** dress/process game promptly, minimize contamination from gut contents during field dressing, **cook meat to an internal temperature of 165°F or higher**, eat cooked food promptly rather than letting it sit, and store any preserved food properly.

## Animal Scat — a Real, Specific Hazard

**Certain roundworm parasites survive in scat for real, specific durations** — raccoon roundworm for at least 30 days, fox roundworm for about 7 — and handling contaminated scat unprotected risks a human infection that **can be nearly fatal.** Avoid handling animal scat with bare hands.

## Detailed Version

**The real pattern across this entire list: almost every one of these diseases has a genuinely simple, specific prevention step (don't handle mice, check for ticks daily, cook to 165°F, drown fleas off a carcass before handling it) that's easy to skip under survival-situation time pressure — and skipping it is exactly where real infection risk comes from, not from the wilderness environment itself being inherently more dangerous.**
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
