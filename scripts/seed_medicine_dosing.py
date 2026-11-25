#!/usr/bin/env python3
"""Seeds 1 more real page from Where There Is No Doctor's Chapter 8
(How to Measure and Give Medicine) -- mined from the real text layer
already extracted in this session. A real, practical dosing-fraction
table that several earlier pages in this build-out implicitly assume
(pediatric doses given as fractions of "the adult dose").

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_medicine_dosing.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"

PAGE = {
    "title": "Measuring & Giving Medicine, Especially to Children",
    "section": "reference",
    "tags": ["medication", "dosing", "children"],
    "risk_level": "high",
    "body_markdown": """## Quick Version

**1 teaspoon = 5 ml. 1 tablespoon = 15 ml.** Many household "teaspoons" actually hold anywhere from 3-8 ml — **if a medicine dose is specified in teaspoons, use an actual 5 ml measuring spoon, not a random kitchen spoon.** Too little under-treats; too much can be dangerous, and "about a teaspoon" isn't precise enough for real medicine.

**If you only have adult dosing instructions and need to dose a child, by age:**
| Age | Fraction of the adult dose |
|---|---|
| 8-13 years (~66 lbs) | ½ dose |
| 4-7 years (~33 lbs) | ¼ dose |
| 1-3 years (~17.6 lbs) | ⅛ dose |
| Under 1 year (~11 lbs) | Use the 1-year dose, but get real medical advice when at all possible |

**Giving medicine safely to a child:**
- **Never give medicine to a child lying flat on their back, or with the head tilted back — sit them up or lean the head forward, to prevent choking.**
- **Never give medicine by mouth to a child who is having a seizure, or who is asleep/unconscious.**
- **Never give honey to a baby under 1 year old** — rare but real risk of a dangerous reaction (infant botulism). This applies even when making a homemade medicine syrup sweetened with honey.

## Detailed Version — making your own children's medicine syrup

Liquid children's medicine (syrup/suspension) usually costs more per dose than the equivalent pills. **A real, lower-cost alternative:** grind a pill (or open a capsule), mix the powder into cooled boiled water with sugar or honey to mask the taste — especially useful for bitter medicines like tetracycline or chloroquine. **Be careful with the dose when doing this yourself** — it's easy to misjudge how much powder is actually in a partial spoonful of mixed syrup compared to a clean, pre-measured commercial dose.

**The core principle behind the age/weight dosing table:** smaller body size means medicine concentrates more per pound of body weight, so a proportionally smaller dose has the same real effect — giving a full adult dose to a small child isn't "extra safe," it's genuinely dangerous overdosing. When real pediatric dosing information is available for a specific medicine, use that instead of this general fraction table — this table is a fallback for when nothing more specific is available, not a replacement for real dosing information when you have it.
""",
}


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

    if PAGE["title"] in existing_titles:
        print(f"SKIP  (already exists): {PAGE['title']}")
        return
    if args.dry_run:
        print(f"WOULD CREATE: {PAGE['title']}")
        return
    res = requests.post(
        f"{args.base_url}/api/wiki/pages",
        headers=headers,
        json={
            "section": PAGE["section"],
            "title": PAGE["title"],
            "body_markdown": PAGE["body_markdown"],
            "tags": PAGE["tags"],
            "source_url": NO_DOCTOR_PDF_URL,
            "verification_status": "verified",
            "risk_level": PAGE["risk_level"],
        },
        timeout=10,
    )
    if res.ok:
        print(f"CREATED: {PAGE['title']}")
    else:
        print(f"FAILED  ({res.status_code}): {PAGE['title']} -- {res.text}", file=sys.stderr)


if __name__ == "__main__":
    main()
