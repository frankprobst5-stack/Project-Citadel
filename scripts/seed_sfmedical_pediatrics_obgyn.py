#!/usr/bin/env python3
"""Seeds 2 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 6 Sections 6-8/6-9 (Pediatrics)
and Chapter 8 Section 8-5 (Obstetrics) -- mined from the OCR output
cached at /tmp/sfmedical.txt.

SCOPING NOTE: checked the existing wiki first. Chickenpox, measles,
German measles, mumps, whooping cough, and diphtheria are already
covered; diaper rash is already covered under "Bed Sores & Diaper
Rash"; pre-eclampsia/eclampsia is already thoroughly covered (with
specific real BP thresholds) under "Danger Signs in Pregnancy."

Most of Chapter 7 (Gynecology -- vulvitis, vaginitis, cervical
polyps, endometritis, salpingitis, oophoritis, dysmenorrhea,
amenorrhea, abnormal uterine bleeding, menopause) is deliberately
NOT seeded: these are chronic, non-emergency conditions that
genuinely require a real pelvic exam to diagnose and differentiate,
which is outside what this wiki can responsibly support -- similar
in kind to the Chapter 4 (Mental Disorders) and Appendix G (Drug of
Choice Chart) exclusions made in earlier sessions.

What IS seeded: viral croup vs. epiglottitis (6-8/6-9), a genuinely
important real safety contrast not covered anywhere else -- one is
safely home-manageable, the other is a true emergency with a
critical "do not examine the throat" warning; and ectopic pregnancy
(8-5), a real pregnancy emergency with distinctive signs that the
existing "Danger Signs in Pregnancy" page doesn't cover.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_pediatrics_obgyn.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Croup vs. Epiglottitis — Telling Apart a Home-Treatable Cough From an Airway Emergency",
        "section": "emergency",
        "tags": ["croup", "epiglottitis", "pediatric-emergency"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**Both conditions cause a harsh, high-pitched sound when a child breathes in (stridor) — but one is safely managed at home, and the other is a true emergency with a critical thing you must NOT do.** Telling them apart matters enormously.

## Viral Croup — Usually Home-Manageable

**Real, typical pattern: a child age 3 months to 3 years, after several days of an ordinary upper-respiratory cold, gradually develops a barking cough and harsh inspiratory stridor.** Fever is usually mild. The child may become anxious/restless as the airway narrows, but this develops gradually, over days.

**Real treatment:**
- **Cool mist therapy — or improvise with steam in an enclosed room (a bathroom with a hot shower running works) if a vaporizer isn't available.** **⚠️ Don't let steam blow directly on the child — it can cause burns.**
- **Keep the child calm, at rest, and with a familiar person (parent) present** — this alone is genuinely one of the most effective ways to keep a child's breathing from worsening with anxiety.
- **⚠️ Watch closely for signs the airway is narrowing further: increasing difficulty breathing, worsening stridor, or cyanosis (bluish skin) — cyanosis is a late, serious sign that can mean the airway is close to fully blocking.** If these appear, this is no longer a stay-at-home situation.

## ⚠️ Epiglottitis — A True Emergency, Different From Croup in 3 Real Ways

**Real, typical pattern: a child age 3-7, with NO preceding cold, develops high fever and looks genuinely sick ("toxic") within just a FEW HOURS — not days.** Real distinguishing signs: severe sore throat with real difficulty swallowing, drooling (from being unable to swallow their own saliva), and a muffled (not hoarse) voice.

**The 3 real differences from croup worth memorizing:**
1. **Speed: hours, not days.**
2. **No preceding cold/cough — it comes on in a previously well-seeming child.**
3. **Drooling and difficulty swallowing — croup doesn't typically cause this.**

**⚠️⚠️ Real, critical warning: do NOT attempt to look down the child's throat with a tongue depressor, spoon, or flashlight, and do not attempt a throat swab/culture.** **Stimulating the epiglottis in this condition has caused complete airway obstruction and death** — the swollen, fragile epiglottis can clamp shut the airway if disturbed. **This is real, specialized hospital work (careful intubation with a tracheostomy set standing by) — not something to attempt or provoke at home.**

**⚠️ Real action: if epiglottitis is suspected, get the child to a hospital immediately, keep them as calm and upright as possible, and do not examine or probe the throat under any circumstances along the way.** **Real, sobering fact: mortality can run as high as 90% without real hospital intubation and antibiotic treatment — but with it, the real outcome is good.**

## Detailed Version

**The real, unifying idea on this page: the same alarming sound (stridor) can come from two conditions that need opposite real approaches — calm observation and steam at home for one, versus immediate hospital transport with zero throat examination for the other.** The real tell is the timeline and the company it keeps: croup creeps in over days on top of a cold; epiglottitis slams in over hours, in a child who seemed fine that morning, with drooling and an inability to swallow as the giveaway.
""",
    },
    {
        "title": "Ectopic Pregnancy — Real Signs of an Emergency Non-Uterine Pregnancy",
        "section": "emergency",
        "tags": ["ectopic-pregnancy", "pregnancy-emergency", "internal-bleeding"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This real pregnancy emergency is NOT covered by the existing Danger Signs in Pregnancy page — a different set of signs, worth knowing separately.** A pregnancy implants somewhere other than inside the uterus (almost always in a fallopian tube) in roughly 1 in 200 pregnancies — real, genuinely dangerous because a growing pregnancy in a tube can rupture it, causing severe internal bleeding.

## ⚠️ Real Signs

**A missed or abnormal menstrual period, followed by irregular uterine bleeding, pelvic pain, and sometimes a palpable pelvic mass.** This can show up as either a sudden/acute presentation or a more gradual/chronic one:

**Acute presentation (about 40% of real cases) — the more dangerous pattern:** **⚠️ sudden onset of sharp, cutting, intermittent, severe lower-abdominal pain on one side, that does NOT spread elsewhere, often with backache during the episode.** Light but persistent vaginal bleeding is present in most of these cases. **⚠️ Real, critical danger: sudden collapse and shock can occur** — this means the tube has likely ruptured and real internal bleeding is underway. **Most people with this presentation have a history of abnormal periods, and many have had trouble conceiving.**

**Chronic presentation (about 60% of real cases):** gradually increasing pelvic discomfort with light but persistent spotting, rather than a sudden crisis.

**⚠️ Real, important nuance: a home pregnancy test is NOT reliable for ruling this out** — this condition can occur with a positive, negative, or borderline test result, so a negative test should never be used to dismiss these symptoms if a period has been missed or is abnormal.

## ⚠️ Real Treatment — This Requires a Real Hospital

**⚠️ Any reasonable suspicion of ectopic pregnancy requires hospitalization — this is surgical, not a home-manageable condition.** While arranging transport: treat for shock if signs are present (see existing shock-treatment content), and avoid unnecessary pelvic examination, since **real, important warning: a pelvic exam itself can trigger sudden collapse and rupture in an unstable ectopic pregnancy.** Real definitive treatment is surgical removal of the affected tube; a blood transfusion is often needed and should be started before surgery when possible.

## Detailed Version

**The real, most useful idea on this page: a missed period plus one-sided (not centered), sharp, non-spreading lower abdominal pain is specifically worth treating as a possible ectopic pregnancy, not ordinary menstrual cramping or early-pregnancy discomfort** — especially with any vaginal bleeding alongside it. The real danger isn't the initial pain itself; it's that this can progress to sudden, severe internal bleeding with little additional warning, which is exactly why "wait and see if it gets better" is the wrong real response to this particular symptom pattern.
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
