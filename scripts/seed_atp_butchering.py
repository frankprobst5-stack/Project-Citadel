#!/usr/bin/env python3
"""Seeds 2 more real pages from ATP 3-50.21 (Survival), Chapter 4
(Food) -- mined from the real text layer already extracted in this
session (/tmp/atp_survival.txt, pages 4-29 through 4-32). Real,
more-detailed technique than the USMC game-processing content already
in this wiki, plus 2 genuinely new real items (a light-trap insect-
catching technique and bird-specific dressing notes).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_atp_butchering.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
ATP_SURVIVAL_PDF_URL = "/files/pdfs/Military Manuals/ATP-3-50.21-Survival.pdf"

PAGES = [
    {
        "title": "Big Game Skinning — Real Field Technique",
        "section": "reference",
        "tags": ["field-dressing", "butchering", "food-procurement"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**A more detailed real technique than a basic skinning overview: the actual finger-guided knife method that separates skin from the membrane without puncturing the entrails underneath.**

## The Real "Big Game" Method

1. **Turn the animal onto its back.** With a sharp knife, cut through the skin in a straight line from the tailbone to a point under the neck, passing around the anus.
2. **⚠️ The real finger-guard technique:** carefully press the skin open until you can insert your first two fingers between the skin and the thin membrane covering the entrails. Once your fingers can move forward, place the knife blade between them, **blade facing up, held firmly** — then advance your fingers (palm up) while the blade follows right behind them, cutting the skin but **not** the membrane underneath.
3. **⚠️ On a male animal: cut parallel to the penis, never touching it** — accidentally cutting the urine tube makes a genuinely messy job and contaminates the meat.
4. **If the gall or urine bladder breaks anyway, washing the meat helps** — otherwise, it's actually better NOT to wash it, letting it form a protective glaze instead.
5. **Once you reach the ribs, the skin grips tighter and the finger-guard method stops working** — from here, alternately force the knife under the skin and lift it to finish the cut; extreme care is no longer needed at this point.
6. **Side cuts:** from the central cut, cut up the inside of each leg to the knee/hock joints; cut around the front legs just above the knees, and the hind legs above the hocks; finish with a cut around the neck, behind the ears.
7. **Skin down one side as far as possible, then roll the carcass to skin the back** — spread the loosened skin out to keep meat off the ground, then flip to the skinned side and repeat on the other side.
8. **Opening the entrail membrane:** use the same finger-guard technique — fingers of one hand guard the knife while separating intestines from the membrane. The thin membrane along the ribs/sides can simply be cut away for a clearer view.
9. **⚠️ Avoid cutting the intestines or bladder.** Where the large intestine passes through the pelvis, carefully separate the tube from the surrounding bone. **Tie a knot in the bladder tube before removing it** — this prevents urine from leaking onto the meat.
10. Once gutting is complete, hanging the carcass is often worthwhile.

**⚠️ Real timing note: if the animal is still warm, gut it BEFORE skinning it** — the order matters for a freshly killed animal.

## A Real Bonus — Saving the Fat

**A well-conditioned animal's intestines are often covered in a lace-like layer of fat** — this can be lifted off and dried on nearby bushes for later use, rather than discarded with the rest of the entrails.

## Detailed Version

**The real, defining skill in this entire technique is the finger-guard method itself: using your own fingers as a physical barrier between the blade and the membrane means the knife can keep cutting skin confidently without the real risk of puncturing the gut and contaminating the meat** — a meaningfully more precise approach than cutting by eye alone.
""",
    },
    {
        "title": "Dressing Birds & a Real Light-Trap Technique for Insects",
        "section": "reference",
        "tags": ["food-procurement", "birds", "insects"],
        "risk_level": "moderate",
        "body_markdown": """## Dressing Birds — Real Technique

**Loosen feathers by dipping the bird in boiling water first, making plucking easier** (skinning instead removes some real nutritional value, so plucking is generally preferable). Open the body cavity and remove the entrails, **saving the heart and liver.** **Most usable meat comes from the breast**; larger birds also yield a fair amount from the legs/thighs. Cut off the feet, then cut between joints to separate the skeleton — **a bird's fragile structure means most of this can be done by hand, no tools required.**

**⚠️ Wash hands and tools after handling raw bird meat** to avoid spreading bacteria. **Leave meat on the bone for cooking.** **Most birds should be cooked with skin on — the real exception is sea birds, whose oily skin should be removed first for better taste.** **⚠️ Carrion-eating birds (vultures and similar) must be boiled at least 20 minutes to kill parasites before any further cooking.**

**Real cooking/preservation:** boiling, baking, roasting, or frying all work — **cook bird meat fully to eliminate food-borne illness risk.** Near the ocean, a saltwater bath preserves it (rinse the salt off before cooking).

## ⚠️ A Real, Clever Light-Trap Technique for Flying Insects

**Insects are genuinely excellent nutrition — some provide 65-80% protein by composition versus roughly 20% for beef.** (Real example: praying mantis runs about 58% protein, 12% fat, 3% ash, plus vitamin B complex and vitamin A.) **The real catch: insects have to be gathered in large numbers to match the protein of one rabbit or similar-sized meat source** — individual insects are nutrient-dense but small.

**Real light-trap method for flying insects:** set up a light source at night, place a piece of material in front of it, and position a vessel of water below. **Insects drawn to the light fly into the material, and some fall into the water below, where they stay for easy collection.**

**Real additional foraging locations:** rotting logs (ants, termites, beetles, grubs), nests on or in the ground, open grassy fields (insects are easier to spot), and under stones/boards lying on the ground. **Worms** (an excellent protein source) are found in humus soil, in grass-clump root balls, or on the surface after rain — **purge them in clean potable water for 15 minutes before eating raw**, letting them naturally clean out their own gut contents first.

**Real preparation:** remove any stinger, plus legs/wings/head, before eating. **Hard-shelled insects carry real parasite risk and should be fully cooked.** **Live storage is itself a real preservation method** for insects — keeping them alive until needed, alongside the other preservation methods already covered (see Preserving Meat — Botulism (TOM) & Real Techniques).

## Detailed Version

**The real, clever engineering behind the light-trap technique: it converts a passive resource (ambient insect activity at night) into an actively harvested one with almost no ongoing effort** — once set up, it works continuously while you do something else, the same real principle behind a fishing set line (see Fishing Set Lines — Catching Fish While You Work) applied to a completely different food source.
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
                "source_url": ATP_SURVIVAL_PDF_URL,
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
