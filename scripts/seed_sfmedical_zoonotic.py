#!/usr/bin/env python3
"""Seeds 5 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 2 Sections III and V (Bacterial
and Rickettsial/Spirochetal Diseases) -- mined from the OCR output
cached at /tmp/sfmedical.txt.

SCOPING NOTE: checked the existing wiki first. None of these 5 real
diseases (tularemia, anthrax, leptospirosis, relapsing fever, and
the rickettsial-fever cluster: epidemic/murine typhus, Rocky Mountain
spotted fever, scrub typhus, Q fever, rickettsialpox, trench fever)
are covered anywhere else. All 5 are genuinely relevant beyond the
source's own military context: tularemia connects directly to this
wiki's existing hunting/trapping/butchering content (real risk from
handling wild rabbits/rodents); leptospirosis connects directly to
flood/disaster water exposure; relapsing fever is explicitly noted
in the source as occurring in the western US; the rickettsial
cluster covers common US tick/louse/flea/mite exposure. Deliberately
NOT seeded from this same stretch of source material: yaws, endemic
syphilis, pinta, and rat-bite fever (real diseases, but essentially
restricted to specific tropical/endemic-poverty contexts not
relevant to this wiki's intended real-world use), and syphilis
(already covered under "Sexually Transmitted Infections").

Rather than create 6 separate thin pages for the individual
rickettsial diseases (epidemic typhus, murine typhus, RMSF, scrub
typhus, Q fever, etc.) -- which share the same real practical
takeaway (unexplained fever + rash after a tick/louse/flea/mite
exposure = treat with tetracycline/doxycycline, don't try to pin
down the exact species) -- they're combined into one page that
preserves each disease's real distinguishing features while leading
with the shared, more actionable pattern.

Real antibiotic dosing from the source is included, consistently
flagged (as with the existing Gangrene and Cholera/Typhoid pages)
as needing real medical administration, not home guessing.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_zoonotic.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Tularemia (Rabbit Fever) — Real Risk From Handling Wild Game",
        "section": "reference",
        "tags": ["tularemia", "wild-game", "zoonotic-disease"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**This real disease connects directly to trapping and butchering wild rabbits/rodents** already covered elsewhere in this wiki — anyone processing wild game should know this risk exists.

## Real Cause & Spread

**Caused by bacteria infecting wild rodents, especially rabbits and muskrats.** Real transmission routes: **direct contact with infected animal tissue while trapping, skinning, or butchering**; the bite of certain ticks and biting flies; eating infected meat that wasn't cooked thoroughly; or drinking contaminated water. **Real incubation period: 2-10 days.**

## Real Signs

**Sudden fever, headache, and nausea**, with a papule (small bump) developing at the site where the bacteria entered — this soon ulcerates. The lesion is often on an exposed extremity (consistent with a skinning-knife nick or contaminated hands) or, less commonly, the eye. **If the exposure was through eating contaminated meat, it can instead show up as gastrointestinal illness, stupor, and delirium.** General rash, body aches, and prostration can occur. **Nearby lymph nodes become enlarged, tender, and may fill with pus.**

## Real Treatment & Prevention

**⚠️ Real antibiotic treatment: streptomycin combined with tetracycline, continued until 5 days after the fever resolves** — this needs real medical administration, not home guessing, but is worth knowing as the real drug-of-choice combination if a clinician is reachable. **Adequate fluid intake matters throughout.** A pus-filled lymph node may need draining, but only after antibiotic treatment has had time to work.

**⚠️ Real prevention, directly actionable for anyone processing wild game:** wear gloves when skinning or butchering wild rabbits, hares, muskrats, or other rodents; cook wild game meat thoroughly; avoid drinking from water sources that could carry it; use tick/insect protection in the field.

## Detailed Version

**The real, practical takeaway: an unexplained fever and swollen, tender lymph node showing up within 2-10 days of trapping, skinning, or eating wild rabbit or rodent meat is specifically worth connecting to that activity** rather than assuming it's an unrelated bug — this is exactly the kind of real occupational-hazard knowledge that doesn't come up unless someone is actually doing the trapping/butchering themselves.
""",
    },
    {
        "title": "Anthrax — Real Signs in Those Handling Livestock",
        "section": "reference",
        "tags": ["anthrax", "livestock", "zoonotic-disease"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**A real disease of sheep, cattle, horses, goats, and swine that can transfer to humans** — uncommon, but real risk is concentrated specifically in farmers, people butchering/processing livestock, and anyone working with animal hides or wool.

## Real Cause & Spread

**Transmitted to humans through broken skin or mucous membranes, or by inhaling contaminated dust/particles** (the inhaled form is historically called "woolsorter's disease" from exposure while processing contaminated wool/hides).

## Real Signs — Cutaneous (Skin) Form

**A red bump appears on exposed skin, develops a blister, then forms a distinctive purple-to-black center** — the surrounding area becomes swollen. The center eventually forms a dead, blackened scab (eschar) that sloughs off. Malaise, headache, nausea, and vomiting may accompany it. **⚠️ Real, important danger: after the scab sloughs off, the infection can spread into the bloodstream** — shock, bluish skin, sweating, and collapse are real signs of this more serious progression. **Anthrax bloodstream infection can occur even without any visible skin lesion.**

## Real Signs — Pulmonary (Inhaled) Form

**Fever, malaise, headache, and labored breathing with cough** — this form shows signs resembling pneumonia.

## Real Treatment

**⚠️ Real antibiotic treatment: penicillin G, high-dose IV; or for mild, localized skin cases, tetracycline for 10 days** — this needs real medical administration, not home guessing, but is worth knowing as the real drug-of-choice information if a clinician is reachable.

## Detailed Version

**The real, most important practical idea: a skin lesion with a distinctive black center, appearing on exposed skin after handling livestock, carcasses, hides, or wool, is specifically worth treating as a real possible anthrax exposure** rather than an ordinary infected cut — the usual "wash it and watch it" approach that works for most skin infections is not adequate here, since the bloodstream spread this specific disease can cause is a genuine emergency.
""",
    },
    {
        "title": "Leptospirosis — Real Risk From Flood & Contaminated Water Exposure",
        "section": "reference",
        "tags": ["leptospirosis", "flood", "contaminated-water"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**This is a real, specific reason to avoid wading through or bathing in floodwater** — it's one of the few diseases on this page transmitted through intact skin and even the eyes, not just by drinking contaminated water.

## Real Cause & Spread

**Caused by Leptospira bacteria, found worldwide.** Real transmission routes: eating or drinking food/water contaminated by rodent, cattle, or pig urine or waste; direct contact through minor skin breaks; **probably also through the eyes**; and **real, important: through bathing or wading in contaminated water** — flooding that mixes sewage, animal waste, and standing water is exactly the real-world scenario this applies to. **Real incubation period: 2-20 days.**

## Real Signs

**Sudden fever (102-104°F), chills, abdominal pain, vomiting, nausea, muscle aches (especially the calves), and a relentless headache behind the forehead.** Light sensitivity, sore throat, cough, and diarrhea are common. A rash may appear. **Most cases clear up within 3-4 days, but some people stay sick for weeks.** **⚠️ Real, important pattern: symptoms can disappear for 1-3 days, then the fever and other signs return** — don't mistake this lull for the illness being over.

**As it progresses:** the eyes become markedly red/bloodshot; the liver becomes noticeably enlarged in about half of cases, with **jaundice typically appearing around day 5**; small capillary hemorrhages and purple skin spots can appear; meningitis-like irritation can occur.

## Real Treatment

**⚠️ Real antibiotic treatment: procaine penicillin IM, or tetracycline for 7 days** — this needs real medical administration, not home guessing, but is worth knowing as the real drug-of-choice information if a clinician is reachable.

## Real Prevention

**Avoid wading, swimming, or bathing in floodwater or water that could be contaminated by rodent or livestock waste.** Cover any skin breaks before unavoidable water contact, and avoid letting floodwater get in the eyes or mouth.

## Detailed Version

**The real, most actionable idea on this page: unlike cholera or typhoid, which need contaminated water to be swallowed, this disease can enter through skin contact and the eyes alone** — which is specifically why floodwater exposure itself (not just drinking it) is a real, independent risk worth protecting against, even for someone who is careful never to drink from a contaminated source.
""",
    },
    {
        "title": "Tick & Louse-Borne Relapsing Fever — Real Signs & the Relapsing Pattern",
        "section": "reference",
        "tags": ["relapsing-fever", "tick-borne", "louse-borne"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**A real spirochete-bacteria disease spread by tick bite, or by crushed lice getting into broken skin** — the source specifically notes the tick-borne form occurs in the western US and Canada (in addition to Mexico, Central/South America, Europe, Africa, and Asia), so this isn't purely an overseas concern. **Real incubation period: 2-10 days, occasionally up to 3 weeks.**

## ⚠️ Real Signs — The Relapsing Pattern Is the Diagnostic Clue

**Sudden onset of high fever (up to 104-105°F), chills, dizziness, severe headache, nausea, and vomiting.** A temporary rash can appear during the initial fever, usually most visible around the neck and shoulders before spreading to the chest and abdomen. **The initial fever episode usually lasts 3-10 days.**

**⚠️ Real, most important diagnostic feature: after 1-2 weeks symptom-free, the fever RELAPSES — often somewhat milder than the first time.** **Real pattern: there can be anywhere from 3 to 10 of these relapses before the person finally recovers.** Rapid heartbeat is common at each onset; delirium can occur with high fever; a yellow tinge to the eyes (jaundice) is common and can become pronounced in severe cases.

## Real Treatment

**⚠️ Real antibiotic treatment: a single oral dose of tetracycline or erythromycin, or a single IM dose of procaine penicillin** — this needs real medical administration, not home guessing, but is worth knowing as the real drug-of-choice information if a clinician is reachable. **Real, notable detail: unlike many of the illnesses in this wiki, this one can genuinely be treated with a single dose rather than a multi-day course.**

## Detailed Version

**The real, most useful idea on this page: a fever that seems to fully resolve after about a week, then comes roaring back 1-2 weeks later, is itself a real and recognizable pattern** — rather than assuming a "second, unrelated illness" has struck, recognizing this relapsing rhythm (especially after a known tick or lice exposure) points specifically toward this disease and its real, simple single-dose treatment.
""",
    },
    {
        "title": "Tick, Lice & Mite-Borne Fevers — Recognizing the Rickettsial Diseases",
        "section": "reference",
        "tags": ["rickettsial-disease", "tick-borne", "typhus"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**This page covers a real family of related diseases — all spread by the bite (or crushed/scratched bite site) of ticks, lice, fleas, or mites — that largely share the same real practical bottom line: you don't need to identify the exact species to act correctly.** All of them call for the same antibiotic family, and all of them are worth treating seriously rather than dismissing as "just a bug bite fever."

## Real Shared Pattern Across All of Them

**Fever, headache, and malaise, developing days after a bite from an infected tick, louse, flea, or mite** — often with a rash that develops after the fever starts, and sometimes with a distinctive dark scab (eschar) forming right at the bite site itself.

**⚠️ Real, universal treatment: tetracycline or chloramphenicol (doxycycline is a modern equivalent), started as early as possible** — real response is prompt when treatment starts early, and delaying treatment while trying to pin down the exact species is not worth the real risk of some of these progressing to more severe complications (meningitis, pneumonitis, myocarditis, or kidney involvement have all been described across this family).

## Real Distinguishing Features, by Disease

**Rocky Mountain spotted fever (tick-borne):** 3-10 days after a tick bite — chills, fever, bone/joint/muscle aches. **⚠️ Real, distinctive rash pattern: starts on the wrists and ankles first, THEN spreads inward to the arms, legs, and trunk** — the opposite direction from some of the other rashes in this family. Starts small and red, becomes larger and can turn into small hemorrhage-like spots over 2-3 days.

**Epidemic louse-borne typhus:** 10-14 days after exposure — abrupt chills, high unremitting fever, severe headache, progressing toward delirium if untreated. **Rash appears first in the armpits and spreads over the trunk then the limbs — it rarely involves the face, palms, or soles** (a real, useful contrast to Rocky Mountain spotted fever's wrist/ankle start). **⚠️ Real, unusual feature: someone who recovers can carry the organism for years and have a spontaneous recurrence without being bitten again** — and can become a new source of infection for lice during that recurrence.

**Murine (flea-borne) typhus:** Milder, shorter version of epidemic typhus (6-13 days of fever) — carried by rats and their fleas, so real risk is tied to rat-infested conditions.

**Scrub typhus (mite-borne):** 1-3 weeks after a mite-larva bite — malaise, chills, severe headache and backache, **with a flat black scab forming right at the actual bite site.** Rash develops by the end of the first week, most visible on the trunk.

**Q fever (from cattle, sheep, goats — inhaled dust or unpasteurized milk):** Headache, prostration, muscle pain, sometimes a dry cough or abdominal pain — **real, notable difference: no tick/louse/mite bite is needed at all, just airborne exposure to contaminated animal dust or droplets, or drinking unpasteurized milk.**

**Rickettsialpox (mite-borne, from mice) and trench fever (louse-borne):** both generally milder and self-limited; rickettsialpox causes a chickenpox-like scattered rash, trench fever causes a relapsing fever with pain behind the eyes and in the back/legs.

## Real Prevention (Shared Across the Whole Family)

**Protective clothing, insect repellent, and frequent tick checks (with a buddy, for hard-to-see spots) for the tick-borne forms; delousing (clothing, bedding, frequent bathing) for the louse-borne forms; rodent and flea control for the flea-borne/rat-associated forms.**

## Detailed Version

**The real, most useful idea across this entire page: a fever with a rash and/or a dark scab at a bite site, appearing days to weeks after real exposure to ticks, lice, fleas, or mites (or contaminated animal dust), deserves tetracycline-family treatment started early — regardless of which exact rickettsial species turns out to be responsible.** The specific rash patterns and timelines above are genuinely useful for narrowing things down, but they're refinements on top of that one actionable decision, not a prerequisite for it.
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
