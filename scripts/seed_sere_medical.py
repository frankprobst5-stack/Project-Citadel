#!/usr/bin/env python3
"""Seeds 2 real pages from the Navy/Marine Corps SERE Student
Handbook's Medical chapter -- mined from the real text layer already
extracted in this session (/tmp/sere.txt). Most of this handbook
(Code of Conduct, Geneva Convention, Recovery Operations, Evasion,
Induced Conditions/POW resistance) is combat/captivity-specific and
is deliberately not mined. Its Medical chapter substantially overlaps
with TCCC and other sources already covered in this wiki (airway,
bleeding control, tourniquets, shock, fractures) -- but it contains
a handful of genuinely new, complementary real details not captured
elsewhere: an improvised 3-sided-tape chest seal technique (a
different real approach than the full-seal vented chest seals already
covered from TCCC), flail chest, specific finger-splinting
positioning, a real heat/cold cycling rule for fracture care, and a
real saline ratio for burn-related fluid loss.

This script deliberately does NOT re-seed content already covered
(airway/breathing basics, general bleeding control, shock, general
tourniquet technique) -- only the real, new, complementary details.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sere_medical.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
SERE_PDF_URL = "/files/pdfs/Military Manuals/Navy-Marine-Corps-SERE-Student-Handbook.pdf"

PAGES = [
    {
        "title": "Chest Trauma — 3-Sided Tape Seal & Flail Chest",
        "section": "emergency",
        "tags": ["chest-trauma", "sucking-chest-wound", "flail-chest"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This page covers 2 real chest-trauma techniques that complement, rather than replace, Penetrating Chest Wounds — Chest Seals & Needle Decompression** (from the TCCC material already in this wiki) — a genuinely different improvised sealing technique, and a distinct injury (flail chest) not covered there.

## An Improvised 3-Sided Tape Seal (a Real Alternative to a Full Seal)

**Real signs of a sucking chest wound:** the chest wall is penetrated, the person may gasp for breath, you may hear an actual sucking sound, and bloody froth can escape the wound as air passes through it.

1. **Seal the wound immediately with your hand or any airtight material** as a first step.
2. **Tape airtight material over the wound on 3 sides only — leave the 4th side untaped.** This real design creates a one-way (flutter) valve: air can escape outward through the open side when the person exhales, but the taped sides stop outside air from being drawn back in on inhale.
3. **Keep monitoring the dressing and the person's breathing.** If breathing gets harder, **lift the untaped side briefly to let trapped air vent out**, then let it reseal.

**⚠️ Real, important contrast with a standard vented chest seal: a commercial vented seal has a built-in valve; this improvised 3-sided design creates the same one-way effect using ordinary tape and any airtight material, specifically for situations where no purpose-built seal is available.**

## Flail Chest — a Distinct, Serious Injury

**Caused by blunt trauma breaking 3 or more ribs in 2 or more places** — that broken section (the "flail segment") moves opposite to the rest of the chest: it sinks in when the person inhales (while the rest of the chest expands) and bulges out when they exhale (while the rest of the chest falls).

**Real treatment:**
1. **Immediately immobilize the flail segment** — your hand pressed over the area, right away, to stop its paradoxical motion.
2. **If tape is available, tape the segment down from breastbone to backbone on the injured side — but do NOT wrap tape all the way around the chest**, which would dangerously restrict overall breathing.
3. **Without tape, keep the segment still using hand pressure, or roll the person onto their injured side** — this uses the ground/surface itself to immobilize the segment.

## Fractured Ribs (Without Flail Chest)

**Encourage deep breathing even though it's painful** — shallow breathing to avoid the pain raises real risk of pneumonia developing afterward. **Never tape or wrap the chest tightly enough to restrict breathing**, even though that impulse feels like it should help.

## Detailed Version

**The real principle distinguishing flail chest from an ordinary rib fracture: a flail segment's paradoxical motion actively interferes with normal breathing mechanics, which is why it needs immediate stabilization, while an ordinary fracture's main real risk is the person avoiding deep breaths out of pain — two different problems that look superficially similar but need genuinely different responses.**
""",
    },
    {
        "title": "Fracture Splinting Technique & Burn Fluid Loss",
        "section": "reference",
        "tags": ["fractures", "splinting", "burns"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Two real, specific details worth adding to general splinting and burn-care knowledge: how to actually position a splinted finger, and a real heat/cold timing rule for any fracture injury.**

## Real Splinting Technique

- Remove watches, rings, and constricting clothing near the injury before swelling makes that harder later.
- **Dress any wound where a fracture has broken through the skin** — clean it if possible before applying a dressing.
- Move the limb into as close to a normal position as you safely can, then improvise a splint from any available stiff, straight material, securing it to the body (a leg to the other leg, an arm to the chest).
- **If you can't safely move the limb to a normal position, splint it exactly as you found it instead** — don't force it.
- **⚠️ Splint a fracture by immobilizing the joints on both sides of the break; splint a joint injury by immobilizing the bones on both sides of the joint** — the real principle is to stabilize whatever structure sits adjacent to the actual damage.
- **Check for a pulse beyond the injury periodically** — this real check confirms the splint isn't cutting off circulation.

## ⚠️ Real Finger-Splinting Detail — Not Straight

**Splint an injured finger in a slightly flexed position, not straight — the hand should look like it's gently grasping an apple.** This is a real, specific, easy-to-get-wrong detail: the intuitive instinct to splint a finger perfectly straight is actually the less functional, less comfortable position for a healing finger joint.

## Real Heat/Cold Timing Rule for Fractures, Sprains & Dislocations

- **Apply cold during the first 24 hours after injury; switch to heat after that first 24-hour window.**
- **Use 15-20 minute application periods** for either — not continuous application.
- **⚠️ Never apply continuous cold or heat therapy** — both carry real risk of tissue damage if left in place too long without a break.

## Real Burn Fluid-Loss Detail

**Burns significantly increase real fluid loss from the body — drink water accordingly.** **A real, specific improvised oral rehydration ratio: mix ¼ teaspoon of salt into each quart of water** given to a burn patient, if salt is available — replacing lost electrolytes along with the fluid itself, not just plain water alone.

## Detailed Version

**The real, shared lesson across the finger-splinting detail and the heat/cold timing rule: the intuitively "obvious" choice (splint straight; apply cold or heat continuously, as long as possible) is the wrong one in both cases.** A joint that heals in the wrong position causes lasting dysfunction, and tissue exposed to continuous cold or heat risks its own separate injury on top of the original one — both real reasons this level of specific technique detail matters more than it might seem at first glance.
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
                "source_url": SERE_PDF_URL,
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
