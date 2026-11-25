#!/usr/bin/env python3
"""Seeds 3 real pages from Where There Is No Dentist's Chapter 11
(Taking Out a Tooth, pages 153-167) -- mined from the real text layer
already extracted in this session (/tmp/dentist.txt). This is the
core "no dentist" skill the user specifically named this book for:
real tooth-extraction technique, not just diagnosis.

Covers: when to pull a tooth + pre-extraction health screening, the
real step-by-step extraction + suturing + aftercare technique, and
real complications (broken roots, root pushed into the sinus, bone
chips, post-extraction swelling).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_tooth_extraction.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Tooth Extraction — When to Pull & Health Screening",
        "section": "reference",
        "tags": ["dental", "extraction", "screening"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Not every painful tooth needs to come out.** Some problems — an abscessed tooth that could take root-canal treatment, a loose tooth that could be wired — need an experienced dental worker's skill to save, not pull. **Pull a tooth only for one of these 3 real reasons:**
1. It hurts constantly, or hurts enough to wake the person at night.
2. It's loose and painful when moved.
3. It has a broken root, or a broken top with an exposed nerve.

**This is a skill to learn hands-on from someone experienced, not purely from a book** — find an experienced dental worker who can both demonstrate the technique and then watch you attempt it yourself.

## Before You Begin: Ask These 5 Screening Questions

Explain what to expect, then ask:

1. **"Do you bleed a lot when your skin is cut?"** — they may bleed heavily when the tooth comes out. Explain aftercare very carefully, and consider placing a suture to hold the gums tightly together.
2. **"Do you have swollen feet or difficulty breathing?"** — possible heart disease. Ask specifically what medicine they take: **heparin, Coumadin, and warfarin are anticoagulants** that block normal clotting — if the person takes one, proceed only with extra caution (digitalis is a different heart medicine and is NOT an anticoagulant). Even if not on an anticoagulant, **never use more than 2 cartridges of local anesthetic** — the epinephrine inside it can harm a weak heart.
3. **"Do you have any allergies?"** — they may be allergic to aspirin, penicillin, erythromycin, or other medicines commonly used. Identify the specific medicine that caused a past reaction and substitute a different one.
4. **"Are you diabetic?"** — the wound may heal slowly and is more prone to infection. Watch the extraction site carefully afterward and start antibiotics promptly if infection begins.
5. **"Are you pregnant?"** — during the last month of pregnancy, extraction may be too uncomfortable; control any infection with a 5-day penicillin course and wait to extract until after the baby is born. Also wait if the woman has high blood pressure, since bleeding risk during extraction is higher.

## Be Patient, Careful, and Considerate

- Inject local anesthetic slowly in the right place, and actually test that the area is numb before starting — **if the person says it still hurts, believe them and give more anesthetic**, rather than proceeding anyway.
- Use the correct instrument correctly — careful technique avoids breaking the tooth. When removing a baby tooth, take extra care not to injure the permanent tooth growing underneath it.
- **Explain everything as you go**, including anything that will hurt even a little (e.g., describing the feeling of pressure, and even demonstrating it by pressing on the person's arm first) — and explain afterward what was done and what home care is needed.

## Detailed Version

The real judgment call underlying this whole page: deciding *not* to pull a tooth — because it could be saved, or because a screening answer changes the risk — is as much a part of this skill as the extraction technique itself. A pulled tooth cannot be put back; the screening questions exist specifically to catch the cases where skipping them turns a routine extraction into a genuinely dangerous one.
""",
    },
    {
        "title": "Tooth Extraction — Step-by-Step Technique",
        "section": "reference",
        "tags": ["dental", "extraction", "surgery"],
        "risk_level": "high",
        "body_markdown": """## The 4 Basic Instruments

You can extract most teeth with just these 4: a spoon or probe (separates gum from tooth), a straight elevator (loosens the tooth or lifts out a broken root), and two forceps — one shaped for upper teeth, one for lower. (Specialized "cowhorn"/"hawk's bill" forceps and curved Cryer elevators help with tougher back-molar extractions, but add real cost.)

## Setup

Work somewhere bright — sunlight or a lamp, plus a dental mirror to direct more light into the mouth. Use a chair with a high enough back to support the head. **Positioning matters for leverage:** for a lower tooth you push down then pull up, so seat the person low (stand on a box yourself if needed); for an upper tooth you push up then pull down, so seat the person higher (cushions under them work). Wash your hands and put on clean gloves; make sure every instrument is sterile — this is the actual infection-prevention step, not an afterthought.

## The 8 Real Steps

**1. Explain what you're doing** — how many teeth, why — and begin only once the person understands and agrees.

**2. Inject local anesthetic slowly**, in the correct spot (the injection technique differs for upper vs. lower teeth — see Chapter 9 for the injection method itself). Wait 5 minutes, then actually test that the area is numb before starting. If the person still feels pain, give another injection — don't proceed on an assumption.

**3. Separate the gum from the tooth.** The gum attaches to the tooth inside a shallow pocket; skipping this step lets the gum tear during extraction (which bleeds more and heals slower). Slide an instrument along the side of the tooth into that pocket, find where the gum attaches, and work the instrument back and forth to separate it — on both the cheek side and tongue side. Control the depth carefully; the attached gum is thin.

**4. Loosen the tooth with a straight elevator** before pulling a strong tooth — a loosened tooth is far less likely to break.
   - **Caution:** used wrong, a straight elevator does more harm than good. Brace your first finger against the *neighboring* tooth as you turn the handle, to control the blade and avoid loosening (or injuring) the good tooth next to it.
   - Slide the curved face of the blade down the side of the bad tooth, as far under the gum as possible, then turn the handle to rock the tooth's top backward. **Apply pressure against the bone, not against the neighboring tooth.**

**5. Take out the tooth with forceps.** Push the forceps as far up the root as possible — the beaks must grip the root under the gumline, not just the visible crown. Support the surrounding bone with your other hand; you'll feel it expand slightly as the tooth loosens.
   - **A tooth with 1 root: turn/rotate it.** **A tooth with 2-3 roots: tip it back and forth** rather than rotating.
   - **Take your time** — squeezing too hard or rushing is what breaks a tooth. Think of it like working a post out of the ground: small movements, repeated, gradually loosen it enough to lift free.
   - Front teeth typically come straight out; back teeth usually come out toward the cheek (though some lower molars come out toward the tongue).
   - **"Cowhorn" forceps for lower molars** work differently: fit the points under the gum between the roots, then squeeze gently while moving up-down and side-to-side to force the points further between the roots. **Never use cowhorn forceps on a baby molar** — the pointed beaks can damage the permanent tooth growing underneath.
   - **After the tooth is out, inspect the roots** for any broken-off fragment left behind — remove it if you can, since a retained root fragment can seed a later infection.

**6. Stop the bleeding.** Squeeze the sides of the now-empty socket back into their normal shape, cover with cotton gauze, and have the person bite firmly for 30 minutes (2 hours for a child).
   - **If 2+ adjacent teeth were removed, suture the gums together:** use sterile needle and thread (boiled 30 minutes), pass the needle through the looser gum first then the firmer one, tie 2 knots (tightened to the side of the wound, not on top of it), and trim the thread ends to about 0.5cm (too long irritates the tongue; too short and the knot can open). Have the person bite on gauze for 1 hour and return in 1 week to remove the sutures (self-dissolving suture material exists and skips that return visit, but costs more).

**7. Explain home aftercare** — the person's mouth is still numb, so they can't yet feel what you're describing:
   - Bite firmly on gauze for an hour (longer if bleeding resumes); send extra gauze home with them.
   - Aspirin/acetaminophen for pain as needed, every 3-4 hours.
   - **Keep the head elevated while resting** — it reduces bleeding and pain.
   - **Do NOT rinse the mouth** — despite being common local practice, rinsing washes away the protective blood clot and is actively harmful.
   - **Avoid hot drinks** (tea, coffee — heat encourages bleeding); cool liquids and plenty of water are fine.
   - Keep eating soft food, chewing on the opposite side from the wound.
   - **Starting on day 2**, resume gentle cleaning with warm salt-water rinses and careful brushing near the socket.

**8. Discuss replacing the tooth with a false tooth.** Leaving the gap unfilled lets neighboring teeth drift into the space over time, weakening their own roots until they, too, eventually loosen and need extraction — "like removing a brick from a wall and letting the area around it crumble." A plastic replacement tooth isn't for chewing — it exists to hold the remaining teeth in healthy position (and has the real side benefit of a more youthful appearance).

## Detailed Version

The single most failure-prone step in this whole sequence is skipping step 3 (separating the gum) or rushing step 5 (forcing instead of gradually working the tooth loose) — both save a minute or two in the moment but routinely cause the two most common avoidable complications: torn, slow-healing gums, and a broken tooth root left behind in the bone.
""",
    },
    {
        "title": "Tooth Extraction — Broken Roots, Sinus & Swelling",
        "section": "reference",
        "tags": ["dental", "extraction", "complications"],
        "risk_level": "high",
        "body_markdown": """## Broken Roots

**If you can see the broken root, try to remove it — a root left inside the bone can start an infection.**

**Removing a broken UPPER root:** slide a straight elevator's blade along the socket wall until it meets the root, force the blade between the root and the socket wall, work the root loose by moving it progressively further from the wall, then grab the loosened root and pull it out.

**Removing a broken LOWER root** (molar): use a straight or curved elevator — break away a bit of bone between the root and the blade, force the blade between the root and the socket, move the root away from the socket wall, then grab and remove it.

**⚠️ Important exception: if the broken root is small, it's often better to leave it in the socket.** Within about a week it will loosen on its own and come out much more easily — forcing it immediately risks pushing it deeper or damaging surrounding bone.

## Root Pushed Into the Sinus (Upper Teeth Only)

An upper tooth root that seems to vanish during extraction may have been pushed into the sinus above it. **Do not try to search for it yourself.** Cover the socket with gauze and send the person to a hospital — retrieving it requires a real surgical procedure to open the sinus. **Tell the person not to blow their nose** in the meantime; that forces air through the opening and prevents it from healing.

## Bone Chips & Tags of Loose Flesh

Small loose bone fragments left in the socket can cause ongoing bleeding and slow healing — reach in gently with an elevator or spoon instrument to feel for and lift them out (give more local anesthetic first if needed). Small, harmless tags of loose flesh that bother the person can be trimmed free with sterile scissors while held steady with cotton tweezers. **Resume gentle warm-water rinsing to toughen the gums and aid healing — but not within the first 24 hours.**

## Bleeding That Won't Stop

If the first gauze doesn't control bleeding, place fresh gauze and wait 5 minutes to reassess. If that still doesn't work, place a suture (see Tooth Extraction — Step-by-Step Technique).

## Swelling

**Before swelling starts** (especially after a difficult or lengthy extraction): cold, wet cloth against the face helps prevent it.
**Once swelling has already developed:** switch to heat — a hot wet cloth, 30 minutes on / 30 minutes off, being careful not to burn the skin.
**A large swelling usually signals infection and needs real additional treatment** (see Dental Emergencies — Tooth Abscess), not just cold/heat management alone.

## Related complications covered elsewhere

- **Strong, steady pain lasting several days** after extraction → see Problems After Tooth Extraction — Dry Socket, Bleeding & Tetanus.
- **Jaw dislocated during the extraction itself** (from pressure applied while pulling) → see Dislocated Jaw & Jaw Joint (TMJ) Pain — the same reduction technique applies regardless of cause.

## Detailed Version

The real pattern tying these complications together: several of the correct responses are the opposite of the intuitive first instinct — leaving a small broken root alone rather than digging for it, never searching for a root lost into the sinus, and switching from cold to heat only once swelling has already set in rather than applying one or the other throughout. Getting the timing and the "don't" right matters as much as the active technique.
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
