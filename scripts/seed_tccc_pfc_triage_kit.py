#!/usr/bin/env python3
"""Seeds 5 more real pages from the TCCC Handbook, Version 5 -- mined
from the real text layer already extracted in this session
(/tmp/tccc.txt). Covers content genuinely applicable to a civilian
disaster/no-EMS-access scenario, not just combat:

- Mass casualty triage categories (Appendix C) -- directly relevant
  to any scenario with multiple injured people and limited help.
- Medical evacuation priority categories and helicopter LZ marking
  (Appendix D) -- relevant if ever coordinating a real medevac.
- Prolonged Field Care (Appendix F) -- the single most directly
  relevant TCCC appendix to a disaster-prep context: sustaining a
  casualty for an extended period when evacuation isn't coming soon.
- The real TCCC-Medical Provider drug reference guide (Appendix G),
  presented factually as reference -- several of these are
  controlled substances requiring real medical training and are
  documented here for completeness, not as a how-to for untrained
  self-administration.
- A real trauma kit packing list, built directly from the IFAK
  Generation I/II contents tables (Chapter 3), with the
  military-specific NSN stock numbers dropped since they're
  irrelevant to a civilian buyer.

The book's own real 9-Line MEDEVAC Request/MIST Report format
(Appendix E) is a figure/diagram in the source PDF, not text -- it is
deliberately NOT reproduced here, since this build-out's standing
discipline is to transcribe only confirmed real extracted text, never
reconstruct a figure's content from training-data recall.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_tccc_pfc_triage_kit.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
TCCC_PDF_URL = "/files/pdfs/Medical/TCCC-17-13-Army-Tactical-Combat-Casualty-Care.pdf"

PAGES = [
    {
        "title": "Mass Casualty Triage — IDME Categories",
        "section": "emergency",
        "tags": ["tccc", "triage", "mass-casualty"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**When there are more injured people than you can treat at once, triage — sorting people by how urgently they need care — is what actually saves the most lives.** The real categories, remembered by the acronym **IDME**: Immediate, Delayed, Minimal, Expectant. **No real treatment happens at the sorting stage itself** — triage is purely about rapidly deciding who goes where, then moving people to get actual care.

## Immediate

**Needs attention within minutes to 2 hours to avoid death or permanent disability.** Real examples: an airway that's blocked or at risk of becoming blocked, a tension pneumothorax, uncontrolled bleeding, a limb at risk of being lost, or multiple limb amputations. **This group goes first, full stop.**

## Delayed

**Needs real treatment (sometimes surgery) but can safely wait without a meaningfully higher risk to life, limb, or eyesight.** Real examples: blunt or penetrating torso injuries, fractures, significant soft-tissue injuries, facial fractures that aren't blocking the airway, eye injuries, and burns that are serious but survivable.

## Minimal

**Genuinely minor injuries** — small cuts, scrapes, small-bone fractures, minor burns — **that the person can largely manage themselves with basic care.** These people can often help carry or care for more seriously injured people. **A real, counterintuitive risk here: a crowd of walking-wounded minor cases can overwhelm your limited care capacity before you even finish sorting the serious ones** — control access to wherever you're treating people as soon as you realize you have a mass-casualty situation.

## Expectant

**The hardest category: injuries severe enough that treating them would consume resources needed to save people who can actually be saved.** Real examples given: no vital signs/signs of life, a gunshot wound through the skull, an open pelvic injury with uncontrolled bleeding and severe shock, burns without a realistic chance of survival, or a high spinal cord injury. **This category does NOT mean abandoning the person** — move them out of view of other casualties, and keep reassessing them periodically, providing comfort measures. Priorities can genuinely change if your resource situation improves or the person's condition changes.

## Detailed Version

**The real discipline behind triage is emotional as much as medical: it means consciously choosing to walk past someone who looks desperately injured to treat someone whose injury looks less dramatic but is actually more survivable with the resources on hand.** This is genuinely hard to do under stress, which is exactly why having the categories memorized in advance — before an actual mass-casualty event — matters; working it out in the moment, under real emotional pressure, is far harder than following a framework you already know cold.
""",
    },
    {
        "title": "Medical Evacuation Priority & Helicopter Landing Zones",
        "section": "emergency",
        "tags": ["tccc", "medevac", "evacuation", "helicopter"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**When multiple injured people need transport out and you can't move everyone at once, evacuation priority decides the order** — similar logic to triage, but specifically about who gets moved first.

## The Real Priority Categories

- **Priority I — Urgent:** evacuate as soon as possible, within a maximum of 1 hour, to save life, limb, or eyesight, or to prevent a serious complication/permanent disability.
- **Priority IA — Urgent Surgical:** needs real surgical intervention immediately to save life and become stable enough for further transport.
- **Priority II — Priority:** needs prompt care — evacuate within 4 hours, since waiting longer risks the person deteriorating into Urgent, or they need specialized treatment not available on-site, or they'd otherwise suffer unnecessary pain/disability.
- **Priority III — Routine:** needs evacuation, but isn't expected to significantly worsen — evacuate within 24 hours.
- **Priority IV — Convenience:** evacuation is a matter of convenience, not medical necessity.

**The more severe categories (Urgent, Urgent Surgical) get evacuated ahead of Priority or Routine cases whenever transport capacity is limited.**

## Marking a Helicopter Landing Zone

**The real marking system used by U.S. forces for a helicopter to identify a landing site: an inverted "Y" shape.** For daytime operations, there's normally no special LZ marking needed beyond smoke to show wind direction. At night, or when lighting is otherwise needed, that inverted "Y" can be formed with:
- Chemical glow sticks (Chemlights) placed on the ground, or
- Improvised "beanbag" lights, or
- A single Chemlight tied to a length of cord and swung in a circle to make its position visible from the air.

**The lit inverted "Y" marks exactly where the lead/first helicopter should land.**

## Detailed Version

The real, transferable lesson for anyone coordinating a real evacuation (not just a military one): establishing a clear, visible, and specific landing/pickup marker — understood in advance by whoever might respond — removes real ambiguity and delay exactly when every minute matters most. A chemical light swung in a circle is a low-cost, improvised version of this signal that a civilian household genuinely could replicate with basic supplies.
""",
    },
    {
        "title": "Prolonged Field Care — Sustaining a Casualty Without Evacuation",
        "section": "emergency",
        "tags": ["tccc", "prolonged-field-care", "austere-medicine"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Prolonged Field Care (PFC) is real medical doctrine for exactly the scenario a disaster-prep household plans for: caring for an injured person well beyond when they "should" have reached a hospital, because evacuation or outside help genuinely isn't coming soon.** The real NATO framing: field care sustained with limited resources, applied longer than normally planned, specifically to reduce death and complications while waiting for the next real level of care to become reachable.

## The 10 Real PFC Capabilities

These are the categories of ongoing care a real prolonged-care situation requires attention to — not every one applies to every injury, but all 10 are worth reviewing against the person's actual condition:

1. **Monitor** — track vital signs over time to spot a trend (improving or worsening), not just a single snapshot.
2. **Resuscitate beyond basic fluids** — real blood products if available; a reminder that plain IV fluid alone is a limited, partial substitute for actual blood loss.
3. **Support breathing** — supplemental oxygen or ventilation support if available and needed.
4. **Maintain definitive airway control** — if a surgical airway or advanced airway device was placed, it needs ongoing monitoring and care, not just the initial placement.
5. **Manage pain and sedation** — ongoing pain control, not just an initial dose at the point of injury.
6. **Reassess with exam/diagnostics** — physical exam findings can change meaningfully over hours; keep re-examining rather than treating the first assessment as final.
7. **Provide nursing/hygiene/comfort care** — real wound care, keeping the person clean and as comfortable as possible, matters increasingly the longer care continues.
8. **Advanced interventions if genuinely needed** — further surgical-level care (the source names chest tube placement, fasciotomy, amputation) as capability categories, not casual home procedures.
9. **Seek remote consultation if any channel exists** — even a basic phone/radio description of the situation to someone more experienced can meaningfully improve decisions.
10. **Prepare the person for eventual transport** — whenever movement does become possible, the person should already be packaged and as stable as achievable.

## ⚠️ Tourniquet Conversion Timing — a real, specific decision point

A tourniquet that's been left on needs to be reassessed and, if safely possible, converted (loosened/removed in favor of a proper wound dressing) once the immediate danger has passed — **but the timing genuinely matters:**

- **Under 2 hours:** generally considered safe to attempt conversion.
- **2-6 hours:** likely still safe, but the real upper safe limit hasn't been scientifically established — attempt conversion with real caution and readiness to reapply if bleeding resumes.
- **Over 6 hours:** converting a tourniquet in the field is not advised — the limb has likely adapted to the lack of blood flow in a way that makes sudden restoration genuinely risky; this situation needs real medical evaluation before conversion, not a field attempt.

**Converting a tourniquet means slowly loosening it while watching closely for bleeding to resume — if it does, retighten immediately and do not continue trying to convert it at that time.**

## Detailed Version

**The real mindset shift PFC represents: once it's clear that quick evacuation isn't happening, the goal changes from "stabilize until help arrives in minutes" to "sustain this person's condition, potentially for hours or days, with what's actually on hand."** That shift changes real priorities — ongoing hygiene and pain management become as important as the initial dramatic intervention, because a person who survives the first few minutes can still be lost to a preventable complication hours later if ongoing care is neglected.
""",
    },
    {
        "title": "TCCC Drug Reference Guide",
        "section": "reference",
        "tags": ["tccc", "medications", "drug-reference"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**This page is a factual reference of the real medications named in the TCCC-Medical Provider guidelines, preserved for completeness — it is not a how-to guide for self-administering these.** Several are controlled substances (fentanyl, ketamine, diazepam) that require real medical training, a prescription, and real legal authority to possess or administer outside a military medical context. Several others (acetaminophen, meloxicam) are genuinely accessible over-the-counter options. Treat the controlled-substance entries as reference knowledge of what real combat medicine uses and why, not as guidance for untrained use.

## Pain Management

- **Acetaminophen (Tylenol), 625mg:** mild-moderate pain in a conscious person who can swallow — 2 tablets every 8 hours.
- **Meloxicam, 15mg oral:** mild-moderate pain in a conscious person who can swallow.
- **Fentanyl citrate (oral transmucosal lozenge), 800mcg:** moderate-severe pain — taped to the casualty's finger and directed into the mouth to dissolve against the cheek; the person is told not to bite or swallow it. *(Controlled substance.)*
- **Ketamine injection:** moderate-severe pain in a conscious OR unconscious casualty — real dosing varies by route (roughly 50mg intranasal; 20mg IV/IM/IO). *(Controlled substance.)*

## Antibiotics (for traumatic/penetrating injury)

- **Ertapenem, 1g IV** — broad-spectrum, effective against both major bacteria classes.
- **Cefotetan, 2g IV** — broad-spectrum second-generation cephalosporin.
- **Moxifloxacin, 400mg oral** — used for eye injuries specifically, as well as general traumatic injury, in a conscious person who can swallow.

## Reversal Agents & Anti-Nausea

- **Naloxone (Narcan), 1mg/2ml** — reverses opioid effects (including fentanyl, morphine, and partially reverses ketamine).
- **Flumazenil (Romazicon), 0.4mg every 15 min** — reverses benzodiazepine (diazepam/Valium) effects.
- **Ondansetron (Zofran), 4mg oral rapid-dissolve** — prevents/treats nausea from opioid pain medication.

## Fluids & Bleeding Control

- **Hetastarch, 500ml IV bag** — for hemorrhage or burns.
- **Sodium chloride (normal saline), 10ml** — IV/IO line flush; larger bags (500ml-1L) as an alternative IV fluid; a 3% hypertonic version treats elevated pressure inside the skull specifically.
- **Tranexamic acid (TXA), 1g IV** — an antifibrinolytic (helps blood clot rather than keep bleeding) for significant hemorrhage, **given within 3 hours of the injury** — timing matters, it's not equally effective given later.

## Sedation/Seizure Control

- **Diazepam (Valium), 5mg/2ml injection** — used for active or anticipated seizures, sedating a combative casualty, or as part of advanced airway procedures. *(Controlled substance.)*

## Detailed Version

**The real pattern worth noting across this list: TCCC pairs almost every powerful medication with a specific reversal agent** (naloxone for opioids, flumazenil for benzodiazepines) — a real acknowledgment that these medications carry genuine risk alongside real benefit, and that having the undo button ready is treated as part of giving the medication safely in the first place, not an afterthought.
""",
    },
    {
        "title": "Building a Trauma Kit — Real IFAK Contents",
        "section": "reference",
        "tags": ["tccc", "ifak", "trauma-kit", "gear"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**The U.S. military's Individual First Aid Kit (IFAK) is the real, field-tested baseline for what a personal trauma kit should contain** — built around exactly the injuries MARCH is designed to treat. The list below is the real contents (with military stock numbers dropped, since they're meaningless to a civilian buyer) — a genuinely good reference for building or buying an equivalent civilian kit.

## Generation I IFAK Contents

- 1 Combat Application Tourniquet
- 1 elastic bandage
- 1 roll of 4.5-inch gauze bandage
- 1 roll of 2-inch surgical adhesive tape
- 1 nasopharyngeal airway (NPA)
- 4 pairs of patient exam gloves
- 1 combat gauze (hemostatic) dressing
- A resupply contents kit and a folding-panel insert for organizing the above

## Generation II IFAK — What's Added

The newer version keeps everything above and adds:

- **A second tourniquet** (carrying two, not one, is the real current standard)
- A vented chest seal (the Bolin Chest Seal, specifically)
- An eye shield (the Fox Eye Shield)
- A rescue strap cutter (for cutting through clothing/gear quickly)
- A permanent marker (for writing the tourniquet application time directly on the skin or tourniquet — see Tourniquet Application & Hemostatic Wound Packing)

## A Larger Kit: What the Vehicle-Level WALK Adds

For a kit meant to treat multiple people or support an evacuation (not just carried on one person), the real vehicle-level kit (WALK) scales up to include:

- Multiple pairs of trauma gloves
- Two NPAs with lubricant
- Two chest seals and two needle-decompression kits (14-gauge, 3.25-inch)
- Two tourniquets
- Six trauma dressings and several rolls of gauze
- One abdominal trauma dressing (for larger torso wounds)
- Two SAM splints (for fracture stabilization)
- Trauma shears (for cutting through clothing)
- Multiple eye shields
- A hypothermia prevention kit (see Hypothermia Prevention in Trauma)

## Detailed Version

**The real principle behind this list, worth keeping when adapting it for a household kit: every single item maps directly to one specific step in MARCH** — the tourniquet and hemostatic gauze for massive hemorrhage, the NPA for airway, the chest seal and decompression needle for respirations, the splint for PAWS's splinting step, the eye shield for penetrating eye trauma. **A trauma kit built this way is not a generic "first aid kit" with band-aids and aspirin — it's specifically built to let one person execute the MARCH sequence on another person without having to guess what they'll need next.**
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
                "source_url": TCCC_PDF_URL,
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
