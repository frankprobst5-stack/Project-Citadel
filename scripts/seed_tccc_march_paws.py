#!/usr/bin/env python3
"""Seeds 7 real pages from the Tactical Combat Casualty Care (TCCC)
Handbook, Version 5 (May 2017) -- mined from the real text layer
already extracted in this session (/tmp/tccc.txt), Chapter 1 (pages
1-43). TCCC is the real, battlefield-proven prehospital trauma care
doctrine used by the U.S. military and NATO, developed specifically
because civilian trauma courses don't reflect combat/austere
conditions -- directly applicable to any severe-trauma, no-EMS-access
emergency, not just combat.

Covers: the MARCH/PAWS treatment-priority framework, tourniquet
application and hemostatic wound packing (massive hemorrhage), NPA
insertion (airway), penetrating chest wounds -- chest seals and
needle decompression (respirations), hypothermia prevention, basic
peripheral IV access, and surgical cricothyroidotomy as an explicit
last resort when every other airway measure has failed.

Device-specific proprietary equipment (FAST1, FASTResponder, sternal
EZ-IO) is deliberately NOT included here -- it requires specific
commercial hardware most readers won't own, unlike the broadly
generalizable techniques covered.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_tccc_march_paws.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "MARCH & PAWS — The TCCC Treatment Priority Framework",
        "section": "emergency",
        "tags": ["tccc", "trauma", "march", "triage"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**MARCH and PAWS are memory aids for treating trauma in the order that actually saves lives** — developed from real combat casualty data, where treating injuries out of order is one of the most common preventable causes of death. Treat each letter completely before moving to the next, unless a later problem is more immediately life-threatening in front of you.

## M — Massive Hemorrhage (the #1 preventable cause of death)

**Over 90% of a large post-2001 combat-death dataset died from hemorrhage-related injuries** — this is why it comes first, ahead of even airway. **Apply a tourniquet immediately for any life-threatening limb bleeding** — hastily, over clothing, high and tight, without waiting to find the "perfect" spot. Once safe to do so, convert to a deliberate tourniquet directly on skin, 2-3 inches above the wound. For bleeding a tourniquet can't reach (torso, neck, groin), pack the wound with a hemostatic dressing (Combat Gauze) — see Tourniquet Application & Hemostatic Wound Packing.

## A — Airway

**A conscious, speaking person has a working airway** — don't intervene unnecessarily. An unconscious person who IS breathing often benefits from a nasopharyngeal airway (NPA) to keep the airway open. An unconscious person who is NOT breathing may need a surgical airway (cricothyroidotomy) as a genuine last resort — see the Surgical Cricothyroidotomy page. **In the field, standard endotracheal intubation is extremely difficult, often effectively impossible — don't plan around it.**

## R — Respirations

**Watch for tension pneumothorax** — air trapped in the chest cavity that progressively collapses lung function and compresses the heart toward cardiac arrest. Any open/sucking chest wound gets a vented chest seal immediately; a suspected tension pneumothorax gets needle decompression. See Penetrating Chest Wounds — Chest Seals & Needle Decompression.

## C — Circulation

**Controlling bleeding always takes priority over giving fluids.** Only someone in shock, or who needs IV medication, actually needs an IV line. **Signs of shock in the field: altered mental status (not explained by a head injury or drugs), and/or an abnormal/weak radial pulse** — these are checked by touch and observation, not equipment. Tranexamic acid (TXA), given as early as feasible, helps casualties in or at risk of hemorrhagic shock.

## H — Head Injury / Hypothermia

**Low blood pressure and low blood oxygen both make a head injury worse — avoid both if at all possible.** Hypothermia (body temp below 95°F/35°C) is itself a real, preventable cause of additional harm, and can develop from blood loss alone regardless of how warm the air is. **Hypothermia + acidosis + abnormal blood clotting together form the "lethal triad" in trauma** — each one makes the other two worse. See Hypothermia Prevention in Trauma.

## PAWS — the follow-up checklist people skip under stress

Real field data showed these 4 things are the ones most often forgotten once the immediate crisis feels handled:

- **Pain** — managing it isn't just comfort; it reduces movement, improves cooperation, and genuinely reduces later PTSD risk. Treat pain starting from the point of injury, not just once things are "stable."
- **Antibiotics** — **every penetrating battlefield-type wound is considered contaminated** and should get antibiotics; don't wait for visible signs of infection.
- **Wounds** — re-examine the whole person for wounds you missed in the initial rush (a small scalp laceration can bleed surprisingly heavily), and recheck that your own dressings/tourniquets are still working before moving the person.
- **Splinting** — stabilizing fractures genuinely reduces both pain and ongoing bleeding; don't treat it as optional once the "big" problems are addressed.

## Detailed Version

**The real discipline behind MARCH/PAWS is sequencing, not just knowledge.** Someone under real stress will often fixate on the most visually dramatic injury rather than the most lethal one — a severed finger draws attention faster than a slow-bleeding thigh wound, even though the thigh wound kills first. Working the letters in order, every time, is what actually prevents that mistake.
""",
    },
    {
        "title": "Tourniquet Application & Hemostatic Wound Packing",
        "section": "emergency",
        "tags": ["tccc", "tourniquet", "bleeding", "hemorrhage"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Massive limb bleeding kills faster than almost anything else — a tourniquet applied immediately, even imperfectly, beats a perfect tourniquet applied late.** Apply it hastily first; refine it once the immediate danger has passed.

## Applying a Tourniquet (e.g. Combat Application Tourniquet / CAT)

1. **Place it as high on the limb as possible, over the clothing** — this is the hasty application. (It gets converted to a deliberate placement — directly on skin, 2-3 inches above the wound — once you're safe enough to do so properly.)
2. Route the self-adhering band through the friction-adapter buckle and pull it tight, removing all slack.
3. Wrap the band securely around the limb and fasten it back on itself. **No more than 3 fingers should fit between the band and the limb.**
4. **Twist the windlass rod until the bleeding fully stops AND the pulse below the tourniquet is gone** — stopping visible bleeding isn't enough on its own; the distal pulse must be eliminated too.
5. Lock the windlass rod in place with its clip.
6. Pull the windlass strap tight and secure it to the clip.
7. **If a pulse is still present below the tourniquet once tactically safe to check, apply a second tourniquet side-by-side, just above the first, and tighten it too.**

**⚠️ Always write the application time directly on the tourniquet** — this is critical information for whoever provides follow-up care; a tourniquet left on too long without anyone knowing how long is a real additional risk.

## Hemostatic Dressing (Combat Gauze) — for bleeding a tourniquet can't reach

For wounds where a tourniquet isn't usable (torso, neck, groin/junctional areas) or as an adjunct before removing a tourniquet:

1. Hold the end of the gauze against your dominant index finger. Pack it directly into the wound, at the source of the bleeding (the pulsating point if visible), continuing until the wound cavity is completely filled.
2. Pack any excess gauze directly over the wound and apply firm direct pressure for a full 3 minutes without checking early.
3. **If bleeding continues after 3 minutes of real pressure, remove the gauze and repeat from step 1** — try to actually see where blood is flowing or spurting from and pack the fresh gauze directly onto that source.
4. Once bleeding is controlled, secure the packed dressing with an outer bandage (an elastic wrap or an emergency/pressure dressing).

**More than one package of gauze is often needed to fully pack a serious wound — don't assume one package is enough.**

## Detailed Version

The real counterintuitive point in both techniques: **speed over polish for the first application, polish once safe.** A hasty, imperfect tourniquet slapped on in seconds while under direct threat saves more lives in aggregate than waiting for ideal conditions to apply a perfect one — which is exactly why TCCC doctrine explicitly separates "hasty" from "deliberate" tourniquet placement into two distinct steps rather than treating it as one action.
""",
    },
    {
        "title": "Nasopharyngeal Airway (NPA) Insertion",
        "section": "emergency",
        "tags": ["tccc", "airway", "unconscious"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**For an unconscious person who IS breathing, an NPA (a soft flexible tube inserted through the nose into the back of the throat) can keep the airway open** when the tongue or relaxed throat tissue would otherwise obstruct it.

**⚠️ Do NOT use an NPA if clear fluid is coming from the ears or nose** — this can indicate a skull fracture, and inserting a tube in that situation risks real additional harm.

## The Technique

1. Place the person on their back with the head in a neutral position (not tilted).
2. **Lubricate the tube with a water-based lubricant only** — petroleum-based lubricant can damage the delicate nasal/throat tissue lining and increase infection risk.
3. Gently push the tip of the nose upward. Position the tube so its angled tip (bevel) faces toward the nasal septum (the middle divider).
4. **Insert at roughly a 90-degree angle to the face — never angled upward toward the top of the head.** Advance using a gentle rotating and/or back-and-forth motion until the flange rests against the nostril.
5. **Most attempts should go in the right nostril first.** If you meet resistance, don't force it — withdraw and try the left nostril instead (note the bevel orientation is reversed for the left side).

**⚠️ Never force the tube.** Real resistance means try the other side, not more pressure.

## Before Inserting Any Airway Device

- Check the upper airway for a visible obstruction first.
- Try a chin-lift or jaw-thrust maneuver — this alone sometimes resolves the obstruction without any device.
- Once the NPA is in and the person is unconscious but breathing on their own, **place them in the recovery position** (on their side) so their airway stays protected and any vomit or fluid can drain rather than being inhaled.

## When an NPA Isn't Enough

If the person remains unconscious with an airway obstruction despite a chin-lift/jaw-thrust and an NPA, and you're able to reach a medic, do so immediately. If no medic is reachable and the person genuinely cannot breathe, a surgical airway becomes the real last resort — see Surgical Cricothyroidotomy — Last-Resort Airway.

## Detailed Version

The real diagnostic logic worth remembering: a conscious, talking person already has a functioning airway by definition — the entire airway-intervention decision tree only applies once someone is unconscious, and even then, the least invasive option (chin-lift, then NPA) comes first, with surgical intervention reserved for when those genuinely fail.
""",
    },
    {
        "title": "Penetrating Chest Wounds — Chest Seals & Needle Decompression",
        "section": "emergency",
        "tags": ["tccc", "chest-wound", "pneumothorax", "breathing"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Any wound that penetrates the chest wall risks letting air leak into the chest cavity, progressively collapsing the lung and compressing the heart — a tension pneumothorax.** Two real interventions address this: sealing the wound itself, and relieving pressure that's already built up.

## Sealing a Penetrating Chest Wound (Chest Seal)

1. Expose the torso fully (navel to Adam's apple, all the way around) to find every wound — **don't assume there's only one.**
2. Wipe blood/sweat from the skin around each wound so an adhesive seal will actually stick. **Don't remove clothing that's stuck to the wound itself.**
3. **Check the back too** — logroll the person to look for an exit wound you might otherwise miss entirely.
4. Seal each wound: apply a vented chest seal if available (ideally timed to the person's exhale), making sure it extends at least 2 inches past the wound's edges on all sides, taped down completely around the perimeter. **In a genuine emergency, any airtight material works** (plastic wrap) as long as it's large and sturdy enough not to get sucked into the wound itself.
5. **Treat every penetrating chest wound as if it's a true sucking chest wound**, even if it doesn't look dramatic.
6. Position the person sitting up, or lying on the injured side, and monitor closely for worsening breathing difficulty.

## Needle Chest Decompression (for a suspected tension pneumothorax)

**Needed equipment:** a large-bore needle/catheter, 10-14 gauge, at least 3.25 inches long.

1. **Locate the insertion site: the 2nd intercostal space (between the 2nd and 3rd ribs), at the midclavicular line (roughly in line with the nipple), on the affected side.** (An alternate site: the 4th/5th rib space at the anterior armpit line.)
2. Insert the needle at a 90-degree angle to the chest wall, over the top of the 3rd rib (**not** into the space below it — staying on the rib's upper margin avoids the blood vessels and nerves that run along its lower edge). **Push firmly until you feel a distinct "pop" as it enters the chest cavity, often with an audible hiss of escaping air.**
3. **⚠️ Never insert medial to the nipple line** — that increases the risk of hitting the heart itself.
4. If using a catheter-over-needle, advance the catheter fully, then withdraw the needle while holding the catheter still.
5. Secure the catheter to the chest with tape — **but never tape over the open end; air must be able to flow freely through it.**
6. **Keep monitoring.** If symptoms return, the catheter may have clogged — insert a second one beside the first (same technique, placed laterally or above it) rather than assuming the procedure failed outright.

## Detailed Version

The reasoning that ties both interventions together: a chest seal addresses air getting IN through an open wound; needle decompression addresses air that's already trapped and can't get OUT. A person can genuinely need both at once — sealing the visible wound doesn't relieve pressure that's already built up inside, which is why the TCCC framework treats them as two separate, sequential steps rather than one combined action.
""",
    },
    {
        "title": "Surgical Cricothyroidotomy — Last-Resort Airway",
        "section": "emergency",
        "tags": ["tccc", "airway", "surgical", "last-resort"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This is a genuine last resort — a surgical airway, performed only when a person cannot breathe, is unconscious, and every less invasive measure (chin-lift/jaw-thrust, then a nasopharyngeal airway) has already failed, with no medic reachable.** TCCC doctrine itself places this at the bottom of the airway decision tree for exactly that reason. This page preserves the real technique for genuine last-resort reference; it is not a casual procedure, and it carries real risk of harm if done incorrectly. If any less invasive option (see Nasopharyngeal Airway (NPA) Insertion) is still viable, use that instead.

## What You Need

A cutting instrument (scalpel No. 10 or 15), forceps or a tracheal hook, an antiseptic (povidone-iodine or alcohol), an endotracheal tube (cut short so it doesn't protrude far from the neck), gloves, gauze, tape, and local anesthetic if the person is conscious.

## The Real Technique

1. **Position:** lay the person on their back with the neck gently extended (a rolled blanket/jacket under the shoulders helps). **⚠️ Do NOT hyperextend the neck if a spinal injury is even possible.**
2. Put on gloves.
3. **Locate the cricothyroid membrane:** place a finger on the Adam's apple (thyroid cartilage), slide down to feel the "V" notch, then continue sliding down into the shallow depression between the thyroid cartilage and the cricoid cartilage below it — that depression is the membrane.
4. Clean the skin over the membrane with antiseptic; inject local anesthetic first if the person is conscious.
5. Make a **1.5-inch vertical incision through the skin only**, directly over the membrane. **Do not cut the membrane itself with this cut, and do not make it horizontal.**
6. Re-locate the membrane by feel and sight through the incision. **Stabilize the larynx with one hand**, then make a **separate ½-inch horizontal (transverse) incision through the membrane itself.** A rush of escaping air is a normal sign you've entered the airway.
7. Dilate the opening (a hemostat or scalpel handle works) and hook it open with a cricothyroid hook or a bent 18-gauge needle.
8. Keep the cricoid cartilage stabilized with your other hand throughout.
9. Insert the tube through the opening, aimed toward the lungs. **Advance only 2-3 inches** — going further risks the tube sliding into only one lung. Inflate the cuff.
10. Secure the tube around the neck (tape, tubing, or a kit's built-in strap) so it can't be accidentally pulled out.
11. **Confirm correct placement:** listen/feel for air moving through the tube and look for fogging inside it; **both sides of the chest should rise and fall evenly.** If only one side rises, the tube has likely gone too deep into one lung — withdraw it 1-2 inches and recheck (don't pull it out completely). If air is coming from the person's mouth instead, the tube is misdirected — remove, reinsert, and recheck.
12. Once placement is confirmed, begin rescue breathing if needed: a bag-valve mask (or mouth-to-tube if unavailable) at 20 breaths per minute.
13. If the person is breathing on their own, just make sure the tube stays unobstructed and keep reassessing whether assisted breathing becomes necessary.
14. Dress the site: fold gauze around the tube's base to prevent irritation, and tape it securely in place.

## Detailed Version

**The entire structure of this procedure exists to avoid two specific, serious mistakes: cutting too deep too early (risking the airway or nearby vessels before you've even confirmed your landmarks), and advancing the tube too far (risking one-lung ventilation instead of two).** Both of the real safety checks built into the steps above — relocating the membrane by feel before the second incision, and confirming bilateral chest rise before trusting the tube — exist specifically to catch those two failure modes before they become fatal rather than merely serious.
""",
    },
    {
        "title": "Hypothermia Prevention in Trauma",
        "section": "emergency",
        "tags": ["tccc", "hypothermia", "shock", "trauma"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**A seriously injured person can become hypothermic from blood loss alone, regardless of how warm the air actually is** — this is a real, often-overlooked cause of additional harm on top of the original injury, and it's genuinely preventable with simple steps.

**Hypothermia, combined with acidosis (blood becoming too acidic) and coagulopathy (impaired blood clotting), forms the "lethal triad" in trauma** — each of the three makes the other two worse, which is why stopping hypothermia early matters more than it might seem for an otherwise "just cold" person.

## Real Prevention Steps

1. **Stop bleeding first and address shock appropriately** — hypothermia prevention supports the other interventions, it doesn't replace them. Use warmed fluids if any are available.
2. **Remove wet clothing and replace with dry clothing whenever possible** — wet fabric accelerates heat loss dramatically compared to dry.
3. **Insulate and reflect heat back to the body:**
   - Get the person onto an insulated surface, off the bare ground, as soon as possible.
   - A heat-reflective survival blanket/shell wrapped around the person helps retain body heat.
   - A chemical heat pad placed on the torso can actively add warmth — **but never directly against bare skin, which can cause a real burn.**
   - **No proper kit available? Use anything that retains heat and keeps the person dry:** dry blankets, a poncho liner, a sleeping bag — even a dry tarp in a pinch.
4. **During any transport,** keep the person wrapped, and actively shield them from wind exposure (an open vehicle door, a drafty space) — moving air strips heat away far faster than still air at the same temperature.
5. **If giving any IV fluids or liquid medication, warm them first if at all possible** — administering cold fluids directly contributes to worsening hypothermia, undoing some of the benefit of the other steps.

## Detailed Version

The real, easy-to-miss point here: hypothermia prevention isn't a cold-weather-only concern in trauma care — a person bleeding heavily on a warm day can still become dangerously hypothermic purely from blood loss itself, which is why TCCC treats it as a universal step (part of every MARCH sequence) rather than one that only applies when the ambient temperature is actually low.
""",
    },
    {
        "title": "Basic Peripheral IV Access",
        "section": "emergency",
        "tags": ["tccc", "iv", "vascular-access"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**IV access is only needed for someone in shock, or someone who needs IV medication — controlling bleeding always comes first, and most injured people don't actually need an IV line at all.** If the person is conscious, not in shock, and can swallow, oral fluids are a perfectly reasonable alternative.

## What You Need

IV tubing and fluids, an 18-gauge (or larger) IV catheter/needle, a saline lock, a constricting band, antiseptic wipes, gloves, tape, and gauze.

## The Technique

1. Put on gloves.
2. **Choose the access site carefully:** avoid joints, avoid any injured limb, and avoid a limb with significant wounds above (proximal to) where you intend to insert the needle.
3. Apply the constricting band roughly 2 inches above the intended puncture site. Clean the site with antiseptic.
4. **Puncture the vein:** stabilize the skin below the puncture site by pulling it taut with your non-dominant thumb (keep the thumb off the vein itself, so you don't collapse it). Position the needle bevel-up, roughly parallel to the vein, about ½ inch below the entry point. Insert through the skin at a 20-30 degree angle and advance about ½ inch into the vein. **Confirm you're in the vein by seeing blood appear in the flash chamber** — you may also feel a faint "give" as the needle enters.
5. **Advance the catheter:** holding the hub steady, slide the catheter forward off the needle into the vein up to the hub (this also prevents blood backing up out of the hub). Press lightly on the skin over the catheter tip with your other hand while you withdraw the needle itself — **dispose of the needle safely immediately to avoid an accidental needle-stick.**
6. Attach a saline lock (preferably needle-free) and connect the IV tubing. Begin the infusion and watch the site closely for swelling, which would indicate the fluid is leaking into the surrounding tissue rather than the vein.
7. Secure the catheter and tubing to the skin, and dress the site.

## Detailed Version

**The real judgment call that matters more than the needle technique itself: deciding whether an IV is actually needed in the first place.** TCCC doctrine is explicit that bleeding control, not fluid replacement, is what actually saves a bleeding casualty — an IV line is a tool for a specific subset of situations (confirmed shock, or a real need for IV medication), not a default step to perform on every injured person.
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
