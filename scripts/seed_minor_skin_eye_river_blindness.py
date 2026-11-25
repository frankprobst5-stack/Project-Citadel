#!/usr/bin/env python3
"""Seeds 3 more real pages from Where There Is No Doctor, closing out
this build-out's remaining minor skin and eye conditions plus one
real parasitic disease (River Blindness) -- mined from the real text
layer already extracted in this session (/tmp/nodoctor.txt).

Covers: Warts, Corns, Acne & Skin Cancer (Ch.?, p.210-212); Cross-Eyes,
Sty & Pterygium (p.223-224); River Blindness / Onchocerciasis (p.227-228).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_minor_skin_eye_river_blindness.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"

PAGES = [
    {
        "title": "Minor Skin Conditions — Warts, Corns, Acne & Skin Cancer",
        "section": "reference",
        "tags": ["skin", "warts", "acne", "skin-cancer"],
        "risk_level": "moderate",
        "body_markdown": """## Warts (Verrucae)

Most warts, especially in children, resolve on their own within 3-5 years without any treatment. **Avoid strong acids or poisonous "folk cure" plants** — these commonly cause burns or sores worse than the wart itself. Painful plantar warts (on the sole of the foot) can sometimes be removed by a health worker; they're easy to mistake for corns — see below.

## Corns

A hard, thick patch of skin where a shoe/sandal presses, or where one toe presses against another — can be genuinely painful.

**Treatment:**
1. Get footwear that doesn't press on the corn.
2. Soak the foot in warm water for 15 minutes, then file/rasp the corn down thin.
3. Pad around the corn (cotton or cardboard wrapped in soft cloth, with a hole cut around the corn itself) so it stops being pressed against the shoe or the neighboring toe.

## Pimples & Blackheads (Acne)

Common in young people, especially with oily skin — small lumps forming pus-filled whiteheads or dirt-filled blackheads, sometimes becoming larger and sore.

**Treatment:**
- Wash the face twice daily with soap and hot water; wash hair every 2 days if possible.
- Sunlight genuinely helps clear it.
- Eat well, drink plenty of water, get enough sleep.
- **Avoid waxy, oily, or greasy skin/hair products** — they make it worse.
- A nightly mixture of alcohol with a little sulfur (10 parts alcohol : 1 part sulfur) applied to the face.
- **For severe cases** (lumps and pockets of pus not responding to the above): tetracycline — 1 capsule 4x/day for 3 days, then 2 capsules daily, sometimes continuing at 1-2 capsules daily for months.

## ⚠️ Skin Cancer

Most common in light-skinned people with heavy sun exposure, typically appearing where the sun hits hardest: the ear, cheekbone/temple, nose, or lips. **Usually starts as a small pearl-colored ring with a depressed center, growing gradually.**

**Most skin cancers are not dangerous if treated in time** — but treatment requires real surgical removal. **Any chronic, non-healing sore in these sun-exposed areas should be evaluated by a health worker as a possible skin cancer**, not dismissed as an ordinary sore.

**Prevention:** sun protection and a hat for light-skinned individuals; zinc oxide ointment is a cheap, effective sunscreen, especially useful for anyone who has already had skin cancer and must continue working outdoors.

## Detailed Version

The real throughline connecting these four conditions: three (warts, corns, ordinary acne) are genuinely low-stakes and often self-resolving or simply managed, while the fourth (a chronic, slowly growing sore in a sun-exposed spot) is the one that must not be treated with the same "wait and see" patience — the pearl-colored-ring appearance and persistence beyond normal healing time are the real distinguishing signs worth remembering.
""",
    },
    {
        "title": "Minor Eye Conditions — Cross-Eyes, Sty & Pterygium",
        "section": "reference",
        "tags": ["eyes", "strabismus", "sty", "pterygium"],
        "risk_level": "low",
        "body_markdown": """## Cross-Eyes & Wandering ("Lazy") Eye (Strabismus)

**If the eye sometimes wanders but also looks forward normally at other times, this usually isn't a concern** — it typically straightens with time. **But if the eye is consistently turned the wrong way and the child isn't treated early, that eye may never develop normal vision.** See an eye doctor as soon as possible — patching the good eye, surgery, or special glasses may help. **Surgery done later in life can straighten the eye's appearance but will not restore vision in a weak eye that missed early treatment** — the timing genuinely matters more than the cosmetic outcome.

**Every child's eyesight should be checked as early as possible, ideally around age 4**, testing each eye separately (using an "E" chart) — a problem affecting only one eye is otherwise easy to miss since the other eye compensates.

## Sty (Hordeolum)

A red, swollen lump on the eyelid, usually near its edge. **Treatment:** warm, moist compresses with a little salt in the water; antibiotic eye ointment 3x/day helps prevent recurrence.

## Pterygium

A fleshy thickening that slowly grows from the white of the eye (near the nose side) onto the cornea — caused in part by sunlight, wind, and dust exposure. Dark glasses can ease irritation and slow its growth. **It should be surgically removed before it reaches the pupil** (once there, it threatens vision) — though it unfortunately often regrows after surgery. **Folk treatments using powdered shells do more harm than good.** Cold compresses, or chamomile eye drops (boiled, strained, cooled, unsweetened), can ease itching and burning in the meantime.

## Detailed Version

Strabismus is the one genuinely time-sensitive condition on this page — unlike a sty or a slow-growing pterygium, a persistently wandering eye in a young child has a real, narrow window during which treatment can still prevent permanent vision loss in that eye; waiting to see if it resolves "on its own" past early childhood is where the real risk lies.
""",
    },
    {
        "title": "River Blindness (Onchocerciasis)",
        "section": "reference",
        "tags": ["river-blindness", "onchocerciasis", "parasite", "blindness"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

A parasitic worm infection spread by the bite of infected black flies (small, hump-backed gnats that breed in fast-running water) — common in parts of Africa, southern Mexico, Central America, and northern South America. **Left untreated, it's a real and preventable cause of blindness.**

## Signs — a slow, multi-stage progression

- **Months after an infected bite:** painless lumps form under the skin (head/upper body in the Americas; chest/lower body/thighs in Africa) — usually just 3-6 lumps, growing slowly to 2-3cm.
- Itching as the baby worms spread through the body; aching in the back, shoulders, or hip joints, or general body-wide aches.
- Swollen lymph nodes in the groin.
- **Thickened skin with enlarged pores** (an "orange peel" texture) — best seen by shining light across the skin from one side.
- **Untreated, progresses to:** wrinkled, prematurely aged-looking skin; white patches on the lower legs; a dry rash on the limbs and trunk.
- **⚠️ Eye involvement is the real danger:** starts as redness and tearing, progresses to iritis, then a dull/pitted cornea (resembling vitamin A deficiency's xerophthalmia) — and finally vision loss from corneal scarring, cataract, or glaucoma.

## Treatment

**Early treatment genuinely prevents blindness — in any region where river blindness occurs, seek testing and treatment at the first signs, don't wait for eye involvement.**
- **Ivermectin (Mectizan) is the real first-choice medicine** — often available free through local health departments in affected regions.
- Diethylcarbamazine and suramin are alternative medicines, but **can cause real harm, especially once eye damage has already begun — these should only be given by an experienced health worker**, not administered casually.
- Antihistamines help manage the itching.
- Early surgical removal of the skin lumps reduces the worm burden.

## Prevention

- Clear brush and vegetation from the banks of fast-running streams, where black flies breed.
- **Avoid sleeping outdoors, especially during the day** — that's when black flies typically bite.
- Cooperate with any organized black-fly control programs in the area.

## Detailed Version

The real reason early treatment matters so much here: everything before eye involvement (the skin lumps, itching, joint aches) is uncomfortable but reversible. Once the disease reaches the eye and progresses to corneal scarring, cataract, or glaucoma, **the resulting vision loss is permanent** — which is exactly why the guidance is to seek testing at the very first signs in an at-risk region, not to wait until symptoms become severe enough to seem urgent.
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
                "source_url": NO_DOCTOR_PDF_URL,
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
