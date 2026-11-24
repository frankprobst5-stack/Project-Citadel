#!/usr/bin/env python3
"""Seeds 3 more real Emergency Now / reference pages: Choking, CPR, and
Dental Emergencies.

Real judgment call made while researching this batch, worth recording:
this Vault already has a real, text-extractable military first aid
manual (Medical/FM-4-25-11-First_Aid.pdf) that covers choking response
-- but its technique (abdominal-thrusts-only, then a blind finger
sweep if unresponsive) is now superseded. Current civilian guidance
(Red Cross's "5-and-5" -- 5 back blows, then 5 abdominal thrusts,
alternating; and starting chest compressions, not a blind finger
sweep, if the person goes unresponsive) is meaningfully different and
is what's actually taught today. Using the old manual here just
because it's a real local PDF would mean publishing superseded
technique under a "verified" label -- so Choking and CPR are sourced
from current Red Cross/AHA guidance instead (via WebSearch, since both
redcross.org and heart.org block direct WebFetch with a 403 -- the
search tool still surfaces and cites their real indexed page content).
"Verified" has to track what's actually current, not just what's
closest at hand.

Dental Emergencies IS mined from a real local PDF:
Medical/Where-There-is-No-Dentist.pdf (Hesperian Health Guides) --
confirmed to have a real text layer via pdftotext before transcribing
anything. That book's own stated audience is community health workers
in places with zero dental access, which is exactly why it includes
real antibiotic dosing for a tooth abscess -- a genuinely different
context than "skip the dentist," and the page says so explicitly.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_cpr_choking_dental.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
DENTIST_PDF_URL = "/files/pdfs/Medical/Where-There-is-No-Dentist.pdf"

PAGES = [
    {
        "title": "Choking — Adult & Child Response",
        "section": "emergency",
        "tags": ["choking", "first-aid"],
        "risk_level": "critical",
        "source_url": "https://www.redcross.org/take-a-class/resources/learn-first-aid/adult-child-choking",
        "body_markdown": """## Quick Version

**First, ask "are you choking?"** If they can cough, speak, or cry, their airway isn't fully blocked — encourage coughing, don't intervene yet.

**Signs of a fully blocked airway:** weak or no cough, high-pitched squeaking or no sound at all, pale or blue skin color, can't cough/speak/cry.

**The 5-and-5 technique** (responsive adult/child):
1. **5 back blows:** stand slightly behind and to the side, one arm diagonally across their chest, bend them forward at the waist until their upper body is close to parallel with the ground, strike firmly between the shoulder blades with the heel of your hand.
2. **5 abdominal thrusts:** stand behind them, find their navel with two fingers, make a fist with your other hand and place the thumb side against their stomach just above those fingers, cover that fist with your other hand, pull inward and upward.
3. **Alternate 5-and-5** until the object comes out or they go unresponsive.

**If they become unresponsive:** lower them to a firm, flat surface and begin CPR, starting with chest compressions.

## Detailed Version

The back-blow-then-abdominal-thrust sequence (not abdominal thrusts alone) is current Red Cross guidance. If you're trained and the object becomes visible in the mouth during this process, you can remove it — but don't do a blind finger sweep (reaching in without seeing the object); that can push an obstruction deeper rather than clear it, which is why older guidance recommending it has been phased out.

A person in advanced pregnancy, someone too large to wrap your arms around, or someone with a significant abdominal injury should get chest thrusts (hands centered on the breastbone) instead of abdominal thrusts.
""",
    },
    {
        "title": "CPR — Hands-Only, Adult",
        "section": "emergency",
        "tags": ["cpr", "cardiac-arrest", "first-aid"],
        "risk_level": "critical",
        "source_url": "https://cpr.heart.org/en/resuscitation-science/cpr-facts-and-stats",
        "body_markdown": """## Quick Version

1. **Check responsiveness.** Tap and shout. If unresponsive and not breathing normally — call 911 (or have someone else call) and get an AED if one's nearby.
2. **Position:** firm, flat surface. Kneel beside the person.
3. **Hand placement:** heel of one hand on the center of the chest, other hand on top, fingers interlaced, shoulders directly over your hands, elbows locked straight.
4. **Push hard and fast:** **100-120 compressions per minute**, at least **2 inches deep** for an average adult (but not deeper than about 2.4 inches).
5. **Let the chest fully recoil** between compressions — don't lean on it.
6. **Keep going without stopping** until an AED is ready to use, professional help arrives, or the person starts breathing/moving on their own.

**If you're an untrained bystander: compressions only, no rescue breaths — this is "Hands-Only CPR" and it's the current recommended approach for an untrained responder.**

## Detailed Version

Hands-Only CPR exists specifically because the 2015+ resuscitation guidelines found that untrained bystanders doing continuous compressions (no breaths) perform better in practice than bystanders attempting a compression-breath combination they haven't actually trained for — hesitating to get breath technique "right" costs real time that compressions alone don't.

Don't worry about counting perfectly or hitting an exact rhythm — the "about 2 per second" pace (100-120/min) matters more than precision, and continuing without long pauses matters most of all. If an AED arrives, turn it on and follow its own voice prompts — it will guide you through pad placement and timing.

This page intentionally does not cover rescue breaths, child/infant CPR, or AED operation in detail — those need real hands-on training (a 2-4 hour certified course), not a wiki page, to perform safely.
""",
    },
    {
        "title": "Dental Emergencies — Tooth Abscess",
        "section": "reference",
        "tags": ["dental", "tooth-abscess", "infection"],
        "risk_level": "high",
        "source_url": DENTIST_PDF_URL,
        "body_markdown": """## Quick Version

**Signs of a tooth abscess:** constant pain (even when trying to sleep), the tooth feels longer or a bit loose, pain when tapped, a sore ("gum bubble") on the gum near the root, swelling of the gum or face on that side.

**This is a real infection, not just a bad tooth** — pus building up at the root causes the pain, and it can spread. Get to a dentist or doctor as soon as one is reachable. The guidance below is specifically for when none is reachable at all, drawn directly from *Where There Is No Dentist* (Hesperian Health Guides — written for community health workers in places with zero dental access).

**If there's swelling:** treat the swelling first (antibiotic + warm compresses) before attempting to pull the tooth — a local anesthetic won't work properly through active swelling.

**If there's no swelling:** the tooth should come out as soon as possible to let the pus escape and relieve the pressure, unless you're equipped to do an actual root canal.

## Detailed Version — only when no dental/medical care is reachable at all

*Transcribed from* Where There Is No Dentist *(Hesperian Health Guides) — the real book is attached to this page. This is real antibiotic dosing meant for the book's own stated context: community health workers with no dentist or doctor to refer to. If any professional care is reachable, use it instead of self-dosing antibiotics.*

**Treating the swelling (if present):**
- **Penicillin by mouth** is the first choice. Adults and anyone over 25 kg (60 lb): first dose 4×250mg tablets (1000mg) all at once, then 2 tablets (500mg) every 6 hours for 5-7 days. Children under 25 kg take half that amount.
- **If allergic to penicillin:** erythromycin, same dosing pattern, for 5 days — taken with meals to avoid stomach upset. (Anyone allergic to penicillin is also allergic to amoxicillin/ampicillin — don't substitute those instead.)
- Take the *entire course*, even once pain or swelling improves — stopping early risks the infection returning worse than before.
- Warm compresses: soak a cloth in warm water against the face, or hold warm water inside the mouth near the swelling, as often as possible until swelling subsides.
- For pain: aspirin (adults: 600mg/4× daily) or acetaminophen (adults: 1000mg/4× daily) — acetaminophen is safer for children and doesn't cause the stomach irritation aspirin can.
- The tooth can usually come out 1-2 days before finishing the antibiotic course, but the person must finish every dose regardless.

**If the swelling is "pointing"** (a visible, soft, ready-to-drain bump), it can be opened with a sharp, sterilized blade to release the pus, then covered with a sterile dressing — this is a real procedure requiring real sterile technique, not something to attempt casually.

**The book's own standing rule, worth repeating here:** "Never pretend to know something you do not. Only treat problems that you are sure about and have supplies to treat properly." When in doubt, that's the signal to seek more experienced help, not to guess.
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
