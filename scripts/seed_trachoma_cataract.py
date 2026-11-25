#!/usr/bin/env python3
"""Seeds 2 more real pages from Where There Is No Doctor's Chapter 16
(The Eyes): Trachoma, and Cataracts & Night Blindness (Vitamin A
Deficiency) -- mined from the real text layer already extracted in
this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_trachoma_cataract.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Trachoma",
        "section": "reference",
        "tags": ["trachoma", "eye-infection"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

A slow-progressing eye infection that can take months to years to cause real damage — but **left untreated, it's a real cause of blindness.** Spread by direct touch or flies, most common in crowded, poor-sanitation living conditions.

**Signs, in progression:**
1. Starts looking like ordinary pink eye — red, watery eyes.
2. After a month+: small pinkish-gray bumps (follicles) form inside the upper eyelid (visible by turning the lid back).
3. Eventually, tiny new blood vessels appear at the top edge of the cornea (visible with careful inspection or a magnifying glass).
4. **Follicles + this corneal change together are essentially a trachoma diagnosis.**
5. After years, follicles leave scarring — which can thicken the eyelid (limiting how it opens/closes) or pull eyelashes inward, scratching the cornea and causing real blindness.

**Treatment:** antibiotic eye ointment (tetracycline or erythromycin) daily for 30 days, PLUS the same antibiotic taken by mouth for 2-3 weeks for a complete cure — the eye ointment alone isn't considered sufficient.

**Prevention:** daily face-washing and the same cleanliness practices that prevent other infections (see General Cleanliness & Hygiene) genuinely reduce trachoma spread. Everyone living with an infected person — especially children — should have their eyes checked regularly and treated early if signs appear.

## Detailed Version

The real reason trachoma is dangerous specifically despite being slow: it's easy to dismiss early symptoms as "just pink eye" since they look identical at first, and the real damage (scarring, inward-turned eyelashes scratching the cornea) only shows up years later — by which point preventing it would have been far easier than treating the consequences. Early, complete treatment genuinely matters here even though nothing about the early stage feels urgent.
""",
    },
    {
        "title": "Cataracts & Night Blindness (Vitamin A Deficiency)",
        "section": "reference",
        "tags": ["cataract", "vitamin-a", "night-blindness", "nutrition"],
        "risk_level": "high",
        "body_markdown": """## Cataracts

The eye's lens turns cloudy — the pupil looks gray or white when light is shone into it. Common in older people, rare in babies. **Medicine does not help a cataract** — if the person can still distinguish light from dark and notice movement, surgery can genuinely restore vision, though strong glasses (or an implanted artificial lens) are needed afterward.

## Night Blindness & Xerophthalmia (Vitamin A Deficiency)

**Most common in children ages 1-5, and genuinely preventable through diet.** Progression:
1. Night blindness first — can't see as well as others in the dark.
2. Dry eyes (xerophthalmia) — the white of the eye loses its shine, starts to wrinkle.
3. Small gray bubble patches (Bitot's spots) may appear.
4. The cornea itself can become dry, dull, pitted — and in advanced cases can soften, bulge, or even rupture, **usually without pain** — which means a caregiver can't rely on the child's own distress to catch it in time.

**This condition often appears or worsens during another illness** (diarrhea, whooping cough, TB, measles) — **examine the eyes of any sick or underweight child**, don't assume vitamin A status is fine just because the current illness is something else.

**Prevention:**
- Breastfeed up to 2 years if possible.
- After 6 months, feed vitamin-A-rich foods: dark green leafy vegetables, orange/yellow fruits and vegetables (papaya, mango, squash), whole milk, eggs, liver.
- If diet alone isn't reliable, or signs are appearing: **200,000 units vitamin A every 6 months** (100,000 units for babies under 1 year).

**Treatment once signs are present:** 200,000 units by mouth on day 1, again on day 2, and again 14 days later (half-dose for babies under 1). **If the cornea is already severely affected** (dull, pitted, bulging) — this is a real emergency: bandage the eye and get vitamin A immediately, preferably by injection, and seek real medical help.

**⚠️ Too much vitamin A is poisonous — never exceed the doses above.**

## Detailed Version

**The painless progression is the real danger here, more than the disease itself being hard to treat.** Vitamin A deficiency is cheap and straightforward to prevent and even to treat in its early stages — the actual risk is that because it doesn't hurt, a child can progress to corneal damage before anyone realizes something is seriously wrong. In any region or situation where xerophthalmia is a known risk, routine vitamin A supplementation for breastfeeding and pregnant women (second half of pregnancy) is itself a real preventive measure, not just treatment for existing cases.
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
