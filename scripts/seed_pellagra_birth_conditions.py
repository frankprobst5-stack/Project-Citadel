#!/usr/bin/env python3
"""Seeds 2 more real pages from Where There Is No Doctor: Pellagra &
Malnutrition Skin Signs (Chapter 15), and Birth Conditions -- Hip,
Hernia, Hydrocele & Hypothyroidism (Chapter 21) -- mined from the real
text layer already extracted in this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_pellagra_birth_conditions.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Pellagra & Malnutrition Skin Signs",
        "section": "reference",
        "tags": ["pellagra", "malnutrition", "skin"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

Pellagra is a real, specific malnutrition pattern — most common where diet relies heavily on corn/maize or other starchy staples without enough beans, meat, fish, eggs, or vegetables.

**Signs:** in adults, dry cracked skin that peels like sunburn, especially on sun-exposed areas (arms, back of neck, backs of legs). In malnourished children, dark bruise-like marks or peeling sores on the legs/arms, swollen ankles/feet. Often accompanied by other malnutrition signs: swollen belly, sores at the mouth corners, a red sore tongue, weakness, poor appetite, failure to gain weight.

**Treatment:** real food fixes this — beans, lentils, groundnuts, chicken, fish, eggs, meat, or cheese daily. **Whole wheat is a better staple choice than corn/maize where there's a choice.** For severe cases, B-vitamin supplementation (especially niacin — brewer's yeast is a real, accessible source) can help, but **good food matters more than any vitamin pill.**

## Detailed Version

The real, actionable insight here: pellagra isn't really a "skin disease" that needs a skin treatment — it's a nutrition problem that happens to show up on the skin first. Treating the visible skin signs without fixing the underlying diet pattern (over-reliance on one starchy staple) won't actually resolve it.
""",
    },
    {
        "title": "Birth Conditions — Hip, Hernia, Hydrocele & Hypothyroidism",
        "section": "reference",
        "tags": ["newborn", "birth-defects", "congenital"],
        "risk_level": "moderate",
        "body_markdown": """## Dislocated Hip

**A real bedside test:** hold both of the baby's legs with knees bent, then open them wide. **If one leg stops early, or you feel/hear a jump or click, the hip is likely dislocated.**

**Treatment:** carry the baby with knees high and legs wide apart; a harness holding the legs open for 2 weeks can prevent lasting damage. **Recheck in 2 weeks** — if the jump/click is still there, see a health worker.

## Umbilical Hernia (Belly Button Sticking Out)

**Usually harmless — no treatment needed, and a tight belly band will NOT help** (a real, common but ineffective home remedy worth specifically not doing). Even a fairly large one often resolves on its own. **If it's still present after age 5, surgery may be needed** — get real medical advice at that point, but not before.

## "Swollen Testicle" (Hydrocele or Hernia)

**A real, simple way to tell them apart: shine a light through the swelling.**
- **Light shines through easily → probably a hydrocele** (fluid-filled) — usually resolves on its own; get medical advice if it lasts more than a year.
- **Light does NOT shine through, and the swelling gets bigger when the baby coughs/cries → probably a hernia** (a loop of gut) — **this needs real surgery** (see Hernia).

**To distinguish this from a swollen lymph node:** a hernia-related swelling gets bigger when the baby cries or stands and shrinks when lying quietly; a lymph node doesn't change that way.

## Hypothyroidism (Cretinism)

**Caused by lack of iodine in the mother's diet during pregnancy.** Signs in the baby: puffy face, dull expression, prolonged jaundice, tongue hanging out, excess forehead hair, weak/poor feeding, crying little, sleeping a lot, usually with an umbilical hernia too. Mental slowness and deafness can result; walking/talking milestones come later than normal.

**Prevention: pregnant women should use iodized salt instead of plain salt** — a genuinely simple, low-cost preventive measure.

**If suspected, get real medical help immediately** — the earlier real thyroid treatment starts, the more normal the child's development will be.

## Detailed Version

**A real, broader point this source makes worth preserving:** when a child is born deaf, mentally slow, or with a birth defect, often no specific cause can be found, and no one should be blamed — it frequently happens by chance. That said, two real, documented risk factors are genuinely preventable: inadequate maternal nutrition during pregnancy, and iodine deficiency specifically. Both are addressed through real, accessible dietary measures, not guesswork.
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
