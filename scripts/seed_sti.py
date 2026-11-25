#!/usr/bin/env python3
"""Seeds 1 real page from Where There Is No Doctor's Chapter 18:
Sexually Transmitted Infections (Gonorrhea, Chlamydia, Syphilis) --
mined from the real text layer already extracted in this session.
Handled factually, as straightforward health/medical reference
content, same as every other condition in this build-out.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sti.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"

PAGE = {
    "title": "Sexually Transmitted Infections — Gonorrhea, Chlamydia & Syphilis",
    "section": "reference",
    "tags": ["sti", "gonorrhea", "chlamydia", "syphilis"],
    "risk_level": "high",
    "body_markdown": """## Gonorrhea & Chlamydia

**Both can be present with no noticeable signs at all, in either partner.** When signs do appear: pain/burning when urinating, discharge (pus from the penis; yellow/green vaginal or anal discharge), sometimes fever, pelvic pain, painful swollen joints, or a body rash. In men, signs typically start 2 days to 3 weeks after exposure; in women, signs can take weeks or months to show up — **but a person with no signs can still spread the infection to a partner.**

**Left untreated, either can cause permanent infertility in a man or woman.** A pregnant woman with an untreated infection can pass it to the baby's eyes during birth, risking blindness — this is the real reason newborn eye antibiotic ointment is standard practice (see Where There Is No Doctor's own newborn care guidance).

**Treatment:** real antibiotics are required — gonorrhea has become resistant to penicillin in many areas, so current local medical guidance on which antibiotic actually works is essential, not optional. **Every sexual partner needs treatment too, even if they show no signs** — otherwise the infection just passes back and forth. **A real caution:** someone with gonorrhea or chlamydia may also have syphilis without knowing it; treating only the first infection can mask syphilis's early symptoms without actually curing it.

## Syphilis

**First sign:** a usually-painless sore (chancre) appearing 2-5 weeks after exposure, typically on the genitals — it heals on its own within days, which can create a false impression that nothing's wrong. **The infection keeps spreading through the body even after the sore disappears.**

**Weeks to months later:** a second stage can bring sore throat, mild fever, mouth sores, swollen joints, or various skin rashes — these also resolve on their own, again creating a false "I'm fine now" impression. **Untreated, syphilis can eventually cause heart disease, paralysis, and serious neurological/mental effects.**

**If any unusual rash or sore shows up weeks after a genital sore or pimple — treat this as a real possibility of syphilis and get medical advice.**

**Treatment requires real antibiotic dosing** (benzathine penicillin injection is standard; tetracycline or erythromycin for those allergic) — the exact regimen depends on how long the infection has likely been present, and needs real medical guidance to get right. **Every sexual partner of a confirmed case should also be treated.**

## Detailed Version — the pattern worth remembering across all of these

**Absence of symptoms does not mean absence of infection, and resolution of symptoms does not mean the infection is gone.** This is the single most important, counter-intuitive fact about all three of these conditions — each one can go quiet while still actively present and still contagious, which is exactly why partner treatment (regardless of whether the partner has symptoms) is treated as essential, not optional, throughout this whole topic.
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
