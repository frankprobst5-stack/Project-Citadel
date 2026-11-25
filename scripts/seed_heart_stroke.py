#!/usr/bin/env python3
"""Seeds 2 real emergency pages: Heart Attack & Heart Trouble, and
Stroke. Signs and general-care content mined from Where There Is No
Doctor's Chapter 22 (real text layer already extracted); the specific
emergency-response actions (chew aspirin for a heart attack, do NOT
give aspirin for a stroke, the FAST/BE-FAST check) are sourced from
current guidance instead, for a real reason worth recording:

The book recommends "one aspirin tablet a day" as prevention for
BOTH heart attack and stroke, with no real distinction drawn between
preventive daily use and emergency in-the-moment use. Current
guidance draws a sharp, safety-relevant line the book doesn't: chewing
aspirin immediately IS the right emergency response for a suspected
heart attack, but giving aspirin during a suspected stroke is
specifically discouraged -- some strokes are caused by bleeding in the
brain, and aspirin (a blood thinner) can make that bleeding worse.
Mixing these two up in an emergency is a real, documented danger, not
a minor nuance -- so this split is treated as a hard rule, not a
footnote.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_heart_stroke.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Heart Attack & Heart Trouble",
        "section": "emergency",
        "tags": ["heart-attack", "cardiac"],
        "risk_level": "critical",
        "source_url": "https://www.lphealthdirections.com/resources/heart-attack-what-to-do/",
        "body_markdown": """## Quick Version

**Heart attack signs:** a sharp pain like a great crushing weight on the chest that does NOT go away with rest — sometimes spreading to the left shoulder or arm. **Women more often get different signs than the "classic" crushing chest pain:** indigestion-like discomfort, nausea, clammy skin, jaw pain, unexplained tiredness or shortness of breath. Don't dismiss these as "not a real heart attack" just because they don't match the dramatic version.

**If a heart attack is suspected:**
1. **Call 911 immediately.**
2. **If the person isn't allergic to aspirin and has no major bleeding risk, have them chew (not just swallow) one adult aspirin (325mg) or 2-4 low-dose (81mg) tablets.** Chewing gets it into the bloodstream roughly twice as fast as swallowing whole.
3. Have them rest, sitting or lying in whatever position is most comfortable for breathing, in a cool quiet place.
4. If they lose responsiveness and stop breathing normally, begin CPR.

**Angina** (chest/arm pain brought on by exertion that eases with a few minutes of rest) is a real warning sign of heart disease, not the same emergency as a full heart attack — but new, worsening, or longer-lasting episodes deserve real medical evaluation, not just resting it off every time.

## Detailed Version

**Real risk factors worth acting on, not just noting:** being overweight, smoking, high blood pressure, and age all raise real heart attack/stroke risk — and the single biggest lever most people actually control is diet, exercise, and quitting smoking, not medication alone.

**A real, current correction worth being explicit about:** taking daily aspirin specifically to *prevent* a future heart attack is no longer broadly recommended for most adults (current guidance limits this to specific higher-risk situations, due to real bleeding risk) — that's different from chewing aspirin *during* a suspected heart attack right now, which remains correct emergency guidance. Don't conflate "should I take aspirin every day" with "should I chew aspirin right now during a heart attack" — these are different questions with different current answers.

If chest pain is severe and doesn't ease with rest, or shock signs appear (weak rapid pulse, clammy skin, confusion), real heart damage has likely occurred — the person needs real medical care and an extended recovery period, not just bed rest at home.
""",
    },
    {
        "title": "Stroke",
        "section": "emergency",
        "tags": ["stroke", "cardiac"],
        "risk_level": "critical",
        "source_url": "https://www.lphealthdirections.com/resources/stroke-signs-what-to-do/",
        "body_markdown": """## Quick Version

**Check BE-FAST:**
- **B**alance — sudden loss of balance or coordination.
- **E**yes — sudden vision change/loss.
- **F**ace — one side drooping or uneven when they smile.
- **A**rm — one arm drifts down when both are raised.
- **S**peech — slurred, strange, or difficult to produce.
- **T**ime — if any of the above, call 911 immediately and note exactly when symptoms started (or the last time the person was known to be normal) — this timing is critical information for the treating hospital.

**Do NOT give aspirin for a suspected stroke** — unlike a heart attack, this is actively discouraged here. Some strokes are caused by bleeding inside the brain, and aspirin (a blood thinner) can make that bleeding worse. Let emergency medical responders make all medication decisions.

**While waiting for help:**
- Lay the person down with the head slightly elevated above the feet.
- **If unconscious:** tilt the head back and to the side so saliva or vomit drains out rather than into the lungs. Give nothing by mouth — no food, drink, or medicine.
- Stay with them and keep them calm.

**Call 911 even if symptoms start improving** — some stroke symptoms can temporarily ease and then worsen again; "it's getting better" is not a reason to skip emergency care.

## Detailed Version

A stroke happens when blood flow to part of the brain is interrupted — either a clot blocking a vessel, or bleeding into brain tissue — which is exactly why aspirin is a gamble rather than a help in the moment: it's genuinely helpful if the cause is a clot, and genuinely harmful if the cause is bleeding, and there's no way to tell which without real imaging. That specific uncertainty is why "let EMS decide" is the right call, not an evasion.

After a stroke, real recovery can include real paralysis on one side, speech/vision/thinking difficulty — some of which improves with time. Helping someone relearn to walk (a cane, favoring the stronger side) and self-care with their functioning hand are real, practical parts of recovery, alongside avoiding heavy exertion and emotional stress during that period.

**A real, separate condition worth distinguishing:** sudden one-sided facial paralysis with no other stroke signs (no arm weakness, no speech trouble) in an otherwise younger or middle-aged person is more likely Bell's Palsy — a temporary facial nerve issue that usually resolves on its own over weeks to months, not a stroke. It still deserves a real evaluation to rule out stroke, but the prognosis is very different. A real, simple interim care step: if the affected eye can't fully close, tape or bandage it shut at night to prevent dryness-related damage.
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
