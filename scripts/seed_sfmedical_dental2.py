#!/usr/bin/env python3
"""Seeds 3 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 19 Sections 19-5 through 19-8 --
mined from the OCR output cached at /tmp/sfmedical.txt.

SCOPING NOTE: Chapter 19 also covers acute periapical/periodontal
abscess drainage, acute necrotizing ulcerative gingivitis (trench
mouth), herpetic lesions, pericoronitis, dental local anesthesia
injection technique, tooth extraction with forceps, jaw dislocation
reduction, and mandibular fracture wiring. Checked the existing wiki
first and found pericoronitis, jaw dislocation, jaw fracture, and
general tooth-abscess/extraction coverage already present (from
Where There Is No Dentist) with their own real, usable techniques --
seeding a second, different real technique for the same emergency
would risk confusing a reader under stress rather than helping, so
those are deliberately skipped here. Dental anesthesia injection
technique is also skipped: the source's own "see illustrations
below" at the exact needle-placement steps makes it unsafe to
reconstruct from text alone (an existing wiki page, "Giving a
Dental Local Anesthetic Injection," already covers this from a
different, non-figure-dependent source).

What IS seeded: the real periapical-abscess drainage technique and
its real, specific anatomical spread danger (including the Ludwig's
angina warning) which the existing "Dental Emergencies — Tooth
Abscess" page doesn't cover; the distinct periodontal abscess
condition; a real day-by-day trench mouth protocol that expands on
the existing one-paragraph "Gum Disease" page mention; and oral
herpes (cold sores), not covered anywhere else in the wiki.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_dental2.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Tooth Abscess — Real Periapical Drainage Technique & the Ludwig's Angina Danger",
        "section": "emergency",
        "tags": ["dental", "abscess", "ludwigs-angina"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**For when to pull the tooth and real antibiotic dosing, see Dental Emergencies — Tooth Abscess (already in this wiki).** This page adds 2 real things that page doesn't cover: an actual field drainage technique, and the real, specific danger of an untreated abscess spreading into the neck.

## Real Diagnosis

**History of repeated pain episodes that has gradually become more continuous and intense.** The accumulating pus increases pressure, so the tooth feels "long" to the patient and strikes first when the teeth come together. **⚠️ Severe pain on percussion is the single most significant sign** — always tap a normal-looking tooth first for comparison, then progress to the suspected one. Swelling, malaise, loss of appetite, and fever are sometimes present (antibiotics should only be considered if these systemic signs are actually present). Gingival tissue around the tooth is often tender and inflamed. An untreated abscess may eventually burrow through the jawbone and appear as a bright red elevation of the soft tissue.

## Real Drainage Technique — Immediate Pain Relief

**Drainage usually provides immediate relief. Two real methods:**
1. **If the abscess has "pointed"** (a visible soft, fluctuant bump has formed): incise the fluctuant area of soft tissue. Local anesthesia is neither necessary nor easy to obtain through actively infected tissue.
2. **If it hasn't pointed yet — establish drainage through the tooth itself:** stabilize the tooth firmly with your fingers, then remove the soft decay with a spoon-shaped instrument until you reach the pulp chamber. Finger pressure on the gum near the root should then force pus out through that opening. **Pain usually subsides immediately.**

## ⚠️ The Real Danger of Leaving It Untreated

**The real progression of an untreated periapical abscess:** pus accumulates and destroys bone at the root tip → it invades the marrow spaces → it destroys the outer bone layer and lifts the membrane covering the bone (a subperiosteal abscess) → that membrane ruptures, causing visible gum swelling (a "gum boil") → the gum boil ruptures on its own, draining the pus.

**⚠️ Real, critical nuance: spontaneous drainage feels like relief, but it does NOT cure the problem** — it just converts the acute infection into a chronic one that can flare up again at any time, especially when the person's resistance is lowered (illness, stress, malnutrition). The tooth still needs to come out or be treated; waiting for it to drain on its own is not a real fix.

**⚠️ Where the infection spreads depends on the tooth's anatomy, and one specific path is a real emergency:** if a lower (mandibular) tooth's infection spreads toward the tongue side of the jaw at a point BELOW where the floor-of-mouth muscles attach, it tracks into the deep fascial spaces of the neck instead of draining into the mouth. **This can cause Ludwig's angina — a spreading neck infection that can swell enough to close off the airway and can be fatal.** Any tooth abscess with spreading neck/floor-of-mouth swelling, difficulty swallowing, or breathing difficulty is a real emergency requiring the fastest possible evacuation, not field treatment.

**⚠️ Also worth knowing: external heat applied to a facial/jaw swelling can encourage the abscess to drain outward through the skin instead of into the mouth** — this is a real, undesirable outcome worth avoiding, so don't apply a hot compress directly over a swollen abscess hoping to "bring it to a head" externally.

## Related: Periodontal Abscess (A Different, Non-Decay-Related Condition)

**A periodontal abscess is a separate real condition from the periapical/root abscess above — it's not caused by tooth decay, but by a trapped foreign body, hardened tartar under the gumline, or local trauma, leading to infection of the gum and ligament tissue around (not inside) the tooth.**

**Real signs:** redness and swelling of the surrounding gum, the tooth sensitive to tapping and slightly mobile, swollen neck lymph nodes, general malaise and fever.

**Real treatment:**
1. Carefully probe the gum crevice to establish drainage and locate the foreign body.
2. Gently spread the tissue and irrigate with warm water to flush out pus and debris.
3. Remove any foreign body found.
4. Have the person rinse with hot salt water hourly.

## Detailed Version

**The real, most important idea connecting this entire page: a tooth abscess that seems to be getting better on its own (pain suddenly easing, swelling draining) is not necessarily resolving — it can simply be moving toward a worse location, and the single most dangerous version of that is downward-and-inward into the neck rather than outward into the mouth.** Watching specifically for neck swelling, trouble swallowing, or breathing difficulty — not just whether the original pain has eased — is what actually catches that danger in time.
""",
    },
    {
        "title": "Trench Mouth (ANUG) — Real Day-by-Day Field Treatment Protocol",
        "section": "reference",
        "tags": ["dental", "trench-mouth", "gingivitis"],
        "risk_level": "moderate",
        "body_markdown": """## ⚠️ Read This First

**This page expands on the brief trench mouth mention in the existing Gum Disease page** with a real, specific day-by-day protocol — trench mouth (acute necrotizing ulcerative gingivitis, also called Vincent's infection) is common enough, and painful enough, to be worth a real step-by-step plan rather than just "use an antiseptic rinse."

## Real Diagnosis

**Constant gnawing pain and marked gum sensitivity are the main complaints**, along with pronounced gum bleeding, a foul/fetid breath odor, and a foul metallic taste. **Necrotic, crater-like ulcers covered by a grayish film typically appear between the teeth** — this is the hallmark finding. Swollen neck lymph nodes and fever can develop after the oral symptoms start. **Left untreated, the tissue destruction is progressive.**

**⚠️ Real, important caution: any case that hasn't clearly improved within 24 hours of starting treatment needs real blood-work evaluation** — lesions that look identical to trench mouth can actually be caused by a blood disorder or vitamin deficiency, not this infection.

## Real Day-by-Day Protocol

**Day 1:**
1. Wear gloves if available.
2. Swab the teeth and gums thoroughly, twice, with a 1:3 dilution of 3% hydrogen peroxide in water on a cotton-tipped applicator.
3. **Have the person rinse their mouth with this same diluted solution every hour.** ⚠️ **Limit this hydrogen peroxide rinse regimen to a maximum of 2 days** — longer use risks triggering a fungal infection in the mouth.
4. Put the person on a soft diet with plenty of fluids.
5. Reassess in 24 hours.

**Day 2** (the person should already be noticeably more comfortable):
1. Using a soft toothbrush soaked in hot water, clean the teeth without touching the gums directly.
2. Continue the hourly hydrogen peroxide rinse.
3. Have the person brush with a hot-water-soaked soft toothbrush every hour as well.
4. Reassess again in 24 hours.

**Day 3** (pain should be essentially gone):
1. Clean the teeth as before.
2. Floss between all teeth.
3. **Stop the hydrogen peroxide rinse.**
4. Have the person brush 3-4 times a day and floss once a day going forward.

## ⚠️ Real Treatment Mistakes to Avoid

- **Antibiotics should NOT be used unless the person has signs of systemic infection (fever, spreading involvement).**
- **Never use antibiotic lozenges for this condition.**
- **⚠️ Never use silver nitrate or other caustic/burning agents on the lesions** — this is specifically and definitely contraindicated.

## Detailed Version

**The real, underlying reason this protocol works in stages rather than jumping straight to normal brushing: in the acute phase, normal brushing/flossing against the raw, ulcerated gum tissue is itself painful and can worsen the damage** — the hydrogen peroxide rinse does the real cleaning work in the first 1-2 days while the tissue is too inflamed to tolerate direct mechanical cleaning, and only once the acute pain has eased does real mechanical cleaning (brushing, then flossing) get reintroduced, day by day. **⚠️ Completing the full protocol matters even after the pain disappears on day 3** — the acute symptoms resolving does not mean the underlying tissue damage has actually stopped; real follow-up dental cleaning and care is still needed afterward to fully resolve it.
""",
    },
    {
        "title": "Oral Herpes (Cold Sores) — Real Diagnosis & Field Care",
        "section": "reference",
        "tags": ["dental", "cold-sores", "herpes-simplex"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**Oral herpes (cold sores, fever blisters) is caused by the herpes simplex virus, which stays in the body for life near the original infection site** — flaring up again whenever local resistance drops, rather than being a new infection each time.

## Real Diagnosis

**Itching, burning, and a feeling of tissue tightness mark the early stage.** On the lips, a fluid-filled blister stage is often visible; **inside the mouth, these blisters rupture almost immediately**, leaving a small eroded area with a bright red, flat or slightly raised border. In later stages, the lesion becomes covered with a whitish, plaque-like film of dead cells and debris. **Occasionally, a more generalized outbreak produces large areas of fiery red, swollen, severely painful oral tissue — this version comes with real systemic symptoms** (fever, malaise) and is far more extensive than a typical single cold sore.

## Real Triggers

**A degree of lowered local resistance is required for the virus to reactivate** — real common triggers include emotional stress, a common cold or other respiratory infection, digestive upset, nutritional deficiency, food allergy, and physical trauma to the mouth tissue. **In women, menstruation and pregnancy are also real, common triggers.**

## Real Treatment

**Treatment is aimed at symptoms only — antibiotics don't work against this virus** (though in severe cases they may be used to prevent a secondary bacterial infection on top of it). **Force fluids to prevent dehydration.** Avoid spicy food, alcohol, and smoking, since all three irritate the already-painful lesions. Keep up normal oral hygiene despite the discomfort.

## Real Prognosis

**Healing typically takes about 2 weeks; scarring or other serious after-effects are rare.** **⚠️ The very first infection (usually in childhood) is typically far worse than later recurrences** — larger, more numerous lesions and more pain. **A real, practical danger specific to children: the pain can be severe enough that they refuse to eat or drink at all, risking real dehydration** — forcing fluids is especially important in that case, even if solid food has to wait.

## Detailed Version

**The real, most useful thing to understand about this condition: because the virus never actually leaves the body, "curing" an outbreak isn't the right goal — managing the current flare-up's symptoms and reducing whatever triggered it (stress, illness, poor nutrition) is what actually helps, since another flare-up remains possible for the rest of the person's life.**
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
