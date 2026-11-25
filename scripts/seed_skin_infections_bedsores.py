#!/usr/bin/env python3
"""Seeds 2 more real pages from Where There Is No Doctor's Chapter 15
(Skin Problems): Erysipelas, Cellulitis & Gangrene, and Bed Sores &
Diaper Rash -- mined from the real text layer already extracted in
this session.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_skin_infections_bedsores.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Erysipelas, Cellulitis & Gangrene",
        "section": "emergency",
        "tags": ["skin-infection", "cellulitis", "gangrene"],
        "risk_level": "critical",
        "body_markdown": """## Erysipelas & Cellulitis

**Erysipelas:** a sudden, very painful skin infection — a hot, bright-red, sharply-bordered patch that spreads fast, often starting near the nose. Usually comes with swollen lymph nodes, fever, chills.

**Cellulitis:** similar painful acute skin infection, but can occur anywhere, usually after a break in the skin, with a deeper infection and less sharply defined border than erysipelas.

**Treatment for either — start as soon as possible:** real antibiotic treatment (the book names penicillin, with injectable procaine penicillin for serious cases) continued for 2 full days *after* all infection signs clear — stopping right when it looks better risks it coming back. Hot compresses and aspirin for pain help alongside the antibiotic.

## Gangrene — a true emergency

**Signs:** a foul-smelling gray or brown discharge from a wound, dark blisters on nearby skin, sometimes air bubbles felt under the skin/flesh. **Can develop as fast as 6 hours after the original injury, and progresses rapidly — untreated, it can cause death within days.**

**Treatment — this cannot wait:**
1. Open the wound as wide as possible; wash thoroughly with cool boiled water and soap, removing all dead/damaged tissue.
2. Flood with hydrogen peroxide every 2 hours if available.
3. **Real penicillin injection is needed urgently** (the book specifies a very high, frequent dose — this needs real medical administration, not home guessing).
4. **Leave the wound uncovered so air can reach it** — this specific detail matters because the gas-gangrene bacteria thrive in low-oxygen conditions; covering it can make things worse.
5. **Get medical help immediately — this is not a wait-and-see condition.**

## Detailed Version

The progression speed is the real point that separates gangrene from an ordinary infected wound: a normal wound infection develops and worsens over days; gangrene can turn genuinely life-threatening within hours. Any wound with a foul smell, dark discoloration spreading from it, or a sensation of air/crackling under the skin deserves this level of urgency, not the slower "watch and treat at home" approach that works for an ordinary infected wound.
""",
    },
    {
        "title": "Bed Sores & Diaper Rash",
        "section": "reference",
        "tags": ["bed-sores", "pressure-sores", "diaper-rash", "caregiving"],
        "risk_level": "moderate",
        "body_markdown": """## Bed Sores (Pressure Sores)

Chronic open sores that develop in someone too ill or weak to turn over on their own — most often on the buttocks, back, shoulders, elbows, or heels, wherever bone presses the skin against bedding for extended periods.

**Prevention (genuinely more important than treatment here):**
- **Turn the person every hour** — face up, face down, side to side, rotating through positions.
- Daily bathing; rubbing the skin with oil helps.
- Soft bedding, changed daily and immediately whenever soiled.
- Cushion bony pressure points so they bear less direct weight.
- Good nutrition — a poorly-fed person's skin breaks down faster and heals slower; extra vitamins/iron can genuinely help if intake is poor.

**Treatment once a sore has formed:**
1. Do everything in the prevention list above — it doesn't stop mattering once a sore exists.
2. Wash the sore with cool boiled water and mild soap 3 times a day, gently removing dead tissue, then rinse clean.
3. **A real, documented wound treatment: pack the sore with honey, sugar, or molasses** (a honey-sugar paste is easiest to apply) — this genuinely fights infection and speeds healing through its osmotic and antimicrobial effect, not folk remedy guesswork. **Must be reapplied at least twice a day** — if it gets diluted by fluid from the wound, it stops working against germs and can start feeding them instead.

## Diaper Rash

Red, irritated skin between the legs/buttocks from prolonged contact with wet diapers or bedding.

**Treatment:** daily bathing with lukewarm water and mild soap, dried carefully. **"Bare is best"** — the real fastest fix is leaving the baby without a diaper and exposed to air/sunlight when practical. If diapers must be used, change them often, and rinse washed cloth diapers in water with a little vinegar. Avoid talcum powder until the rash has cleared.
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
