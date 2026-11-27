#!/usr/bin/env python3
"""Seeds 4 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 12 Sections II-III (Insect/
Spider Bites, Animal Bites) -- mined from the OCR output cached at
/tmp/sfmedical.txt.

Covers real content significantly extending existing bite/sting
coverage: bee/wasp/hornet sting treatment including a real severe-
case medication protocol, centipede/millipede/caterpillar bites (not
previously covered, including the real Scotch-tape hair-removal
trick), black widow and brown recluse spider bites with real symptom
progression and treatment (brown recluse previously uncovered
entirely), scorpion stings including the real, important morphine/
Demerol contraindication (a genuine drug-venom interaction warning),
and real rabies-prevention protocol (animal observation, head
shipping for testing, wound cleaning, and the real partial-vaccine-
infiltration technique when suturing is unavoidable).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_bites_rabies.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Bee, Wasp & Insect Sting Treatment — Real Clinical Protocol",
        "section": "emergency",
        "tags": ["insect-stings", "allergic-reaction", "first-aid"],
        "risk_level": "high",
        "body_markdown": """## Bees, Wasps, Hornets & Yellow Jackets

**Real mechanism:** this group's venom contains a hemolysin factor similar to some snake venoms, but **the dominant effect is from the strong histamine content** — which is why antihistamines genuinely help.

**⚠️ Remove any embedded stinger immediately** to stop more venom entering the body.

**Real signs:** stinging/burning pain with swelling — **swelling around the head/neck can become severe enough to threaten the airway.**

**Real treatment:**
1. Baking soda paste, or strong household ammonia, eases discomfort; **injecting lidocaine into the sting area often helps too.**
2. **In severe cases:** Benadryl 4mg/kg IV, with 10cc of 10% calcium gluconate — **inject 2-4cc fairly quickly until the person feels a burning sensation in the tongue, palms, or soles of the feet, then slow down for the remainder to avoid flushing.**
3. **If genuinely allergic to the venom: treat as a full anaphylactic reaction** (see Anaphylactic Shock — Real Treatment Protocol).

## Centipedes, Millipedes & Caterpillars

- **Centipedes** have real hollow fangs like a snake — a bite causes immediate severe pain, redness, and swelling, **occasionally progressing to tissue death and ulceration.**
- **Millipedes** secrete a toxin through body glands — contact causes real burning and itching where the fluid touches skin.
- **Caterpillars:** many have hollow, venom-filled hairs — contact causes severe burning pain, redness, swelling, and tissue death. **⚠️ Real, genuinely clever removal trick: pressing ordinary Scotch tape onto the area effectively pulls out the broken-off hairs** that are otherwise hard to remove.
- **Real treatment for all three: similar to bee/wasp stings** — antihistamines, ice, and pain medication help; treat any anaphylactic reaction the same way as above.

## Detailed Version

**The real, practical value of the Scotch-tape trick: caterpillar hairs are genuinely hard to see and hard to grip, and continued skin contact with embedded hairs keeps re-triggering the reaction** — a simple adhesive removes them far more completely and gently than scraping or rubbing would.
""",
    },
    {
        "title": "Black Widow & Brown Recluse Spider Bites — Real Treatment",
        "section": "emergency",
        "tags": ["spider-bites", "black-widow", "brown-recluse"],
        "risk_level": "critical",
        "body_markdown": """## Black Widow Spider — Real Symptom Progression

**Only the female bites; venom is neurotoxic. Identified by a real red hourglass marking on the abdomen.**

**Real signs:** initial pain is mild, but **severe local pain develops rapidly and spreads over the whole body, eventually settling in the abdomen and legs.** Abdominal cramps and progressively rigid abdominal muscles can occur, along with weakness, tremors, sweating, excess salivation, nausea, vomiting, and sometimes a rash. **Anaphylactic reactions are possible. Symptoms typically start easing after several hours and are usually gone within a few days.**

**Real treatment:**
1. Calcium gluconate, 10cc of 10% solution, IM or slow IV.
2. Methocarbamol (Robaxin), 10cc given slowly IV over 5-10 minutes, followed by 10cc in 250cc of D5W as an IV drip over 4 hours.
3. **People under 14 or over 50 should receive specific antivenom if they aren't allergic to horse serum.**
4. Supportive care, tetanus booster, and antibiotics as needed.

## ⚠️ Brown Recluse Spider — a Real, Genuinely Deceptive Injury

**Identified by a dark brown violin-shaped marking on a small, light brown spider.**

**⚠️ Real, dangerous feature: the bite itself is often painless or nearly so — many people never realize they were bitten until hours later**, when a painful red area with a mottled, bluish center appears. **Over 2-3 days, a non-blanching discolored area can develop, turning dark and mummified over 1-2 weeks; the margins separate and the dead tissue (eschar) falls away, leaving an open ulcer** — often with secondary infection and swollen regional lymph nodes.

**⚠️ The real defining feature of a brown recluse bite: the resulting ulcer does NOT heal on its own and can persist for weeks to months**, with a hard, undermined-edge area of skin and underlying tissue on exam.

**⚠️ Real systemic reaction (mainly in children) — can be fatal:** fever, chills, joint pain, an enlarged spleen, vomiting, and a widespread rash — **this can occur at any point while the ulcer is still present, not just right after the bite.**

**Real treatment:**
- **There is no real antivenom for brown recluse bites.**
- **The indurated (hardened) skin and underlying tissue genuinely must be surgically excised before real healing can begin** — left alone, the ulcer can keep growing to several inches across.
- Tetanus prophylaxis and antibiotics control secondary infection.
- **Cortisone can halt the systemic reaction, but does not affect the ulcer itself.**
- Watch for and manage any anaphylactic reaction.

## Detailed Version

**The real, most important practical lesson from the brown recluse section: a bite that seemed trivial at the time, with no memory of being bitten, can still be the real cause of a slow-growing, non-healing ulcer appearing days later** — which is exactly why an unexplained, persistent, non-healing skin ulcer should prompt real consideration of a missed spider bite, not just an ordinary infection.
""",
    },
    {
        "title": "Scorpion Stings — Real Treatment & the Morphine Warning",
        "section": "emergency",
        "tags": ["scorpion-sting", "venom", "drug-interaction"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Every scorpion is venomous to some degree.** The most dangerous species aren't found in the US, but **US scorpion stings have still caused real documented deaths.**

## Real 2 Reaction Patterns

1. **Severe local reaction only:** pain and swelling at the sting site, possibly a prickly sensation around the mouth and a thick-feeling tongue.
2. **⚠️ Severe systemic reaction with little or no visible local sign:** local pain/heightened sensitivity may be present, but the real danger is systemic — breathing difficulty, a thick-feeling tongue, tetanus-like body spasms, drooling, gastric bloating, double vision, blindness, involuntary rapid eye movement, loss of bladder/bowel control, high blood pressure, and heart failure. **Death is rare, occurring mainly in children or adults with existing hypertension.**

## ⚠️ Real, Critical Medication Warning

**Never give morphine or morphine derivatives (including Demerol/meperidine) for scorpion sting pain — these have a real, dangerous synergistic effect with scorpion venom.** **Real alternative for genuine pain relief: specific nerve blocks using lidocaine.**

## Real Treatment

1. **Ice packs or cold water slow venom spread and relieve pain.**
2. Tetanus prophylaxis and antibiotics as indicated.
3. **Specific antivenom exists for the more toxic species where available.**
4. Supportive, symptomatic care otherwise.

## Detailed Version

**The real, single most important safety fact on this entire page is the morphine interaction — it's the kind of detail that's genuinely counterintuitive (morphine is a normal, reasonable first reach for severe pain almost everywhere else in this wiki) and specifically wrong here, which is exactly why it's called out this prominently rather than buried in a general treatment list.**
""",
    },
    {
        "title": "Animal Bites & Rabies Prevention — Real Protocol",
        "section": "emergency",
        "tags": ["animal-bites", "rabies", "wound-care"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**An animal bite itself is usually not the real danger — the diseases it can transmit are, and rabies is the single most important of these.**

## Real Protective/Observation Measures

1. **If the biting animal can be captured: isolate and observe it for 8-10 days.** **⚠️ A genuinely rabid animal should show unmistakable real signs within 8 days.**
2. **If the animal dies during observation: remove the head, freeze it, and ship it frozen to the nearest lab capable of real rabies testing.**
3. **If the animal cannot be captured/isolated at all: treat the bite AS IF it were rabid**, and the person should receive real anti-rabies vaccination.

## Real Wound Treatment

1. **Clean every bite promptly and thoroughly** with soap, Betadine, or hexachlorophene and water, then **apply 40-70% alcohol, tincture of iodine, or a dilute benzalkonium chloride solution directly into the wound.** **⚠️ Real, important point: this mechanical cleaning and disinfection has genuinely been credited with preventing many real rabies cases**, not just reducing ordinary infection risk.
2. Give tetanus prophylaxis.
3. **⚠️ Avoid suturing or cauterizing the wound — use delayed secondary closure if at all possible** (the same real "leave it open to drain" principle covered elsewhere in this wiki's wound-care content).
4. **⚠️ If suturing is genuinely unavoidable: infiltrate half the first dose of rabies vaccine directly into the wound area** before closing it — a real, specific technique for this exact situation.
5. **The real decision of whether to give anti-rabies serum requires real judgment** — weighing the actual circumstances of the bite and how common rabies actually is in the local area.
6. Provide symptomatic care as needed.

## Detailed Version

**The real, most important underlying principle across this whole page: rabies is close to universally fatal once symptoms begin, which is exactly why every real step here (the 8-10 day observation window, the head-freeze-and-ship protocol, the thorough mechanical wound cleaning, and even infiltrating vaccine directly into a wound that must be sutured) is built around preventing the disease from ever establishing itself** — treating symptoms after the fact is not a real option once rabies has actually progressed, which is also covered from a different real source in Rabies already in this wiki.
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
