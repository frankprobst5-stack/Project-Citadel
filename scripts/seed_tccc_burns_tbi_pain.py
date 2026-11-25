#!/usr/bin/env python3
"""Seeds 5 final real pages from the TCCC Handbook, Version 5 --
mined from the real text layer already extracted in this session
(/tmp/tccc.txt), Chapter 6's Tactical Field Care/Tactical Evacuation
Care basic management plans (p.85-91). This closes out the
genuinely new procedural content in this source -- Chapters 2, 4, 5,
and 6's own training-curriculum sections are confirmed to be
administrative/instructor-certification material repeating skill-set
checklists already covered by earlier batches, not new technique.

Covers: burn severity estimation and fluid resuscitation, traumatic
brain injury monitoring and the real impending-herniation
emergency-management steps, real battlefield pain/antibiotic dosing
branched by shock status, penetrating eye trauma and pelvic fracture
field splinting, and the real (and counterintuitive) battlefield rule
for when NOT to attempt CPR.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_tccc_burns_tbi_pain.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
TCCC_PDF_URL = "/files/pdfs/Medical/TCCC-17-13-Army-Tactical-Combat-Casualty-Care.pdf"

PAGES = [
    {
        "title": "Burns in Trauma — TBSA Estimation & Fluid Resuscitation",
        "section": "emergency",
        "tags": ["tccc", "burns", "fluid-resuscitation"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**A burn large enough to need real fluid resuscitation needs its size estimated first — treatment decisions are driven by what percentage of the body is actually burned, not just how severe a single area looks.**

**⚠️ Facial burns need aggressive, ongoing airway monitoring** — the real risk isn't just the visible burn, it's a possible inhalation injury swelling the airway closed over the following hours, sometimes well after the initial injury.

## Estimating Burn Size — The Rule of Nines (adult)

Estimate total body surface area (TBSA) burned, rounded to the nearest 10%, using these real body-region percentages:

| Body region | % of TBSA |
|---|---|
| Head | 9% |
| Chest (front) | 9% |
| Abdomen (front) | 9% |
| Upper/mid/lower back + buttocks | 18% |
| Each arm | 9% (front 4.5% + back 4.5%) |
| Groin | 1% |
| Each leg | 18% (front 9% + back 9%) |

## Treatment Based on Burn Size

- **Cover burned areas with dry, sterile dressings** regardless of size.
- **For burns over 20% TBSA:** consider wrapping the person in a hypothermia-prevention kit or equivalent — burns this large impair the body's own temperature regulation, making hypothermia a real added risk on top of the burn itself.
- **Fluid resuscitation ("Rule of Ten"), for burns over 20% TBSA:** start IV or IO fluids (lactated Ringers, normal saline, or Hextend) as soon as feasible. **If using Hextend specifically, give no more than 1000ml before switching to lactated Ringers or normal saline for any further fluid needed.**

## Detailed Version

**The real reason burn size is calculated so specifically, rather than just treated by eye: fluid needs scale directly with burned surface area, and both too little and too much fluid carry real risk** — too little under-resuscitates a major burn's real fluid loss, while flooding a smaller burn with large-burn-level fluids causes its own harm. The Rule of Nines exists specifically to make that calculation fast and consistent under real field pressure, not to add unnecessary procedure.
""",
    },
    {
        "title": "Traumatic Brain Injury — Monitoring & Impending Herniation",
        "section": "emergency",
        "tags": ["tccc", "tbi", "brain-injury", "head-injury"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**A moderate-to-severe traumatic brain injury (TBI), especially a penetrating one, needs real ongoing monitoring — it can progressively worsen over time even after the initial injury, and catching that progression early changes the outcome.**

## What to Monitor

- **Level of consciousness** — any decrease is a real warning sign, not something to dismiss as "just tired."
- **Pupil size** — one pupil becoming larger (dilated) than the other is a specific, serious sign.
- **Blood pressure** — keep systolic blood pressure over 90 (or mean arterial pressure over 60).
- **Blood oxygen** — keep saturation over 90% by pulse oximetry if available.
- **Body temperature** — watch for hypothermia (core temp under 96°F/35.5°C), which worsens brain injury outcomes.
- **For penetrating head trauma specifically:** give antibiotics (ertapenem 1g).
- **⚠️ Assume a spinal injury until it's actually been ruled out** — don't move the head/neck freely just because the obvious injury is to the head.

## ⚠️ Impending Brain Herniation — a Real, Time-Critical Emergency

**Signs this is happening include a rapidly worsening level of consciousness and pupil changes** (see above) — this means pressure inside the skull is building dangerously and the brain is being pushed against structures it shouldn't be. **Real emergency actions, in this order:**

1. **250ml of 3% or 5% hypertonic saline, given rapidly by IV or IO** — this draws fluid out of brain tissue to reduce swelling/pressure.
2. **Elevate the head 30 degrees** — this helps blood and fluid drain away from the skull rather than pooling.
3. **Control pain, even in an unconscious person — but specifically NOT with morphine** for this situation.
4. **Hyperventilate the person** (bag-valve-mask ventilation at 14-20 breaths/minute) — deliberately breathing faster than normal lowers blood carbon dioxide, which constricts brain blood vessels and reduces pressure, as a genuine emergency bridge measure.
5. Package the person in a hypothermia-prevention kit or equivalent insulation — TBI patients are at real added risk of harm from hypothermia specifically.

## Detailed Version

**The real logic tying monitoring to the herniation protocol: none of these interventions are "default" care for a head injury — they're specifically reserved for the moment signs suggest the brain is actively herniating.** Hyperventilating or giving hypertonic saline to someone who isn't actually herniating doesn't help and can cause its own harm; the whole point of the monitoring checklist above is to catch the real, specific signs that justify escalating to this emergency protocol, rather than guessing.
""",
    },
    {
        "title": "Battlefield Pain Management & Antibiotic Dosing",
        "section": "reference",
        "tags": ["tccc", "pain-management", "antibiotics", "dosing"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Real battlefield pain management is deliberately branched by severity AND by whether the person is in shock** — because some pain medications are dangerous to give someone who's in shock, and the "right" choice changes based on that one factor.

## Pain Management — the Real 3-Tier Decision

1. **Mild-moderate pain, and/or the person is still able to fight/function:** oral pain medication (acetaminophen, meloxicam) from a basic combat wound pill pack.
2. **Moderate-severe pain, person is NOT in shock:** 800mcg of oral transmucosal fentanyl citrate (OTFC) — a lozenge, not swallowed (see When (and When Not) to Give an Injection-adjacent dosing caution: this is a controlled substance requiring real training and legal authority).
3. **Moderate-severe pain, person IS in shock:** ketamine instead of fentanyl — 50mg IM or intranasal every 30 minutes as needed, OR 20mg by slow IV/IO push every 20 minutes as needed. **The real endpoint for "enough" ketamine is a specific eye-movement sign (nystagmus)** — not just "the person stopped complaining." Nausea from ketamine can be managed with ondansetron (Zofran) 4mg every 8 hours.

**Why shock changes the choice:** certain medications behave less predictably or more dangerously when the body's circulation is already compromised — ketamine's profile is considered safer for a person already in shock than fentanyl is.

## Antibiotic Choice — Branched by Whether the Person Can Swallow

**Every open combat-type wound is treated as needing antibiotics — this isn't optional or dependent on visible infection.**

- **If the person can swallow:** 400mg oral moxifloxacin.
- **If the person CANNOT swallow** (shock, unconsciousness): 1g ertapenem by IV or IM instead.

## Detailed Version

**The real pattern across both decision trees: the "better" option on paper (a stronger painkiller, a more convenient oral antibiotic) isn't automatically the right choice — the person's actual physiologic state (in shock or not, able to swallow or not) determines which option is genuinely safe to give.** Treating these as fixed defaults rather than conditional choices is exactly the kind of mistake real battlefield medicine training exists to prevent.
""",
    },
    {
        "title": "Penetrating Eye Trauma & Pelvic Fracture — Field Splinting",
        "section": "emergency",
        "tags": ["tccc", "eye-injury", "pelvic-fracture", "splinting"],
        "risk_level": "high",
        "body_markdown": """## Penetrating Eye Trauma

**Real 3-step field protocol:**
1. **Perform a rapid field test of visual acuity** — a simple check (can they see/count fingers, read something) before covering the eye, so there's a real baseline documented before any further handling.
2. **Cover the eye with a rigid eye shield — never a soft pressure patch or pressure dressing.** Any pressure on a penetrating eye injury risks pushing contents of the eye out through the wound and causing permanent vision loss — this is the single most important thing to get right here.
3. **Give antibiotics to prevent infection inside the eye:** 400mg oral moxifloxacin if the person can swallow; IV or IM antibiotics instead if they can't.

**⚠️ Never apply a pressure dressing to a suspected penetrating eye injury — this is worth repeating as its own standalone warning, since the instinct to apply pressure to any wound is strong and is specifically wrong here.**

## Pelvic Fracture — When to Apply a Pelvic Splint

**Apply a pelvic splint/binder specifically when the mechanism of injury suggests it, even without obvious signs:** a lower-extremity traumatic amputation, a vehicle rollover, or a building collapse. **The real reasoning:** the same force that caused an amputation or came from a rollover/collapse often travels through the body and can disrupt the pelvis too, even when the pelvis itself doesn't look obviously injured — the splint is applied based on the mechanism of injury, not waiting for pelvic pain or visible deformity to appear.

## Detailed Version

**Both of these share the same real underlying lesson: the correct action is sometimes preventive, based on mechanism of injury, rather than reactive, based on visible signs.** A pelvic splint applied to someone whose pelvis "looks fine" after a rollover, and a rigid eye shield applied instead of the instinctively-reached-for pressure dressing, are both examples of trained protocol overriding an untrained first instinct — specifically because waiting for the "obvious" sign in either case risks the injury becoming significantly worse in the meantime.
""",
    },
    {
        "title": "When NOT to Attempt Resuscitation (CPR) in Trauma",
        "section": "emergency",
        "tags": ["tccc", "cpr", "resuscitation", "trauma"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ A Real, Counterintuitive Battlefield Rule

**In blast or penetrating trauma, a casualty with no pulse, no breathing, and no other signs of life should NOT be resuscitated.** This runs against the instinct (and against standard civilian CPR training for cardiac-arrest-type emergencies) to always start CPR — but in severe blast/penetrating trauma specifically, the real data behind TCCC doctrine is that CPR in this situation does not restore life and simply consumes time and resources that could save someone else who is actually savable.

## The One Real Exception — Check for a Treatable Cause First

**Before fully stopping, if the person has torso trauma or injuries in multiple body regions (polytrauma) with no pulse or breathing: perform needle chest decompression on BOTH sides of the chest first**, to rule out (or treat) a tension pneumothorax as the actual cause of the apparent death. **A tension pneumothorax is a real, reversible cause of this exact presentation** — if that's what's actually happening, decompressing both sides can restore signs of life; if it doesn't, that confirms resuscitation efforts should stop.

## Detailed Version

**The real principle behind this rule, worth stating plainly because it cuts against typical first-aid instinct: in a mass-casualty or severe-trauma context with limited rescuers, time spent on CPR for someone who cannot actually be revived is time NOT spent on someone who can be** — this is the same triage logic from Mass Casualty Triage — IDME Categories applied to a single, specific, data-backed scenario. The bilateral needle decompression check exists precisely so this isn't a blind rule — it's a deliberate, fast check for the one real reversible cause before committing to stop.
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
                "source_url": TCCC_PDF_URL,
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
