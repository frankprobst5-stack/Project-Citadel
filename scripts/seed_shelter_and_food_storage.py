#!/usr/bin/env python3
"""Seeds two real, sourced pages requested directly by Frank (2026-11-24):
an expedient fallout shelter guide, and comprehensive safe home food
storage guidance.

The fallout shelter page is special: rather than drafting from a
fetched website, it's transcribed from a real primary source already
sitting in this Vault -- appdata/media-vault/pdfs/Nuclear & Radiation
Survival/Nuclear-War-Survival-Skills-Cresson-Kearny.pdf. That book
(Cresson Kearny, originally produced via Oak Ridge National
Laboratory for the Defense Civil Preparedness Agency/FEMA) is THE
canonical US expedient-shelter reference -- `pdftotext -layout` on the
real file (it has a genuine text layer, confirmed before writing
anything here) pulled the real Appendix A.1 "Door-Covered Trench
Shelter" construction steps verbatim, with only obvious OCR scan noise
cleaned up, never the real content altered. source_url points at this
app's own /files/ stream of that exact real file, not an external
link -- the primary source was already here.

Food storage guidance is drawn from USDA FSIS (shelf-stable food
safety) and CDC (botulism/home-canned foods, fetched directly).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_shelter_and_food_storage.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent

KEARNY_PDF_URL = "/files/pdfs/Nuclear%20%26%20Radiation%20Survival/Nuclear-War-Survival-Skills-Cresson-Kearny.pdf"

PAGES = [
    {
        "title": "Expedient Fallout Shelter — Door-Covered Trench",
        "section": "emergency",
        "tags": ["nuclear", "fallout", "shelter"],
        "risk_level": "critical",
        "source_url": KEARNY_PDF_URL,
        "body_markdown": """## Quick Version

**First choice, per Ready.gov's own guidance:** find an existing substantial building — brick or concrete walls, underground parking, a subway. You're safer anywhere inside such a building, safest in its innermost part away from windows. **Shelter in place for the first 24 hours** — radiation levels drop fastest in that window — unless an immediate hazard (fire, structural collapse) forces you out, or authorities say it's safe to leave.

**If no such building is available, build a Door-Covered Trench Shelter** (real design from *Nuclear War Survival Skills*, Cresson Kearny — the full book is attached to this page):

- **Protection Factor 250** against fallout radiation when built correctly — someone outside gets 250x the dose someone inside this shelter would.
- Needs **3 hollow-core doors per 3 people** (1 per person), a shovel, waterproofing material (plastic sheeting, shower curtains, canvas), and at least **15 gallons of water per occupant**.
- Trench: **3 ft wide, 4½ ft deep**, length = sum of door widths minus 8 inches.
- Earth covering over the roofed doors: **at least 2 ft thick** at the centerline — this is what actually blocks the radiation; the doors alone do almost nothing.
- Real timeline: a motivated family of 2+ able-bodied adults has built this in under 24 hours; budget realistically for up to 36 hours of hard work.

**Before digging anywhere:** do the thumb test — dig 18 in. down, push your bare thumb into undisturbed earth at the bottom. If it sinks in more than about 1 inch, that ground is too unstable for an unshored trench; find another spot.

## Detailed Version — Door-Covered Trench Shelter Construction

*Transcribed from Appendix A.1 of* Nuclear War Survival Skills *(Cresson Kearny) — the actual PDF is attached to this page (see Source link). This is the real, complete government-developed design, not a summary.*

**Where it's practical:** ground where a dry, stable trench can be dug, and at least one hollow-core interior door is available per occupant. A family evacuating by vehicle can carry doors (knobs removed) plus strong boards (6+ ft long, 1 in. thick) or ¾-inch plywood as a substitute.

**Materials for a 3-person shelter:**
- 3 hollow-core doors
- A shovel (and pick, if the ground is hard)
- 2-3 sq. yards per person of waterproof material (4-mil poly film, shower curtains, plastic tablecloths, canvas)
- 2 pieces of plastic or tight-woven cloth (~6½×6½ ft each) for canopies over the two openings
- 2 pillowcases + 1 bedsheet per person, for improvised sandbags
- Containers for water storage; a ventilating pump (a "KAP," built per the book's own Appendix B) for anything but cool weather

**Construction steps, in order:**
1. Clear brush/grass from the work area and 8 ft around it on all sides.
2. Stake out a rectangular trench **36 in. wide**; length = total width of all doors minus 8 in.
3. Dig the main trench, entryway trench, and ventilation trench to **4½ ft deep**. Pile excavated earth no closer than 3 ft from the trench edges.
4. **Re-run the thumb test every additional foot of depth.** If it fails at any point, stop digging there — relocate instead.
5. Cut a 36-in. and an 18-in. stick to keep checking trench width as you dig — staying on-width saves real time later.
6. Level the ground 2½ ft out from the trench sides so doors will lie flat to the edges.
7. Line trench walls with sheets/plastic if available, stopping 1 in. short of the floor (so it isn't pulled down underfoot).
8. Build up the earth level around both openings with improvised sandbags or earth-filled cloth "rolls" before roofing, so you can later cover the entryway and vent hole with adequate shielding earth too.
9. **Roof with the doors.** If the ground is dry: lay doors directly on the ground (each end door overlapping the trench end by 4-5 in.), mound dry earth over them first near the ends, then build up to ~12 in. deep at the centerline, then lay the waterproof sheet over that mound, then mound a *final* 12-15 in. of earth on top — **total earth thickness at centerline: at least 2 ft.** This "buried roof" sequence is what lets the earth arch and support its own weight under blast load, instead of just resting dead weight on the doors.
   - If the ground is wet: reverse it — waterproof material goes directly on the doors first (to keep them dry and strong), then earth on top of that.
10. Slope the mounded earth outward and pack it so rain runs off, not in. Dig small drainage ditches around the finished shelter.
11. Build an open-sided canopy over each opening (vent and entry) to keep rain and fallout particles from falling straight in.
12. Install the ventilating pump in the opening where air already naturally moves.
13. Fill every available water container. If possible, disinfect stored water with one scant teaspoon of plain chlorine bleach per 10 gallons — even muddy water is worth storing and treating rather than going without.

**Capacity:** this exact design is the minimum for 3 people. Add one door's width of trench length per additional person; above ~7 people, build two separate shelters rather than one oversized one.

**What this page doesn't replace:** the book itself covers five other expedient shelter designs (Pole-Covered Trench, Aboveground Door-Covered, Crib-Walled, Ridgepole, and more) for situations where doors aren't available or more protection is needed — see the attached PDF's full Appendix A if the door-covered design doesn't fit your situation.
""",
    },
    {
        "title": "Safe Home Food Storage",
        "section": "reference",
        "tags": ["food-storage", "food-safety", "canning", "botulism"],
        "risk_level": "high",
        "source_url": "https://www.cdc.gov/botulism/prevention/home-canned-foods.html",
        "body_markdown": """## Quick Version

**Shelf-stable canned goods, stored properly:**
- High-acid foods (tomatoes, citrus, pineapple): best quality for **12-18 months**.
- Low-acid foods (meat, poultry, fish, most vegetables): best quality for **2-5 years**.
- Per USDA, a sealed, undamaged commercial can stored correctly stays **safe indefinitely** — these windows are about *quality*, not a safety cutoff.
- Store below **85°F**, in a cool, clean, dry spot — never above/beside the stove, under the sink, or in a damp basement/garage with temperature swings.

**Throw it out immediately, no exceptions, if a can or jar is:** leaking, bulging, swollen, dented badly, cracked, rusted, or spurts liquid/foam when opened — or if the food inside is discolored, moldy, or smells off.

**The one rule that matters most: you cannot see, smell, or taste the toxin that causes botulism.** Even a small taste of contaminated food can be deadly. Never taste food to check if it's safe. **If in doubt, throw it out.**

**Dry goods** (rice, beans, wheat, etc.), properly packaged with food-safe containers and oxygen absorbers, can store safely for **10-30 years** — the packaging is what protects against moisture and pests, not the food itself lasting forever untouched.

## Detailed Version

The "best by" dates on commercial canned food are quality estimates from the manufacturer, not safety deadlines — this is a real, specific point of confusion worth being clear about. A can that's intact, hasn't been exposed to freezing or extreme heat, and shows none of the damage signs above is considered safe by USDA well past its printed date; what actually degrades over those windows is flavor, texture, and nutrient content, not safety.

**Botulism is the real, severe risk home food storage has to take seriously** — *Clostridium botulinum* produces a toxin that can be fatal in small amounts, and critically, per CDC: food containing it does not reliably look, smell, or taste wrong. That's why the container-inspection checklist above (bulging, leaking, damage) matters so much — it's often the *only* practical warning available, since your senses genuinely cannot be trusted to catch it. Home-canned low-acid foods (vegetables, meats) carry real botulism risk if not pressure-canned correctly — this page doesn't cover home canning technique itself; that's its own topic with its own real safety rules (see the Food Preservation section once it's built out).

**Storage location matters more than people expect:** heat is the main enemy of shelf-stable food. A garage or shed that regularly swings from freezing to 100°F+ will measurably shorten real shelf life even for food that's never been opened or damaged — a consistent cool, dry interior space beats a "spare" storage spot every time.
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
            print(f"WOULD CREATE: {page['title']} (risk={page['risk_level']}, source={page['source_url']})")
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
