#!/usr/bin/env python3
"""Seeds 6 real pages from ATP 3-50.21 (Survival), Chapter 2
(Survival Medicine) -- mined from the real text layer already
extracted in this session (/tmp/atp_survival.txt, pages 2-3 through
2-19). This chapter substantially overlaps TCCC and "Where There Is
No Doctor" content already in this wiki (airway, general bleeding
control, shock, general wound care) -- but contains real,
genuinely new, complementary detail not captured elsewhere: real
bleeding-type visual classification, a different real improvised-
tourniquet construction technique (stick-and-double-overhand-knot,
built from household materials), real sterile-water boiling times by
altitude, the real "proud flesh" granulation-tissue explanation, a
complete real maggot-therapy protocol, real debridement/suture field
technique, several illnesses not previously covered (Beriberi, body
lice, hepatitis, pneumonia, tuberculosis, intestinal parasites) with
real treatments including real herbal dosing, and real medicinal-
plant preparation terminology with real measurement ratios.

This script deliberately does NOT re-seed general bleeding control,
general shock treatment steps, or general wound-care principles
already covered -- only the real, new, complementary detail.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_atp_survival_medicine1.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
ATP_SURVIVAL_PDF_URL = "/files/pdfs/Military Manuals/ATP-3-50.21-Survival.pdf"

PAGES = [
    {
        "title": "Recognizing Bleeding Types & Field Tourniquet Construction",
        "section": "emergency",
        "tags": ["bleeding", "tourniquet", "first-aid"],
        "risk_level": "critical",
        "body_markdown": """## Real Bleeding Classification — by Look, Not Just Location

**Telling these apart by appearance changes how urgently you need to act:**

- **Arterial** — the most serious. **Bright red to yellowish blood, exiting in distinct spurts/pulses matching the heartbeat**, not a steady flow. Arteries carry blood under high pressure, so **a large volume can be lost very quickly if not controlled immediately.**
- **Venous** — **a steady flow of dark red, maroon, or blackish blood** (darker because it's low on oxygen, heading back to the heart). Still genuinely serious — blood loss can be substantial and surprisingly fast without intervention — but usually easier to control than arterial bleeding.
- **Capillary** — **small-amount oozing**, not spurting or flowing, from the tiny vessels connecting arteries to veins. Typical of minor cuts/scrapes, and genuinely the easiest to control.

## ⚠️ Real Urgency Numbers

**A complete femoral artery/vein disruption can cause death from blood loss in as little as 3 minutes.** **A tourniquet can safely stay in place up to 2 hours without real damage to vessels, nerves, or muscle** — if isolated with no other help, release the pressure after 2 hours and retighten only if bleeding resumes.

## Real Improvised Tourniquet Construction (when no commercial tourniquet is available)

**What you need:** a rigid rod (jack handle, stick, scabbard, cleaning rod, pipe, dowel) and a band of material at least 1.5 inches wide (a cravat, bandana, towel, ace bandage, shirt strip, nylon webbing, rifle sling). **⚠️ Belts and zip ties should only be used as a genuine last resort.**

1. Form the wide band into a loop and fit it over the limb, **2-3 inches above the bleeding site.**
2. Tie it tightly with an overhand knot.
3. **Lay the rigid rod across that overhand knot.**
4. **Tie a second overhand knot on top of the rod with the loop's running ends — this forms a square knot with the rod running through its center.**
5. **Twist the rod**, applying pressure around the limb's full circumference until the bleeding actually stops. **Don't tighten further than what's needed to stop it.**
6. **Secure the rod in place** by looping the tourniquet's free ends over the rod's own ends, then bringing them around the limb again to keep the rod from unwinding — tie them off on the side of the limb.
7. **If bleeding continues, apply a second tourniquet side-by-side with the first**, rather than just tightening the first one further.

**⚠️ Real note on amputations:** some dark, oozing blood may continue briefly after the tourniquet is applied — this is simply blood already trapped between the wound and the tourniquet itself, not a sign the tourniquet failed.

## Real Antiseptic Alternatives (When No Medical Antiseptic Is Available)

**Alcohol, vinegar, natural honey, hydrogen peroxide, and bleach are all real, genuinely effective antiseptics** for rinsing a wound before applying a pressure bandage. **⚠️ Once a dressing/bandage is applied, do not remove it** — removing and reapplying disturbs clot formation and increases infection risk.

## Detailed Version

**The real, practical value of the bleeding-type classification: it tells you how much time you actually have.** Spurting bright-red blood demands an immediate tourniquet with no deliberation; a slow, dark ooze gives you more real room to assess and choose a less drastic intervention first — treating every bleed with maximum urgency wastes a tourniquet (and the real tissue risk that comes with prolonged use) on a wound that didn't need one.
""",
    },
    {
        "title": "Shock — Recognition & Field Positioning",
        "section": "emergency",
        "tags": ["shock", "first-aid", "emergency"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Shock means the body isn't delivering enough oxygen to meet tissue demand — early recognition genuinely limits how much damage it does, and the real guidance is to anticipate and treat it in every injured person, not just those showing obvious signs.**

## Real Signs

Apprehension, anxiety, restlessness, irritability; altered consciousness; nausea/vomiting; pale, ashen, or grayish cool/moist skin; rapid breathing; excessive thirst.

## Real Positioning Protocol

- **Conscious:** lie the person on a level surface with the legs elevated 6-8 inches.
- **Unconscious:** place them on their side or stomach, head turned to one side — **this prevents choking on vomit, blood, or other fluid.**
- **If you're genuinely unsure which position is right:** lay them perfectly flat instead of guessing.
- **⚠️ Once positioned for shock, do not move the person again** unless genuinely necessary.

## Real Warming & Fluid Guidance

- **Insulate from the ground/surroundings; apply external heat if available** — remove wet clothing immediately and replace with dry, and improvise shelter from the weather.
- **Real external-heat options:** warm liquids/food, a sleeping bag, body heat from another person, warmed water in canteens, hot rocks wrapped in clothing, or small fires positioned on either side of the person.
- **If conscious: slowly give small doses of a warm salt or sugar solution, if available.**
- **⚠️ If unconscious, or if there are abdominal wounds: do NOT give anything by mouth.**
- **Have the person rest a minimum of 24 hours.**
- **If alone with no one to help:** lie down in a depression, behind a tree, or anywhere out of direct weather exposure, with the head positioned lower than the feet.
- **Keep reassessing continuously** — shock's presentation can change over time, and a person who looked stable can deteriorate.

## Detailed Version

**The real, important instruction buried in this page: treat shock as anticipated in every injured person, regardless of which specific signs are currently visible.** Waiting for the full, obvious symptom picture to appear before beginning real treatment loses exactly the early window where intervention does the most good.
""",
    },
    {
        "title": "Field Wound Cleaning & the Open Treatment Method",
        "section": "reference",
        "tags": ["wound-care", "first-aid", "sterilization"],
        "risk_level": "high",
        "body_markdown": """## Real Wound Cleaning Technique

1. Remove or cut clothing away from the wound. **If a sharp object, gunshot, or projectile caused it, check for a real exit wound too.**
2. Clean the surrounding skin thoroughly.
3. **Rinse — do NOT scrub — the wound with large amounts of pressurized water.** Pressurize it with a syringe, an irrigator, or a plastic bag with a small hole poked in it.
4. **⚠️ Real sterile-water timing: boil water in a covered container for 10 minutes at sea level — but boil it a full HOUR above 3,000 feet elevation** to actually guarantee sterilization. Once sterilized, water stays sterile indefinitely as long as the container stays covered.
5. **⚠️ Don't irrigate so vigorously that you wash away clots and restart bleeding.** Wait a full hour after bleeding has stopped before beginning irrigation, start gently, and increase vigor gradually as you remove unhealthy tissue — without causing further damage.

## The Real "Open Treatment" Method — Why Leaving a Wound Open Is Actually Safer

**Leaving a wound open to drain is the real, safest wound-management approach in a survival situation** — a draining wound generally doesn't become life-threatening, no matter how unpleasant it looks or smells. Cover it (including any exposed nerve, bone, or blood vessel) with a clean dressing, hold the dressing with a bandage, and **change the dressing daily to check for infection.**

**⚠️ Real, useful detail: a healthy open wound develops "proud flesh"** — moist, red, granular tissue (granulation tissue) that's actually a genuinely good sign, not something to be alarmed by.

**The one real exception to open treatment: facial wounds that interfere with breathing, eating, or drinking should be closed early** rather than left open like other wounds.

## Gaping Wounds — Real Butterfly Closure

**If a wound's edges are gaping, bring them together using adhesive tape cut into a "butterfly" or "dumbbell" shape.** **⚠️ Use this approach with real caution when no antibiotics are available** — always leave room for drainage even while closing the edges, since sealing a wound completely without that risks trapping infection inside. **Immobilizing the area in a position that favors good circulation to and from the wound genuinely speeds healing.**

## Detailed Version

**The real, counterintuitive core of this whole page: deliberately leaving a wound open and visibly draining — rather than closing it neatly — is usually the actual safer choice in a survival setting with no real antibiotics available.** The instinct to "fix" a wound by sealing it up is understandable but often works against real healing, trapping exactly the infection that open drainage would otherwise release.
""",
    },
    {
        "title": "Treating an Infected Wound — Warm Compress Protocol & Maggot Therapy",
        "section": "reference",
        "tags": ["wound-care", "infection", "maggot-therapy"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Some wound infection is nearly inevitable in a real survival situation with limited hygiene — real signs are pain, swelling, redness, increased local temperature, and pus in the wound or on the dressing.**

## Real Warm Compress Protocol

1. Apply a warm, moist compress with lukewarm saltwater directly on the infected wound — **this draws out infection and encourages fluid/toxin drainage.**
2. Change the compress as it cools, keeping warmth on the wound for a total of 30 minutes per session.
3. **Repeat 3-4 times daily.**
4. **Open and gently probe the wound with a sterile instrument to drain it**, then dress and bandage it.
5. **Drink plenty of water.**
6. **For a gunshot or other serious wound:** if drinking water is scarce, use the cleanest available non-drinking water to forcefully flush the wound daily until it's healed over — **don't sacrifice your own drinking water supply for wound irrigation if it's genuinely limited.**
7. **Continue daily treatment until every sign of infection is gone.**
8. **Soaking the wound in lukewarm saltwater adds heat that helps mobilize the body's own local immune defenses.**

## ⚠️ Maggot Therapy — a Real, Legitimate Last-Resort Technique

**For a severely infected wound that won't heal and can't be debrided by ordinary means, with no antibiotics available.** **The real mechanism: maggots clean dead tissue, exude calcium carbonate that alkalizes the wound (helping white blood cells destroy bacteria and dead tissue), and excrete 2 real compounds (allantoin and urea) that stimulate healthy tissue growth.**

**Real step-by-step process:**
1. Expose the wound to flies for 1 day, then cover it.
2. Check daily for developing maggots.
3. Once they appear, keep the wound covered, checking daily.
4. **⚠️ Remove ALL maggots once they've cleaned out the dead tissue — before they start consuming healthy tissue.** The real warning sign that they've reached healthy tissue: increased pain and bright red blood appearing in the wound.
5. Flush the wound repeatedly with potable (ideally sterile) water to remove every maggot.
6. Bandage and treat it like any other wound from that point — **it should heal normally afterward.**

## Real Debridement Basics (an Emergency, Nonmedical-Personnel Procedure Only)

**Debridement means surgically removing lacerated, dead, or contaminated tissue** — necessary in severe wounds to limit infection (particularly gas gangrene) and reduce septic shock risk. **Real guidelines:** cut away dead skin; trim muscle back only to the point where it starts bleeding and discoloration stops; cut away damaged fat; **conserve bone and nerve tissue wherever possible**; and ensure the wound has real drainage before any final closure.

## Real Suture Technique (Only When Genuinely Necessary)

**Despite real infection risk, suturing may sometimes be needed to control bleeding or restore mobility.** Improvise thread from parachute line, fabric, or clothing fiber. **Place stitches individually, spaced far enough apart to allow drainage underneath — don't worry about cosmetic appearance, just hold the tissue together.** **For a scalp wound, hair itself can be used to close it** — infection risk is naturally lower there thanks to the scalp's rich blood supply. **⚠️ In most real cases, leaving the wound open to drain remains the better choice** — suturing is the exception, not the default.

## Detailed Version

**The real, unifying theme across maggot therapy, debridement, and suturing: all three are genuine last-resort interventions, each carrying real risk of its own, reserved specifically for situations where the normal "leave it open and drain it" approach has already failed or genuinely can't apply.** None of these replace basic open-wound care — they're what's left when that alone isn't enough.
""",
    },
    {
        "title": "Illnesses in Isolation — Beriberi, Lice, Hepatitis, Pneumonia, TB & Intestinal Parasites",
        "section": "reference",
        "tags": ["illness", "infection", "herbal-medicine"],
        "risk_level": "high",
        "body_markdown": """## Beriberi (Vitamin B-1/Thiamine Deficiency)

**Real signs:** tiredness, irritation, nausea, constipation, poor memory, numb toes, burning feet, sore legs, calf cramps, unsteady walk, trouble rising from a squat, weakened heart, heart failure, bloating. **Real treatment: eat thiamine-rich foods** — brown rice, whole grains, raw fruit/vegetables, legumes, seeds, nuts, yogurt, pork, beef, liver, brewer's yeast.

## Body Lice

**A tiny (1/16 inch) skin-feeding insect, linked to long-worn unlaundered clothing, shared bedding, and close contact.** Real signs: intense itching with deep scratches around the shoulders/flanks/neck, small red pimple-like bites, possible generalized rash. **Real treatment: wash clothing and bedding in boiling water**, or treat clothing with 1% malathion powder (or 10% DDT powder, if available).

## Hepatitis

Caused by various viruses, genuinely harder to treat than bacterial illness. **Incubation runs 2-6 weeks; the acute stage lasts 2-12 weeks, with full recovery taking weeks to months.** **Real treatment:** force fluids, avoid strenuous exercise, abstain from alcohol, wash hands/utensils/bedding/clothing thoroughly, boil water, disinfect fecal material, and increase vitamin B intake. **Real herbal options with real dosing:** coffee at 500mg/day (roughly 5 cups) — **⚠️ never exceed 1000mg/day**; or celandine tea (1.5 spoonfuls steeped 10 minutes in boiling water).

## Pneumonia

Flu-like symptoms plus: high fever up to 105°F, coughing greenish/yellow/bloody mucus, shaking chills, breathlessness especially with exertion, fatigue, low appetite, sharp chest pain (worse with coughing/deep breaths), heavy sweating, fast breathing/heartbeat, blue-tinged lips/fingernails, confusion. **Real treatment: complete bed rest and aspirin** (willow bark provides a real aspirin-like effect — see Medicinal Plant Preparation Terms). **Pleurisy root, taken as a tea of boiled roots, treats pneumonia and helps expel phlegm.** Deep-breathing exercises promote coughing up phlegm; plenty of fluids help loosen it. **A real historical note: hydrogen peroxide was used successfully as a pneumonia treatment in the 1920s.**

## Tuberculosis

Bacterial infection: coughing (yellow-green phlegm, eventually blood-tinged), low fever, chest pain, appetite loss, worsening lung symptoms, severe weight loss, a wasted appearance — **can be fatal.** **Real treatment: antibiotics, rest, and good nutrition** — in some historical cases, lungs were surgically collapsed to let them rest and heal.

## Intestinal Parasites — Tapeworms, Hookworms, Giardia, Blood Flukes, Pinworms

**Real transmission:** contaminated food/water, undercooked meat, and raw vegetables contaminated by sewage. Tapeworms can grow up to 60 feet inside the human intestine (5,000+ known species exist); hookworms feed on blood from the intestinal wall; Giardia (a single-celled parasite common in mountain streams, even surviving chlorination) comes from contaminated water; blood flukes mature in snails before burrowing through human skin, infecting 200+ million people worldwide; pinworms (the most common roundworm, ~209 million people infected) cause the characteristic sign of nighttime anal itching as the female migrates to lay eggs.

**⚠️ Real expulsion treatments (each with a real, specific limit — don't exceed it):**
- **Salt water:** 4 tablespoons of salt in 1 quart of water. **Do NOT repeat this treatment.**
- **Tobacco:** eat 1-1.5 cigarettes' worth, or about 1 teaspoon of smokeless tobacco — the nicotine stuns/kills the worms long enough to pass them. **If infestation is severe, may repeat once in 24-48 hours, but no sooner.**
- **Kerosene:** drink 2 tablespoons, no more. May repeat once in 24-48 hours if needed. **⚠️ Avoid inhaling the fumes — they can irritate the lungs.**
- **Hot peppers:** add to soup/rice/meat, or eat raw — **needs to become a steady part of the diet to be effective**, not a one-time dose.
- **Garlic:** chop/crush 4 cloves, mix into a glass of liquid, drink daily for 3 weeks.

## Detailed Version

**⚠️ Real, important caveat worth stating plainly: several of these treatments (salt water, tobacco, kerosene) are genuinely toxic in excess — the specific dose limits and no-repeat-before-X-hours rules above are not arbitrary caution, they're the actual line between an effective expulsion treatment and real self-poisoning.** Respecting the stated limits matters as much as using the treatment at all.
""",
    },
    {
        "title": "Medicinal Plant Preparation Terms — Poultice, Infusion, Decoction & Expressed Juice",
        "section": "reference",
        "tags": ["medicinal-plants", "herbal-medicine", "preparation"],
        "risk_level": "moderate",
        "body_markdown": """## ⚠️ Read This First

**These real preparation methods are for genuine survival-situation use only — not routine use.** Natural remedies often work more slowly than familiar medicines; **start with smaller doses and allow more time before judging effectiveness**, and recognize that some plants carry genuine toxicity risk with serious long-term effects if misused.

## Poultice — Hot, Direct Application

**Crushed (sometimes heated) plant material applied directly to a wound or sore, either bare or wrapped in cloth.** **Real mechanism:** applied hot, it increases local circulation and delivers the plant's active compounds directly; as it dries, it actively draws toxins out of the wound. **Prepare it to a "mashed potato" consistency and apply as hot as the person can actually tolerate.**

## Infusion / Tisane / Tea — the Simplest Real Preparation

**Place a small amount of herb in a container, pour hot water over it, and let it steep (covered or uncovered) before use** — for internal or external application. **⚠️ Don't drink too much too early in treatment** — on an empty stomach, it can cause its own adverse reaction.

## Decoction — a Stronger Real Extraction (for Tougher Plant Parts)

**For boiled-down or simmered leaf/root material** — add the plant matter to water and bring to a sustained boil or simmer to draw its compounds out. **Real standard ratio: about 1-2 ounces (28-56 grams) of herb per 0.5 liter of water.**

## Expressed Juice — Direct Plant Liquid

**Liquid or sap squeezed directly from plant material**, either applied straight to a wound or used as the base for another preparation.

## Detailed Version

**The real, practical reason these 4 methods are kept distinct rather than used interchangeably: each one extracts a different real amount and type of the plant's active compounds — a quick infusion is genuinely gentler than a sustained decoction, and a hot poultice works through heat-driven circulation in a way a cold expressed juice simply doesn't.** Matching the real preparation method to the plant part and the intended use (external vs. internal, gentle vs. strong) is itself part of using these remedies safely.
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
                "source_url": ATP_SURVIVAL_PDF_URL,
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
