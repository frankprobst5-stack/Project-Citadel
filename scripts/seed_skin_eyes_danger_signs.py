#!/usr/bin/env python3
"""Seeds 5 more real pages from Where There Is No Doctor: skin
infestations (scabies/lice), boils & abscesses, eye injuries &
chemical burns, pink eye, and a general "signs of dangerous illness"
triage reference -- all confirmed from the real text layer already
extracted to /tmp/nodoctor.txt in this session.

"Signs of Dangerous Illness" (Chapter 4) is a genuinely universal
triage checklist -- not age- or condition-specific -- and is one of
the most broadly useful single pages in the whole book: a plain list
of "if you see this, get real medical help now" signs that applies
regardless of what's actually wrong.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_skin_eyes_danger_signs.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Scabies & Lice",
        "section": "reference",
        "tags": ["skin", "scabies", "lice", "parasites"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**Scabies:** intensely itchy little bumps, most common between fingers, on wrists, around the waist, genitals, between toes. Caused by tiny mites tunneling under the skin — spreads by skin contact or shared clothing/bedding.
- **Treat everyone in the household and all sexual contacts at once**, even if only one person shows signs.
- Bathe and change clothes daily; wash all clothing/bedding in hot water or boil it, then sun-dry.
- Permethrin cream (Elimite) is the standard treatment: wash the body first, apply the cream everywhere except the face, leave on 10-14 hours, bathe again, repeat in 1 week.
- **Never use lindane — it's a poison.**
- Itching can persist up to 2 weeks *after* successful treatment — that alone doesn't mean it failed. If it's still going after 2 weeks, retreat or try a different medication.

**Lice (head, body, or pubic):** itching, sometimes skin infection or swollen lymph nodes.
- Scrub hair with regular shampoo for 10 minutes, rinse, comb thoroughly with a fine-tooth comb to remove lice AND eggs (nits) — repeat daily for 2 weeks. Combing matters more than any product.
- Medicated shampoos (permethrin/pyrethrin) can help but avoid them in pregnancy or in children under 2.
- **Again: never use lindane.**
- Body lice: daily hot-water bath for 10 days, wash thoroughly each time, keep bedding/clothing clean.

## Detailed Version

The reason whole-household treatment matters for scabies isn't caution for its own sake — a single untreated person keeps re-infecting everyone else, so partial treatment just means a repeating cycle. The same logic applies to lice in a household with multiple children.

A home remedy worth noting: for lice nits, olive oil (or diluted vinegar) loosens the egg's grip on the hair shaft, making the fine-tooth comb genuinely more effective — this isn't a cure on its own, but it measurably helps the part of treatment (combing) that actually removes the eggs.
""",
    },
    {
        "title": "Boils & Abscesses",
        "section": "reference",
        "tags": ["skin", "boils", "abscess", "infection"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

A boil is a pocket of pus under the skin — often starting at an infected hair root, a puncture wound, or a dirty needle injection. Painful, with red, hot skin around it; can cause fever or swollen lymph nodes.

**Treatment:**
- Hot compresses several times a day.
- **Let it open and drain on its own — never squeeze or press it.** Squeezing can push the infection deeper or spread it elsewhere in the body.
- Once it opens, keep applying hot compresses and let the pus drain freely.
- If it's very painful and hasn't opened after 2-3 days of hot soaks, it may need to be lanced (cut open) — real medical help is the safer route for this if available.
- If it's causing fever or swollen lymph nodes, that's a sign a real antibiotic course is needed — get medical guidance on which one and how much.

## Detailed Version

**The "never squeeze" rule is the one thing worth remembering above everything else here.** It feels counterintuitive — squeezing looks like it's helping the pus come out faster — but it risks forcing infected material into deeper tissue or the bloodstream, which can turn a simple boil into a much more serious, spreading infection. Patience with hot compresses is slower but genuinely safer.
""",
    },
    {
        "title": "Eye Injuries & Chemical Burns",
        "section": "emergency",
        "tags": ["eye-injury", "first-aid"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Any injury that cuts or punctures the eyeball itself is a real emergency** — cover with a clean bandage (don't press on it) and get medical help immediately. Don't try to remove anything stuck deep in the eyeball.

**Chemical in the eye (battery acid, lye, gasoline, pesticide):**
1. Hold the eye open.
2. **Flood it immediately with clean, cool water for a full 30 minutes**, or until pain stops — don't stop early just because it feels better after a few minutes.
3. Be careful not to let contaminated water run into the other eye.

**A speck of dirt or sand (not embedded, not a chemical):**
1. Have them close their eyes and look left/right/up/down — this alone often works the dirt out naturally via tears.
2. If not, flood with clean water or lift it out with the corner of a clean cloth or moist cotton.
3. If it's under the upper lid, gently fold the lid back over a thin stick while they look down — it's usually sitting in the small groove near the lid's edge.
4. If you can't get it out, don't keep trying repeatedly — antibiotic ointment, a bandage, and real medical help.

**Get real medical help immediately for any of these:** a cut/ruptured eyeball, a grayish spot on the cornea with redness, severe pain inside the eye, a noticeable difference in pupil size with eye/head pain, blood visibly behind the cornea, sudden vision loss in one or both eyes, a white glow in the pupil, or any eye infection that isn't improving after 5-6 days of antibiotic ointment.

## Detailed Version

**Why 30 minutes for a chemical burn, not just a quick rinse:** chemicals continue damaging tissue as long as they're in contact with the eye — a 10-second rinse removes the bulk of it but leaves enough behind to keep causing harm. The full 30 minutes (timed, not estimated) is what actually clears it.

A sudden, dramatic increase in pain a few days after a blunt eye injury (a fist, a ball) is a specific warning sign of acute glaucoma developing from the injury — that's a different, later emergency than the original injury, so pain that gets *worse* well after the fact deserves the same urgency as a fresh injury.
""",
    },
    {
        "title": "Pink Eye (Conjunctivitis)",
        "section": "reference",
        "tags": ["eye", "conjunctivitis", "infection"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**Signs:** redness, pus, mild burning in one or both eyes; eyelids often stuck together after sleep. Especially common in children.

**Treatment:**
1. Clean pus from the eye with a clean cloth moistened with boiled (then cooled) water.
2. Apply antibiotic eye ointment — pull the lower lid down and place it inside the lid, not on the outside of the eye (ointment on the outer lid does nothing useful).

**It's very contagious.** Don't let an affected child share a towel, pillow, or bed with others, and wash hands after touching the eyes — both the sick person's and your own.

## Detailed Version

Several different problems cause red, painful eyes, and pink eye is only one of them — dirt/debris, chemical exposure, allergic conjunctivitis (hay fever), and more serious causes like glaucoma or iritis all overlap in symptoms. The real distinguishing clues: pink eye usually affects both eyes with redness/pus and sticky eyelids after sleep, while a foreign object usually affects just one eye, and serious causes like glaucoma tend to bring severe pain concentrated near the cornea rather than general redness. When in doubt — especially if it's one-sided, severely painful, or not improving after several days of antibiotic ointment — treat it as something needing real evaluation, not assumed pink eye.
""",
    },
    {
        "title": "Signs of Dangerous Illness — When to Seek Help",
        "section": "reference",
        "tags": ["triage", "warning-signs"],
        "risk_level": "high",
        "body_markdown": """A general triage checklist — not specific to any one illness. **Any one of these signs means the person is probably too sick to manage safely at home, and needs real medical help as soon as possible.**

## The signs

- Loss of a large amount of blood from anywhere in the body.
- Coughing up blood.
- New blueness of the lips or nails.
- Serious difficulty breathing that doesn't improve with rest.
- Can't be woken up (coma).
- So weak that standing up causes fainting.
- 12+ hours without being able to urinate.
- A full day or more without being able to drink any liquid.
- Heavy vomiting or severe diarrhea lasting more than a day (or more than a few hours in a baby).
- Black, tar-like stools, or vomit containing blood.
- Strong continuous stomach pain with vomiting, in someone without diarrhea and unable to have a bowel movement.
- Any strong continuous pain lasting more than 3 days.
- A stiff neck with an arched back (with or without a stiff jaw).
- More than one seizure in someone with fever or serious illness.
- A high fever (above 102°F/39°C) that won't come down, or that lasts more than 4-5 days.
- Unexplained weight loss over an extended period.
- Blood in the urine.
- A sore that keeps growing and doesn't improve with treatment.
- A lump anywhere in the body that keeps getting bigger.
- Very high blood pressure (220/120 or higher).

## Why this list matters as its own reference

Specific-illness pages (fever, diarrhea, wounds) tell you how to treat the common, usually-not-dangerous version of a problem. This list is the override: regardless of what you think is going on, any one of these signs is reason enough to stop managing it at home and get real medical help — these are warning signs that something is more serious than the ordinary case, even when you aren't sure exactly what that something is.

A sick person's actual vital signs — temperature, pulse rate, breathing rate — tracked a few times a day, plus how much they're drinking and urinating, are worth writing down even at home. That record is genuinely useful information for a health worker or doctor if the situation does escalate to needing one.
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
                "source_url": NO_DOCTOR_PDF_URL,
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
