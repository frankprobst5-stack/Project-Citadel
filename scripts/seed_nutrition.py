#!/usr/bin/env python3
"""Seeds 2 more real pages from Where There Is No Doctor's Chapter 11
(Nutrition): Main Foods & Helper Foods, and Recognizing Malnutrition --
mined from the real text layer already extracted in this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_nutrition.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Main Foods & Helper Foods — Eating Right on a Budget",
        "section": "reference",
        "tags": ["nutrition", "food"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**Most diets center on one cheap "main food"** (rice, wheat, corn, potatoes, etc.) that covers most of the body's energy needs — but main food alone isn't enough, especially for growing children, pregnant/breastfeeding women, and the elderly.

**The real problem with main food alone:** it's often high in water and fiber, so a child's stomach fills up before they've actually gotten enough energy to grow well — they can eat "enough" by volume and still be malnourished.

**Two real fixes:**
1. **Feed more often** — at least 5 times a day for a young, thin, or slow-growing child, plus snacks between meals.
2. **Add energy-dense "helper foods"** to the main food: vegetable oil, nuts, seeds (pumpkin/sesame are specifically called out), sugar, or honey. A small amount of added oil can meaningfully cut the sheer *volume* of rice/grain needed to meet the same energy need.

**Three real helper-food categories to round out a diet, added to whatever main food is already eaten:**
- **Energy helpers:** fats/oils, nuts, oil seeds, sugars.
- **Body-building helpers (protein):** beans/peas/lentils, nuts, animal products (milk, eggs, fish, meat).
- **Protective helpers (vitamins/minerals):** dark green leafy vegetables, orange/yellow fruits and vegetables.

## Detailed Version

**The real, practical point this book emphasizes above food-group theory:** you don't need to eat every category perfectly — eat the main food your family already relies on, and add whatever helper foods are actually available locally from each category as often as you can. **Feeding children enough, and often, matters more than hitting a textbook-perfect combination of food types.**
""",
    },
    {
        "title": "Recognizing Malnutrition",
        "section": "reference",
        "tags": ["malnutrition", "nutrition", "children"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Mild malnutrition is the most common form, and it's easy to miss** — the child simply doesn't look obviously sick, just smaller/thinner and slower-growing than expected. The real danger: a mildly malnourished child fights off infections worse — colds last longer and turn into pneumonia more easily, and ordinary childhood illnesses (measles, etc.) become far more dangerous. **Regular weighing or upper-arm measurement in young children is how this gets caught before it becomes severe.**

**Severe malnutrition has two recognizable patterns, usually visible without any measurement:**
- **"Dry" malnutrition (marasmus):** the child simply isn't getting enough food of any kind — small, very thin, wasted, visibly "just skin and bones." **Needs more food, especially energy-dense food.**
- **"Wet" malnutrition (kwashiorkor):** feet, hands, and face become swollen — this often happens specifically when a child isn't getting enough *energy* food, so their body burns protein for energy instead of using it to build tissue, even if some protein is being eaten. **Needs more food overall, more often, with both energy-rich and protein-rich foods.** Eating moldy/spoiled stored beans or lentils can also contribute — avoid feeding spoiled food even when food is scarce.

**Other real nutrition-deficiency conditions, each from a specific missing nutrient:** night blindness (vitamin A), rickets (vitamin D), certain skin/mouth sores and bleeding gums (various vitamins), anemia (iron), goiter (iodine).

## Detailed Version

**The distinction between marasmus and kwashiorkor matters for treatment, not just appearance:** a swollen (kwashiorkor) child can look deceptively less "starved" than a wasted (marasmus) child at a glance, since the swelling can mask how malnourished they actually are — don't assume a swollen child is better-fed than a visibly thin one. Both need more food, but recognizing which pattern is present helps target what kind of food matters most (energy-dense food matters in both, but is the more specific first need in marasmus).
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
