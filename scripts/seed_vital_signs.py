#!/usr/bin/env python3
"""Seeds 1 more real page from Where There Is No Doctor's Chapter 3
(How to Examine a Sick Person): Taking Vital Signs -- temperature,
pulse, and breathing rate, with real normal-range numbers by age.
Mined from the real text layer already extracted in this session.

This page ties together numbers already cited in several earlier
pages (Fever, Shock, Pneumonia, Asthma) by giving the actual baseline
normal ranges those pages assume the reader can check against.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_vital_signs.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"

PAGE = {
    "title": "Taking Vital Signs — Temperature, Pulse & Breathing",
    "section": "reference",
    "tags": ["vital-signs", "examination"],
    "risk_level": "low",
    "body_markdown": """## Quick Version

**Normal resting pulse (beats/minute):** adults 60-80 · children 80-100 · babies 100-140. Pulse rises roughly 20 beats/minute per degree (°C) of fever — a fast pulse alone isn't alarming if there's a fever to explain it. **A weak, rapid pulse can mean shock. A very rapid, very slow, or irregular pulse can mean a real heart problem.**

**Normal breathing rate (breaths/minute):** adults/older children 12-20 · younger children up to 30 · babies up to 40. **More than 30 shallow breaths/minute in an adult, or 60/minute in a newborn, usually means pneumonia.** Count for a full minute while the person is calm — not while crying or right after.

**Taking a temperature:**
1. Clean the thermometer, shake it down below 36°C/96.8°F.
2. Place under the tongue (mouth closed), in the armpit (if biting risk), or in the anus for a small child (lubricated first).
3. Leave 3-4 minutes, then read. **Armpit readings run slightly lower than oral; rectal readings run slightly higher** — know which method you used before comparing to a "normal" number.
4. Clean the thermometer after use.

**In a newborn, an unusually high OR unusually low temperature (below 36°C/96.8°F) can both signal a serious infection** — don't assume only high fever matters in a baby.

## Detailed Version

**What to actually listen for, beyond just counting:** a whistling/wheezing sound on breathing out suggests asthma. A gurgling or snoring sound with difficulty breathing in an unconscious person suggests something (the tongue, mucus, an object) is blocking the airway. **Visible "sucking in" of the skin between the ribs or at the base of the neck on each breath in** is a real sign that air isn't moving freely — worth checking for directly, not just listening.

**Write vital signs down, repeated 4 times a day, for anyone seriously ill** — a single reading tells you less than a trend. A pulse or breathing rate that's climbing over several checks is a real, objective warning sign even before the person "looks" worse.
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
