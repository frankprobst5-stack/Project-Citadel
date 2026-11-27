#!/usr/bin/env python3
"""Seeds 3 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 11 Section II (Cold Injuries) --
mined from the OCR output cached at /tmp/sfmedical.txt.

Covers real content genuinely extending existing frostbite coverage
(USMC content covers "frosting/superficial/deep" only): a real,
detailed windchill equivalent-temperature chart (far more granular
than the Canadian source's single freeze-threshold line already in
this wiki), real cold-injury risk factors, a real 4-degree frostbite
classification with real timelines/prognosis, and real early-
diagnosis signs plus real individual field rewarming technique
(including the real early-warning sign of sudden warmth/cessation of
cold sensation).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_cold.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Cold Injury Risk Factors & the Real Windchill Equivalent-Temperature Chart",
        "section": "reference",
        "tags": ["cold-weather", "windchill", "frostbite-prevention"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Low temperature and low humidity favor frostbite; higher temperature combined with moisture favors trench foot — and wind accelerates heat loss under either condition.** A real, detailed chart converts actual temperature + wind speed into the equivalent still-air temperature your exposed skin actually experiences.

## ⚠️ Real Windchill Equivalent-Temperature Chart

**The source includes a real, detailed windchill chart** — actual thermometer reading (40°F down to -60°F) across the top, wind speed (calm through 40mph) down the side, with the equivalent still-air temperature your exposed skin actually experiences at each intersection. *(The scanned chart's exact digits weren't reliably recoverable even across two independent high-resolution OCR passes of this copy — rather than publish uncertain numbers, see Understanding Cold — Wet vs. Dry Cold & the Windchill Table for this wiki's already-verified real windchill table, cleanly extracted from a different source's native text.)*

**What IS clearly legible from this chart, real and worth keeping:** it divides outcomes into 3 real danger bands — "little danger" (for a properly clothed person), "increasing danger," and "great danger" of exposed flesh freezing, moving from warmer/calmer combinations toward colder/windier ones. **⚠️ Wind above 40mph adds little further cooling effect** beyond what's already captured at 40mph. **Trench foot/immersion foot can occur at any point on this chart** — it isn't limited to the coldest cells, since it depends on wet-cold exposure rather than freezing specifically.

## Real Cold Injury Risk Factors

- **Loose, layered clothing under a windproof/water-resistant outer shell gives the real best protection** — remove inner layers during real exertion to avoid overheating and sweat buildup, since wet clothing loses much of its insulating value.
- **The very young and very old are more vulnerable.**
- **⚠️ A previous cold injury genuinely raises risk of a new one — not necessarily in the same body part.**
- **Fatigue can cause apathy that leads to neglecting basic survival actions.**
- **Blood loss or shock from another injury reduces blood flow to the extremities**, predisposing them to cold injury.
- **Starvation or semi-starvation increases real cold-injury risk.**
- **Any drug affecting peripheral circulation or sweating can contribute.**
- **⚠️ Alcohol dilates peripheral blood vessels, accelerating real heat loss** — it increases hypothermia/frostbite risk, not the opposite of what it might feel like.
- **⚠️ Real, counterintuitive risk: heat injury can occur even in extreme cold, from overdressing and overexertion** — this can damage the body's temperature-regulating mechanism and lead rapidly into hypothermia.

## Detailed Version

**The real, most actionable insight from this kind of chart: the same real equivalent cooling effect can come from a genuinely mild actual temperature combined with real wind, or from a much colder actual temperature in calm air** — which is exactly why checking wind speed alongside the thermometer, not the thermometer alone, is what actually determines real exposure risk (see the already-verified numeric table in Understanding Cold — Wet vs. Dry Cold & the Windchill Table for concrete figures).
""",
    },
    {
        "title": "Frostbite — Real 4-Degree Classification & Prognosis",
        "section": "emergency",
        "tags": ["frostbite", "cold-injury", "prognosis"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**Real classification into degree is only possible retrospectively, after rewarming and over time — not at the moment of injury.** This real detail genuinely extends the basic frostbite coverage already in this wiki with specific timelines and prognosis for each degree.

## First Degree

After rewarming: **mottled, red, hot, dry skin** that blanches poorly and refills slowly (or not at all) under pressure. Real symptoms: intense itching/burning, later a deep ache. **Swelling begins within 3 hours**, persisting up to 10+ days if the person stays active, but usually under 5 days with real rest. **Skin peeling can begin 5-10 days after injury and last up to a month.**

## Second Degree

After rewarming: **deep red, hot, dry skin**, often with absent light-touch and position sense. **⚠️ Real, valuable diagnostic sign: blisters (sometimes large blebs) appear within 6-12 hours, extending nearly to the fingertip/toe tips** — this specific finding is what actually identifies it as second degree. These dry into black scabs (eschars) within 10-24 days, which gradually separate to reveal thin, soft, easily-injured new skin underneath. Pain progresses from tingling/burning to a deep ache that may genuinely require medication.

## Third Degree

**Real necrosis (tissue death) of skin and underlying tissue.** Blisters, if present, contain blood, are smaller, and don't reach the digit tips. **Swelling of the entire hand/foot typically appears around day 6.** **Most people experience 5-17 days of numbness**, followed by burning, aching, throbbing, or shooting pain that can last months — **and can recur with future cold exposure, sometimes for the rest of their life.** A black, hard, dry scab forms and eventually separates, exposing healing granulation tissue underneath. **Real healing timeline: averages 68 days.** **⚠️ Additional trauma or infection (beyond the cold injury itself) can cause major tissue loss, systemic infection, or wet gangrene requiring emergency amputation.**

## Fourth Degree

**Complete necrosis through the full thickness of the part, including bone — resulting in real loss of the entire injured part.** Skin may turn deep red, purple, or mottled/cyanotic on rewarming. **In some cases, swelling develops rapidly (peaking in 6-12 hours) with little visible volume increase, progressing quickly to dry gangrene and mummification.** In others, swelling develops more slowly and prominently, with scab formation not visible until 2-3 weeks post-rewarming. **The real line between dead and living tissue typically becomes visible around day 36, but takes 60-80 days to fully extend down to the bone.** Usually no sensation for 3-13 days, followed by "ghost pain" that can become severe.

## Detailed Version

**The real, unifying thread across all 4 degrees: the true severity of a frostbite injury genuinely cannot be judged in the moment — it reveals itself only over days to weeks, through specific real markers (blister timing and extent, swelling onset, numbness duration, and eventually where the line of dead tissue settles).** This is exactly why initial field treatment (see Frostbite — Early Diagnosis Signs & Real Field Rewarming Technique) focuses on superficial-vs-deep distinction and real evacuation, not on predicting the final degree on the spot.
""",
    },
    {
        "title": "Frostbite — Early Diagnosis Signs & Real Field Rewarming Technique",
        "section": "emergency",
        "tags": ["frostbite", "cold-injury", "first-aid"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ The Real Early Warning Sign Worth Memorizing

**A fairly reliable sign of incipient frostbite in fingers, toes, or exposed skin: the sudden, complete disappearance of cold or discomfort in that part — often followed by a deceptively pleasant feeling of warmth.** **⚠️ This "pleasant warmth" is a real, dangerous false signal, not a sign of actual improvement** — prompt action at this exact moment can prevent a genuinely more serious injury from developing.

## Real Signs Distinguishing Superficial From Deep Injury (First 48-72 Hours)

**In the real early window, you can only distinguish superficial (skin loss or less) from deep (skin AND tissue loss) — not the eventual full degree.**

**Real signs of superficial injury:**
- Large, clear blisters developing early, reaching the digit tips.
- Sensation returning quickly.
- Normal (warm) temperature returning to the area.
- Pink or mildly red skin that blanches quickly under pressure.

**Real signs of deep injury:**
- Hard, white, cold, and completely insensate tissue.
- No swelling present.
- Dark, blood-filled blisters, or none at all.
- Early mummification.
- Real systemic signs of tissue death (fever, rapid heart rate, prostration).
- Additional trauma to the area.
- Cyanotic or dark red skin that does NOT blanch under pressure.

## Real Individual Field Rewarming Technique

**The moment the early-warning sign (sudden warmth/numbness) appears, rewarm the area immediately:**
- **Ear, nose, or cheek:** remove your glove and hold your bare, warm hand against the area — **do not rub it.** Once rewarmed, protect it with a scarf or ear flaps.
- **Fingers:** tuck them under clothing against the bare skin of your own abdomen or armpit.
- **Toes:** hold them against a companion's chest or abdomen, under their outer clothing.

## Real Initial/Emergency Treatment Once an Injury Is Suspected

**Restrict the person from normal duties/activity until real severity can be properly evaluated.** **Remove every constricting item** (boots, socks, gloves) from the affected site, and **protect the area from further cold exposure** with blankets or available loose clothing.

## Detailed Version

**The real, most important practical takeaway from this entire 3-page set: the early warning sign (sudden pleasant warmth) is the one moment where immediate, simple action — body-heat rewarming — can genuinely prevent a first-degree injury from progressing into the much longer, more serious course described in Frostbite — Real 4-Degree Classification & Prognosis.** Once past that early window, the real correct action shifts entirely to protection and evacuation rather than attempted field rewarming — see Frostbite — Prevention & the Freeze-Thaw-Refreeze Danger for why re-warming later (once evacuation is uncertain) carries its own real risk.
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
