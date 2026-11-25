#!/usr/bin/env python3
"""Seeds 1 real page from Where There Is No Doctor's Chapter 1 (Home
Cures and Popular Beliefs) -- mined from the real text layer already
extracted in this session. This is the book's own meta-commentary on
information reliability: when belief in a remedy genuinely helps (and
why), versus when a remedy has no real physical effect regardless of
belief -- directly reinforcing the Snakebite page's own "no home
remedy helps" point with the book's real supporting example.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_home_remedies_belief.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"

PAGE = {
    "title": "Home Remedies — Belief, Placebo & What Actually Works",
    "section": "reference",
    "tags": ["home-remedies", "critical-thinking"],
    "risk_level": "moderate",
    "body_markdown": """## Quick Version

**Some home remedies have a real, direct physical effect. Others only seem to work because the person believes in them — and that belief effect is genuinely real, just limited to certain kinds of problems.**

**Belief-driven healing works best for:** conditions that are partly psychological to begin with — anxiety, stress-related aches, hysterical fear, asthma/hiccups/indigestion/migraines made worse by worry, even some warts. For these, feeling cared for and believing you'll improve can measurably help, regardless of what the "remedy" actually was.

**Belief does NOT change a physical poison, infection, or injury — no matter how strongly someone believes it will.** The book's own real example: many different cultures have traditional snakebite remedies (specific leaves, biting the snake, tobacco, animal parts) — **none of them has any real effect on snake venom.** If someone survived using one, they were very likely bitten by a non-venomous snake, not saved by the remedy. Belief can genuinely help here too, but only indirectly: feeling calmer slows the heart rate, which slows how fast venom spreads — not because the remedy did anything to the venom itself. **This is exactly why modern antivenom, prepared in advance, matters more than any traditional remedy for a real venomous bite** (see Snakebite).

**Belief can also make someone genuinely sick, with no real physical cause at all** — fear itself can produce real symptoms. The flip side: something with literally no medical effect (the book's own example: an injection of plain distilled water) can genuinely resolve those symptoms, purely because the person trusted it.

## Detailed Version

**The real, honest point behind all of this:** understanding which category a problem falls into changes what actually helps. For a stress-related or fear-driven symptom, compassion and reassurance are a genuinely legitimate treatment, not "doing nothing." For a real physical injury, infection, or poisoning, belief alone changes nothing about the underlying physical process — and leaning on a remedy's placebo effect instead of real treatment (real antivenom, real antibiotics, real wound care) is where good intentions turn genuinely dangerous.

**On witchcraft, hexes, and the "evil eye":** believing strongly enough that you've been cursed can produce real illness — but the cause is the fear itself, not any actual power the supposed curse holds. Real physical illnesses (including frightening ones like tumors or liver disease) are sometimes mistaken for a curse specifically because they're scary and poorly understood — but their causes are real and physical, and treating them requires real medical care, not addressing the belief about their cause.
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
