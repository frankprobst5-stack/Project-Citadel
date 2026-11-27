#!/usr/bin/env python3
"""Seeds 2 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 2 Section III (Bacterial
Diseases) -- mined from the OCR output cached at /tmp/sfmedical.txt
(sections 2-30 Typhoid Fever and 2-31 Cholera).

SCOPING NOTE: Chapter 2 is a large catalogue of named infectious
diseases (parasitic, fungal, bacterial, viral, rickettsial/
spirochetal, venereal). Checked the existing wiki first: malaria,
meningitis, and tetanus are already well covered (from Where There
Is No Doctor); gas gangrene is already covered under "Erysipelas,
Cellulitis & Gangrene"; generic diarrhea/dysentery home care is
covered under "Diarrhea & Dysentery — Home Care." Cholera and
typhoid fever specifically are NOT covered anywhere in the wiki,
despite both being real, historically major causes of death after
exactly the kind of water-system disruption (flooding, sanitation
breakdown) this wiki's broader disaster context is built around --
and cholera in particular has a distinctly faster, more dangerous
dehydration course than the generic diarrhea guidance captures.
Many of the chapter's other named diseases (exotic tropical
parasites rarely relevant outside endemic regions, venereal
diseases) are left for a possible future pass rather than mined
here, to keep this batch focused on genuinely high-value, broadly-
relevant, non-duplicate content.

Real antibiotic dosing from the source is included (as with the
existing Gangrene page) but explicitly flagged as needing real
medical administration, not home guessing.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_waterborne.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Cholera — Real Signs, Rapid Dehydration & Field Treatment",
        "section": "emergency",
        "tags": ["cholera", "waterborne-illness", "dehydration"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**Cholera is a distinct, far more dangerous disease than ordinary diarrhea — it genuinely kills half of untreated patients, through dehydration alone.** For general diarrhea/dysentery home care, see Diarrhea & Dysentery — Home Care; this page covers what's specifically different and more dangerous about cholera.

## Real Cause & Spread

**Caused by the bacterium Vibrio cholerae, spread by ingesting food or water contaminated with feces from an infected person** (including people who carry it without being visibly sick themselves). **Real incubation period: 1-5 days — though only a small minority of people actually exposed go on to get sick.**

## ⚠️ Real Signs — Why This Looks Different From Ordinary Diarrhea

**Explosive onset of frequent, watery stools that quickly lose all normal fecal appearance and odor** — the real, distinctive description is a grayish, cloudy, watery stool (classically called "rice-water stool"), without the blood or heavy mucus of dysentery. **⚠️ Real, critical number: a person can lose up to 1 liter of fluid per hour** through stool alone. Vomiting can occur early too.

**As dehydration rapidly sets in:** sunken eyes, low blood pressure, subnormal body temperature, rapid/shallow breathing, muscle cramps, reduced urination, progressing to shock and coma if not corrected.

## ⚠️ Real Treatment — Speed and Volume Are Everything

**The entire treatment is replacing fluid and electrolytes as fast as they're being lost, continuously, without interruption:**
1. **If the person can still drink:** give oral rehydration fluid in roughly the same volume being lost in stool — this means far more fluid, far more urgently, than typical home diarrhea care calls for. Keep reassessing and keep pace with ongoing losses rather than giving a fixed amount and stopping.
2. **If the person can't keep fluid down: IV fluid replacement is genuinely necessary** — this is a real sign to get the person to medical care as fast as possible rather than continuing to attempt oral rehydration alone.
3. **Real antibiotic treatment: tetracycline 500mg by mouth every 6 hours for 3-5 days** shortens the illness and reduces how much fluid is lost — this needs real medical dosing/administration, not home guessing, but is worth knowing as the real drug of choice if a clinician is reachable.
4. **⚠️ Strict isolation of the patient is NOT actually necessary, and full quarantine is considered undesirable** — but safely disposing of and decontaminating the person's stool/waste is essential to avoid spreading it further.

## Real Prevention

**⚠️ The cholera vaccine only gives limited protection and does not meaningfully control outbreaks** — real prevention in an area with known or suspected cholera means boiling or avoiding ALL water, drinks, food, and eating utensils that could be contaminated, not relying on vaccination.

## Detailed Version

**The real, single most important distinction from ordinary diarrhea: the sheer VOLUME and SPEED of fluid loss is what makes cholera lethal — not the infection itself.** A person who is replaced fluid-for-fluid, fast enough and continuously enough, generally survives even a severe case; a person who falls behind on replacement, even briefly, can deteriorate into shock within hours. This is exactly why cholera calls for a more aggressive, higher-volume rehydration approach than the general diarrhea guidance already in this wiki.
""",
    },
    {
        "title": "Typhoid Fever — Real Diagnosis & the Stepladder Fever Pattern",
        "section": "reference",
        "tags": ["typhoid", "waterborne-illness", "fever"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Typhoid fever is a real, serious systemic bacterial illness spread through contaminated food or water** — often traced to a chronic carrier (someone with a persistent gallbladder or urinary infection who sheds the bacteria without necessarily being sick themselves). **Real incubation period: 5-14 days.**

## ⚠️ Real Diagnosis — The Stepladder Fever Pattern

**Onset is usually gradual, but can be abrupt (especially in children)**, with chills and a sharp temperature rise. Increasing malaise, headache, cough, body aches, sore throat, and nosebleeds are common; abdominal pain, constipation or diarrhea, and vomiting often follow.

**⚠️ Real, distinctive pattern worth recognizing: during the first week, the fever climbs in a "stepladder" fashion — each day's peak temperature is slightly higher than the day before, and it's always higher in the evening than the morning.** This specific rising, day-stepped pattern is a real diagnostic clue pointing toward typhoid rather than a typical short-lived fever.

**After 7-10 days, the fever plateaus and the person becomes genuinely very sick.** "Pea soup" diarrhea, or alternatively severe constipation with marked abdominal distension, is common. **In severe cases, the person lies motionless and unresponsive, eyes half-shut, looking wasted and exhausted (the real "typhoid state")** — though they can usually still be roused to follow simple commands.

**⚠️ Real recovery pattern: if the person survives this stage with no complications, the fever then declines in the same stepladder fashion, over another 7-10 days, back to normal — and symptoms fade along with it.** **Real, important caution: relapse can occur as late as 1-2 weeks after the temperature returns to normal** — usually milder than the original illness, but real nonetheless, so apparent recovery doesn't mean the risk is fully over.

**Other real supporting signs:** an enlarging spleen, abdominal tenderness/distension, and — in the second week — **a rash of small pink spots ("rose spots"), mainly on the trunk, that fade under pressure and disappear over 3-4 days.**

## Real Treatment

**⚠️ Real antibiotic options: ampicillin or chloramphenicol, continued at a reduced dose for roughly 2 more weeks after the fever disappears** — this needs real medical dosing and supervision, not home guessing, but is worth knowing as the real drug-of-choice information if a clinician is reachable. **IV fluids may be genuinely necessary** to supplement oral intake and maintain adequate urination, especially during the severe stage.

**⚠️ Real, important nuance: anyone caring for a typhoid patient should maintain strict stool and urine precautions** — careful handwashing and waste disposal, since the organism is shed in both.

## Real Prevention

**Protecting food and water sources and properly disposing of waste are the real foundations of prevention** — along with vaccination for household contacts of a known carrier, anyone traveling into an area where it's endemic, or during a recognized outbreak.

## Detailed Version

**The real, most useful diagnostic idea on this page: a fever that keeps climbing a little higher each day, rather than peaking and breaking within a day or two, is itself a meaningful clue** — most short-lived illnesses don't behave this way, and recognizing the stepladder pattern early is what distinguishes typhoid from an ordinary passing fever, well before the more dramatic second-week signs (rose spots, the "typhoid state") appear.
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
