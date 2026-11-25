#!/usr/bin/env python3
"""Seeds 2 real pages from Where There Is No Doctor's chapter on
injections (pages 65-74) -- mined from the real text layer already
extracted in this session (/tmp/nodoctor.txt). This is a genuinely
load-bearing capstone: dozens of already-seeded wiki pages instruct
"give penicillin by injection" or similar without the safety context
behind that instruction -- this fills that real gap.

Covers: when injections are actually appropriate vs. when they're
dangerous overuse (with the book's own real emergency-medicine table
and "never inject" list), and the real safe IM injection technique
plus allergic-shock recognition/prevention, which the book treats as
its single most safety-critical injection topic.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_injections.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "When (and When Not) to Give an Injection",
        "section": "reference",
        "tags": ["injection", "antibiotics", "medicine-safety"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**The book's own blunt framing is worth keeping exactly: injections are routinely over-prescribed, partly because they're more profitable for whoever is giving them — not because they usually work better than medicine taken by mouth.** For most illnesses, pills are just as effective and far safer. Reserve injections for the real emergencies below.

## ⚠️ Never Give an Injection When:

- You can get real medical help quickly instead.
- The illness isn't serious.
- It's for a cold or the flu — injections do nothing for either.
- The medicine isn't actually recommended for the specific illness you're treating.
- Your needle hasn't been boiled/sterilized.
- You don't know and can't follow the medicine's required precautions.

## Medicines That Should (Almost) Never Be Injected

| Medicine | Why not |
|---|---|
| Vitamins | Oral vitamins work just as well, injected ones cost more and carry real risk for no real benefit — real food beats either |
| Liver extract, vitamin B12, iron (e.g. Inferon) | Can cause abscesses or dangerous shock reactions; oral ferrous sulfate treats anemia just as effectively |
| Calcium | Genuinely dangerous given IV unless done very slowly by a trained person; can cause a large abscess if given in the buttock. Untrained people should never inject it |
| Penicillin | Nearly every infection penicillin treats responds just as well to oral penicillin, which is safer — reserve injection for truly dangerous infections |
| Penicillin + streptomycin combined | Avoid generally; never for a cold/flu (it does nothing); can cause deafness or death, and overuse makes real tuberculosis harder to cure later |
| Chloramphenicol or tetracycline | Oral capsules/syrup work as well or better |
| IV solutions / IV medicines | Only for severe dehydration, only by someone genuinely trained — done wrong, these cause dangerous infections or death |

## Real Emergencies Where Injection IS Appropriate (if medical help will be delayed)

Severe pneumonia, gangrene, post-childbirth infection, tetanus, appendicitis/peritonitis/penetrating abdominal wounds, poisonous snakebite, scorpion sting in a child, meningitis, uncontrollable vomiting, and severe allergic reaction/shock are the real situations this book names as injection-appropriate when real medical help can't be reached fast enough — see each condition's own page for the specific medicine and dose. Tuberculosis, syphilis, and gonorrhea sometimes need injected medicines too, but these are rarely true emergencies — get a real health worker involved rather than improvising.

## ⚠️ How Injections Can Disable or Kill Children

**This is the book's own strongest warning on the subject, worth preserving directly:** an unsterilized needle or syringe can spread HIV, hepatitis, or other serious infections — and can cause infections leading to paralysis or death. **Never inject more than one person with the same needle or syringe without re-sterilizing it in between.** Some injected medicines (the book specifically names labor-inducing hormone injections given to speed up childbirth) are dangerous enough to cause brain damage or death in the baby — "giving strength" is not a real medical justification for an injection.

## Detailed Version

The real throughline across this whole page: the question to ask before reaching for a needle is never "could an injection help," but "does this specific situation actually require one, and is there no safer oral alternative" — because for the overwhelming majority of illnesses this book covers, the honest answer is no, and the injection itself becomes the larger risk.
""",
    },
    {
        "title": "How to Give a Safe Intramuscular Injection",
        "section": "reference",
        "tags": ["injection", "technique", "allergic-shock"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This page assumes an injection is genuinely necessary** — see When (and When Not) to Give an Injection first. Injecting carries two real risks regardless of technique: infection from a non-sterile needle, and an allergic or poisonous reaction to the medicine itself. Both are preventable with real, specific precautions below.

## Preparing the Syringe

1. Wash your hands with soap and water before touching anything.
2. Take the syringe apart and boil it with the needle for 20 minutes; pour out the water without touching either piece.
3. Reassemble, touching only the needle's base and the plunger's button — never the needle itself or the plunger shaft.
4. Clean the medicine ampule/bottle rubber top with alcohol or boiled water before drawing from it.
5. Fill the syringe without letting the needle touch the outside of the ampule.
6. **If mixing a powdered medicine:** inject distilled water into the bottle, shake until fully dissolved, then refill the syringe and remove all air bubbles.
7. **If the needle touches anything else at any point — your finger, alcohol-soaked cotton, a surface — boil it again before use.** There's no safe shortcut around this.

## Where to Inject

Wash hands again immediately before injecting. **Adults: the upper-outer quarter of the buttock muscle.** **Infants and small children: the upper-outer thigh instead — never the buttock**, where the nerve runs close enough to risk real injury in a small child. **Never inject into skin that's infected or has a rash.**

## The Injection Itself

1. Clean the skin with soap and water (or alcohol — if alcohol, let it dry first, since injecting through wet alcohol causes worse pain).
2. Insert the needle straight in, all the way, in one quick motion — a fast, confident insertion hurts less than a slow, hesitant one.
3. **Pull back on the plunger before injecting anything.** If blood enters the syringe, withdraw the needle and reposition to a different spot — you've entered a blood vessel.
4. If no blood appears, inject the medicine slowly.
5. Withdraw the needle and clean the skin again.
6. Immediately rinse the syringe and needle (squirt water through the needle), then disassemble and wash — boil again before any reuse.

## ⚠️ Allergic Shock — the Real Danger With Certain Medicines

**Penicillins (including ampicillin), and antitoxins made from horse serum (scorpion antivenom, snake antivenom, tetanus antitoxin) can cause a dangerous reaction called allergic shock shortly after injection.** Risk is meaningfully higher in anyone previously injected with that medicine or another in the same group — especially if that earlier injection caused hives, rash, itching, swelling, or breathing trouble.

**Before injecting any of these:**
1. Confirm the injection is truly necessary.
2. **Have ready: 2 ampules of epinephrine (Adrenalin) and an ampule of an antihistamine** (promethazine/Phenergan or diphenhydramine/Benadryl) — before you inject, not after a reaction starts.
3. **Ask directly: "Have you ever had a rash, itching, swelling, or trouble breathing after an injection?"** A "yes" means do not use that medicine or anything else in its group — injected or oral.
4. **For high-stakes cases** (tetanus or snakebite antitoxin in someone with a history of allergies, asthma, or prior horse-serum exposure): give promethazine or diphenhydramine 15 minutes before the antitoxin (adults 25-50mg, children 10-25mg by size).
5. **After injecting, stay with the person for a full 30 minutes**, watching for: cool/moist/pale/gray skin (cold sweat), a weak rapid pulse, difficulty breathing, or loss of consciousness.
6. **If any of these appear: inject epinephrine immediately** (adults ½ml, children ⅓-¼ml by size), treat for Shock, and follow with double the normal antihistamine dose.

**For penicillin specifically:** prefer oral pills over injection whenever the infection is mild-to-moderate; always ask the allergy question first; have epinephrine ready before injecting regardless; and watch for 30 minutes afterward every time, not just the first time.

## Detailed Version

The real pattern across both the technique and the allergic-shock sections: almost every serious injection complication in this chapter traces back to skipping a preparatory step under time pressure — not re-boiling a touched needle, not asking the allergy question, not having epinephrine ready before (not after) injecting. The technique itself is simple; the discipline around the steps before and after it is where safety actually lives.
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
