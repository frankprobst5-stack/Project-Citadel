#!/usr/bin/env python3
"""Seeds 4 more real pages rounding out Where There Is No Dentist's
Chapter 7 (Treating Some Common Problems) -- mined from the real text
layer already extracted in this session (/tmp/dentist.txt). Covers
real content not yet captured by the earlier abscess/broken-tooth/
jaw/extraction batches: Cavities, Infected Sinus, the 3 common mouth-
sore look-alikes (fever blisters, thrush, canker sores), and the
Tumor/Cancer warning-signs page referenced repeatedly by this book's
own diagnostic charts.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_cavities_sores_cancer.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DENTIST_PDF_URL = "/files/pdfs/Medical/Where-There-is-No-Dentist.pdf"

PAGES = [
    {
        "title": "Cavities & Lost or Broken Fillings",
        "section": "reference",
        "tags": ["dental", "cavity", "filling"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

**Signs:** pain when drinking cold water or eating something sweet, a visible hole or black spot on the tooth (or between two teeth), pain if food gets packed into the hole — **and importantly, no pain when the tooth is tapped** (tapping pain usually means it's progressed to an abscess instead — see Dental Emergencies — Tooth Abscess).

**Treatment (when there's no abscess):**
1. Remove any loose filling fragments with a probe, then put in a temporary filling: cement if you have it, or plain cotton packed into the hole to keep food out if you don't.
2. Check the person's other teeth for cavities or failing fillings too, and fill each one before it worsens into pain.
3. **Within a few months, arrange for a permanent filling** from someone experienced with a dental drill, or using Atraumatic Restorative Treatment (ART) — a real drill-free cavity-removal technique.

**A cavity at the neck/base of a tooth (a groove) is harder to fill** and needs the groove shaped with a drill for cement to hold. As a temporary measure: fluoride toothpaste rubbed into the groove weekly, or oil of cloves (eugenol) painted inside it to reduce pain. **Avoid a hard toothbrush, back-and-forth brushing along the gumline, and chewing tobacco or betel nut against the teeth** — all three make this specific kind of cavity worse.

## Detailed Version

The real diagnostic value of "pain when tapped" is worth remembering on its own: a cavity that doesn't hurt when tapped is still just a cavity, treatable with a temporary filling and no urgency beyond preventing it from worsening. The moment tapping produces pain, the problem has progressed to the root and become an abscess — a meaningfully more urgent, different treatment path.
""",
    },
    {
        "title": "Infected Sinus (Sinusitis Causing Tooth Pain)",
        "section": "reference",
        "tags": ["dental", "sinusitis", "toothache"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

The sinuses sit just under the eyes, on either side of the nose — close enough to the roots of the upper teeth that a sinus infection can cause real tooth pain even though the teeth themselves are completely healthy.

**Signs that point to the sinus, not the teeth:**
- Toothache across **several** top teeth at once, and the teeth look completely healthy, but hurt when tapped.
- A head cold with a plugged nose, breathing through the mouth.
- Pain when pressing on the cheekbone under the eyes.
- The tooth pain changes/worsens when the person bends forward.

**Treatment — do NOT extract any teeth.** The teeth will stop hurting once the actual sinus infection is treated:
1. Penicillin for 5 days.
2. Drink plenty of water, breathe steam from boiling water to help clear the nose, hold a warm wet cloth against the face often. **Wipe the nose rather than blowing it** — blowing can force pressure into the ears and cause ear pain.
3. **Recheck in 3 days** — re-examine and tap the teeth to confirm they're genuinely healthy; if the person isn't improving, get help from a more experienced health worker.

## Detailed Version

This page exists specifically to prevent an unnecessary extraction. Several healthy top teeth all hurting at once, with no cavity or abscess findings, is the real tell that the pain's source is the sinus above the roots, not the teeth themselves — treating the sinus resolves teeth that were never actually diseased.
""",
    },
    {
        "title": "Mouth Sore Look-Alikes — Fever Blisters, Thrush & Canker Sores",
        "section": "reference",
        "tags": ["dental", "mouth-sores", "thrush", "herpes"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version — telling them apart matters because treatment differs completely

| | Cause | Where it appears | Real treatment |
|---|---|---|---|
| **Fever blisters** | Herpes virus | Gums/roof of mouth (children 1-5, can cause dangerous dehydration if they stop eating/drinking) OR lips (after age 5, often when weak/sick) | No medicine kills the virus — resolves in ~10 days on its own. Comfort care, keep fluids and food up |
| **Thrush** | Candida yeast fungus | Tongue, cheek, roof of mouth (babies); under dentures (adults) | Nystatin drops, or gentian-violet-painted cotton if unavailable. Fix the underlying cause (malnutrition, antibiotic use, ill-fitting denture) |
| **Canker sores** | Unknown cause | Cheeks, inside lips, tongue, under the gums (smooth skin only — not the gums themselves) | Self-limited, ~10 days, comfort measures only |

## Fever Blisters (Herpes)

**Mouth sores in a child age 1-5 are the serious version** — the child can become too sick to eat, and **dehydration from not drinking is the real danger**, not the sores themselves. Signs: sore throat, fever, crying and stopping sucking 2-3 days before sores appear, drooling because swallowing hurts, painful swelling under the jaw, bright red blisters on the gums (not between the teeth) and sometimes the roof of the mouth.

**Treatment:** aspirin/acetaminophen for fever; wipe milk or yogurt over the sores before meals to protect them; soft, non-spicy food (a milk-oil drink if they can't eat solids at all — see Broken Jaw page for the recipe); plenty of fluids.

**Lip sores (after age 5)** usually appear when the person is weak from another illness, usually without fever, break open and crust over, and **can recur and spread by contact while leaking fluid** — wash your hands immediately after any contact. Antibacterial cream or petroleum jelly helps prevent secondary infection; ice held against them for several minutes daily may speed healing.

## Thrush (Candida)

Appears when someone is weak, malnourished, sick, or on long antibiotic courses (tetracycline, ampicillin) — and is very common in people living with HIV. **Test:** wipe the white patch — if it doesn't bleed, it's old milk; **if it bleeds, it's thrush.**

**Treatment:** find and address what's letting it grow (malnutrition, diabetes, anemia, a long antibiotic course, an unwashed denture left in too long) — treating only the surface patches without this fixes nothing for long. Nystatin drops 4-5x/day until clear, or gentian-violet-soaked cotton painted on 2x/day if nystatin isn't available. **Don't start penicillin or another antibiotic unless treating something unrelated** — antibiotics can make thrush worse. If a breastfeeding mother has sore nipples, she likely has thrush there too and should treat them the same way.

**⚠️ Watch for a different, more serious look-alike:** white lines on the inside of an adult's cheek or roof of the mouth that become sore and don't improve with treatment can turn into cancer. Reducing that risk means stopping smoking (especially pipes), stopping betel nut chewing, and fixing ill-fitting dentures.

## Canker Sores

White-or-yellow sores with a bright red border, appearing on the cheeks, inside the lips, the tongue, or the smooth skin under the gums (**not** on the gums themselves — that pattern points to something else). Common in youth, exact cause unknown.

**Treatment:** resolves on its own in about 10 days; medicine doesn't speed that up, though a poorly-fitting denture rubbing the area should be left out for 2-3 days and refitted. Soft, non-spicy food, lots of water, chewing on the opposite side, warm salt-water rinses (4 cups/day). **If it's still there after 10 days, treat as a possible infection with penicillin — and if it still doesn't heal after that, treat as a possible cancer and get real medical evaluation immediately.**

## Detailed Version

The real unifying rule across all three: **location is the fastest way to tell them apart** — on the gums themselves points to fever blisters, under a denture or in a weakened person points to thrush, and on the smooth cheek/lip/tongue tissue (never the gums) points to a canker sore. Getting the location-based differential right avoids reaching for an antibiotic that actively worsens thrush, or dismissing a sore as "just a canker sore" past the point where cancer needs to be ruled out.
""",
    },
    {
        "title": "Mouth Tumor & Cancer — Warning Signs",
        "section": "reference",
        "tags": ["dental", "cancer", "tumor"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**A tumor is a lump growing under the skin or inside the bone — slowly, steadily, and usually without pain.** This is exactly why it's dangerous: a painless, slow-growing lump doesn't prompt the urgency a painful one would.

**Red flag:** any facial/jaw swelling that does NOT improve after a full course of antibiotics and heat treatment should be treated as a possible tumor, not a stubborn infection — don't keep repeating the same treatment hoping for a different result. **Send for real medical help; a tumor needs surgical removal, and continuing to treat it as a simple infection wastes time it can't afford to lose.**

## ⚠️ Mouth Cancer — the single most important rule on this page

**Any sore or bump in the mouth that has not healed within 2 weeks should be evaluated as possible cancer.** The lips and tongue are the two most common starting points, but also check the floor of the mouth under the tongue, the soft roof of the mouth, and the gums.

**Why this matters more than almost anything else in this book: cancer can spread internally, out of sight, and become fatal — but it's genuinely treatable when caught early.** The entire actionable point of this page is the 2-week rule itself, not a home treatment:

**If you're treating a mouth sore and it is not improving on schedule, send the person for real medical evaluation immediately.** A doctor can biopsy it (remove a small piece, examine it under a microscope) to confirm or rule out cancer. If confirmed, the person needs specialized treatment beyond what any home or community-health setting can provide.

## Detailed Version

This page is intentionally short because its entire value is a single trigger rule, not a technique: **2 weeks of non-healing is the line.** Every other page in this book that mentions a persistent sore, ulcer, or white patch (canker sores, thrush's cheek-lining white lines, non-healing denture sores) cross-references back to this same rule for a reason — it's the one place where "keep treating it a bit longer at home" is the wrong call, and the earlier a real evaluation happens, the better cancer's actual odds are.
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
                "source_url": NO_DENTIST_PDF_URL,
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
