#!/usr/bin/env python3
"""Seeds 2 more real pages from Where There Is No Doctor's Chapter 19:
Newborn Warning Signs, and Childbirth Fever & Breastfeeding Care --
mined from the real text layer already extracted in this session.
Completes this build-out's childbirth/newborn coverage (joining Labor
& Normal Childbirth, Danger Signs in Pregnancy, Postpartum Hemorrhage,
Care of the Newborn at Birth, and Delivery of the Placenta from
earlier batches).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_newborn_warning_postpartum.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Newborn Warning Signs — When a Baby Seems Ill",
        "section": "emergency",
        "tags": ["newborn", "childbirth"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Newborns show illness very differently than older children — almost any vague sign (poor feeding, excess sleepiness, pale skin, vomiting, fever OR low temperature, a swollen belly, seizures, episodes of turning blue) can mean a serious blood infection (septicemia). Several of these signs together is reason enough to treat it as a real emergency, even without a clear single diagnosis.**

**Jaundice (yellow skin/eyes) timing matters a lot:**
- Appearing in the **first day of life, or after day 5** — **serious, get medical help.**
- Appearing between **day 2 and day 5** — usually not serious. Give extra breast milk, undress the baby, and place them in bright indirect light near a window (not direct sunlight).

**Check the soft spot on top of the head (fontanel):**
- **Sunken** → possible dehydration.
- **Swollen/bulging** → possible meningitis.
- **Important:** if both dehydration and meningitis are present together, the soft spot can feel deceptively normal — don't rule either out based on the soft spot alone; check for other signs of each separately.

**Breathing and color:** fast breathing (50+ breaths/minute), blue coloring, grunting, or the skin pulling in between the ribs with each breath are real pneumonia signs — small babies with pneumonia often don't cough and may show none of the "obvious" signs older children show.

**Stiffness or sudden muscle tightening when touched/moved** can mean tetanus, meningitis, or birth-related brain injury — check if the jaw opens freely and test knee reflexes (see Tetanus).

**A baby who stops nursing well between days 5-15 of life may have tetanus** — this specific timing detail is a real, useful diagnostic clue.

## Detailed Version — Suspected Septicemia (blood infection)

Most common after day 2 of life, since it takes bacteria that entered through the skin or cord that long to spread through the body. **Newborns do NOT reliably run a fever with serious infection — temperature can be high, low, or completely normal, so "no fever" does not rule this out.**

**If septicemia is suspected, this needs real antibiotic treatment calculated by the baby's actual body weight** (the source gives real weight-based ampicillin and gentamicin dosing) — this is not a home-dosing situation; get real medical help immediately, using weight-based dosing only as an emergency bridge if no other option exists.
""",
    },
    {
        "title": "Childbirth Fever & Breastfeeding Care",
        "section": "reference",
        "tags": ["childbirth", "postpartum", "breastfeeding"],
        "risk_level": "high",
        "body_markdown": """## Childbirth Fever (Womb Infection)

**Signs:** chills/fever, headache or low back pain, sometimes belly pain, and a foul-smelling or bloody vaginal discharge after giving birth. Often traced back to unclean conditions or technique during the birth itself.

**This can be genuinely dangerous.** Real treatment requires a real multi-antibiotic course (the source specifies ampicillin, gentamicin, and metronidazole together) continued until 2 full days after the fever clears. **If the mother isn't feeling better by the next day — get medical help; don't keep waiting at home.**

## Breastfeeding & Breast Care

**Begin breastfeeding as early as possible after birth** — this isn't just about feeding the baby; sucking stimulates the womb to contract and helps the placenta deliver sooner. The first milk (colostrum, a thick yellow fluid) is genuinely important — rich in protein and real infection-fighting value for the newborn, not something to skip waiting for "real" milk to come in.

**Supply matches demand:** breasts make roughly as much milk as is actually removed — a baby who nurses well keeps supply up; a baby who can't nurse (illness, weakness) will cause supply to drop within days unless milk is actively expressed by hand in the meantime.

**If the baby is too weak to suck:** hand-express milk and feed it by spoon or dropper rather than letting supply crash — this also prevents the breast from becoming painfully overfull, which raises real risk of a breast abscess.

**Daily bathing is enough breast hygiene** — don't use soap directly on the breasts/nipples, since it can cause cracking, soreness, and a real entry point for infection.

**Sore or cracked nipples** usually happen when the baby latches onto just the nipple instead of taking in part of the surrounding breast too. **Keep nursing through the discomfort** rather than stopping — frequent nursing with a proper latch is both the cause-prevention and the actual fix.

## Detailed Version

The real throughline across both halves of this page: early, frequent breastfeeding isn't just nutrition — it actively helps prevent two separate real postpartum risks (heavy bleeding, via uterine contraction, and breast abscess, via keeping the breast from overfilling) at the same time. Interrupting it, even for good-seeming reasons, removes those protective effects too.
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
