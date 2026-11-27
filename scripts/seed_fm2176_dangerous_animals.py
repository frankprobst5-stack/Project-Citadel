#!/usr/bin/env python3
"""Seeds 2 real pages from the OCR'd FM 21-76 (US Army Survival
Manual, 1992/1999) Chapter 11 (Dangerous Animals) -- mined from the
OCR output cached at /tmp/fm2176.txt.

FM 21-76 is the direct predecessor to ATP 3-50.21 (the current 2018
Army Survival manual), which has already been extensively mined in
this wiki -- so most of FM 21-76's content on shelters, fire,
water, and food procurement substantially overlaps material already
seeded. Chapter 11 (Dangerous Animals) is different: it's an
avoidance/identification-focused chapter not mirrored by anything
else in the wiki, which so far only has treatment-after-the-fact
content (bite/sting treatment from the SF Medical Handbook) and no
real "how to avoid the encounter in the first place" guidance.

SCOPING NOTE: the source chapter also catalogues region-specific
venomous snakes by continent and a long list of tropical reef fish
and marine invertebrates (blue-ringed octopus, cone shells, etc.).
Given this wiki's real-world use case (the source's own geographic
sweep includes polar regions, Australian reefs, and Southeast Asian
rivers that are not broadly relevant here), only the universally
applicable avoidance principles and the few individually memorable,
non-region-specific toxic-food warnings are seeded -- not the full
species catalog, which belongs more to a field guide than a safety
reference.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_fm2176_dangerous_animals.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
FM2176_PDF_URL = "/files/pdfs/Military Manuals/FM-21-76-US-Army-Survival-Manual.pdf"

PAGES = [
    {
        "title": "Avoiding Dangerous Animal Encounters — Real Field Safety Rules",
        "section": "reference",
        "tags": ["dangerous-animals", "snake-avoidance", "tick-prevention"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**⚠️ Real, important perspective: small animals are a genuinely bigger real threat to a survivor than large ones.** More people die every year from small venomous snake bites and bee-sting allergic reactions than from bears, sharks, or alligators — most large-animal incidents are, in some real way, the victim's own fault (surprising it, cornering it, leaving food out). **Avoidance, not confrontation skill, is the real core of this entire page.**

## Real General Rules

- **Don't attract large predators by leaving food lying around camp.**
- **Carefully survey a scene before entering water or forest** — most large-animal encounters are preventable simply by looking first.
- **Check footgear, clothing, bedding, and shelter every morning** in any area known to have spiders or scorpions — and use care when turning over rocks or logs (use a stick, not your hand).

## ⚠️ Real Snake Avoidance Rules

**There are no foolproof field rules for identifying a venomous snake at a glance — the real differences require close inspection most people shouldn't attempt.** The real strategy is to leave every snake alone rather than try to identify it:

- **Step ONTO logs, never over them** — look first, then move.
- **Look closely before picking fruit or moving around water.**
- **Never tease, molest, or harass a snake.** **⚠️ Real, important fact: snakes cannot close their eyes, so you genuinely cannot tell whether one is asleep just by looking.** Some species (the source specifically names mambas, cobras, and bushmasters) attack aggressively when cornered or guarding a nest.
- **Use a stick to turn over logs and rocks, never your hand.**
- **Wear proper footwear, especially at night.**
- **Check bedding, shelter, and clothing carefully before using them.**
- **Stay calm if you do encounter one.** **Real, useful fact: snakes cannot hear** — you can genuinely surprise a sleeping or sunning snake, and most will flee if given the chance to.
- **⚠️ Real, worth knowing: a warm, sleeping human body can occasionally attract a snake looking for warmth** — this is an unusual but real reason to keep a shelter/sleeping area as sealed as practical.

## ⚠️ Real Tick Removal Window

**Ticks spread real diseases including Lyme disease, Rocky Mountain spotted fever, and encephalitis** (see Tick, Lice & Mite-Borne Fevers — Recognizing the Rickettsial Diseases for RMSF specifically). **⚠️ Real, critical number: most authorities agree a tick must stay attached for at least 6 hours before it can transmit disease** — this means a thorough daily body check genuinely has time to catch and remove a tick before transmission occurs. **Real, practical risk windows: passing through thick vegetation, cleaning an animal carcass for food, and gathering natural materials for shelter-building are all real tick-exposure moments worth a check afterward.**

## Detailed Version

**The real, unifying idea behind this entire page: almost every dangerous-animal incident described in the source traces back to a preventable moment — reaching under a rock, stepping over a log instead of onto it, leaving food out, handling a snake to identify it instead of just avoiding it.** Spending effort on avoidance habits is a far better real investment than spending effort trying to correctly identify a threat once you're already close enough for it to matter.
""",
    },
    {
        "title": "Animals & Fish You Should Never Eat — Real Poisonous Species Warnings",
        "section": "reference",
        "tags": ["poisonous-food", "wild-game", "foraging-safety"],
        "risk_level": "high",
        "body_markdown": """## ⚠️ Read This First

**A handful of specific wild animals and fish are genuinely toxic to eat regardless of cooking method** — unlike bacterial contamination, cooking doesn't neutralize these particular toxins. This page covers the individually memorable, real exceptions worth knowing before eating unfamiliar wild food.

## ⚠️ Real, Specific Toxic Organs & Species

- **⚠️ Polar bear liver is genuinely toxic enough to kill** — it concentrates extremely high levels of vitamin A. **This is a real, specific, well-documented survival-manual warning**, not a general "don't eat too much liver" caution.
- **The hawksbill turtle's flesh is toxic.** Recognizable by its down-turned beak and yellow polka-dot pattern on the neck and front flippers; it also weighs over 275kg (600+ lbs), making an accidental catch unlikely for most people anyway.
- **⚠️ Puffer fish (blowfish) are extremely dangerous: their blood, liver, and reproductive organs are so toxic that as little as 28mg (about 1 ounce) can be fatal.** They're stout, round-bodied, often short-spined, and can inflate into a ball when alarmed. **Real, counterintuitive fact: some cultures still eat them as a delicacy at certain times of year** — this requires genuine specialized preparation knowledge to remove the toxic organs safely, not something to attempt without that specific training.

## Real General Caution for Unfamiliar Fish

**⚠️ Be wary of eating any unidentifiable fish, wherever you are** — this is the single most broadly useful rule on this page. **Real, important nuance: even normally-safe predatory fish (like barracuda or snapper) can become toxic if the smaller fish they've been eating were themselves toxic** — the toxin concentrates up the food chain. **A real, rough visual warning sign: fish with parrot-like beaks and hard, shell-like, spiny skin that can inflate their bodies are disproportionately likely to be among the toxic ones** (this describes puffers and triggerfish specifically) — though this is a rough pattern, not a reliable rule on its own.

## Detailed Version

**The real, most important idea on this page: unlike most food-safety risks in this wiki (bacteria, parasites, spoilage), these specific toxins are NOT destroyed by cooking** — thorough cooking is otherwise this wiki's default answer to "is this safe to eat," and these are the real, documented exceptions where that default answer doesn't apply. When in doubt about an unfamiliar fish or organ, the real safe choice is simply not eating it, rather than relying on cooking to make it safe.
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
                "source_url": FM2176_PDF_URL,
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
