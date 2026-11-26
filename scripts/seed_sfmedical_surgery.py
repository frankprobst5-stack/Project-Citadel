#!/usr/bin/env python3
"""Seeds 2 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 16 (Emergency War Surgery) --
mined from the OCR output cached at /tmp/sfmedical.txt (see
seed_sfmedical_primitive.py for OCR provenance).

Covers real surgical treatment-priority triage (the ABC rule plus a
real 3-tier priority system distinct from TCCC's MARCH, since this
source addresses surgical/definitive-care prioritization rather than
point-of-injury trauma care) and real wound debridement technique --
the real "4 Cs" test for distinguishing viable from dead tissue, and
the real delayed-primary-closure (DPC) protocol with real antibiotic
dosing. This extends, rather than duplicates, the brief debridement
overview already in this wiki from ATP 3-50.21.

This content describes real intermediate-level field surgical
technique written for trained Special Forces medics, not laypeople --
preserved here as real reference, with that context kept explicit,
consistent with how comparably advanced content (tooth extraction,
cricothyroidotomy) has been handled throughout this wiki.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_surgery.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Emergency War Surgery — Treatment Priorities (ABC & 3-Tier Triage)",
        "section": "reference",
        "tags": ["triage", "emergency-medicine", "trauma"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This reflects real medical doctrine written for trained Special Forces medics, not a laypeople's guide — the real value here is in understanding WHICH injuries genuinely need care first, even if you ultimately provide that care by getting the person to a trained provider rather than operating yourself.** This complements, rather than replaces, MARCH & PAWS — The TCCC Treatment Priority Framework and Mass Casualty Triage — IDME Categories already in this wiki — those address point-of-injury trauma care and sorting many casualties; this addresses prioritizing actual surgical/definitive treatment once someone capable of providing it is involved.

## The Real ABC Rule

- **A — Airway.** Confirm it's clear.
- **B — Breathing.** Confirm the person can actually breathe (no sucking chest wound or similar obstruction).
- **C — Circulation.** Confirm the heart is beating with adequate circulating blood volume.

## Real First Priority (Treat Immediately)

- **Asphyxia or respiratory obstruction** from mechanical causes, sucking chest wounds, tension pneumothorax, or maxillofacial wounds where asphyxia exists or is likely to develop.
- **Shock from:** major external or internal hemorrhage, visceral (internal organ) injury, massive muscle damage, major fractures, multiple wounds, or severe burns over 20% of the body.

## Real Second Priority

- **Visceral injuries:** GI tract perforation, biliary/pancreatic system wounds, genitourinary tract wounds, chest wounds without asphyxia.
- **Vascular injuries needing repair** — **⚠️ real, important rule: any injury severe enough to require a tourniquet automatically falls into this category**, not a lower one.
- **Closed head injuries with worsening consciousness.**
- **Burns covering 20%+ of specific sensitive locations:** hands, feet, genitals, perineum.

## Real Third Priority

- Brain/spinal injuries requiring decompression.
- Soft-tissue wounds needing debridement where muscle damage is NOT major.
- Lesser fractures/dislocations.
- Eye injuries.
- Maxillofacial injuries without asphyxia.
- Burns under 20% at other body locations.

## Detailed Version

**The real, useful mental model this page provides: injuries that threaten airway/breathing/circulation outrank injuries that are merely severe-looking, and within "severe," the specific combination (hemorrhage, shock risk, asphyxia risk) determines real urgency — not how dramatic an injury appears.** A tourniquet already in place is itself real, built-in evidence that an injury belongs in the second-priority vascular category, which is a genuinely useful, fast triage shortcut.
""",
    },
    {
        "title": "Wound Debridement — The 4 Cs & Delayed Primary Closure",
        "section": "reference",
        "tags": ["wound-care", "debridement", "surgery"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This describes real intermediate field-surgical technique for debriding a serious wound — genuinely more detailed than the basic debridement guidelines already in this wiki (see Treating an Infected Wound — Warm Compress Protocol & Maggot Therapy), and written for someone with real training.** The core real principle — remove everything dead or foreign, and leave the wound open rather than closing it immediately — is the same one already established throughout this wiki's wound-care content; this page adds the real specific technique for actually telling dead tissue from living tissue.

## The Real Goal

**Localize and isolate the damage** from a serious wound by removing all foreign material and dead tissue while preserving blood supply to what remains viable.

## The Real Two-Step Process

1. **Thorough debridement, done as early as possible after injury.** (If delay is unavoidable, start systemic antibiotics in the meantime.) **The wound is left open afterward, with few exceptions, to granulate** — the same real "open treatment" principle covered elsewhere in this wiki.
2. **Delayed primary closure (DPC), 4-10 days later** — only once the wound looks genuinely clean. The wound must stay clean through this window, and antibiotics are usually indicated throughout.

## Real Antibiotic Dosing (Started BEFORE Debridement)

- **Penicillin (aqueous):** 10 million units IV every 8 hours for 3 days, then reassess.
- **Kanamycin:** 500mg IM every 12 hours for 3 days, then reassess.
- **Tetanus toxoid:** 0.5cc IM or subcutaneous, once (test for allergy only if not previously immunized).

## Real Debridement Technique

**Make an incision long enough for real, adequate exposure** — over both entry and exit wounds, along the long axis of a limb (S-shaped where it crosses a joint crease), **avoiding incisions directly over superficial bone.** When trimming skin alone, cut back 2-3cm from the wound's edge. **Separate skin, fascia, and muscle for clear visibility, debriding each individual muscle group separately** rather than working through everything at once.

## ⚠️ The Real "4 Cs" — Distinguishing Viable From Dead Tissue

| Test | Viable tissue | Dead or dying tissue |
|---|---|---|
| **Color** | Bright reddish-brown (⚠️ the least reliable of the 4 signs on its own) | Dark, cyanotic |
| **Consistency** | Springy | Mushy |
| **Contractility** | Contracts when pinched or cut | Does not contract |
| **Circulation** | Bleeds when cut | Does not bleed |

**⚠️ Real priority rule: when in doubt, remove the tissue.** Leaving devitalized muscle behind to avoid a cosmetic deformity is explicitly the wrong trade — **a real, worse deformity from infection is the actual alternative**, not a clean save. **Cut dead muscle away in full strips or blocks along one side of a muscle group — never piecemeal, in small bits** — this real technique gives a cleaner, more complete removal than nibbling at it.

**Real exploration technique:** clear all blood clots, foreign material, and debris from the wound using a gloved finger, while **actively protecting major nerves and vessels from further damage**, and working gently throughout.

## Detailed Version

**The real, most load-bearing idea on this page is the 4 Cs test itself: color alone is explicitly the least reliable of the four signs, which is exactly why it's checked alongside consistency, contractility, and circulation rather than used by itself.** A single ambiguous sign (tissue that looks slightly dark but still bleeds and still contracts when cut) is a real, common judgment call this combined test exists specifically to resolve.
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
