#!/usr/bin/env python3
"""Seeds 2 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 14 (NBC) Sections 14-1 and 14-3,
with the real 2-PAM dosing cross-checked against Chapter 13's
organophosphate poisoning sub-entry -- mined from the OCR output
cached at /tmp/sfmedical.txt.

SCOPING NOTE: checked the existing wiki first. Mass-casualty triage
(14-1's IDME categories) is already covered under "Mass Casualty
Triage — IDME Categories," so that part of 14-1 is skipped here;
what's seeded instead is the real acute radiation syndrome dose-
response timeline, which is genuinely new and complements the
existing "Nuclear Survival Kit Checklist" page (a supply checklist,
not exposure-response content).

Biological warfare (14-2) and blister/vesicant agents like mustard
gas (part of 14-3) are deliberately NOT seeded -- both are lower
real-world relevance for this wiki's civilian audience than the
nerve-agent/organophosphate content, and their actionable content
either requires specialized protective equipment unlikely to be on
hand or doesn't add much beyond what's already covered.

Nerve agent poisoning IS seeded, reframed to lead with its far more
probable civilian equivalent: organophosphate PESTICIDE poisoning
produces the identical real symptom pattern and responds to the
identical real antidote (atropine, with pralidoxime/2-PAM as an
adjunct) -- genuinely relevant to this wiki's existing self-
sufficiency/farming context, not just a chemical-attack scenario.
This specific sub-topic was carved out from the broader Chapter 13
(Overdose and Poisoning), which was judged out of scope in an
earlier session for requiring hospital-level interventions (gastric
lavage, forced diuresis, dialysis) -- unlike those, atropine
titrated to symptom response is a real, field-executable technique
the source itself describes via IM and oral routes, not just IV.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_nbc.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Acute Radiation Sickness — Real Dose-Response Timeline",
        "section": "emergency",
        "tags": ["radiation-sickness", "nuclear", "triage"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**Pairs with the existing Nuclear Survival Kit Checklist** (gear) and **Expedient Fallout Shelter — Door-Covered Trench** (shelter) — this page covers what the body's own symptoms can tell you about radiation dose received, which matters most precisely when a dosimeter or Geiger counter isn't available.

## ⚠️ Real, Important Idea: Symptom Timing Is a Real Clue to Dose Received

**Radiation dose is cumulative, and the real severity of acute radiation sickness tracks directly with total dose received.** The timing of when symptoms first appear, and whether a "latent period" of apparent recovery follows, are themselves real, useful clues to roughly how severe the exposure was — this is genuinely still used as a field triage method when exact dosimetry isn't available.

**50-200 rad (lower-dose range):** Symptoms, if any, appear around 6 hours after exposure — at most, transient mild headache and a slight dip in ability to function. **Real outcome: well under 5% need hospitalization, and no deaths occur at this dose range.**

**200-500 rad (moderate range):** Headache, malaise, nausea, and vomiting begin 4-6 hours after exposure (not relieved by anti-nausea medication at the upper end of this range). Moderate-to-heavy exertion is impaired for 6-20 hours, **then the person appears to recover and enters a latent (symptom-free) period lasting 17-21 days.** **⚠️ Real, specific warning sign: losing large amounts of hair 12-18 days after exposure indicates a dose of 300+ rad specifically.** After the latent period ends, symptoms return and roughly 90% require hospitalization for 60-90 days. Real mortality: under 5% at the lower end of this range, rising toward the upper end.

**500-1000 rad (severe range):** Severe, hard-to-control nausea and vomiting begin just 1-4 hours after exposure; diarrhea and fever develop early at the upper end. Initial symptoms last over 24 hours, then a shorter latent period of only 7-10 days follows. **After that, symptoms return and 100% require hospitalization. Real, severe mortality: roughly 50% at the lower end of this range, rising toward the upper end — all deaths occur within 45 days**, and survivors need 90-120 days to recover.

**1000+ rad:** Severe vomiting, diarrhea, and prostration begin in under 1 hour. **⚠️ There is no latent period at all** — symptoms are continuous. Real outcome: universal hospitalization need, and death within 30 days.

## Real Treatment

**Wash the person thoroughly to remove radioactive contamination from the skin and hair, treat symptoms as they appear, and watch closely for secondary infection** (radiation damages the immune system's ability to fight it off) — real definitive treatment beyond this requires a real hospital.

## Detailed Version

**The real, most useful idea on this entire page: how FAST symptoms appear, and how LONG any symptom-free latent period lasts afterward, are themselves rough real indicators of dose severity** — a person who develops severe vomiting within an hour with no latent period at all has received a vastly more severe dose than someone whose only sign is a mild headache 6 hours later. This timing information is genuinely actionable for triage decisions even with zero radiation-detection equipment on hand.
""",
    },
    {
        "title": "Nerve Agent & Organophosphate Pesticide Poisoning — Real Signs & Atropine Treatment",
        "section": "emergency",
        "tags": ["organophosphate-poisoning", "pesticide-safety", "atropine"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This real symptom pattern and treatment apply equally to military nerve agents (sarin, VX, etc.) and to organophosphate pesticide poisoning** — a real, far more probable hazard for anyone working with agricultural chemicals. Both work on the body the same way and respond to the same real antidote.

## ⚠️ Real Early Warning Signs — Suspect Exposure If Any Occur

- **A feeling of tightness or constriction in the chest.**
- **Unexplained runny nose.**
- **Difficulty breathing, on either the inhale or exhale.**
- **⚠️ Real, distinctive sign: small, pinpoint pupils** — check your own eyes in a mirror, or check others nearby. **Real, important nuance: if exposure was through skin contact or contaminated food/water rather than inhaled vapor, pupil pinpointing can be delayed or even absent** — don't rule out exposure just because the pupils look normal.
- **A drawing, slightly painful sensation in the eyes, or unexplained blurred vision, especially together with pinpoint pupils.**

## Real Fuller Symptom Picture (as Absorption Increases)

**Local exposure:** pinpoint pupils, frontal headache, eye pain on focusing, runny nose, chest tightness with wheezing/cough.

**Systemic absorption — real, classic pattern (often remembered by the mnemonic SLUDGE: Salivation, Lacrimation, Urination, Defecation, GI distress, Emesis):** increased salivation, tearing, sweating; nausea, vomiting, abdominal cramps, diarrhea, involuntary defecation; increased urination frequency; muscle twitching and fasciculations progressing to generalized weakness including the muscles used for breathing; and in severe cases, confusion, slurred speech, coma, convulsions, and respiratory/circulatory failure.

**⚠️ Real, important fact: effects are cumulative** — repeated low-level daily exposure that wouldn't cause symptoms from a single dose can still produce real symptoms after several days of accumulated exposure.

## ⚠️ Real Treatment — Atropine

1. **Immediately remove from further exposure and decontaminate** — if liquid got in the eyes, irrigate immediately with copious water.
2. **⚠️ Real, specific dosing: 2mg of atropine (IM, IV, or orally) as soon as any symptom appears** — **do NOT take atropine preventively before exposure.**
3. **Real titration by severity:** repeat the 2mg dose every 20 minutes for mild symptoms, or every 10 minutes for moderate-to-severe symptoms, **until signs of "atropinization" appear: dry mouth and blurry near vision.** Those signs are the real signal that enough atropine is on board — not a fixed dose count.
4. **Real maintenance: once atropinization is reached, a mild degree should be maintained for at least 24 hours** with repeat doses of 1-2mg every 30 minutes to 4 hours as needed.
5. **⚠️ Real, severe-case protocol: if the person is in severe respiratory distress or convulsing, 4-6mg IV, then 2mg every 5-8 minutes until secretions and symptoms ease** — in severe poisoning, **each dose's effect may last only 3-10 minutes, requiring very close monitoring and frequent re-dosing.** Severe exposure can cause respiratory arrest — artificial respiration may be needed alongside the atropine.
6. **Real route timing: IM atropine takes about 5 minutes to act; IV works within 1 minute (maximum effect by 6 minutes); oral tablets take about 20 minutes (maximum effect by 50 minutes).**
7. **⚠️ Real adjunct, if available: pralidoxime (2-PAM chloride), 1g IV slowly over 15-30 minutes** — this genuinely shortens how long artificial respiration is needed, but **only works if given within 24 hours of exposure.**

## Detailed Version

**The real, most important idea on this page: atropine dosing here isn't a fixed amount — it's titrated against the body's own response (dry mouth, blurred near vision) rather than a one-size dose, and severe cases can need doses repeated every few minutes rather than every few hours.** This real, symptom-driven titration approach is exactly what makes atropine genuinely usable in the field without lab monitoring, unlike the hospital-level interventions (gastric lavage, forced diuresis, dialysis) this wiki deliberately excludes for other types of poisoning.
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
