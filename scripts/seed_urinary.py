#!/usr/bin/env python3
"""Seeds 2 more real pages from Where There Is No Doctor's Chapter 18
(The Urinary System and the Genitals): Urinary Tract Infections &
Kidney Stones, and Enlarged Prostate -- mined from the real text
layer already extracted in this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_urinary.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Urinary Tract Infections & Kidney Stones",
        "section": "reference",
        "tags": ["uti", "kidney-stones"],
        "risk_level": "moderate",
        "body_markdown": """## Urinary Tract Infection (UTI)

**Signs:** painful, frequent urination; cloudy or reddish/bloody urine; sometimes a feeling the bladder won't empty fully; sometimes fever, chills, or lower back/kidney-area pain. **Much more common in women than men.** Pain spreading around the sides below the ribs, with fever, points to a more serious kidney-involving infection, not just a bladder infection.

**Treatment:**
- **Many minor UTIs resolve just from drinking a lot of water** — at least a glass every 30 minutes for 3-4 hours, then keep up a high water intake. **Exception: don't push fluids hard if the person can't urinate at all, or has hand/face swelling** — that's a different, more serious problem.
- If water alone doesn't help, or there's fever, a real antibiotic course (the book names cotrimoxazole, amoxicillin, or ciprofloxacin if the infection has reached the kidneys) is needed — this requires real medical guidance on which one and how much, often for a full 10-day course to clear it completely.
- **Keep drinking water while on antibiotics**, not just before starting them.
- If it doesn't improve quickly — get real medical advice.

## Kidney or Bladder Stones

**Signs:** sharp/severe pain in the lower back, side, lower belly, or (in men) the base of the penis. Sometimes the urine stream is blocked or reduced to drops; sometimes blood appears at the start of urination. A urinary infection can be present at the same time.

**Treatment:** same general approach as a UTI (fluids, possible antibiotic), plus pain relief and an antispasmodic. **If urination is blocked, try lying down to urinate** — this can sometimes let a stone in the bladder roll away from the opening. **Severe cases may need real medical treatment, including surgery** — don't try to manage severe, unrelieved blockage at home indefinitely.

## Detailed Version

The real distinguishing clue between a simple bladder infection and a more dangerous kidney infection is location and severity: pain that's spread to the mid/lower back and sides, combined with fever, means the infection has likely moved up into the kidneys — that combination is the real signal to escalate from "drink water and wait" to "get real antibiotics and possibly medical help," not just worse version of the same problem.
""",
    },
    {
        "title": "Enlarged Prostate",
        "section": "reference",
        "tags": ["prostate"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

Common in men over 40 — the prostate gland (between the bladder and urethra) swells and restricts urine flow.

**Signs:** difficulty urinating, urine reduced to dribbling or blocked entirely (sometimes for days), sometimes difficulty with bowel movements too. **Fever indicates an infection is also present**, which changes treatment.

**Treatment:**
- If unable to urinate at all: **sitting in a tub of hot water** can sometimes help relax things enough to urinate. If that doesn't work, a catheter may be needed.
- If fever is present, a real antibiotic course is needed.
- **Serious or long-term cases may need real medical evaluation, possibly surgery.**

## Detailed Version

**A real, important distinguishing clue worth knowing:** both an enlarged prostate and a sexually transmitted infection (gonorrhea/chlamydia) can cause difficulty urinating, and they need different treatment entirely. **Age is the real tell:** an older man is more likely dealing with an enlarged prostate; a younger man — especially with a recent sexual exposure to a partner with gonorrhea or chlamydia — is more likely dealing with an STI. Don't assume difficulty urinating in a younger man is automatically prostate-related.
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
