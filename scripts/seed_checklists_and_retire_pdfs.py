#!/usr/bin/env python3
"""Seeds 4 real gear-checklist pages, fully transcribed from 4 short,
single-purpose PDFs already in the Vault -- then deletes those 4 PDFs
and their wiki_attachments catalog rows.

This is deliberately different from the other scripts/seed_*.py files:
those pulled ONE topic out of a large multi-chapter reference book
(hundreds/thousands of lines) that still has real unmined content left
in it -- deleting those source files now would destroy chapters not
yet in the wiki. These 4 files are short (26-80 lines each), single-
purpose checklists with nothing else inside them once this script's
own transcription captures the full list -- genuinely safe to remove,
not just convenient to remove.

Real source note: each of these 4 PDFs is itself a printout from
trueprepper.com's own gear-list pages (the URL is printed at the
bottom of each PDF) -- a commercial gear-review site, not a government
or medical authority. verification_status='supported' here, not
'verified', to reflect that honestly: this is a faithful transcription
of a real, credible curated list, not content drafted against an
authoritative government/medical source the way the Emergency Now
pages are.

Idempotent: skips creating a page whose title already exists, and
skips deleting a PDF/attachment that's already gone (so re-running
after a partial failure is always safe).

Usage:
    python3 scripts/seed_checklists_and_retire_pdfs.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
VAULT_ROOT = REPO_ROOT / "appdata" / "media-vault"

PAGES = [
    {
        "title": "Bug-Out Bag Checklist",
        "tags": ["gear", "checklist", "bug-out-bag"],
        "source_url": "https://trueprepper.com/kits/bug-out-bag-list/",
        "retire_pdf": "pdfs/Survival/Bug-Out-Bag-Checklist-v3-2-Page.pdf",
        "body_markdown": """Organized by priority -- Essential items first, then Suggested, then Situation-Specific (only relevant to some households/regions).

## Essential — Bug Out Bag
- Bug Out Backpack

## Essential — Water
- Water Filter, Purification Tablets, Steel Water Bottle, Canteen With Cup, Water (3L+), Bleach, Coffee, Electrolyte Mix, Sillcock Key

## Essential — Food
- Emergency Ration Bars, MREs, Camp Utensils, Can Opener, Stove, Steel Pot, Fishing Kit, Snare Kit, Beef Jerky, Condiments, Multi-Vitamins, Conibear Trap, Edible Plants Guide

## Essential — Shelter & Warmth
- Waterproof Tarp, Survival Blanket, Bivvy Sack, Waterproof Matches, Lighter, Tent, Ferro Rod, Tinder, Sleeping Bag, Sleeping Mat/Ground Pad, Rainproof Shell, Magnifying Glass, Handwarmers, Tent Stakes

## Essential — Power & Energy
- Cell Phone Charger, Flashlight, Headlamp, Batteries, Candles, Power Bank, Glow Sticks, Solar Panel, Power Station, Stove Fuel

## Suggested — Nav & Comms
- Weather Radio, Compass, Local Maps, Survival Mirror, Signal Flares, Whistle, GPS Watch, Ranger Beads, Ham Radio, CB Radio, Binoculars

## Suggested — Medical & First Aid
- Basic First Aid Kit, Prescription Medication, Sun Screen, Insect Repellent, Anti-diarrheal Tabs, Iodide Tablets, Extra OTC Medication, Trauma Kit (if trained), Sting Relief, First Aid Guide

## Suggested — Hygiene & Sanitation
- Toothbrush, Toothpaste, Soap, Feminine Supplies, Hand Sanitizer, Portable Bidet, Garbage Bags, Shaving Supplies, Foot Powder, Toilet Paper, Floss, Compressed Towels

## Suggested — Clothing
- Work Gloves, Socks, Long Sleeve Shirt, Underwear, Pants, Rain Poncho, N95 Masks, Nitrile Gloves, Bandana, Hat, Jacket, Boots/Shoes, Long Underwear, Sunglasses, Scarf/Shamagh, Earplugs

## Situation-Specific — Protection
- Handgun (if trained), Ammunition, Pepper Spray, Rifle, Ammo Pouch, Perimeter Alarm

## Situation-Specific — Tools
- Survival Knife, Bushcraft Knife, Multitool, Paracord, Duct Tape, Folding Saw, Super Glue, Zip Ties, Sewing Kit, Hatchet, Shovel, Machete, Prybar, Hacksaw, Zip-Lock Bags, Waterproof Bags, Pliers, Rope, Steel Wool, Pocket Sharpener, Gun Cleaning Kit

## Situation-Specific — Personal Items
- Emergency Plan, Copy of ID, Cash Stash, Rainproof Pen, Waterproof Notebook, Copy of Birth Certificate, Copy of Passport, Playing Cards, Silver, Gold, USB Drive, Important Documents
""",
    },
    {
        "title": "Survival Food Storage Checklist",
        "tags": ["gear", "checklist", "food-storage"],
        "source_url": "https://trueprepper.com/survival-food-list/",
        "retire_pdf": "pdfs/Survival/Survival-Food-Checklist-v3.pdf",
        "body_markdown": """A gear/stocking list for food independence — pair with the **Safe Home Food Storage** page for the actual safety rules on storing and rotating this.

## Essential — Short-Term Stockpile
- Canned Food, Energy Bars or Granola, Peanut Butter, Crackers/Chips, Pasta, Dried Fruits, Nuts, Powdered Milk, Oatmeal or Cereal, Jams and Jellies, Condiments, Baby Formula, Pet Food

## Essential — Long-Term Stockpile
- Freeze Dried Meal Kits, Bulk Beans, Bulk Rice, Bulk Oats, Bulk Wheat, Bulk Corn, Salt, Cooking Oils and Lard, Bulk Sugar, Honey, Dehydrated Fruits & Veggies, Freeze Dried Meat/Fruit/Vegetables/Dairy, Survival Bread

## Suggested — Bug-Out Survival Food
- Survival Food Bars, Beef Jerky, Energy Bars, Freeze-Dried Mobile Packs, Nuts, MREs, Tuna Pouches

## Suggested — Hunting + Trapping
- Rifle, Ammo, Fishing Gear, Bow and Arrows, Snares, Conibear Traps, Hunting Knife, Hunting Dog(s)

## Suggested — Foraging
- Edible Plant Guide, Edible Fungus Guide, Foraging Bag, Nutcracker

## Suggested — Gardening
- Survival Seed Vault, Tended Garden Beds, Garden Tools, Irrigation Plan, Indoor Grow Lights, Hydroponics, Compost

## Situation-Specific — Food Storage Tools
- Can Opener, Food-Grade Buckets, Mylar Bags, Heavy-Duty Shelving, Oxygen Absorbers, Canning Equipment, Freezer, Dehydrator, Vacuum Sealer, Freeze-Dryer, Impulse Heat Sealer

## Situation-Specific — Homesteading
- Chickens, Goats, Rabbits, Cows, Fruit Trees, Animal Feed, Vet Supplies, Fencing
""",
    },
    {
        "title": "Nuclear Survival Kit Checklist",
        "tags": ["gear", "checklist", "nuclear"],
        "source_url": "https://trueprepper.com/nuclear-survival-kit/",
        "retire_pdf": "pdfs/Survival/Nuclear-Survival-Kit-Checklist-v3.pdf",
        "body_markdown": """Pair with **Expedient Fallout Shelter — Door-Covered Trench** for what to actually do with this gear.

## Essential — Personal Protection
- Gas Mask, Coveralls, Gloves, Boots, Clothes (Skivvy Roll), Rain Slick/Poncho, N95 Masks, Goggles

## Essential — Hardening
- Faraday Bags, Sandbags, Shovel, Crank Flashlight

## Suggested — Detection
- Geiger Counter, Dosimeter

## Suggested — Decontamination
- Wet Wipes, Dish Soap, Scrub Brush, Water for Washing

## Suggested — Self Care
- Potassium Iodide Pills, Shaving Supplies

## Suggested — Documents
- Nuclear Survival Guides

## Situation-Specific — Other Kits
- Home Survival Kit, Bug Out Bag (or variant), Everyday Carry, Shelter in Place Kit, Bug Out Vehicle
""",
    },
    {
        "title": "Home Survival Kit Checklist",
        "tags": ["gear", "checklist", "home"],
        "source_url": "https://trueprepper.com/kits/survival-kits/",
        "retire_pdf": "appdata_special:Emergency Checklists/Home-Survival-Kit-Checklist-v3-2-Page.pdf",
        "body_markdown": """Broad preparedness for common household threats — not bug-out specific.

## Essential — Security & Protection
- Fire Extinguisher, Reinforced Doors, Security Safe, Shotgun (if trained), Ammunition, Handgun (if trained), Baseball Bat, Hidden Safe

## Essential — Water
- Water Containers, Water Filter, Water Purification, Rain Barrels, Bleach, Coffee, Electrolyte Mix, Siphon

## Essential — Food
- Canned Foods, Emergency Food Supply, Bulk Food Storage, Can Opener, Emergency Stove, Fishing Supplies, MREs, Survival Seed Vault, Snares, Conibear Trap

## Essential — Shelter & Warmth
- Lighter, Waterproof Tarps, Survival Blanket, Sleeping Bag/Bivvy, Ferro Rod, Magnifying Glass, Tinder, Firewood, Matches

## Essential — Clothing & PPE
- Work Gloves, Wet Weather Clothes, Winter Clothes, N95 Masks, Nitrile Gloves

## Suggested — Medical & First Aid
- Basic First Aid Kit, Prescription Medication, Insect Repellent, Anti-Diarrheal Tabs, Iodide Tablets, Sting Relief, Extra OTC Medication, Trauma Kit (if trained)

## Suggested — Nav & Comms
- Weather Radio, Ham Radio, Signal Flares, Whistle, GMRS Radio, Walkie Talkies, Local Maps, Compass

## Suggested — Power & Energy
- Flashlight, Headlamp, Cell Phone Charger, Candles, Batteries, Generator, Generator Fuel, Grill and Stove Fuel, Power Station, Solar Panels

## Suggested — Personal Items
- Fireproof Document Bags, Bank Information, Cash Stash, Birth Certificates, Social Security Cards, Passports, Medical History, Emergency Plan, Survival Guides and PDFs, Portable Harddrive, Games + Entertainment, USB Drive, Insurance Documents, Gold, Silver, Bible

## Situation-Specific — Tools
- Survival Knife, Paracord, Duct Tape, Tool Collection, Spare Keys, Sewing Kit, Sharpener, Gun Cleaning Kit, Rifle, Tree Saw, Construction Adhesive/Supplies, Zip Ties, Axe, Water Main Shutoff Tool, Binoculars, Rope

## Situation-Specific — Hygiene & Sanitation
- Feminine Supplies, Soap/Detergent, Toilet Paper, Garbage Bags, Portable Bidet, Bucket Toilet, Hand Sanitizer, Shaving Supplies

## Situation-Specific — Other Survival Kits
- Bug Out Bags, Specialized Kits
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


def resolve_pdf_path(retire_pdf):
    # "Emergency Checklists" lives at a different real top-level path
    # than "Survival" -- both are under appdata/media-vault/pdfs/, this
    # just documents which subfolder each retire_pdf entry means.
    if retire_pdf.startswith("appdata_special:"):
        return VAULT_ROOT / "pdfs" / retire_pdf.split(":", 1)[1]
    return VAULT_ROOT / retire_pdf


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
    existing_pages = requests.get(f"{args.base_url}/api/wiki/pages", headers=headers, timeout=10)
    existing_pages.raise_for_status()
    existing_titles = {p["title"] for p in existing_pages.json()}

    existing_attachments = requests.get(f"{args.base_url}/api/wiki/attachments", headers=headers, timeout=10)
    existing_attachments.raise_for_status()
    attachments_by_filename = {a["filename"]: a["id"] for a in existing_attachments.json()}

    created, skipped, pdfs_removed, attachments_removed = 0, 0, 0, 0
    for page in PAGES:
        if page["title"] not in existing_titles:
            if args.dry_run:
                print(f"WOULD CREATE: {page['title']}")
            else:
                res = requests.post(
                    f"{args.base_url}/api/wiki/pages",
                    headers=headers,
                    json={
                        "section": "reference",
                        "title": page["title"],
                        "body_markdown": page["body_markdown"],
                        "tags": page["tags"],
                        "source_url": page["source_url"],
                        "verification_status": "supported",
                    },
                    timeout=10,
                )
                if res.ok:
                    print(f"CREATED: {page['title']}")
                else:
                    print(f"FAILED  ({res.status_code}): {page['title']} -- {res.text}", file=sys.stderr)
                    continue
            created += 1
        else:
            print(f"SKIP page (already exists): {page['title']}")
            skipped += 1

        # Retire the source PDF -- fully transcribed above, nothing left in it.
        pdf_path = resolve_pdf_path(page["retire_pdf"])
        category_and_name = "/".join(str(pdf_path).split("/")[-2:])  # "<category>/<basename>"
        if pdf_path.exists():
            if args.dry_run:
                print(f"  WOULD DELETE PDF: {pdf_path}")
            else:
                pdf_path.unlink()
                print(f"  deleted PDF: {pdf_path}")
            pdfs_removed += 1
        else:
            print(f"  (PDF already gone: {pdf_path})")

        attachment_id = attachments_by_filename.get(category_and_name)
        if attachment_id:
            if args.dry_run:
                print(f"  WOULD DELETE attachment catalog row: {category_and_name}")
            else:
                requests.delete(f"{args.base_url}/api/wiki/attachments/{attachment_id}", headers=headers, timeout=10)
                print(f"  deleted attachment catalog row: {category_and_name}")
            attachments_removed += 1
        else:
            print(f"  (no catalog row found for: {category_and_name})")

    print(f"\n{created} pages created, {skipped} skipped. {pdfs_removed} PDFs removed, {attachments_removed} catalog rows removed.")


if __name__ == "__main__":
    main()
