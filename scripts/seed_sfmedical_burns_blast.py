#!/usr/bin/env python3
"""Seeds 5 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 10 (Burns and Blast Injuries) --
mined from the OCR output cached at /tmp/sfmedical.txt.

Covers real content genuinely extending the existing burns coverage
(TCCC's Rule of Nines page covers sizing/fluid resuscitation but not
degree classification or situational first aid): real situational
burn first aid (clothes on fire, scalds, burning room rescue,
electrical burns), real 1st/2nd/3rd degree classification with real
course/treatment per degree, real burn-depth testing technique, real
severity classification (critical/moderate/minor) by percentage and
location, and real cleansing/blister/bandaging guidance. Also covers
blast injuries entirely -- genuinely new content not in this wiki at
all: real blast-type physics (air/water/solid), real primary/
secondary/tertiary classification, and real blast lung/blast abdomen
recognition and treatment.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_burns_blast.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Burn Situational First Aid & Degree Classification",
        "section": "emergency",
        "tags": ["burns", "first-aid", "emergency"],
        "risk_level": "critical",
        "body_markdown": """## Real Situational First Aid, by Cause

- **Clothes on fire:** since flames rise, **get the person flat on the floor (forcibly if needed), flames facing upward**, then smother with a coat, rug, or blanket.
- **Scalds:** immediately strip off the affected clothing to cut short how long the hot fluid stays against the skin.
- **Rescuing someone in a burning room:** the rescuer should hyperventilate first, tie a wet cloth over their own face, and enter staying low, holding their breath — **give the rescued person oxygen immediately once out**, if available.
- **Electrical burns:** push the person off the conductor with a non-conductive object, or pull them off by their belt — **⚠️ never touch their body directly while they're still in contact with the conductor**, unless you're wearing insulated gloves. **Check for a pulse immediately; if absent, start CPR and continue until the heart resumes, the person breathes on their own, they're pronounced dead, or up to a real maximum of 3 hours.**

## Real Burn Degree Classification

### First Degree
**Real examples:** sunburn, a low-intensity flash. Only the outer skin layer (epidermis) is affected. **Signs:** reddened, blanches with pressure, little/no swelling. **Symptoms:** tingling, painful, extremely touch-sensitive. **Course: peels and fully recovers within about 7 days.** **Treatment:** a soothing cream (the source names Noxzema) or mild pain relief.

### Second Degree
**Real examples:** scalds, flash flame. Most but not all of the skin's thickness is burned; damaged capillaries leak plasma into the tissue. **Signs:** blisters (intact or broken), a weeping surface, mild swelling. **Symptoms: genuinely very painful**, with pin-prick sensation normal or only slightly reduced. **Course: heals with minimal-to-no scarring in 2-3 weeks — but infection can convert it into a third-degree burn.**

### Third Degree
**Real example:** fire burns. **Full skin thickness destroyed**, with the most severe swelling of all 3 degrees. **⚠️ Signs: skin looks dry, pale white, or charred.** **⚠️ Symptoms: genuinely PAINLESS to pin prick** — the nerve endings themselves are destroyed, which is a real, counterintuitive severity marker (less immediate pain does not mean less severe). **Real shock symptoms can appear if swelling is extensive.** **Course: a scab forms and sloughs off in about 3 weeks; skin grafting becomes necessary since scar tissue, not real skin, closes the wound.**

## Detailed Version

**The real, most counterintuitive fact worth remembering from this whole page: third-degree burns can hurt LESS than second-degree ones, not more — because the nerve endings that would transmit pain are themselves destroyed.** Judging burn severity purely by how much pain the person reports is a real, dangerous mistake; the degree classification above (based on appearance and sensation testing, not reported pain alone) is the real way to judge it correctly.
""",
    },
    {
        "title": "Burn Depth Testing & Severity Classification",
        "section": "reference",
        "tags": ["burns", "triage", "assessment"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Correctly treating a burn requires actually knowing how deep it goes and what percentage of the body it covers — both are testable with real, simple field techniques, not guesswork.**

## Real Burn-Depth Testing

- **Pin-prick test:** areas where the full skin thickness is lost show NO sensation to a pin prick, and no response to light touch either.
- **Hair-pluck test:** if hair can be pulled out with little resistance and no pain, **the burn is a genuinely deep one.**

## Real Rule of Nines (Body Surface Area)

**No one can treat a burn intelligently without first correctly estimating what percentage of total body surface is actually burned.**

| Body region | % of body surface |
|---|---|
| Each arm | 9% |
| Head and neck | 9% |
| Front of trunk | 18% |
| Back of trunk | 18% |
| Each thigh | 9% |
| Each lower leg | 9% |
| Perineum | 1% |

**⚠️ Real, common error: overestimating the percentage.** Be deliberately conservative in the estimate.

## Real Severity Classification

- **Critical burns:** second-degree over 30% of the body; third-degree over 10%; third-degree on the hands, feet, or face; **or any burn complicated by a respiratory injury, fracture, or major soft-tissue injury.**
- **Moderate burns:** second-degree covering 15-30%; third-degree covering 4-10% (not on hands/feet/face).
- **Minor burns:** second-degree under 15%; third-degree under 4% (not on hands/feet/face).

## Detailed Version

**The real reason hands, feet, and face get their own special critical-burn category regardless of percentage: these are real, specific areas where even a small third-degree burn causes outsized real functional impairment** (hand function, mobility, airway/vision involvement near the face) — percentage alone understates how serious a burn in one of these specific locations actually is.
""",
    },
    {
        "title": "Burn Treatment — Cleansing, Blisters & Bandaging Method",
        "section": "reference",
        "tags": ["burns", "wound-care", "infection-prevention"],
        "risk_level": "high",
        "body_markdown": """## Real Cleansing

**Gently wash a fresh burn with an antiseptic cleanser (the source names pHisoHex) and sterile saline, removing all trash, dirt, and clothing fragments.** Once the real infection risk window has passed, ordinary soap and tap water become sufficient.

## Real Blister Management

**Leave an intact blister alone until it breaks on its own, then trim away the loose skin with scissors.** **⚠️ An intact blister that shows signs of infection (pus inside, or surrounding red streaking/lymphangitis) should be opened and cleaned immediately, under sterile conditions** — don't wait for it to break naturally in that specific case.

## Real Tetanus & Ointment Guidance

**Every second-degree-or-worse burn should get a tetanus booster.** **Real, honest finding: no real evidence shows antibiotic ointment outperforms plain petroleum jelly, or even no ointment at all** — but real-world experience with routinely applying specific antibiotic creams (Furacin, Silvadene) to second/third-degree burns has shown reduced infection rates, and may keep a borderline second-degree burn from progressing to third-degree. **A rare person may react to these specific creams, but the real benefit is judged to outweigh that risk.**

## ⚠️ Real "Open vs. Closed" Bandaging Rule, by Location

**A genuinely simple, reliable real rule:**
- **Head, neck, and perineum burns: leave OPEN** (no bandage).
- **Hands, joints, and any burn wrapping all the way around a limb or the trunk: BANDAGE.**
- **A burn on just one side/aspect of the trunk or a limb: either method works** — use your own judgment, and **bandage if genuinely unsure.**

**⚠️ Real caution: extensive bandaging on a patient kept in a warm environment can cause dangerous overheating (hyperpyrexia)** — don't over-bandage reflexively.

**When bandaging: place a non-adherent material directly against the burn first** — this stops healing granulation tissue from growing into the gauze itself and tearing away at the next dressing change.

## Detailed Version

**The real, underlying logic behind the location-based open/closed rule: areas with complex, hard-to-immobilize anatomy (joints, hands) or where a full-circumference wrap would restrict swelling (limbs, trunk) need the structural support of a bandage, while flatter, more exposed areas (head, neck, perineum) heal better exposed to air.** The rule isn't arbitrary — it follows from each location's real anatomical and swelling behavior.
""",
    },
    {
        "title": "Blast Injuries — Classification & Recognition",
        "section": "emergency",
        "tags": ["blast-injury", "explosion", "trauma"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**A blast injury can exist with zero visible external marks — which makes it genuinely dangerous to miss, since the person may seem fine and attempt something that turns out to be fatal.**

## Real Blast Physics, by Medium

- **Air:** blast waves travel slowest here and generally do less direct body damage — **most "air blast" injuries are actually from flying debris, not the pressure wave itself.**
- **Water:** blast waves travel much faster and farther in water. **The human body's density closely matches seawater, so the wave can pass through solid tissue without damaging it directly** — real damage concentrates instead in hollow organs, lungs, the abdomen, and other gas-filled cavities.
- **Solid:** blast waves travel fastest through dense solid material (a ship's deck, for instance) — **this can rupture major blood vessels with no break in the skin at all.**

**⚠️ Real pressure thresholds:** a sudden 7 psi increase can rupture an eardrum; **over 30 psi is needed to injure the body's hollow organs/cavities.**

## Real 3-Tier Classification

1. **Primary:** direct effect of the blast wave itself — ruptured eardrums, hollow-organ damage.
2. **Secondary:** injury from flying debris (shrapnel, brick, plaster) — including someone trapped and hurt inside a collapsing structure.
3. **Tertiary:** injury from the blast physically throwing the body into another object.

**⚠️ Real, important note: these categories frequently overlap in the same person** — don't assume only one applies.

## ⚠️ Why Blast Injury Is Easy to Miss

**With no visible external injury, a real blast-injured person is often mistakenly treated as "walking wounded."** **The real tell: if there are no visible signs of injury but the person is developing shock, suspect blast injury specifically.** Correct diagnosis often only comes once shock, difficulty breathing, apprehension, and trembling become obvious — **by which point real internal damage has already progressed.**

## Detailed Version

**The real, most dangerous failure mode this page describes: a person near any real explosion (even one that caused no visible wounds) genuinely needs evaluation for blast injury, not just a glance-and-clear.** The entire reason "walking wounded" misclassification happens is that the body shows nothing externally while real internal injury (ruptured eardrum, lung, or bowel damage) is already present and worsening.
""",
    },
    {
        "title": "Blast Lung & Blast Abdomen — Real Treatment",
        "section": "emergency",
        "tags": ["blast-injury", "blast-lung", "blast-abdomen"],
        "risk_level": "critical",
        "body_markdown": """## Ruptured Tympanic Membrane — the Most Common Blast Injury

**Occurs from as little as 7 psi of sudden pressure increase.** **Real signs:** sudden, severe, sharp ear pain, possible bleeding from the ear, varying hearing loss. **Real treatment: clean the opening gently, then leave it alone — do NOT pack it, syringe it, or put any medication inside.**

## ⚠️ Blast Lung

**Real signs:** beyond general blast symptoms — bluish skin (cyanosis), rapid pulse, chest/upper abdominal pain with mild abdominal rigidity, ineffective coughing with bloody frothy mucus, and multiple bruises along the front rib margins.

**Real treatment:**
- **Move the person as little as possible — ideally stabilize for 48 hours before even attempting evacuation, if that's genuinely possible.**
- Give oxygen for cyanosis/breathing difficulty.
- **⚠️ Always suspect pulmonary edema from bleeding inside the lung's air sacs** — if IV fluids are truly necessary, use them with real caution, at a slow rate.
- Small doses of atropine sulfate can help reduce secretions.
- **⚠️ Avoid ether or gas-based anesthetics entirely.**
- Antibiotics are genuinely useful for serious blast lung cases.

## ⚠️ Blast Abdomen

**Real signs:** a sudden "kick in the belly" sensation, a brief period where it seems to ease, then a return of severe, worsening, unrelenting pain. Frequent bowel movements, difficulty urinating, dark/bloody stool (melena or frank blood). **Real diagnostic clue:** pain starting in the upper abdomen then spreading downward strongly suggests this; pain confined to the lower abdomen from the start strongly suggests actual internal (intraperitoneal) damage.

**Real treatment:**
- **Serious cases genuinely need surgery — place them high on any evacuation priority list.**
- If hemorrhage or perforation is suspected, antibiotics are warranted.
- **Keep the person NPO (nothing by mouth)**, place a nasogastric tube, use an indwelling urinary catheter, and manage pain carefully.
- **⚠️ Real, important caution: withhold morphine until the injury has been properly assessed** — specifically, don't give it if surgery/anesthesia is expected within the next 1-2 hours, since morphine can complicate that care.

## Other Real Blast-Related Injuries

**Fractures and other tissue trauma** are treated the same as any other time. **Scrotal/testicular contusion and pain are common** — treat with adequate support. **Temporary limb weakness after a blast** is likely from minor vascular disturbance in the spinal cord, not a permanent injury on its own.

## Detailed Version

**The real, shared caution across blast lung and blast abdomen treatment: both call for deliberately minimizing intervention in the short term (limited movement, cautious fluids, withheld morphine) specifically because the real injury is often still evolving internally — acting too aggressively, too early, can make it measurably worse rather than better.** This runs against the instinct to act decisively on a serious-looking injury, which is exactly why it's worth stating explicitly.
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
