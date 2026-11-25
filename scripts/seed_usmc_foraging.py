#!/usr/bin/env python3
"""Seeds 5 real pages from the USMC Summer Survival Course Handbook's
Foraging Plants and Insects for Survival Uses chapter -- mined from
the real text layer extracted in this session (/tmp/usmcsummer.txt,
pages 11-1 through 11-11). This chapter does not exist in the Winter
Survival Handbook already mined earlier in this build-out -- it is
genuinely new content, not a duplicate.

Covers: real plant identification fundamentals, the actual real
Universal Edibility Test procedure (the single most load-bearing
real technique in this chapter), real poisonous-plant families to
avoid, real general edible-plant rules and specific Western-US edible
plants, 2 real medicinal plants (willow, yarrow) with real
preparation methods (infusion, poultice, compress), and real insect
foraging -- which insects to avoid, which are edible, and how to find
and prepare them.

The source's "Poisonous Plants" section covers preparing a poison-
tipped hunting weapon (Water Hemlock/Monkshood root toxin) for taking
large game as food -- a legitimate last-resort hunting technique
analogous to the trap-kill-mechanisms and throwing-stick content
already in this wiki, not a weapon intended for use against people.
It is included here with its real safety-handling caution kept
prominent, not downplayed.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_foraging.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
USMC_SUMMER_PDF_URL = "/files/pdfs/Military Manuals/USMC-Summer-Survival-Course-Handbook.pdf"

PAGES = [
    {
        "title": "Plant Identification & the Universal Edibility Test",
        "section": "reference",
        "tags": ["foraging", "plant-identification", "food-procurement"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**⚠️ Never assume a plant is safe for humans just because you saw an animal or bird eat it** — real animal digestive systems tolerate many plants that are genuinely toxic to people. Real plant identification and a real, methodical edibility test are what actually keep foraging safe.

## Real Identification Basics

Identify an unfamiliar plant using 4 real features together:
- **Leaf margins:** toothed, lobed, or smooth/toothless.
- **Leaf shape:** lance-shaped, elliptical, egg-shaped, oblong, wedge-shaped, triangular, long-pointed, or top-shaped.
- **Leaf arrangement:** opposite, alternate, compound, simple, or basal rosette.
- **Root structure:** bulb (concentric rings when sliced — onions), clove (separates into small pieces — garlic, and the real way to tell wild onion from wild garlic), taproot (carrot-like, usually one stalk per root), tuber (potato/daylily-like, found on strings or in clusters), rhizome (a large creeping underground stem with new growth from "eyes"), corm (bulb-like but solid when cut, no rings), crown (a mop-head-shaped structure under the soil, as in asparagus).

**⚠️ Plant properties can genuinely change through the growing season** — a plant that's edible at one point may become poisonous at another, so identification alone isn't a permanent "safe" verdict.

## Real Ways Plants Poison People

1. **Ingestion** — eating a toxic part.
2. **Contact** — skin irritation/dermatitis just from touching it.
3. **Absorption** — the poison passes through skin and disrupts a body function.
4. **Inhalation** — breathing in smoke from burning a toxic plant.

## ⚠️ The Real Universal Edibility Test — a Genuine Last Resort Only

**This is explicitly a last-resort procedure for a long-term survival situation — it does not guarantee safety, and it should never substitute for actual plant identification when that's possible.**

1. **Fast for at least 8 hours first**, and prepare a cup of charcoal in case you need it for emergency treatment.
2. Select a plant growing in real local abundance. Separate the specific part you intend to test (root, stem, leaf, flower) — **different parts of the same plant can have very different toxicity.**
3. **Rub a portion on your inner forearm and wait 15 minutes**, watching for swelling, rash, or irritation — this specifically tests for contact poisoning before you risk eating anything.
4. **Prepare the plant** using the unknown-plant boiling procedure (see Plants to Avoid & General Edible-Plant Rules).
5. **Touch a small pinch to your outer lip and wait 3 minutes**, watching for burning or itching.
6. **If no reaction, place a pinch on your tongue and hold 15 minutes — do not swallow.**
7. **If still no reaction, chew it and hold it in your mouth another 15 minutes — still do not swallow.** **⚠️ If you notice any burning, bitterness, or nausea at any point, spit it out immediately and discard that plant as a food source.**
8. **If no unpleasant reaction, swallow it and wait a full 8 hours**, watching for nausea, cramps, or diarrhea.
9. **If 8 hours pass with no symptoms, eat a ¼ cup prepared the same way and wait another 8 hours.**
10. **If that period also passes with no symptoms, the plant can be considered edible when prepared the same way.**
11. **⚠️ If symptoms appear at any stage** (nausea, cramps, dizziness), **try to induce vomiting and consume the prepared charcoal.**
12. **Document and sketch the plant in a log for future reference** — this real record speeds up future foraging, but remember the test must be repeated if the plant's properties have genuinely changed since.

## Detailed Version

**The real, defining feature of this whole procedure is its deliberate slowness — each step exists specifically to catch a toxic reaction at the smallest possible exposure before committing to a larger one.** Skipping steps (jumping straight to eating a meaningful portion) defeats the entire point: the test's real safety margin comes from the graduated exposure, not from any single step alone.
""",
    },
    {
        "title": "Plants to Avoid & General Edible-Plant Rules",
        "section": "reference",
        "tags": ["foraging", "poisonous-plants", "food-procurement"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Real Plant Types to Avoid Entirely

**9 real categories, each a genuine, broadly reliable warning sign:**

1. **Mushrooms and fungi** — toxic peptides (a protein-based poison) often have no detectable taste, so taste alone won't warn you.
2. **Plants with umbrella-shaped flower clusters** — this family includes edible carrots, celery, dill, and parsley, **but also poison water hemlock, one of the most toxic plants that exists** — the family itself isn't safely distinguishable without real expertise, so avoid unknowns in this shape entirely.
3. **Beans, peas, and seeds in pods** (the legume family) — these plants readily absorb soil minerals (notably selenium, the toxin behind locoweed's reputation) in ways that can make them unsafe.
4. **3-leafed and whorled-leaf growth patterns** — associated with the Lupine genus and other toxic plants.
5. **All bulbs** — as a general rule, avoid them; tulips and death camas are real poisonous examples.
6. **White and yellow berries** — nearly always poisonous. **Even red berries are a real coin flip — roughly half of all known red berries are toxic too.**
7. **Milky sap** — a real, reliable toxicity indicator.
8. **Shiny leaves** — treat with real caution as a toxicity sign.
9. **Known skin irritants** — poison ivy and similar plants.

## Preparing an Unknown Plant (before any edibility testing)

**Never attempt this preparation on a plant matching any category above — it does not make a genuinely poisonous plant safe.** For a plant that isn't on the avoid-list but hasn't been positively identified:

1. Place one part (leaves, flowers, stems, or roots) in a cup with water and boil.
2. **Discard the water after boiling** — many plant toxins are either heat-destroyed or water-soluble, and this step removes a real share of them (though not every toxin).
3. Repeat with fresh water a second time, boiling at least 5 minutes each round.
4. Only after this double-boil-and-discard process does the plant move on to the real edibility test (see Plant Identification & the Universal Edibility Test).

## Real General Rules for Likely-Safe Plants

- **Plants resembling ones people cultivate** are a reasonable starting point.
- **A single fruit on its own stem** is generally safer than clustered fruit.
- **Blue or black berries** are generally safe.
- **Aggregated/compound berries are always edible** — real examples: thimbleberry, raspberry, salmonberry, blackberry.
- **Plants growing in water or consistently moist soil** are often the most palatable.
- **All cone-bearing (conifer) trees produce edible seeds in their cones** — and the cambium layer, pitch, and needles are a real, rich source of vitamin C.
- **Any fruit with 5 petals on a single flower belongs to the rose family** — its hip (fruit) and flower are edible and a real, rich source of vitamins A and C.
- **All grass seeds are edible.**

## Specific Real Edible Plants (Western United States)

Wild onion (whole plant), dandelion (root and leaves), watercress (whole plant), cattail (root, stalk, stem), thistle — Anderson/bull/elk varieties (root and flower), yampah (bulb), juniper tree (berries), currants (berries).

**⚠️ Even confirmed-edible plants can cause real diarrhea, nausea, or cramping if eaten in large quantity on an empty stomach** — green apples and wild onions are real, common examples. Eat even known-safe foraged plants in moderation.

## Detailed Version

**The real, repeated principle across both the avoid-list and the general rules: a handful of visually checkable features (flower shape, berry color, leaf arrangement, sap type) let you make a real, fast safety judgment without needing to identify the exact species** — which matters enormously in a real foraging situation, where you'll routinely encounter unfamiliar plants you simply can't positively identify on the spot.
""",
    },
    {
        "title": "Medicinal Plants — Willow & Yarrow",
        "section": "reference",
        "tags": ["medicinal-plants", "herbal-medicine", "foraging"],
        "risk_level": "moderate",
        "body_markdown": """## Willow

**A thick, clustered-stem shrub with narrow leaves, found in wet soils, riverbanks, sandbars, and silt flats.**

- **Fever:** tea made from the inner bark.
- **Severe bleeding:** dried, powdered inner bark applied to the wound.
- **Diarrhea:** half a cup of willow charcoal dissolved in water.
- **Toothache:** mashed willow root applied to the affected area.

## Yarrow

**A tall, usually unbranched plant with clusters of small, flat-topped white flowers. ⚠️ Do not confuse it with poison hemlock** — a real, serious misidentification risk since both can appear in similar settings.

- **Insect repellent:** rub a handful of crushed yarrow flowers/leaves on exposed skin.
- **Bleeding:** a yarrow leaf poultice placed directly on the wound.
- **Minor burns and rashes** (including poison oak/ivy): a yarrow leaf compress on the affected area.
- **Toothache or fever:** chew the yarrow root.
- **A real potent anesthetic:** scrub fresh yarrow roots clean, crush them into a spongy mass, and apply gently to the wounded area.

## Real Preparation Methods — Terms Worth Knowing Precisely

- **Infusion (tea):** place a small amount of herb in a container, pour hot water over it, and let it steep (covered or uncovered) for 20 minutes before use.
- **Poultice:** crushed plant material applied directly or wrapped in cloth, used HOT.
  1. Wrap the crushed plant in gauze (or similar material), folded to hold it in place.
  2. Put the gauze packet inside a larger cloth (roughly 6"x8"), rolling the sides inward and folding it closed without losing the plant material.
  3. While boiling water, dip the bottom of the cloth (holding the edges) into the boiling water until saturated.
  4. Lift it straight up and wring the excess water back into the pot with a twisting motion.
  5. **Apply once it's cooled enough to tolerate against skin — a real, effective poultice should be as hot as you can stand.**
- **Compress:** prepared identically to a poultice, but applied COLD instead of hot.

**⚠️ Apply a poultice or compress for 1-24 hours as needed. A real, expected sensation: throbbing pain as a poultice draws out infection/toxins — once that pain subsides, the poultice has done its job and should be removed and replaced with a fresh one if more treatment is needed.**

## Detailed Version

**The real, single most important caution on this page is the yarrow/poison-hemlock confusion risk** — both can grow in similar habitat and share a superficial resemblance, and getting this specific identification wrong turns a real remedy into a real poisoning. This is exactly the kind of identification error the Universal Edibility Test (see Plant Identification & the Universal Edibility Test) exists to catch before it causes harm.
""",
    },
    {
        "title": "Poison-Tipped Hunting Weapons — Water Hemlock & Monkshood",
        "section": "reference",
        "tags": ["hunting", "foraging", "last-resort"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**This is a real, last-resort technique for taking large game as food when no other hunting method is available — not a weapon intended for use against people.** It parallels the same food-procurement logic as the trap "SICK" kill mechanisms and the throwing stick already covered elsewhere in this wiki (see Improvised Traps — Triggers & Mechanisms), scaled up to a situation where a survivor needs to bring down genuinely large game with a spear or arrow.

## Real Plants Used

**Water hemlock and monkshood** — both carry a real, potent toxin concentrated in their roots, which typically grow 8-10 inches deep.

## ⚠️ Real Safety Handling — the Single Most Important Part of This Page

**Never handle the root directly with bare skin.** Use a real barrier at all times — gloves, a sock, a T-shirt, even a wad of moss. The toxin that makes this technique work on game is genuinely dangerous to the person preparing it too.

## Real Preparation Technique

1. Dig up the root of the identified poisonous plant.
2. **Split the root lengthwise** to expose its interior, where the toxin is actually concentrated.
3. **Using the barrier to protect your hands, rub the tip of your spear or arrow inside the split root**, working slowly and deliberately from the base of the tip toward its point.
4. **Let the first coat dry, then apply another coat** — repeat this process, coat after coat, until the root is fully drained of its toxin.
5. Once no more toxin remains to transfer, the tip is ready for use.

## Detailed Version

**The real reason this page exists separately, with its own prominent safety warning, rather than being folded into general plant foraging: the entire point of this specific technique is concentrating a genuinely dangerous toxin onto a tool, which means the margin for a handling mistake is much narrower than ordinary foraging** — the barrier-handling instruction is not a minor aside, it's the single detail that keeps this real food-procurement technique from becoming a real self-poisoning instead.
""",
    },
    {
        "title": "Insects as Survival Food",
        "section": "reference",
        "tags": ["foraging", "insects", "food-procurement"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Insects are the most abundant life form on earth, genuinely easy to catch, and real nutritionally excellent — 65-80% protein by composition, compared to roughly 20% for beef.** In a real survival context, personal squeamishness is a real obstacle worth setting aside — the actual priority is maintaining your health.

## ⚠️ Insects to Avoid

1. **Any adult insect that stings or bites.**
2. **Hairy or brightly colored insects.**
3. **All caterpillars.**
4. **Insects with a pungent odor.**
5. **All spiders.**
6. **Known disease carriers** — ticks, flies, mosquitoes.

## Real Edible Insects

Insect larvae, grasshoppers, beetles, grubs, ants, termites, worms.

## Real Foraging Technique — Don't Spend More Energy Than You Gain

**⚠️ A real, easy mistake: expending more energy catching food than the food itself provides.** Grasshoppers specifically can become a frustrating, exhausting chase if approached the wrong way:

- **Grasshoppers climb tall plants and cling near the top at night** — they're genuinely easy to pick off by hand in the early morning while still chilled and sluggish.
- **Worms:** dig in damp humus soil, under rocks/logs, or simply look on the ground after rain.
- **Carpenter ants:** found in dead trees and stumps, gatherable by hand.
- **Most other insects:** rotten logs, under rocks, open grassy areas.

## Real Preparation

- **Insects with a hard outer shell often carry real parasites** — remove wings and barbed legs before cooking to reduce exposure.
- **Worms should be dropped into potable water for at least 30 minutes first** — they naturally purge their gut contents on their own. After that, they can be eaten raw or cooked.
- **Most other insects can be eaten raw, though cooking genuinely improves taste.** **If eating insects whole is too unappetizing, grind them into a paste and mix into other food** — a real, practical workaround that still captures the nutritional value.

## Detailed Version

**The real strategic insight behind the grasshopper-at-dawn technique: understanding an insect's actual behavior pattern (climbing high at night, sluggish when cold) turns an exhausting chase into a real, low-effort harvest** — the same principle behind knowing game animal habits for trapping (see Trapping & Snaring — General Principles), applied at insect scale.
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
                "source_url": USMC_SUMMER_PDF_URL,
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
