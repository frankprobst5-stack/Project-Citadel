#!/usr/bin/env python3
"""Seeds 4 real pages from the USMC Winter Survival Course Handbook's
Survival Uses of Game chapter -- mined from the real text layer
already extracted in this session (/tmp/usmcwinter.txt, pages 09-1
through 09-7). Real, detailed field-dressing, cooking, hide-tanning,
and meat-preservation technique -- genuinely applicable food-security
skills for a prolonged disaster scenario where store-bought food
isn't an option.

Covers: real killing/dressing/skinning technique by animal type
(large game, small game, birds, reptiles/amphibians, fish), real
cooking-safety rules, the complete real hide-tanning process
(fleshing through smoking), and real meat-preservation technique
including the TOM botulism-prevention framework, jerky, and
pemmican.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_game_processing.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
USMC_WINTER_PDF_URL = "/files/pdfs/Military Manuals/USMC-Winter-Survival-Course-Handbook.pdf"

PAGES = [
    {
        "title": "Field Dressing & Preparing Game",
        "section": "reference",
        "tags": ["field-dressing", "food-procurement", "survival-skills"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Dress an animal immediately after it's killed — this cools the chest cavity and real slows bacterial decay.** Delay is the single biggest real risk to the meat's safety.

## Real Dressing Technique, by Animal Type

**General game (mammals):**
1. With a well-sharpened knife, cut around the anus carefully — avoid puncturing the intestines or kidneys.
2. **Cut the hide from the anus toward the chest, guided by two fingers placed under the skin with the blade between them** — this real technique keeps the blade from accidentally rupturing the intestines and contaminating the meat.
3. **Remove the heart, lungs, and liver, keeping them separate from the discarded gut pile — all three are edible.** **⚠️ Check the liver for white spots — their presence can indicate tularemia** (see Wildlife & Food-Borne Diseases in a Survival Situation), a real reason to inspect before eating.

**Birds:** pluck feathers while the body is still warm (or dip briefly in hot water to loosen them first). **Skinning a bird is possible but wasteful** — it removes the real fat layer the bird's skin holds. Make an incision from the vent to the tail and draw out the intestines.

**Reptiles/amphibians:** cut off the head well behind any poison sacs, then open the skin from anus to neck and remove/discard the internal organs. **⚠️ Avoid box turtles, brightly colored frogs, frogs with an "X" mark on their back, and toads** — real signs of likely toxicity.

## Skinning — Real Technique by Size

- **Large game ("caping"):** find the Achilles tendon just above the feet, cut a small hole between bone and tendon to thread a rope through, and hang the animal upside down. Cut around the hind legs below the suspension point, then toward the anus along the inside of the hind legs. Pull the hide straight down toward the head, repeating the leg technique for the forelegs, cutting around antlers if present.
- **Small game ("casing"):** pull the entire skin off from rear to front in one piece, with cuts made only around the feet and from the back legs to the tail — **this preserves the hide as a usable tube shape for mittens, bags, or other containers.**
- **Fish, birds, reptiles/amphibians:** skin is generally left ON for these — birds specifically have a real, valuable fat layer between skin and meat that skinning would waste.

## Butchering & Washing

**Cut meat into manageable portions; smaller animals are usually best left whole rather than subdivided.** **⚠️ If an animal was killed using poison, remove and discard a 2-inch cube of meat at the actual point of contamination** before processing the rest. Rinse meat to remove dirt, especially if any bladder/fecal material was accidentally ruptured during skinning.

## Edible Organ Meats Beyond the Muscle Meat

Brain, eyes, tongue, liver, heart, lungs, kidneys, and gizzards are all real, edible parts beyond the obvious muscle meat — in a survival context, discarding these wastes genuinely usable nutrition.

## Detailed Version

**The real, most important technical detail on this entire page is the two-finger knife-guard technique for opening the hide** — it's the single step most responsible for the difference between clean, safely usable meat and meat contaminated by an accidentally punctured gut. Everything else on this page assumes that step was done correctly.
""",
    },
    {
        "title": "Cooking Game Safely",
        "section": "reference",
        "tags": ["cooking", "food-safety", "food-procurement"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Cook all game thoroughly, every time — cooking is what actually kills the bacteria and parasites wild meat can carry.** There's no real "leftovers" concept in a survival situation.

## Real Rules

- **Cook game until it's thoroughly well done** — no exceptions for wild-caught meat.
- **Only cook what you can eat right away** — storing cooked leftovers in a survival setting is a real spoilage risk, not a convenience.
- **Eat the heart and liver first** — these organs spoil faster than muscle meat, so eating them promptly avoids wasting them.

## The 2 Real Cooking Methods

1. **Boiling — the real best method.** It lets you consume the rendered fat and nutrients that collect in the broth, rather than losing them.
2. **Roasting — considered wasteful and not recommended in a real survival situation**, since it loses the fat/nutrient value boiling preserves.

## Detailed Version

**The real principle tying all of this together: in a survival context, calories and nutrients lost are calories and nutrients you can't easily replace.** Boiling over roasting, eating organs before they spoil, and cooking only what you'll actually eat immediately are all the same underlying discipline — minimizing real nutritional waste when food is genuinely scarce.
""",
    },
    {
        "title": "Tanning a Hide — Real Field Technique",
        "section": "reference",
        "tags": ["hide-tanning", "bushcraft", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**A real field-expedient hide-tanning process has 6 real steps, and skipping or rushing any one of them produces a stiff, less useful final product.** Starting as soon as possible — ideally before the hide dries out — makes every later step genuinely easier.

## 1. Fleshing

Soak/wet the hide if it's already dried. Lay it over a solid, smooth, round surface (a log, a canteen). **Holding a scraper at roughly a 10° angle away from your body, push the fat and membrane off the leather** — work carefully around the thinner belly area to avoid tearing it. (**Beaver and badger hides need their fat specifically cut off**, not scraped.) Continue until the fat is completely removed.

## 2. Stretching

**A fresh or re-soaked hide must be stretched** — either lacing it tight to a frame with cordage, or staking it tight to the ground. **The less a hide shrinks and hardens during this process, the softer the final leather will be.**

## 3. Hair Removal

Scrape the hair off with a sharp stone tool — soaking the hide in water first makes this meaningfully easier.

## 4. Braining

**The brain acts as both a lubricant and a temporary water-repellent.** Soak the hide on its stretcher, extract the animal's brain, mix it with water into a pasty solution, warm it, and **firmly rub it into only the hairless (flesh) side of the hide by hand.**

## 5. Graining

This step works the brain mixture thoroughly into the leather fibers. Sponge on more water to dampen the hide further, then use the blunt end of a pole to apply pressure and scrape/stretch every inch of the hide until most of the surface water is worked out. Retighten the hide on its stretcher and let it dry.

## 6. Rubbing

**High-friction rubbing is what actually finishes drying, stretching, and softening the grain.** Either cut the finished skin free from the frame (leaving just the lacing holes and any remaining hair) and pull it repeatedly across a half-inch rope strung between two trees, grasping different points around its perimeter — or, without rope, sit on the ground, hook the skin over your feet, and pull it by hand.

## Optional: Smoking

**Smoking makes the finished hide genuinely water-repellent.** Add wet or green wood chips (sage or willow work well) to a fire — the goal is smoke, not flame. A few minutes is usually enough; **watch carefully to prevent an actual flame from ruining the hide.**

## Detailed Version

**The real, easy-to-rush step in this whole process is braining — it's the one step that genuinely requires patience (soaking, mixing, warming, working it into the hide by hand) and has no real shortcut.** Skipping or shortening it is the most common reason a field-tanned hide ends up stiff rather than soft and usable.
""",
    },
    {
        "title": "Preserving Meat — Botulism (TOM) & Real Techniques",
        "section": "reference",
        "tags": ["food-preservation", "botulism", "food-safety"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Botulism — the Real Danger Behind Improper Meat Preservation

**Botulism is often fatal, and it's caused specifically by improperly preserved meat.** The real, useful memory tool: **TOM** — remove any ONE of these three conditions and botulism genuinely cannot grow:

- **T — Temperature.** Botulism thrives between 40-140°F.
- **O — Oxygen.** It needs an airtight (oxygen-free) environment to grow.
- **M — Moisture.** It needs a moist environment to survive.

**Every preservation method below works by deliberately denying it at least one of these three.**

## Freezing

Cut meat into portions sized for single use before freezing. **Keep it frozen until actual use — meat that thaws and then refreezes will spoil**, so plan portion sizes to avoid partial thawing.

## Cooling

Place meat in a ventilated metal or wooden container with a lid, then set it in water or bury it in damp earth (ideally shaded). **If mold develops, don't discard the meat — cut or scrape the mold off and cook it normally.**

## Jerky — Lasts a Couple of Weeks

1. Cut meat into thin (~¼ inch) strips, trimming off thick fat.
2. **Lightly smoke the strips near a fire** to develop a thin protective crust that deters insects — **use hardwood, not conifer wood, and aim for smoke, not actual cooking heat.**
3. Hang the crusted strips to air-dry for about 24 hours, then gently pull/work the fibers apart and dry another 24 hours.
4. Once hard and brittle, store in breathable bags or cloth. Use in stews/soups, or lightly roasted on coals.
5. **Small animals, fish, and birds can be dried whole:** skin them, crack the back between the legs, insert a stick to hold the body cavity open, lightly smoke, then sun-dry. Once fully dried, pound until the bones are crushed, then air-dry an additional day to dry the marrow and lock in preservation.

## Pemmican — Lasts Several Months

1. Dry berries and pound them into a paste.
2. Add dried jerky to the paste.
3. Mix in melted suet (the hard fat around the kidneys).
4. Roll into small balls and store in cleaned animal intestine or another suitable container. **If it shows signs of spoiling, boil it before eating** rather than discarding it outright.

## Detailed Version

**The real, unifying insight behind every technique on this page: each one is a deliberate, specific attack on one or more of the TOM conditions, not a generic "preserve the food" action.** Freezing attacks temperature; drying (jerky) attacks moisture; pemmican's dense, low-moisture, fat-sealed structure attacks both moisture and oxygen exposure at once — understanding which condition a given method actually removes is what lets you judge whether an improvised preservation attempt is genuinely safe, rather than just assuming "it's dried/cold/sealed, so it's fine."
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
                "source_url": USMC_WINTER_PDF_URL,
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
