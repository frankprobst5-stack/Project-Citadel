#!/usr/bin/env python3
"""Seeds 1 more real page from Where There Is No Doctor's Chapter 16
(The Eyes): Glaucoma & Iritis -- two real causes of painful red eye
that are both emergencies, mined from the real text layer already
extracted in this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_glaucoma_iritis.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"

PAGE = {
    "title": "Glaucoma & Iritis",
    "section": "emergency",
    "tags": ["eye", "glaucoma", "iritis"],
    "risk_level": "critical",
    "body_markdown": """## Quick Version

**Both of these are real emergencies that can cause permanent vision loss if not treated fast — antibiotic eye ointment does NOT help either one.**

**Acute glaucoma:** sudden headache or severe eye pain, redness, blurred vision, the eyeball feels hard like a marble when touched, sometimes vomiting, the affected pupil larger than the other. **Will cause blindness within days if untreated — get medical help immediately; surgery is often needed.**

**Iritis:** usually one eye, pain (sudden or gradual), heavy watering, worse in bright light, pain when the eyeball itself is touched, blurred vision — but **no pus** (the real distinguishing feature from pink eye/conjunctivitis). **This is also an emergency — get medical help; antibiotic ointment won't help here either.**

## Detailed Version

**Chronic glaucoma is the dangerous, slow-moving version of the same disease** — pressure rises gradually, usually painlessly, and vision loss starts from the sides (peripheral vision) and is easy not to notice until it's advanced. **A real, simple screening test:** cover one eye, look straight ahead with the other, and note where you first notice fingers moving in from the side of your head. Normal peripheral vision picks this up fairly far back; in glaucoma, the fingers have to come noticeably farther forward before they're noticed — meaning the visual field has already narrowed.

**Anyone over 40, or with a family history of glaucoma, should have eye pressure checked about once a year** — this is genuinely preventable blindness if caught early (pilocarpine eyedrops, used for life, or surgery), but only if it's actually caught before vision loss has already progressed.

**The real pattern worth remembering across red, painful eyes:** pus points to an infection like conjunctivitis; no pus with a hard eyeball and vomiting points to acute glaucoma; no pus with heavy watering and pain on touching the eyeball points to iritis. None of these three should be treated the same way, and two of the three need real emergency care, not just antibiotic ointment.
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
