#!/usr/bin/env python3
"""Seeds 4 more real pages from Where There Is No Doctor's Chapter 14
(Serious Illnesses That Need Special Medical Attention): Rabies,
Tetanus, Meningitis, and Malaria -- all mined from the real text layer
already extracted in this session.

These are all "recognize fast, get real help immediately" illnesses --
the book's own framing for this chapter is that home remedies will not
cure any of them, and the real first-aid value is early recognition,
not home treatment.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_rabies_tetanus_meningitis_malaria.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"

PAGES = [
    {
        "title": "Rabies",
        "section": "emergency",
        "tags": ["rabies", "animal-bite"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Rabies is fatal once symptoms begin — there is no cure after that point. Treatment only works if started before symptoms appear.**

**Signs in the animal:** acting strangely (unusually sad, restless, or irritable), foaming at the mouth, unable to eat/drink, sometimes turning aggressive and biting anything nearby. A rabid animal typically dies within 5-7 days.

**Signs in a person** (first symptoms appear 10 days to 2 years after the bite, usually 3-7 weeks): pain/tingling at the bite site, irregular breathing, painful difficulty swallowing with fear of liquids, thick sticky saliva, alert but very nervous/excitable, eventually seizures and paralysis as it progresses.

**If bitten by an animal that might have rabies:**
1. Clean the bite thoroughly with soap, water, and hydrogen peroxide if available. **Leave the wound open — don't close it.**
2. **If possible, confine the animal (cage or tie it) for a week to watch for it dying or showing worsening signs — don't kill it immediately unless necessary for safety, since watching it is the fastest way to rule rabies out.**
3. If the animal dies within that week, or can't be captured/observed at all, **get the bitten person to a health center immediately for the anti-rabies injection series — don't wait for symptoms, by then it's too late.**

## Detailed Version

**The real reason speed matters so much here:** rabies has an unusually long incubation period compared to most infections — someone can feel completely fine for weeks while the virus is still progressing. That gap is exactly why "wait and see if symptoms develop" is the wrong approach — the vaccine series needs to start during that symptom-free window to work at all.

Any animal acting strangely deserves real caution even without a bite — rabies-infected saliva can transmit through an existing cut or scratch, not just a fresh bite wound. Keep children away from any wild or domestic animal that seems sick or is behaving oddly.
""",
    },
    {
        "title": "Tetanus (Lockjaw)",
        "section": "emergency",
        "tags": ["tetanus", "wound-care"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

Tetanus enters through a wound — deep or dirty wounds are the highest risk (animal bites, gunshot/knife wounds, dirty needles, barbed wire injuries, puncture wounds from thorns/splinters/nails).

**Signs:** an infected wound (sometimes none found), difficulty swallowing, jaw stiffness ("lockjaw") progressing to neck and whole-body stiffness, painful whole-body spasms — sometimes triggered just by touch, sudden noise, or bright light.

**Newborns:** signs appear 3-10 days after birth — continuous crying, inability to nurse, often an infected umbilical area, progressing to lockjaw.

**A real bedside test (knee-jerk reflex):** tap just below the kneecap with the leg hanging freely. A normal, small jump is fine; **a strong, exaggerated jump suggests tetanus (or meningitis, or certain poisonings)** — especially useful for spotting tetanus in a newborn who can't otherwise communicate symptoms.

**This is a real emergency — get medical help at the first sign.** Even in the best hospitals, roughly half of tetanus cases die; prevention is dramatically easier than treatment.

## Detailed Version

**Prevention is genuinely the whole game here:**
- **Vaccination is the single most effective protection** — for the whole family, repeated every 10 years. Vaccinating pregnant women specifically protects the newborn from tetanus too.
- **Real wound care matters directly:** clean any wound thoroughly (see Infected Wounds), and for a big/deep/dirty wound in someone unvaccinated, penicillin plus a tetanus antitoxin injection are real preventive steps, not just treatment for after symptoms start.
- **Newborn cord care is a documented, real cause/prevention pair:** a cord cut with a sterilized instrument, cut short, and kept clean and dry prevents tetanus; a cord cut long, kept tightly covered, and not kept dry is a real, documented cause of fatal newborn tetanus. This single hygiene practice is the difference the source itself illustrates directly — one baby stayed healthy, the other died of tetanus, from exactly this difference in cord care.
""",
    },
    {
        "title": "Meningitis",
        "section": "emergency",
        "tags": ["meningitis"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

A serious brain infection, more common in children, sometimes developing as a complication of measles, mumps, whooping cough, malaria, or an ear infection.

**Signs:** fever, severe headache, **stiff neck** (the person lies with head and neck bent back, and the back is too stiff to bring the head toward the knees), vomiting, sometimes seizures. In babies under a year: **the soft spot on the head bulges outward.** In infants, early signs can be subtle — a strange, distinctive high-pitched "meningitis cry," or unusual sleepiness, even when nursing.

**This is a real emergency — every minute counts. Get to a hospital immediately.**

While arranging transport:
- A high fever (over 104°F/40°C) should be brought down with wet cloths and fever medication.
- Real antibiotic treatment (ampicillin, often with chloramphenicol) genuinely changes the outcome — this needs real medical dosing, started as fast as possible.

## Detailed Version

**Speed of onset is itself a real diagnostic clue:** tubercular meningitis develops slowly over days or weeks, while other forms come on fast — hours to days. Either way, "get to real medical help immediately" doesn't change; the distinction mainly matters for the treating clinician's choice of medication, not for what a caregiver should do in the moment.

A stiff neck combined with fever and headache is the real pattern worth remembering — it's the single most distinguishing combination that separates meningitis from an ordinary bad headache or fever.
""",
    },
    {
        "title": "Malaria",
        "section": "reference",
        "tags": ["malaria", "mosquito-borne"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

A blood infection spread by mosquito bites, causing a distinctive 3-stage attack:
1. **Chills** — shivering/shaking for 15 minutes to an hour, often with headache.
2. **Fever** — often 104°F (40°C) or higher, weak, flushed, sometimes delirious. Lasts several hours to days.
3. **Sweating** — temperature drops, person feels weak but often more functional afterward.

**Fever often repeats every 2-3 days** (the exact pattern depends on the malaria species), though it can be daily at first or irregular — **don't rule out malaria just because the fever pattern doesn't look textbook.** Anyone with an unexplained recurring fever in a malaria-risk area should get tested.

**Chronic/repeated malaria can cause an enlarged spleen and anemia** even between acute attacks.

**Treatment requires real antimalarial medication** (the book names artesunate/quinine for severe cases) — this isn't a home-remedy illness; get real medical treatment and testing.

## Detailed Version

People with HIV are roughly twice as likely to contract malaria — a real, documented interaction worth knowing if that's a relevant factor for anyone in the household.

The practical takeaway for a prevention-minded household: mosquito control (netting, eliminating standing water, repellent) is the actual lever that matters most here, since there's no reliable home treatment once infection occurs — this is squarely a "prevent, don't try to treat at home" illness.
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
                "source_url": NO_DOCTOR_PDF_URL,
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
