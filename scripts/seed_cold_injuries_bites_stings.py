#!/usr/bin/env python3
"""Seeds 3 more real Emergency Now pages: Frostbite & Cold Injuries,
Snakebite, and Insect Stings & Anaphylaxis.

Frostbite/chilblain/immersion foot is mined directly from Medical/
FM-4-25-11-First_Aid.pdf's Chapter 5 -- cross-checked against current
guidance and found consistent (it correctly says never rub a frostbite
injury with snow, massage it, or expose it to direct heat, which
matches current practice), so used as-is.

Snakebite is NOT drawn from that same manual's Chapter 6, even though
it's a real, text-extractable section -- its "constricting band"
instruction is now actively contraindicated: current medical consensus
(Mayo Clinic, and broader literature -- see "Tourniquets in snakebite:
a harmful tradition needing urgent public education") says any
constricting band or tourniquet on a snakebite risks worse local
tissue damage than the venom itself and should not be used. Same
discipline as Choking two batches ago: a real local PDF existing
doesn't make its technique current.

Insect Stings & Anaphylaxis draws its emergency-shock recognition from
the same manual (still accurate) plus current epinephrine-use guidance
from Mayo Clinic/Red Cross (via WebSearch -- both sites block direct
WebFetch with a 403).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_cold_injuries_bites_stings.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
FIRST_AID_PDF_URL = "/files/pdfs/Medical/FM-4-25-11-First_Aid.pdf"

PAGES = [
    {
        "title": "Frostbite & Other Cold Injuries",
        "tags": ["cold-weather", "frostbite", "first-aid"],
        "risk_level": "high",
        "source_url": FIRST_AID_PDF_URL,
        "body_markdown": """## Quick Version

**Signs of frostbite:** numbness, skin suddenly turns white/pale (light skin) or grayish (dark skin), followed by tingling; blisters, swelling, or tender areas; in deep frostbite the tissue feels solid/wooden to the touch and pain sensation is lost.

**First aid:**
- **Face, ears, nose:** cover with bare hands until sensation and color return.
- **Hands:** tuck under the armpits, against bare skin.
- **Feet:** if the person does NOT need to walk further, remove boots/socks and warm the feet against another person's body under clothing.

**Do NOT:** rub or massage the area, rub it with snow, expose it to a fire/stove/direct heat, or slap/chafe it.

**If the person must walk to get help: do not thaw the feet first.** Walking on thawed feet causes more damage than walking on (still numb) frozen ones — this sounds backwards, but re-freezing after thawing is far more destructive than staying frozen a bit longer during a short walk out.

## Detailed Version

Cold injury isn't just frostbite — this covers a real spectrum:

- **Chilblain:** repeated exposure of bare skin to cold (above freezing, 32-60°F). Swollen, red, tender, itchy skin, no tissue loss if treated — responds to body heat within minutes. Still get it checked; damage can be slower to show than it feels.
- **Immersion foot / trench foot:** feet wet for a long period at 32-50°F, especially in tight boots that restrict circulation. Can be serious enough to cause tissue loss. Dry the feet thoroughly and get the person evacuated.
- **Frostbite:** actual tissue freezing, usually below 32°F. Most common on cheeks, nose, ears, chin, wrists, hands, feet — the extremities and exposed skin.

**Why not rub/massage/direct-heat:** ice crystals in frozen tissue cause real mechanical damage if the area is rubbed or massaged, and thawing too fast with direct heat (fire, stove) risks burning tissue that's already compromised and may have lost pain sensation — the person may not feel the burn happening. Slow, gentle rewarming with body heat is the safe method precisely because it can't overshoot.

People with a prior cold injury are at real higher risk of another one — not necessarily the same body part.
""",
    },
    {
        "title": "Snakebite",
        "tags": ["snakebite", "first-aid"],
        "risk_level": "critical",
        "source_url": "https://www.mayoclinic.org/first-aid/first-aid-snake-bites/basics/art-20056681",
        "body_markdown": """## Quick Version

**Do:**
- Move away from the snake. Keep the person as still and calm as possible — movement and panic speed venom circulation.
- Remove rings/watches/anything tight from the bitten limb before swelling starts.
- Keep the bitten limb at or **below** heart level.
- Immobilize the limb loosely (a simple splint is fine) — minimize movement, don't try to walk it off.
- Clean the bite gently, cover with a clean dry dressing.
- Get to a hospital as fast as possible. If you can safely note the snake's color/pattern/size (never try to catch or kill it), that helps treatment — but don't delay getting help to do this.

**Do NOT:**
- Apply a tourniquet or any constricting/pressure band — this is now known to risk **worse** tissue damage than the bite itself, not better outcomes.
- Cut the wound or try to suck out venom.
- Apply ice.
- Give the person food, alcohol, caffeine, or any drugs.
- Elevate the bitten limb above heart level.

## Detailed Version

**Why the constricting-band advice changed:** older first-aid guidance (including some older military field manuals) recommended a tight band above and below a snakebite to slow venom spread. Current medical consensus has reversed this — restricting blood flow concentrates venom's damage locally, which can mean worse tissue necrosis and a higher chance of needing amputation, without reliably slowing the overall danger. This is a real, documented example of first-aid guidance correcting itself — treat any older printed source recommending a tourniquet/band for snakebite as outdated.

Most snakebites, even from venomous species, don't inject a fatal dose of venom — but you cannot tell from the outside whether this one did, so every snakebite from a species that could be venomous gets treated as a real emergency and gets the person to a hospital, not a wait-and-see approach.
""",
    },
    {
        "title": "Insect Stings & Anaphylaxis",
        "tags": ["anaphylaxis", "allergic-reaction", "first-aid"],
        "risk_level": "critical",
        "source_url": "https://www.redcross.org/take-a-class/resources/learn-first-aid/allergic-reaction-anaphylaxis",
        "body_markdown": """## Quick Version

**Anaphylaxis is a true medical emergency** — a severe, whole-body allergic reaction that can kill within minutes if untreated.

**Signs:** swelling of the face, lips, tongue, or throat; hives or widespread flushing; trouble breathing, wheezing, or a tight throat; dizziness or a sudden drop in responsiveness; sometimes vomiting or abdominal pain.

**What to do, immediately:**
1. **Call 911.**
2. **If the person has their own epinephrine auto-injector (EpiPen or similar), use it right away** — press firmly into the outer thigh (through clothing is fine), hold per the device's own instructions. Don't wait to see if symptoms improve on their own first.
3. Have the person lie down with legs elevated (unless breathing is easier sitting up — follow what actually helps them breathe).
4. Watch their breathing and pulse. Be ready to start CPR if they stop responding.
5. **A second epinephrine dose may be needed** if there's no improvement within about 5-15 minutes and a second auto-injector is available — but this still requires real emergency transport, not a substitute for the hospital.

## Detailed Version

Epinephrine works fast and is genuinely the right first response to anaphylaxis — but its effect wears off, and symptoms can return hours later even after an auto-injector seemed to work. **That's why calling 911 and getting to a hospital is still required even if epinephrine made things better** — this isn't a "just in case," it's because the reaction can recur.

If you know you (or someone in your household) has a serious insect/food allergy, keep an auto-injector within reach and check its expiration date regularly — an expired or degraded dose may not deliver full strength when it matters.
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
                "section": "emergency",
                "title": page["title"],
                "body_markdown": page["body_markdown"],
                "tags": page["tags"],
                "source_url": page["source_url"],
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
