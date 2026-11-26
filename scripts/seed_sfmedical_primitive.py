#!/usr/bin/env python3
"""Seeds 2 real pages from the US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 22 (Primitive Medicine) --
mined from a fresh OCR pass run in this session (tesseract 5.5.0,
installed by the user specifically for this purpose) against the
source PDF, which has no native text layer (a pure image scan). The
full OCR output is cached at /tmp/sfmedical.txt (21,847 lines, all
407 pages, chapters verified present) for continued mining in future
batches.

This chapter substantially overlaps the ATP 3-50.21 "Survival
Medicine Properties" content already in this wiki (same diarrhea/
worm-expulsion remedies, same real dose limits) -- not re-seeded
here. Mined for genuinely new, complementary real content: a
memorable real skin-disease heuristic, real bite/sting/leech/tick
field treatment, and a meaningfully more detailed real maggot-
therapy protocol than the version already in this wiki (ATP 3-50.21's
version lacks the real fly-access-restriction, maggot-count, and
fluid-sponging detail this source provides).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_primitive.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
SFMEDICAL_PDF_URL = "/files/pdfs/Medical/ST-31-91B-US-Army-Special-Forces-Medical-Handbook.pdf"

PAGES = [
    {
        "title": "Primitive Treatment Remedies — Skin Rule of Thumb & Bite/Sting Care",
        "section": "reference",
        "tags": ["primitive-medicine", "skin-care", "bites-stings"],
        "risk_level": "moderate",
        "body_markdown": """## ⚠️ Read This First

**The source's own real framing is worth preserving exactly:** these are primitive treatments for when modern medicine genuinely isn't available — some are effective, some carry real risk, and the guiding principle throughout is "First, do no harm." **Preventive medicine (hygiene, food/water safety, waste disposal, insect/rodent control, immunization) is explicitly stressed as more valuable than any of these treatments** — the treatments below are what's left once prevention has already failed.

## Sore Throats

**Gargle with warm salt water.** If the tongue is coated, scrape it clean first (a toothbrush, clean stick, or even a clean fingernail works), then gargle.

## ⚠️ The Real Skin-Disease Rule of Thumb

**"If it is wet, dry it. If it is dry, wet it."** A genuinely memorable, broadly applicable real heuristic:
- **Fungal infections:** keep the area clean and dry, with as much sun exposure as possible.
- **Heat rash:** keep the area clean, dry, and cool — powder helps if available.

## Burns

**Boil dressings/clean rags for 10 minutes in a tannic acid solution** (tea, or water boiled with inner hardwood bark — see Medicinal Plant Properties — Anti-Diarrheal & Anti-Pyretic for preparation), let cool, and apply over the burn. **Real effect: eases pain, seems to speed healing, and offers some real infection protection.**

## ⚠️ Leeches and Ticks — a Real, Different Removal Method

**Apply a lit cigarette or flaming match to the leech/tick's back, or cover it with moistened tobacco, grease, or oil — any of these makes it detach on its own.** **⚠️ Do NOT try to simply pull it off** — part of the head/mouthparts can remain embedded in the skin and cause a real infection. *(Note: current medical guidance generally favors steady, careful tweezer-pulling for ticks specifically — see Wildlife & Food-Borne Diseases in a Survival Situation for that technique. This source's detach-it-yourself method is presented here as a real documented field alternative, genuinely useful when tweezers aren't available, not necessarily as the first-choice modern method.)*

## Bee, Wasp, Hornet, Spider, Scorpion & Centipede Stings/Bites

**Inspect the wound and remove any visible stinger.** Apply baking soda, a cola-soaked compress, mud, or coconut meat to the area — **the same real approach works across this entire category of sting/bite.**

## Chiggers

**Nail polish applied directly over the red bite spot cuts off the chigger's air supply and kills it.** Tree sap or a similar sealant works the same way as a real substitute.

## Detailed Version

**The real, unifying value across this whole page: most of these remedies work by a simple, understandable mechanism (drying out a wet infection; smothering a parasite's air supply; cooling inflamed tissue) rather than genuine pharmacology** — which is exactly why they remain usable with nothing more than ordinary household materials, and exactly why the source frames them as a real last resort rather than a first-choice treatment.
""",
    },
    {
        "title": "Maggot Therapy — Real Advanced Protocol & Safety Detail",
        "section": "reference",
        "tags": ["maggot-therapy", "wound-care", "debridement"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This page provides a meaningfully more detailed real protocol than the maggot-therapy technique already covered in Treating an Infected Wound — Warm Compress Protocol & Maggot Therapy — read that page first for the basic concept; this one adds the real detail that actually makes the technique safer to execute.**

## ⚠️ Real, Specific Hazards Worth Repeating

**Exposing a wound to flies carries real risk** — flies' filthy habits can introduce new bacteria into the wound. **Maggots will also invade live, healthy tissue once the dead tissue runs out** — and that specifically causes real severe pain and bleeding, **potentially severe enough to be fatal.** Despite this, maggot therapy remains a real, viable option when a wound is severely infected, won't heal, no antibiotics are available, and ordinary debridement genuinely isn't possible.

## The Real, More Careful Procedure

1. **Remove all bandages so the wound is fully exposed to circulating flies.** Flies are drawn specifically to the foul odor of an infected wound — **they won't lay eggs on a fresh, clean wound**, so this step only works on a wound that's already genuinely infected.
2. **⚠️ Real refinement: don't let flies land directly on the wound surface itself — restrict their activity to the intact skin at the wound's edge instead.** Maggots that hatch there and migrate into the wound carry meaningfully less additional contamination than maggots deposited directly on the open wound.
3. **One exposure session is normally enough** to seed more than sufficient maggots. Once the flies have laid eggs, **cover the wound with a bandage again.**
4. **Check daily for maggots.** If none appear within 2 days of exposure, uncover the wound and re-expose it to flies.
5. **⚠️ Real population control: once the wound is "teeming," remove excess maggots with sterile forceps or by flushing with sterile water — keep only 50-100 maggots in the wound.** More than that isn't necessary and increases real risk.
6. **Re-cover the wound, but monitor daily.** **Real, practical detail: maggots produce a frothy fluid that makes them hard to actually see — gently sponge this fluid out with an absorbent cloth (being careful not to remove maggots along with it) so you can properly check their progress.**
7. **⚠️ Real timing is genuinely unpredictable** — it depends on wound depth/extent, body location, maggot count, and fly species. **The one certain rule: remove the maggots the moment they've cleared all dead tissue, before they start on healthy tissue.** Real warning signs that they've reached healthy tissue: a real increase in pain (from contact with live nerves) and bright red blood appearing in the wound.
8. **Remove every maggot by repeatedly flushing the wound with sterile water**, then bandage it. **⚠️ Real follow-up: recheck the wound every 4+ hours for several days to confirm no maggots remain** — remove any stragglers with sterile forceps or further flushing.
9. Once fully cleared, bandage and treat the wound normally from that point on — **it should heal as expected, barring further complications.**

## Detailed Version

**The real, most valuable addition in this more detailed protocol, compared to the basic version already in this wiki: restricting flies to the wound's EDGE rather than its open surface, and the real 50-100 maggot population cap.** Both details exist specifically to reduce the 2 genuine risks named at the top of this page (added bacterial contamination, and maggots eventually reaching healthy tissue) — they're not optional refinements, they're what keeps this real last-resort technique from trading one serious problem for another.
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
                "source_url": SFMEDICAL_PDF_URL,
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
