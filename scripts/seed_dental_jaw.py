#!/usr/bin/env python3
"""Seeds 5 real pages from Where There Is No Dentist's Chapter 7
(Treating Some Common Problems, pages 85-123) -- mined from the real
text layer already extracted in this session (/tmp/dentist.txt).

Covers: Dislocated Jaw & TMJ Pain, Broken Jaw (Jaw Fracture), New
Tooth Growing In (erupting molar), Problems After Tooth Extraction
(dry socket, bleeding, tetanus), and Sores on the Face (draining
tooth abscess, Noma, spit gland infection). These are real,
page-numbered sections transcribed from the book's own diagnostic
chart for "trouble opening/closing the mouth" and "a sore on the
face" (pages 82-84), which point into this exact chapter.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_dental_jaw.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Dislocated Jaw & Jaw Joint (TMJ) Pain",
        "section": "reference",
        "tags": ["dental", "jaw", "tmj", "dislocation"],
        "risk_level": "moderate",
        "body_markdown": """## Dislocated Jaw

**Signs:** the mouth is stuck open — can't close the teeth or lips together, the lower jaw looks long and pointed, it hurts to press the joint just in front of the ear, speech is unclear. Most common in someone missing several back teeth (opening wide to yawn or shout lets the jaw joint slip too far forward and get stuck); it can also happen by accident during a tooth extraction.

**Treatment (real reduction technique):**
1. Support the person's head — have them sit on the floor with their head against a wall.
2. Kneel in front of them. Put your fingers under the jaw, outside the mouth. Put your thumbs beside the last molar on each side — **not on top of the molars themselves, since the person may bite down involuntarily.**
3. Press down hard with your thumbs, forcing the jaw down and back into position — **press down before pressing back.** If the muscles are too tight to move it, a doctor or dentist can sedate the person to relax them.
4. Support the jaw with a head-and-chin bandage for 3-4 days.
5. Aspirin or acetaminophen for pain. Soft foods for 2 weeks, warm wet cloth on the jaw, and avoid opening the mouth wide again — missing back teeth should be replaced with dentures if at all possible, since that's the real underlying cause.

## Pain in the Jaw Joint (TMJ)

The jaw has two joints, one in front of each ear, where the jawbone slides against the skull. Pain there has three real, distinct causes — treatment depends on telling them apart:

1. **Muscle tension** (stress/anxiety-related jaw clenching) — by far the most common. Treat with soft foods, a hot wet cloth against the jaw to relax the muscle, aspirin/acetaminophen for pain, and — genuinely part of the treatment — helping the person find some resolution to whatever is causing the tension.
2. **A fracture near the joint** (often from a blow to the *other* side of the face — always check the opposite jaw too) — needs an X-ray and an experienced dental worker to wire the teeth so the bone can heal. This is not a home-treatment situation.
3. **Teeth that don't meet properly** — check by imagining a line between the 2 front upper and 2 front lower teeth when the mouth is closed; if that line visibly shifts sideways when the mouth opens, the jaw itself is shifting unevenly, which can cause joint pain over time. Advise smaller bites and avoiding wide mouth-opening; a dentist can sometimes grind the teeth to correct the fit.

## Detailed Version

The real diagnostic value here is in the clicking/pain pattern: pain specifically in front of the ear that worsens with opening the mouth or chewing points at the joint itself, not the teeth or gums — and distinguishing simple tension (very treatable at home) from a fracture (needs real wiring) or a bite misalignment (needs a dentist's correction) changes the entire treatment path.
""",
    },
    {
        "title": "Broken Jaw (Jaw Fracture)",
        "section": "reference",
        "tags": ["dental", "jaw", "fracture", "trauma"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Signs of a broken or cracked jaw/facial bone:** a recent injury, the upper and lower teeth no longer meet normally when closed, trouble opening or closing the mouth properly, bleeding from between two teeth, swelling or bruising on the face/jaw, bleeding into the eye. (A cracked bone around a tooth's roots specifically: moving one loose tooth also moves the tooth next to it and the bone itself moves with it, with blood coming from under the gums.)

**This is a real emergency needing wiring by an experienced dental worker — but there are 5 real things to do immediately while arranging that:**

1. **Make sure the person can breathe.** Lie them on their side so the tongue and jaw fall forward (carry/transport them the same way — sitting with head forward if in a vehicle). Check inside the mouth for any loose broken tooth fragment that could block the airway and remove it now; a root left behind can be removed later by hospital staff.
2. **Stop the bleeding.** Wipe away dried blood to find the actual bleeding point; sew any deep facial cuts. Gentle, firm cotton gauze pressure against bleeding gums usually controls it. Bleeding *between* broken bone fragments inside the mouth is harder — pull the two sides together and hold them with ligature wire (0.20 gauge) looped around the strongest tooth on each side of the break, twisted tight with pliers/hemostat, ends bent toward the teeth so they don't poke the lips.
3. **Put on a head-and-chin bandage** to gently hold the jaw closed (teeth touching, or very slightly apart) — support it, don't forcibly pull it shut, and never tie it tight enough to choke the person.
4. **Give penicillin by injection for 5 days** to prevent infection inside the bone.
5. **Pain control** — aspirin 600mg by mouth 4-6x/day as needed is often enough; codeine (30mg, adult, 4-6x/day) if pain prevents sleep.

**Get the person to real medical/dental care within 1 week** — the jaw needs proper wiring, which must stay in place 4-6 weeks with weekly tightening visits.

## Caring for Someone Who Can't Eat While Wired Shut

**Milk-oil drink** (daily): 9 cups water + 3 cups milk powder + 150ml peanut oil or coconut milk + ½ cup honey or 1 cup sugar.

**Vegetable soup** (strained through a holed tin so it can be sucked through the teeth): ½ tin of fish or a handful of dried fish, 4 spoonfuls of peanut/palm oil, 6 sweet potatoes or small yams, a large handful of green leaves, 1 spoonful of salt — cooked together, then pressed through small holes in the bottom of a clean tin.

**Oral hygiene still matters even with the jaw wired:** scrub both the wires and teeth with a soft brush after eating, and rinse with warm salt water (2 cups/day) — neglecting this lets the mouth become infected and sore while already injured.

## Detailed Version

The real sequencing matters here: airway and bleeding come before anything else, because an unconscious or choking person with a jaw injury can die from the jaw itself blocking breathing — long before the fracture becomes the limiting problem. The wiring and weeks-long recovery are real necessities, but only once the person is stable enough to survive getting to that care.
""",
    },
    {
        "title": "New Tooth Growing In (Erupting Molar / Pericoronitis)",
        "section": "reference",
        "tags": ["dental", "children", "molar", "eruption"],
        "risk_level": "low",
        "body_markdown": """## Quick Version

When a new tooth (commonly a back molar) is still cutting through the gums, germs can get trapped under the loose flap of gum tissue still covering part of it — especially when the opposite tooth bites down directly on that sore flap each time the person chews.

**Signs:** toothache at the back of the jaw, limited mouth opening, a bad taste from the back of the mouth, sore throat, tender/sore skin over the new tooth — happening at the age when a new molar is expected to come in.

**Treatment:**
- **Do not pull the new tooth while it's infected and painful.** Treat the infection first; only after it clears do you assess (ideally with a dental X-ray) whether there's even room for the tooth to erupt fully.
- Warm salt-water rinses: 4 cups/day until normal mouth-opening returns, then 1 cup/day as maintenance until the tooth is fully in.
- Warm wet cloth against the jaw as often as possible; aspirin for pain.
- **Penicillin if there's fever, swelling, or significantly limited mouth-opening.**
- New molars are often genuinely difficult to extract — if extraction becomes necessary, get an experienced dental worker rather than attempting it yourself.

## Related: A Loose Baby Tooth

A baby tooth can be loose for several different real reasons, each with a different correct treatment — getting this right prevents unnecessary extractions or missed problems:

| Why it's loose | What to actually do |
|---|---|
| A permanent tooth is growing in underneath it | Explain to the parent/child what's happening; pull the loose baby tooth only if it's actively hurting the child |
| Gum disease or an old abscess ate away the supporting bone | Take the tooth out, especially if it hurts; address the underlying gum disease to protect the other teeth |
| The root itself is broken | Remove both parts; if the broken root resists removal, leave it and try again a week later |
| **The bone around the root is cracked** (bone moves when you push the tooth) | **Do NOT pull the tooth** — pulling it brings the cracked bone with it. Splint/wire it instead and let it heal |
| Another tooth bites too hard against it | Smooth the biting edges of both opposing teeth with a file or stone rather than extracting |

## Detailed Version

The real throughline: a loose or erupting tooth is not automatically "pull it" by default. The cracked-bone case above is the clearest example — the intuitive move (pull the loose tooth) is actively the wrong one, because the tooth isn't the problem; a cracked bone underneath it is, and extracting makes that worse, not better.
""",
    },
    {
        "title": "Problems After Tooth Extraction — Dry Socket, Bleeding & Tetanus",
        "section": "reference",
        "tags": ["dental", "extraction", "tetanus", "bleeding"],
        "risk_level": "high",
        "body_markdown": """## Dry Socket

Some pain after an extraction is normal, and aspirin is usually enough. **But if a severe new pain starts inside the socket 2-3 days after extraction, that's "dry socket"** and needs specific treatment, not just more aspirin.

**Treatment:**
1. Clean the socket — squirt warm water into it with a clean syringe (use a blunt needle so it can't injure the gum/bone), have the person spit it out, and repeat once more.
2. Prepare a dressing: soak 1-2 small pieces of cotton in eugenol (oil of cloves), or a local pain-relief medicine if available, and squeeze so it's damp, not wet.
3. Gently push one piece of dressing into each root space of the socket, then cover with plain cotton gauze and have the person bite against it — they can remove the plain gauze after an hour, but **the inner dressing stays in the socket** and gets changed daily until the pain stops.
4. Aspirin or acetaminophen for pain.

## Bleeding From the Socket

Some bleeding after extraction is expected — firm biting on cotton for about an hour usually controls it. Tell the person not to smoke, rinse, or spit for 1-2 days afterward, since that dislodges the healing blood clot.

**If bleeding continues despite firm cotton pressure:**
1. Check blood pressure — if it's high, that itself may need treatment to slow the bleeding.
2. Look for a torn/loose gum and suture it if found.
3. A real field technique: wrap moistened tea leaves in cotton gauze (tea contains tannins that help clotting) and have the person bite against it, or use cotton gauze soaked in cactus juice. Don't send the person home until the bleeding has actually stopped, and send them home with extra clean cotton in case it restarts.

## Tetanus After Extraction

**A genuinely serious risk specifically when extraction instruments were not properly sterilized.** Tetanus germs can be carried into the socket the same way they'd enter through any dirty wound.

**Signs:** the jaw becomes stiff and tight, swallowing becomes difficult, and the whole body develops sudden stiffness/spasms.

**This requires immediate real medical help** — treat as a true emergency (see Tetanus (Lockjaw)). Proper instrument sterilization before every extraction is the actual prevention, not a treatment given after signs appear.

## Detailed Version

The real pattern across all three of these: each one is a *delayed* complication (days, not minutes, after the extraction itself), which means the person is often no longer under direct observation when it starts. Giving clear aftercare instructions — and telling the person exactly what a worsening-not-improving pain, ongoing bleeding, or jaw stiffness would mean — matters as much as the extraction technique itself.
""",
    },
    {
        "title": "Sores on the Face — Draining Abscess, Noma & Spit Gland Infection",
        "section": "reference",
        "tags": ["dental", "noma", "abscess", "children"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Any sore on the cheek or under the chin should raise the question of a tooth or gum problem first** — the skin sore is often just where an underlying dental infection is draining, not an independent skin condition.

## A Draining Tooth Abscess

Look inside the mouth for an infected tooth in the area of the facial sore — it may have a large cavity, be loose, or be noticeably darker than the surrounding teeth (a sign the tooth is dead). **Pus draining onto the skin actually reduces pressure, so the person often reports little or no pain** — the absence of pain does not mean it's minor.

**Treatment:** extract the tooth, give penicillin for 7 days, then recheck the sore after the antibiotic course — if healed, treatment is complete. **If the sore is still open and pus can still be expressed, this needs experienced-worker follow-up**: testing whether the infection is penicillin-resistant, and an X-ray to check for dead bone fragments that are keeping the infection going (these must be surgically removed if present).

## ⚠️ Noma (Cancrum Oris) — a real pediatric emergency

Noma is a severe complication of untreated Vincent's Infection of the gums, seen almost exclusively in children, and **requires all three of these to be true**: (1) low general resistance — usually undernourished, anemic, sometimes with tuberculosis; (2) an existing Vincent's gum infection; (3) a recent serious illness such as measles or malaria. (Noma can also affect adults living with HIV.)

**Progression — recognizing it early matters enormously:**
1. Sore, itchy mouth and swollen gums.
2. Gums bleed with eating or cleaning; bad breath, excess spitting.
3. Loose teeth and loose bone fragments around the teeth.
4. Tight, dark red swelling of the cheek skin.
5. A black spot on the cheek breaks open into a hole connecting to the inside of the mouth.
6. A visible line separates dead tissue from healthy tissue.

**Why speed matters:** the bigger the hole gets before treatment starts, the tighter the scar that forms closing it — and a tight facial scar can permanently limit how wide the child can open their mouth, directly threatening their ability to eat enough to grow.

**Treatment must start immediately:**
1. **Fluids** — the child needs to overcome both dehydration and the underlying low resistance. Start the milk-oil drink (see Broken Jaw page for the recipe) by spoon or syringe if needed, placed against the healthy cheek to swallow.
2. **Treat the anemia** with iron (ferrous sulfate): over 6 years 200mg 3x/day, 3-6 years 100mg 3x/day, under 3 years 50mg 3x/day, continued for 3 months with food. (Expect black stool — this is a normal, harmless side effect, not a danger sign.) Add iron-rich food: meat, fish, eggs, dark green leafy vegetables, peas, beans.

## Spit (Saliva) Gland Infection

A small stone can block the duct that carries saliva from a spit gland (located in front of the ear or under the jaw) into the mouth — causing facial swelling and pain that gets noticeably worse when the person is hungry or smells/sees food (since saliva production increases but can't drain).

**Treatment:** penicillin for 5 days (short-acting crystalline penicillin first if the swelling/infection is severe), aspirin or acetaminophen for pain, a hot wet cloth on the swelling, and enough soft food to prevent hunger-triggered pain spikes. Once the acute infection resolves, a dentist or doctor can remove the stone itself.

## Detailed Version

The real unifying lesson across this whole page: a facial sore, swelling, or discoloration is a symptom location, not automatically the problem's location. In every condition here — draining abscess, Noma, spit gland infection — the actual cause is deeper (a dead tooth, an out-of-control gum infection, a blocked duct), and treating only the visible skin sign without addressing that underlying cause either fails outright or, in Noma's case, can cost precious time against a fast-worsening, disfiguring infection.
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
