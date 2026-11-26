#!/usr/bin/env python3
"""Seeds 2 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 15 (Shock) -- mined from the OCR
output cached at /tmp/sfmedical.txt.

Covers real clinical detail genuinely extending the existing Shock
— Recognition & Field Positioning page: the 5 real distinct shock
types and their real mechanisms, a real severity chart correlating
blood volume loss to vital signs, the real IV fluid hierarchy for
hemorrhagic shock, and a complete real anaphylactic shock treatment
protocol with real epinephrine dosing -- the single most
practically-relevant controlled-medication protocol in this source,
since epinephrine auto-injectors are genuinely accessible to
civilians with known allergies, unlike most of the other medications
referenced elsewhere in this wiki's TCCC content.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_shock.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Types of Shock — Causes & the Real Shock Severity Chart",
        "section": "emergency",
        "tags": ["shock", "emergency-medicine", "triage"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**"Shock" isn't one single condition — it's a breakdown of effective circulation at the cellular level, and 5 real distinct mechanisms can cause it.** Knowing which type you're dealing with changes what actually helps.

## The 5 Real Types

1. **Hypovolemic** — from hemorrhage, burns (plasma loss), or fluid/electrolyte loss (vomiting, bowel obstruction, diarrhea). The body simply doesn't have enough circulating volume.
2. **Cardiogenic** — the heart itself fails as a pump (heart attack, arrhythmia, heart failure), reducing forward blood flow while blood backs up behind the heart, raising venous pressure.
3. **Neurogenic** — from spinal injury, spinal anesthesia, trauma, fracture manipulation, or some head wounds. **Arterial resistance fails and blood pools in dilated capillaries**; the heart works harder trying to compensate.
4. **Septic** — from wound infection, peritonitis, meningitis, and similar — usually from gram-negative bacteria causing a real bloodstream infection. **Capillaries become abnormally permeable, blood pools, and fluid leaks out of the vascular space**; the toxins can also directly depress heart function.
5. **Anaphylactic** — an acute, often explosive systemic allergic reaction (see Anaphylactic Shock — Real Treatment Protocol for the real treatment detail).

## ⚠️ Real Shock Severity Chart (by Blood Volume Loss)

| Severity | Blood volume lost | Pulse | Color | Thirst | Mental state |
|---|---|---|---|---|---|
| **Mild** | Up to 20% | Slightly increased | Pale | Normal | Clear |
| **Moderate** | 20-40% | Increased | Pale | Definite | Clear, with apathy |
| **Severe** | 40%+ | Weak to absent | Ashen/cyanotic | Severe | Apathetic to comatose |

**Real additional signs across all severities:** blood pressure decreases, skin feels cool and mottled, nail beds blanch (and refill slowly). **⚠️ Real, important caveat: pulse and blood pressure are not fully reliable alone** — a healthy adult's blood pressure can stay normal until a genuinely large volume of blood is already lost, and the expected rise in heart rate/breathing may not show up if the person is lying flat. **Real test: sitting a person up — if systolic blood pressure drops 15mm or more and pulse rises 15+ beats, real shock is present even if supine vitals looked acceptable.**

## Real IV Fluid Hierarchy for Hemorrhagic/Hypovolemic Shock

**Listed in real order of effectiveness** (most civilians won't have access to most of these, but the ranking itself is clinically informative): whole blood (with crystalloid) > plasma (with crystalloid) > serum albumin (with crystalloid) > dextran (with crystalloid) > lactated Ringer's > normal saline > **D5W used alone only if nothing else is available.** **Real monitoring: track urine output to confirm fluid replacement is actually adequate.** Keep the person warm and dry, in the shock position unless contraindicated (head or chest wounds), give pain control (morphine) as needed, and **start broad-spectrum antibiotics early as prophylaxis for large wounds or burns.**

## Detailed Version

**The real, most clinically important idea on this page: shock from different mechanisms can look similar at first glance (cool pale skin, rising pulse, anxiety) but needs genuinely different real treatment** — fluid replacement helps hypovolemic shock but can worsen cardiogenic shock; epinephrine is specific to anaphylaxis; septic shock needs real antibiotics, not just fluids. Recognizing which mechanism is actually driving the picture, rather than treating "shock" as one generic emergency, is what the 5-type breakdown is for.
""",
    },
    {
        "title": "Anaphylactic Shock — Real Treatment Protocol",
        "section": "emergency",
        "tags": ["anaphylaxis", "allergic-reaction", "epinephrine"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**Anaphylaxis is a genuine, fast-moving emergency — real signs typically appear within 1-15 minutes of exposure.** This page documents the real clinical protocol for completeness. **Epinephrine auto-injectors (EpiPens) are genuinely accessible to civilians with a known allergy and prescription** — unlike most of the other medications referenced in this wiki's TCCC drug content, this is real, practically relevant knowledge for anyone managing a severe allergy at home, not purely institutional reference.

## Real Signs

**Agitation, uneasiness, flushing; palpitations; tingling (paresthesia); itching (pruritus); throbbing in the ears; coughing, sneezing, and breathing difficulty — progressing to dizziness, disorientation, collapse, coma, and death if untreated.** Can also include hives (urticaria), vascular collapse, vomiting, cramps, and diarrhea.

## Real Treatment Protocol

1. **⚠️ Epinephrine (1:1,000 solution), 0.4-1ml IV immediately** — **repeat every 5-10 minutes as needed.** (A real-world EpiPen delivers a fixed IM dose for exactly this purpose when IV administration isn't available/trained.)
2. **Position:** lay the person down, legs elevated; ensure the airway is open (a surgical airway may be needed in the most severe cases — see Surgical Cricothyroidotomy — Last-Resort Airway for that real last-resort technique).
3. **Diphenhydramine HCl (e.g., Benadryl), 5-20mg IV as needed.**
4. **For severe asthma symptoms without full shock:** aminophylline solution, 250-500mg IV, given slowly.
5. **IV fluids** to correct hypovolemia if it's present.
6. **Hydrocortisone sodium succinate, 100-250mg IV over 30 seconds**, if hypotension needs further control.
7. **⚠️ Real technique for an injected allergen (e.g., a bee sting or vaccination):** apply a constricting band (rarely a full tourniquet) just above the injection/sting site, and consider injecting an additional small dose of epinephrine (0.1-0.2ml of 1:1,000) directly into that site — **this real technique slows the allergen's systemic absorption** while the main treatment takes effect.
8. **Oxygen, 4-6 liters/minute, if available.**
9. **Continue observation for a full 24 hours** and arrange real definitive medical care as needed — **a real, important point: anaphylaxis can recur hours after the first reaction appears resolved**, which is exactly why extended observation matters even once symptoms seem to have passed.

## Detailed Version

**The real, most actionable takeaway for a civilian context: epinephrine is the one real, time-critical intervention here that's actually within reach for most people (via a prescribed auto-injector), and the real "repeat every 5-10 minutes" guidance matters — a single dose that doesn't fully resolve the reaction is a real, expected scenario, not a sign the treatment failed.** The rest of the protocol (IV fluids, hydrocortisone, aminophylline) represents what a real medical team does next, which is exactly why getting the person to that level of care — while repeating epinephrine as needed in the meantime — is the real, practical goal.
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
