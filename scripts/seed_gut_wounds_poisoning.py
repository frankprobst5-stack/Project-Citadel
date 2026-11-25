#!/usr/bin/env python3
"""Seeds 5 more real pages from Where There Is No Doctor's Chapter 10
(First Aid): Loss of Consciousness, Nosebleeds, Closing Large Cuts,
Acute Abdomen & Appendicitis, and Poisoning.

Poisoning needed the same real correction as Choking and Snakebite
earlier in this build-out: the book's own instructions include
inducing vomiting (salty water, a finger in the throat) for certain
poisons -- but the AAP and American Association of Poison Control
Centers no longer endorse inducing vomiting by ANY method for
poisoning, in children or adults, confirmed via Mayo Clinic/poison.org
(the book predates that shift). Built from current guidance instead,
keeping the book's still-accurate prevention advice (lock up poisons,
never store them in drink bottles) and general supportive care.

The book's own Snakebite section in this same chapter is intentionally
NOT reused here -- it repeats the same pressure-bandage approach
already corrected in an earlier batch's Snakebite page; no need to
re-litigate it.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_gut_wounds_poisoning.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Loss of Consciousness — Assessment",
        "section": "emergency",
        "tags": ["unconsciousness", "first-aid"],
        "risk_level": "critical",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

**Common causes:** a hit on the head, shock, seizure, poisoning, drunkenness, fainting (fright, weakness, low blood sugar), heat stroke, stroke, heart attack.

**If someone's unconscious and you don't know why, check these in order:**
1. **Breathing?** If not, tilt the head back, pull the jaw/tongue forward, clear anything blocking the throat. Start rescue breathing if needed.
2. **Losing a lot of blood?** Control it.
3. **Signs of shock** (moist pale skin, weak rapid pulse)? Lay with head lower than feet, loosen clothing.
4. **Could it be heat stroke** (no sweating, high fever, hot red skin)? Shade them, head higher than feet, soak with cool/cold water, fan them.

**Never give anything by mouth to an unconscious person.**

**If a back or neck injury is possible:** don't move them until they wake up, if at all avoidable. If you must move them, do it with extreme care — don't bend the neck or back.

## Detailed Version

Skin color is a real, quick clue for positioning: **very pale skin** points toward shock or fainting (lay with legs up); **red or normal-colored skin** points toward heat stroke, stroke, or a heart problem (keep more upright, don't elevate legs the same way). This isn't a diagnosis — it's a fast triage cue for how to position someone while you get real help moving.

Look for wounds or broken bones while disturbing the person as little as possible — the goal is gathering information for whoever treats them next, not a thorough exam that risks further injury.
""",
    },
    {
        "title": "Nosebleeds",
        "section": "reference",
        "tags": ["nosebleed", "first-aid"],
        "risk_level": "low",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

1. Sit upright, lean forward slightly — **don't tilt the head back** (that just sends blood down the throat instead of stopping the bleed).
2. Blow the nose gently once to clear clots/mucus.
3. **Pinch the nose firmly for a full 10 minutes**, without letting go to check — releasing early is the most common reason this doesn't seem to work.

**If that doesn't stop it:** pack the nostril with a cotton wad (part left sticking out), then pinch firmly again for another 10+ minutes without releasing.

**For an older person with bleeding that won't respond to pinching** (sometimes from deeper in the nose): lean forward, hold something like a cork between the teeth, and try not to swallow — this gives the blood time to clot rather than being swallowed and swept away.

**Prevention for frequent nosebleeds:** a little petroleum jelly inside the nostrils daily, or a mild saltwater nasal rinse.

## Detailed Version

The 10-minute minimum is the real point people get wrong — checking after 2-3 minutes to "see if it's working" restarts the clot formation every time you look. Set a timer and genuinely don't let go until it's done.
""",
    },
    {
        "title": "Closing Large Cuts",
        "section": "reference",
        "tags": ["wound-care", "sutures"],
        "risk_level": "high",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

**Only close a cut yourself if ALL of these are true:**
- The cut is less than 12 hours old.
- It's genuinely clean.
- A health worker can't close it the same day.

**Never close:** old, dirty, or already-infected wounds, or any bite from a person, dog, pig, or other animal — these must be left open. Closing a contaminated wound traps infection inside, which is far more dangerous than an open wound that can drain.

**Before closing anything:** wash thoroughly with cool boiled water (and soap if dirty), ideally squirting it out with a syringe. Make absolutely sure no dirt or soap residue remains inside.

**Two methods:** butterfly adhesive tape strips (simpler, works if the wound isn't under much tension), or actual stitches (needed if the skin edges don't come together naturally on their own).

**To stitch:** boil a sewing needle and thread (nylon or silk) for 20 minutes, wash the wound and your hands thoroughly, stitch starting from the middle of the cut outward. Leave stitches in 5 days (face), 10 days (body), or 14 days (hand/foot) before removal.

**If a closed wound shows any infection sign — remove the stitches immediately and leave it open.**

## Detailed Version

The "12 hours and clean" rule exists because bacteria have a real window to establish an infection inside a wound before closure traps them in — past that window, closing it does more harm than good regardless of how clean it looks on the surface. This is the same underlying principle as "never stitch a bite wound": the real infection risk from the wound's origin matters more than how the edges look right now.
""",
    },
    {
        "title": "Acute Abdomen & Appendicitis",
        "section": "emergency",
        "tags": ["appendicitis", "abdominal-pain"],
        "risk_level": "critical",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

**"Acute abdomen" means a sudden, severe gut emergency (appendicitis, peritonitis, gut obstruction) that often needs real surgery to prevent death.**

**Suspect it when:** continuous, worsening severe belly pain WITH vomiting but WITHOUT diarrhea.

| Acute abdomen — get to a hospital | Less serious — can likely be managed at home |
|---|---|
| Continuous pain that keeps getting worse | Pain that comes and goes (cramping) |
| Constipation and vomiting together | Moderate/severe diarrhea |
| Belly swollen, hard, person protects/guards it | Signs of an ordinary infection (cold, sore throat) |
| Severely ill overall | Only moderately ill, or has had similar pain before |

**Appendicitis specifically:** pain often starts around the navel, then moves and settles in the lower right belly — getting steadily worse, sometimes with loss of appetite, vomiting, mild fever.

**A real bedside test (rebound tenderness):** press slowly but firmly on the belly, then release quickly. A sharp spike of pain *on release* (not just on pressing) suggests appendicitis or peritonitis.

**If acute abdomen is suspected:** get to a hospital as fast as possible. Give nothing by mouth and no enema (unless dehydration develops, in which case only small sips of water or Rehydration Drink). Keep the person resting quietly, half-sitting.

## Detailed Version

**Why "no food/drink" matters here specifically:** if surgery is needed, a stomach full of food or liquid raises real anesthesia risk — this isn't withholding comfort for no reason, it's keeping surgical options open.

A belly that's become hard "like a board" with pain on even light touching is a sign peritonitis has progressed — a real, immediate life-threatening escalation, not just "the same problem, worse."

Gut obstruction (something physically blocking the intestine — a mass of roundworms, a hernia trapping a loop of gut) shows a related but distinct pattern: forceful vomiting (sometimes shooting out, sometimes smelling like stool), a silent belly (no gurgling sounds when you listen), and little-to-no bowel movement. Treat it with the same urgency as appendicitis — get to a hospital fast.
""",
    },
    {
        "title": "Poisoning",
        "section": "emergency",
        "tags": ["poisoning", "first-aid"],
        "risk_level": "critical",
        "source_url": "https://www.mayoclinic.org/first-aid/first-aid-poisoning/basics/art-20056657",
        "body_markdown": """## Quick Version

**Call Poison Control: 1-800-222-1222 (US)** for guidance on any suspected poisoning that isn't an immediate life-threat. **Call 911 immediately if the person is: unconscious or very drowsy, having trouble breathing or has stopped breathing, having a seizure, or uncontrollably agitated.**

**Never try to induce vomiting — not with salt water, not with a finger down the throat, not with ipecac (which isn't even made anymore).** This was once common advice; it is no longer recommended for any poisoning, in children or adults — it doesn't reliably clear the stomach and risks new injury (especially from caustic or petroleum-based substances).

**By type of exposure:**
- **Swallowed:** clear anything left in the mouth. If it's a household chemical, the container's own label often has specific first-aid instructions — follow those.
- **On the skin:** remove contaminated clothing (wear gloves yourself).
- **In the eye:** flush gently with cool water for a full 20 minutes.
- **Inhaled:** get the person into fresh air immediately.

**Keep the container/package if you have it** — having the exact product label in hand when you call Poison Control makes their guidance much faster and more accurate.

## Detailed Version

**Prevention is still the most effective tool here, and this part hasn't changed:** keep all poisons genuinely out of reach of children, and **never store kerosene, gasoline, cleaning products, or any poison in a drink bottle** — a child (or anyone) reaching for a cola bottle has no way to know what's actually inside it. Common household poisoning risks worth specifically keeping locked up: rat poison, insecticides, iron pills and other medications in bulk, bleach, rubbing alcohol, lye/caustic soda, and pesticides.
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
