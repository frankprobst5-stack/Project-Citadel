#!/usr/bin/env python3
"""Seeds 8 real pages mined from the two most comprehensive medical
references already in the Vault: Where There Is No Doctor (Hesperian
Health Guides, 25,065 real text lines) and Where There Is No Dentist
(Hesperian, 9,986 lines) -- both confirmed to have genuine text layers
before transcribing anything.

5 pages from Where There Is No Doctor: Fever, Dehydration & Oral
Rehydration Drink (the real "home mix" ORS recipe), Diarrhea &
Dysentery, Infected Wounds, and Right and Wrong Use of Medicines.

3 more pages from Where There Is No Dentist (adding to the Tooth
Abscess page from an earlier batch): Gum Disease, Broken Tooth, and
Knocked-Out Tooth.

Real judgment call on Knocked-Out Tooth: the book's own framing ("if
less than 12 hours, you can still put it back") is technically true --
reimplantation is attempted even after hours -- but current research
is much more specific about how much the odds actually drop with
time (85-97% success within 5 minutes, down to 20-40% past 60
minutes, 5-10% past 2 hours). The book's real step-by-step technique
(wash gently without scraping the root, slight turning motion to
reinsert) is used as-is; the urgency framing is corrected with current
sourcing so "12 hours" doesn't read as a comfortable window.

IMPORTANT STATUS NOTE for both books: this is a meaningful sample, not
anywhere close to full coverage. Where There Is No Doctor alone has 23
real chapters (skin problems, eye injuries, STIs, childbirth/midwifery,
family planning, children's and elderly health, and much more) --
these 5 pages cover maybe 2,500 of its 25,000+ lines. Neither book
should be deleted yet; there's substantially more real, useful content
left in both.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_no_doctor_no_dentist.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_DOCTOR_PDF_URL = "/files/pdfs/Medical/Where-There-is-no-Doctor-a-Village-Health-Care-Handbook.pdf"
NO_DENTIST_PDF_URL = "/files/pdfs/Medical/Where-There-is-No-Dentist.pdf"

PAGES = [
    {
        "title": "Fever — Recognition and Treatment",
        "section": "reference",
        "tags": ["fever", "illness"],
        "risk_level": "moderate",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

Fever isn't a sickness itself — it's a sign of one. A fever over 102°F (39°C) can signal something serious, especially in a small child.

1. **Uncover the person completely** — undress a feverish small child entirely until the fever comes down. Fresh air/a breeze helps lower fever; wrapping them up in blankets makes it worse, even though that feels backwards.
2. Give **acetaminophen** (safer for children) or aspirin (adults) to bring the fever down.
3. **Push fluids** — water, juice, soup. Watch urination: little or dark urine means give more fluids.
4. Try to identify and treat whatever's actually causing the fever.

**If the fever goes very high (over 104°F/40°C):**
1. Move to a cool place, remove clothing, fan the person.
2. Pour cool (not cold) water over them, or use cool wet cloths on the chest/forehead — change them often to keep them cool. Continue until the fever drops below 100°F (38°C).
3. Give plenty of cool water to drink.
4. **If the fever doesn't come down, the person loses consciousness, or seizures start — get medical help immediately.**

**Acetaminophen dosing (300mg tablets):** adults/12+: 2 tablets every 4 hours · ages 6-12: 1 tablet · ages 3-6: ½ tablet · under 3: ¼ tablet every 4 hours.

## Detailed Version

A high fever is most dangerous for small children specifically because it can trigger seizures — this is the real reason a child's fever gets treated more aggressively and watched more closely than an adult's. The cooling methods above (uncovering, cool water, fanning) work *with* the body's own fever response rather than fighting it chemically, which is why they're the first response even before medication.
""",
    },
    {
        "title": "Dehydration & Oral Rehydration Drink",
        "section": "reference",
        "tags": ["dehydration", "diarrhea", "ors"],
        "risk_level": "high",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

**Signs of dehydration:** thirst (often the earliest sign), little or dark urine, dry mouth, sunken eyes, a sunken soft spot (infants), and skin that doesn't spring back when pinched — lift a fold of skin between two fingers; if it stays "tented" instead of flattening right back out, that's dehydration.

**Don't wait for these signs once watery diarrhea or vomiting starts — act immediately.**

### The Real "Home Mix" Rehydration Drink (2 ways to make it)

**With sugar and salt**, per 1 liter (about 1 quart) of clean water:
- ½ level teaspoon salt
- 8 level teaspoons sugar (raw sugar or molasses works too)
- **Taste it before adding sugar — it should be less salty than tears.** Too much salt is dangerous.

**With powdered cereal and salt** (if sugar isn't available) — rice is best, or finely ground maize/wheat/sorghum, or mashed cooked potato, per 1 liter water:
- ½ level teaspoon salt
- 8 heaping teaspoons (or 2 handfuls) powdered cereal
- Boil 5-7 minutes into a thin gruel, cool quickly before giving it.

**Either recipe:** adding ½ cup of fruit juice, coconut water, or mashed ripe banana adds potassium and can help the person accept more of it.

**Dosing:** sips every 5 minutes, day and night, until normal urination returns. A large person needs 3+ liters a day; a small child needs at least 1 liter a day (or roughly 1 glass per watery stool). Keep giving small sips even if the person vomits — not all of it comes back up.

**If dehydration gets worse, or any other danger sign appears — get real medical help; IV fluids may be needed.**

## Detailed Version

Most deaths from diarrhea are actually deaths from the dehydration it causes, not the infection itself — this is why the rehydration drink matters more than finding the exact cause of the diarrhea. A commercial Oral Rehydration Salts (ORS) packet works the same way (sugar, salt, citrate, potassium) if you have one, but a correctly-made homemade version — especially the cereal-based one — is often cheaper, safer, and just as effective.

**Taste-test every batch before giving it, every time** — this matters for two real reasons: too much salt in the sugar-salt version is dangerous, and a cereal-based drink can spoil within hours in hot weather, so a batch that tasted right in the morning may not be safe by evening.
""",
    },
    {
        "title": "Diarrhea & Dysentery — Home Care",
        "section": "reference",
        "tags": ["diarrhea", "dysentery", "illness"],
        "risk_level": "high",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

**Diarrhea** = loose or watery stools. **Dysentery** = diarrhea with visible mucus or blood — a more serious sign.

**Most diarrhea needs no medicine at all** — the real treatment is the Rehydration Drink (see that page) plus continuing to feed the person, not starving the illness out. A well-nourished person usually recovers in a few days; diarrhea is both more common and more dangerous in a poorly-nourished child, which is why nutrition and diarrhea risk are tangled together.

**Keep doing, even during active diarrhea:**
- Give the Rehydration Drink constantly, in small frequent sips.
- Keep feeding — small frequent meals of whatever the person will accept, even if appetite is low.
- For babies: keep breastfeeding, before other drinks, not instead of them.

**Seek real medical help if:** blood appears in the stool, fever develops, the person becomes unusually drowsy or hard to wake, dehydration signs appear despite rehydration efforts, or diarrhea in a small child lasts more than a couple of days without improvement.

## Detailed Version

The real causes span a wide range: poor nutrition (which both causes and worsens diarrhea — a vicious cycle), unclean water/lack of latrines, viral "intestinal flu," bacterial or parasitic gut infections, worm infections, infections entirely outside the gut (ear infections, measles), difficulty digesting a new food, food allergies, and even a side effect of certain antibiotics. Most of the time, treating the dehydration and keeping the person fed matters more than pinning down which of these caused it — identifying the exact cause changes treatment far less often than people expect.
""",
    },
    {
        "title": "Infected Wounds",
        "section": "reference",
        "tags": ["wound-care", "infection"],
        "risk_level": "high",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

**A wound is infected if:** it's red, swollen, hot, and painful; it has pus; or it starts smelling bad.

**The infection is spreading if:** fever develops, a red line appears above the wound (tracking toward the heart), or nearby lymph nodes ("glands") swell and become tender.

**Treatment:**
- Hot compresses over the wound, 20 minutes, 4 times a day (or soak an infected hand/foot in a bucket of hot water).
- Keep the infected part elevated above heart level and at rest.
- If infection is severe, or the person isn't vaccinated against tetanus, antibiotics are needed (penicillin plus metronidazole, under real medical guidance on dosing).

**Emergency warning — possible gangrene:** a bad smell, brown/gray ooze, or skin around the wound turning black with air bubbles or blisters forming. **Get medical help immediately.**

## Detailed Version

**Some wounds are inherently higher-risk and need real care even if they look "fine" at first:** dirty wounds or wounds from dirty objects, deep puncture wounds that didn't bleed much, wounds from an animal enclosure (barns, pens), heavily bruised/mashed wounds, bites (especially from pigs, dogs, or people), and bullet wounds. For these:
1. Wash thoroughly with boiled water and soap — remove every visible speck of dirt, clot, and dead tissue.
2. These high-risk wounds often need a real antibiotic course, which requires real medical guidance on which one and how much.
3. **These wounds should NOT be closed with stitches or butterfly bandages** — left open, specifically because closing a contaminated wound traps infection-causing material inside where it can't drain.

**Tetanus risk is real for anyone unvaccinated with a high-risk wound** — even a small one. This is the actual reason wound care and tetanus vaccination status go together in every real triage conversation: a tiny puncture wound can be more dangerous for tetanus risk than a large clean cut.

Swollen lymph node location is a real diagnostic clue, not just a symptom: behind the ear often points to a scalp/head infection, below the jaw to a tooth or throat infection, in the armpit to an arm/breast infection, in the groin to a leg/foot/genital infection.
""",
    },
    {
        "title": "Right and Wrong Use of Medicines",
        "section": "reference",
        "tags": ["medication", "medicine-safety"],
        "risk_level": "high",
        "source_url": NO_DOCTOR_PDF_URL,
        "body_markdown": """## Quick Version

**Five real rules for using any medicine:**
1. Use medicine only when it's actually necessary — not just because it feels like "doing something."
2. Know the correct use and real precautions before taking anything.
3. Use the correct dose — not more, not less.
4. If it isn't helping, or it's causing problems, stop.
5. When in doubt, get real medical advice.

**Every medicine carries some real risk — there's no such thing as a risk-free drug, only drugs worth the risk for a given problem.**

**Common dangerous misuses, worth knowing specifically:**
- **Antibiotics for things they don't treat** — colds, simple bruises, or ordinary aches never need antibiotics; antibiotics only work against bacterial infections, and misusing them doesn't just fail to help, it breeds resistant bacteria.
- **Injections "because they seem stronger"** — a real, persistent myth. Oral medicine often works just as well with less risk; injections carry real additional danger and should be limited to situations that genuinely need them.
- **Steroids (cortisone-type drugs) for minor aches** — these are powerful, with serious real side effects (weakened infection defense, stomach bleeding, bone weakening) when used for more than a few days; reserve them for the severe conditions they're actually meant for.
- **"Growth tonics" / anabolic steroids for children** — a real, documented harm: they can cause a child to stop growing *sooner*, ending up shorter overall, among other serious effects. Food solves malnutrition; these drugs don't.

## Detailed Version

**The core idea worth internalizing: more medicine is not inherently better care.** A real, repeated theme in community health work is that both lay caregivers *and* trained health workers over-prescribe — partly because patients expect to leave with something. Asking "is this actually needed?" before taking or giving any medicine is a real, low-cost safety habit, not second-guessing a professional.

This page intentionally does not give blanket dosing guidance for prescription antibiotics or steroids — those need real, current medical guidance matched to the specific drug and situation, which is exactly the kind of judgment call rule #5 above is pointing at.
""",
    },
    {
        "title": "Gum Disease",
        "section": "reference",
        "tags": ["dental", "gum-disease"],
        "risk_level": "moderate",
        "source_url": NO_DENTIST_PDF_URL,
        "body_markdown": """## Quick Version

**Signs:** gums are red instead of pink, loose instead of tight against the tooth, bleed when brushing/flossing or when pressed, bad breath/bad taste.

**Treatment — the only real fix is removing plaque/tartar and keeping teeth clean going forward:**
1. Clean teeth more carefully right at the gumline.
2. Rinse with warm salt water — 4 cups a day until bleeding stops, then 1 cup a day to maintain healthy gums.
3. Eat fresh fruits and vegetables (citrus, pineapple, tomatoes, leafy greens genuinely help gum strength).
4. Gently remove any tartar caught under the gum edge.

**More serious: Vincent's infection ("trench mouth")** — gums between teeth dying and turning gray, pus and old blood around teeth, burning pain, bad mouth odor. This can worsen a child's malnutrition (painful chewing → eating less) and needs real follow-up over roughly 2 weeks: antibiotics if the person is already sick, careful cleaning of pus/tartar, and rinsing with a mild antiseptic solution (weaker concentration for a child than an adult).

## Detailed Version

Weak gums from poor nutrition can't resist infection as well — this is specifically why pregnant women and people with weakened immune systems (the book specifically names HIV) need extra care with both diet and tooth-cleaning, since a gum infection can progress faster when the body's defenses are already compromised.

A pregnant woman's gum swelling that doesn't respond to normal cleaning/rinsing sometimes needs a minor procedure — but that should wait until after the baby is born unless it's causing a real problem sooner.
""",
    },
    {
        "title": "Broken Tooth",
        "section": "reference",
        "tags": ["dental", "tooth-injury"],
        "risk_level": "moderate",
        "source_url": NO_DENTIST_PDF_URL,
        "body_markdown": """## Quick Version

**Signs:** pain when breathing air or drinking, bleeding from the gums around the tooth, the tooth moves when touched.

**Whether it can be saved depends on two things:**
- **Is the nerve still covered?** If not (and no one present can do a real root canal), the tooth has to come out — saliva has already reached inside it and infection has started.
- **Is the root broken?** Push gently against the tooth while feeling the bone around its root: if the tooth moves but the bone doesn't, the root is likely broken. If both move together, the root is probably intact (though the surrounding bone could still be broken).

**If the nerve is still covered and the root isn't broken, the tooth can likely be saved:**
- File down any sharp edges so they don't cut the tongue.
- Rest that tooth — chew on the other side.
- Avoid very hot/cold drinks and spicy food.
- Watch it: a tooth turning dark, or a "gum bubble" developing nearby, means the tooth is dying and needs to come out (unless real nerve/root-canal treatment is available).

## Detailed Version

A real dental professional can later cap or fill the broken part once reachable — the steps above are specifically about keeping the tooth viable and the person comfortable until that's possible, not a permanent fix.
""",
    },
    {
        "title": "Knocked-Out Tooth",
        "section": "emergency",
        "tags": ["dental", "tooth-injury"],
        "risk_level": "high",
        "source_url": NO_DENTIST_PDF_URL,
        "body_markdown": """## Quick Version

**Minutes matter enormously here — this is one of the few dental injuries where speed genuinely determines whether the tooth survives.**

**Baby tooth:** don't try to put it back — have the child bite on cotton to stop bleeding, and let the permanent tooth grow in later (it may take a bit longer than usual).

**Permanent (adult) tooth — act immediately:**
1. **Pick it up by the crown (the chewing surface), never the root.** Don't scrape, scrub, or remove any tissue from the root — that tissue is what helps it reattach.
2. Rinse it gently with saline, milk, or clean water only if visibly dirty — don't scrub it.
3. **Try to reinsert it into the socket right away**, with a gentle turning motion, biting edge level with the neighboring teeth. If you can't get it back in, keep it moist — in milk if available, otherwise in the person's own saliva (inside the cheek) — never dry, and never in plain tap water for a prolonged time.
4. **Get to a dentist or emergency room immediately — treat this as a true race against time, not a same-day errand.**

## Detailed Version

Real success-rate research is specific about this: reimplantation within about 5 minutes succeeds roughly 85-97% of the time; by 60 minutes that drops to roughly 20-40%; past 2 hours, success falls to around 5-10%. The practical takeaway: reinserting it yourself in the first few minutes gives a dramatically better outcome than waiting for a dentist, even a nearby one — don't wait if you're physically able to do it.

**The technique itself** (from *Where There Is No Dentist*): wash the tooth gently without scraping the root or socket, then push it back into the socket with a slight back-and-forth turning motion until its biting edge matches the teeth beside it. Expect it to hurt without anesthetic — that's normal, not a sign something's going wrong.

If it's genuinely impossible to reinsert (the socket itself is damaged, or you can't manage it), cold whole milk is the best storage medium to buy time on the way to real dental care — plain water is specifically worse for the tooth's surviving root tissue than milk or saliva.
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
