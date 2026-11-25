#!/usr/bin/env python3
"""Seeds 3 real pages from Where There Is No Dentist's Chapters 8-10
(Scaling Teeth, Injecting Inside the Mouth, Cement Fillings -- pages
127-151) -- mined from the real text layer already extracted in this
session (/tmp/dentist.txt). These are the book's real hands-on
"no dentist" skill chapters beyond extraction: removing tartar,
giving a local anesthetic injection, and placing a temporary filling
to save a tooth instead of pulling it.

The book itself repeatedly stresses that injecting and scaling are
skills that must be learned hands-on from an experienced person, not
purely from a book -- that caveat is preserved prominently in both
relevant pages below, not just mentioned once and dropped.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_dental_skills.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Scaling Teeth — Removing Tartar",
        "section": "reference",
        "tags": ["dental", "scaling", "tartar", "gum-disease"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

Tartar is hardened germ-coating that builds up on teeth, mostly inside the gum pocket where it's protected and often has to be felt rather than seen. **Scaling (scraping it away) gives infected gums a real chance to heal — but only if ALL the tartar comes off, not just what's visible above the gumline.** Leftover tartar lets new tartar build on top of it and the infection continues.

**You need:** 2 double-ended scalers (one pointed-tip for tartar near the gumline, one rounded-tip/curette for tartar under the gum), a sharpening stone, mirror, probe, tweezers, and cotton gauze.

## The Real 6-Step Technique

1. **Explain what to expect** — some bleeding and possibly pain; local anesthetic is an option if it hurts. Wash hands and sterilize instruments first.
2. **Feel for tartar under the gum** — it feels rough compared to smooth healthy root surface. Use a probe slid along the root under the gum, or twist a corner of cotton gauze and press it between the teeth to push the gum down and reveal more of the tooth surface.
3. **Place the scaler under the tartar.** Hold it almost like a pen for both power and control. **Keep the tip against the tooth at all times — never let it poke the gum.** Rest your third finger against a neighboring tooth to steady your hand while sliding the sharp scaler gently under the gum. Use the pointed-tip scaler for visible tartar first, then the rounded-tip scaler to reach the tartar deeper in the pocket — stop when you feel the bottom of the pocket.
4. **Pull the scaler with a firm, short stroke**, breaking free as much tartar as possible at once. **Removing it a little at a time is actually worse** — the remaining tartar becomes smoother and harder to scrape off with each partial pass. Press against the gum afterward to control bleeding.
5. **Recheck with the probe** that every side of the tooth is smooth before moving to the next tooth. **If there's a lot of tartar, do half the mouth now and the other half another day** rather than rushing — thoroughness matters more than speed.
6. **Explain aftercare:** gum soreness for a few days is normal. Brush with a soft brush reaching into the gum pocket and behind the front teeth (where tartar collects most), clean between teeth, rinse with warm salt water (4 cups/day tapering to 1 cup/day to maintain), and eat tartar-fighting local foods like guava, oranges, and dark green vegetables.

## Removing Something Caught Under the Gum

Red, swollen gum between two teeth may mean something is trapped in the pocket (a fish bone, a string of mango fiber, a sharp tartar fragment) — ask what the person recently ate. Feel for it with a probe, then either lift it out gently with the rounded-tip scaler, or slide a knotted thread between the teeth and pull it out sideways (not up and down) so the knot drags the object with it. **If the gum tissue itself has grown into a lump (an epulis), that needs an experienced dental worker to remove — don't attempt it yourself.**

## Keeping Scalers Sharp and Sterile

A sharp scaler breaks tartar free; a dull one just slides over it. Test sharpness by scraping the edge against a fingernail — if it can't cut the nail, sharpen it on an oiled/wetted Arkansas stone. **Scalers must be fully sterilized (boiled), not just disinfected — they routinely carry blood, which can transmit hepatitis or other bloodborne disease between people.**

## Detailed Version

**The real honest limit on this page:** scaling removes hardened tartar that's already there — it does not cure anything on its own. The book's own framing is worth preserving exactly: scaling gives a person a fresh start, but only their own daily brushing and cleaning afterward actually keeps the tartar from returning.
""",
    },
    {
        "title": "Giving a Dental Local Anesthetic Injection",
        "section": "reference",
        "tags": ["dental", "anesthesia", "injection", "high-risk-skill"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Read This First

**The book itself is explicit: injecting is a skill that develops with experience, and the real way to learn it is by watching an experienced dental worker give injections, then having that person watch and correct you — not from a book alone.** This page preserves the book's real technique and safety rules for reference and for use alongside hands-on training — not as a substitute for it. A badly placed or badly dosed injection carries real risks: hitting a blood vessel, overdosing a person with heart disease, or masking (and worsening) an active infection.

## What You Need

A dental cartridge syringe (metal, uses sealed anesthetic cartridges) or a standard syringe/needle (glass or plastic, draws anesthetic from a bottle) — lidocaine (lignocaine) 2% is the standard local anesthetic; procaine hydrochloride 1% is a fallback. **Use a new needle and a new cartridge/dose for every person — never reuse on a second person.**

## The 5 Real Safety Rules

1. **Never inject into swollen tissue.** It can spread the infection further, and pus inside the swelling stops the anesthetic from working anyway. Treat the swelling first (antibiotics) and do the extraction/filling once it's gone down.
2. **Heart disease changes the rules.** No more than 2 injections in one visit, and avoid anesthetic containing epinephrine entirely — use plain lidocaine or mepivacaine 3% only. Epinephrine can be dangerous for a weak heart.
3. **Check needle direction before pushing in** — the anesthetic needs to come out against the bone where the nerve actually runs, not away from it.
4. **⚠️ Pull back on the plunger before injecting (only works with an aspirating syringe) — if blood enters the syringe, you've hit a blood vessel.** Withdraw the needle partway and reposition before injecting. **Injecting directly into a blood vessel can cause more swelling and can make the person faint** — if that happens: lay them on their back, loosen their collar, and raise their legs above head level.
5. **Sterilize everything.** Boil glass/metal syringes and needles for 30 minutes; for disposable needles, use once and dispose of safely — never pass an infection between people through a reused needle.

## Where to Inject — the Real Technique

**Upper teeth** (the upper jawbone is soft/spongy, so this is the more forgiving injection): lift the lip/cheek to find the line where it meets the gum — that's the injection point. Push the needle in aiming at the tooth's root until it hits bone, then inject about 1ml (half a cartridge) per root; withdraw partway and reposition for a multi-root tooth. For an extraction, add a small injection (.25ml) on the inside gum surface too.

**Lower teeth are genuinely harder** (the lower jawbone is thicker, so anesthetic placed near the root often can't reach the nerve) — for a fully numb lower tooth you generally need to block the main nerve trunk before it branches: feel for the depression where the jawbone turns up toward the head beside the last molar, aim the needle into the "v" formed there, advance until it hits bone (about ¾ the needle's length), aspirate to check for blood, then inject 1.5ml (¾ cartridge). **This specific injection takes real practice to do reliably — it's the clearest example of where hands-on supervised learning genuinely matters more than following written steps.** A second, smaller injection beside a back tooth is needed if treating a molar.

## Extra Care With Children

Topical anesthetic on dry gum tissue first (or "pressure anesthesia" — press firmly with cotton on a matchstick for a minute, then inject quickly into the resulting depression) reduces the pain of the needle itself. Warm the anesthetic in your hands first, use a sharp new needle, keep the syringe out of the child's sight until needed, and inject slowly — a too-fast injection causes a painful pressure spike that frightens the child more than the needle itself.

## After the Injection

Wait 5 minutes, then actually test the area is numb (poke gently with a probe and watch the person's eyes) before starting treatment — if they still feel pain, stop and give more anesthetic rather than proceeding. Afterward, explain: normal feeling returns in about an hour; don't bite or scratch the numb area in the meantime (children especially should have a cotton ball placed between their teeth on the numbed side for 2 hours, specifically so they chew the cotton instead of their own numb lip or cheek); avoid hot drinks until feeling returns, since a numb mouth can't signal a burn.

## Detailed Version

The aspiration check (rule 4) is the single highest-value safety step on this page — it is a direct, concrete way to catch an in-progress mistake (hitting a vessel) before it becomes an injected dose of anesthetic in the bloodstream rather than at the nerve, and it costs only a few seconds to perform.
""",
    },
    {
        "title": "Temporary Cement Fillings — How to Place Them",
        "section": "reference",
        "tags": ["dental", "filling", "cavity"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Not every bad tooth needs to come out — always ask first whether it can be filled instead.**

**Do NOT place a filling if there's an abscess** — signs are facial swelling, a "gum bubble" near the root, constant pain (even while trying to sleep), or sharp pain when tapped. Filling over an abscess traps and worsens the infection — extract instead (unless real root-canal treatment is available).

**A filling is appropriate when there's no abscess:** no swelling, pain only occasional (after food/drink or cold air), and the tooth feels normal when tapped. This means decay has reached the nerve enough to feel temperature, but hasn't progressed to active infection — filling now can prevent it from ever becoming an abscess.

**This chapter covers temporary cement fillings only** (zinc oxide + oil of cloves/eugenol) — lasting a few months, meant to buy time until a permanent filling (requiring a dental drill or Atraumatic Restorative Treatment) becomes available. **A temporary filling is often the real first step to actually saving a tooth**, not a lesser substitute.

## What You Need

Mirror, probe, tweezers, spoon excavator, filling tool, and a mixing spatula with a smooth glass surface; zinc oxide powder and oil of cloves (eugenol) as the filling material itself — the two basic, inexpensive ingredients behind nearly every brand of temporary dental cement.

## The Real 6-Step Technique

1. **Keep the cavity dry** — pack cotton between the cheek/gum (and under the tongue for a lower tooth) and change it whenever it gets wet. Cement bonds and lasts much better in a dry cavity.
2. **Remove some, but not all, of the decay.** You do NOT need to dig out every bit of decay at the bottom of the cavity — doing so risks hitting the nerve; covering remaining deep decay with cement is enough to stop it progressing further. **But you must remove ALL decay at the edges of the cavity** — leftover decay there lets germs and food leak between the cement and the tooth, restarting the decay underneath. If an edge is thin and weak, deliberately break it back to solid tooth structure for the cement to grip. Inject local anesthetic first if this causes pain.
3. **Mix the cement** on a smooth glass surface — combine zinc oxide powder into eugenol liquid gradually until it's thick (test by rolling a bit between your fingers; it's ready once it stops sticking). Practice mixing ahead of time to learn how fast it sets.
4. **Press the cement into the cavity**, building it up in layers pressed firmly against the cavity floor, corners, and walls until slightly overfilled. **If the cavity is between two teeth, place something thin and rounded (a palm-leaf stem, toothpick, comb tooth) between the teeth first** so the cement doesn't get squeezed into and injure the gum.
5. **Remove the excess cement before it hardens**, shaping it to match the natural contour of the tooth so opposing teeth meet it properly. Check bite alignment carefully: while wet, look for a shiny spot where the opposing tooth is striking it and scrape that down; once dry, have the person bite on carbon paper (or pencil-darkened paper) to find and correct any high spot. **The filled tooth must sit correctly against the others before the person leaves — too much bite pressure on a high filling will crack it.**
6. **Explain aftercare:** no eating for 1 hour (lets the cement harden fully), and avoid using that tooth for chewing until a permanent filling replaces the temporary one — the cement and thinned cavity walls can't handle much pressure yet.

**If the tooth hurts MORE after the filling is placed, that almost always means there was an undetected abscess.** Extract the tooth; if swelling prevents immediate extraction, remove the filling itself first to relieve the pressure, treat the swelling, then extract once it's resolved.

## Cleaning Filling Instruments

Don't boil these specific instruments — it weakens their fine pointed tips. Instead: scrape off dried cement, scrub with soap and water, then soak 20 minutes in disinfectant before wrapping and storing.

## Detailed Version

**The real, honest limit on this page, stated plainly:** a cement filling genuinely can last up to about 6 months, but it is explicitly temporary — the person still needs to reach a dental worker with real drilling or ART equipment for a permanent filling within that window. Treating the temporary filling as a permanent fix, rather than as the bridge it actually is, is the single most important expectation to set correctly with the person before they leave.
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
