#!/usr/bin/env python3
"""Seeds 7 real pages from ATP 3-50.21 (Survival), Appendix A
(Survival Knots and Rope) -- mined from the real text layer already
extracted in this session (/tmp/atp_survival.txt, pages A-1 through
A-24). This is genuinely foundational content never covered anywhere
in this wiki before, despite knots/lashing being referenced
repeatedly across already-seeded shelter, raft, and trap pages.

Covers: real rope/knot terminology, the real knot-dressing discipline
(a loosely dressed knot loses up to 50% of its strength), and real
step-by-step tying instructions for every knot/hitch/lashing this
appendix covers, plus real rope-construction technique (natural vs.
manmade fiber properties, a real tensile-strength table, twisting,
braiding, and whipping rope ends).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_atp_knots_rope.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
ATP_SURVIVAL_PDF_URL = "/files/pdfs/Military Manuals/ATP-3-50.21-Survival.pdf"

PAGES = [
    {
        "title": "Rope & Knot Terminology",
        "section": "reference",
        "tags": ["knots", "rope", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**A shared, precise vocabulary for ropes and knots is what makes the rest of real knot instruction actually followable** — every term below describes one specific, distinct part or action.

## Real Core Terms

- **Rope** — strands of fiber twisted or braided together. **Line** — a single thread, string, or cord.
- **Running end** — the free/working end you're actively tying with. **Standing end/part** — the rest of the rope, excluding the running end.
- **Bight** — a bend or U-shaped curve in the rope.
- **Bend** (what this manual calls a "knot") — used to fasten two ropes together, or a rope to a ring/loop.
- **Loop** — a fold/doubling of the rope another rope can pass through. **Overhand loop**: the running end passes OVER the standing part to form it. **Underhand loop**: the running end passes UNDER the standing part instead.
- **Turn** — wrapping the rope around an object (post, rail, ring), with the running end continuing away from the standing end. **Round turn** — the same, but the running end exits in the same general direction as the standing part.
- **Hitch** — ties a rope around a timber/pipe/post so it holds temporarily but can be undone easily.
- **Knot** — any interlacement of rope forming a tie/fastening (includes bends, hitches, splices) — often used to stop a rope from passing through an opening.
- **Pigtail** — the leftover running end after a knot is tied. **Keep it to about 4 inches or less** — this conserves rope and avoids it getting in the way.
- **Lay** — the twist direction of the rope itself.
- **Whipping** — binding a rope's end tightly with small cord/tape to stop it from untwisting or unraveling.

## Real Lashing-Specific Terms

- **Wraps** — simple loops of rope around 2 poles (square lashing) or 3 poles (tripod lashing), starting and ending with a clove hitch.
- **Fraps** — tightening turns looped perpendicular to the wraps, cinching the whole lashing tight.
- **Lashings** — the combination of wraps + fraps used to bind spars/sticks into solid corners or tripods.

## ⚠️ Dressing the Knot — a Real, Easy-to-Skip Step

**"Dressing" means orienting every part of a knot so it's properly aligned, straightened, and not twisted on itself before you load it.** **Skipping this can cost up to 50% of the knot's real holding strength.** A loosely dressed knot can also deform under strain — slipping into a weaker form, or untying entirely, exactly when you're relying on it most.

## Detailed Version

**The real, practical payoff of learning this vocabulary first: every knot description that follows in this wiki (overhand, bowline, clove hitch, lashings) uses these exact terms without re-explaining them each time** — "pass the running end through the bight" only makes sense once "running end" and "bight" are already understood, which is exactly why this page exists as the real foundation underneath all the others.
""",
    },
    {
        "title": "Essential Knots — Overhand, Round Turn & Figure-Eight",
        "section": "reference",
        "tags": ["knots", "rope", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Overhand Knot — the Simplest, Most Common Knot

**Real uses:** stopping a rope end from untwisting, forming a stopper knot, or as a component inside other knots. **This knot should replace the half hitch as a real finishing/safety knot for other knots** — it's simply more reliable. **⚠️ Real caveat: tying an overhand knot alone reduces a straight rope's strength by 55%** — a significant real cost, worth remembering before assuming "a knot is a knot."

**To tie it:** make a loop near the rope's end, pass the running end through the loop, and pull tight.

## Round Turn and Two Half Hitches — the Real Main Anchor Knot

**The go-to real anchor knot for one-rope bridges and other high-load situations where other knots would jam or become impossible to untie.** Most commonly used to anchor a rope to a pole or tree.

## Figure-Eight Knot — a Larger, More Secure Stopper

**Used when an overhand knot's stopper isn't big enough** — specifically to keep a rope end from slipping through a fastening or loop in another rope.

**To tie it:** make a loop in the standing part, pass the running end around the standing part and back over one side of the loop, then down through the loop itself, and pull tight.

## Detailed Version

**The real, repeated pattern across all three of these: each one solves a specific, narrow real problem (stopping fray, anchoring under load, stopping a slip-through) rather than being a general-purpose "good knot."** Reaching for the overhand knot as a universal finishing knot, and the figure-eight specifically when an overhand's stopper is too small, are both real, deliberate upgrades over "just tie something."
""",
    },
    {
        "title": "Knots for Joining Rope — Square Knot & Sheet Bends",
        "section": "reference",
        "tags": ["knots", "rope", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Square Knot — for Joining 2 Ropes of EQUAL Diameter

**To tie it:** lay the running end of each rope together, pointing in opposite directions. Pass one rope's running end under the other's standing part. Bring both running ends up and away from the crossing point, then cross them again. **Once each running end comes out parallel to its own standing part, pull tight.**

**⚠️ Real failure mode — the "granny knot":** if each running end does NOT end up parallel to its own standing part, you've tied a granny knot instead, which **will slip under strain and should never be used.**

**⚠️ Another real failure mode — the "thief knot":** tying a square knot via the bight-and-feed method but routing the second rope from the wrong (standing) side of the bight produces a thief knot — it **looks similar but slips under strain and is genuinely hard to untie.** A true square knot, by contrast, actually draws tighter under strain and can be released easily by grasping both bends and pulling the knot apart.

## Single Sheet Bend — for 2 DRY Ropes of UNEQUAL Size

**To tie it:** pass the smaller rope's running end through a bight in the larger rope, continue it around both sides of the larger rope, then back under the smaller rope's own standing part, and pull tight. **⚠️ Real limitation: this knot draws tight under light load but can loosen or slip once tension is released** — don't trust it for a load that will be repeatedly loaded and unloaded.

## Double Sheet Bend — a Real, More Reliable Upgrade

**Works better than the single sheet bend for equal OR unequal rope diameters, for WET ropes, or for tying a rope to an eye — and won't slip or tighten dangerously under heavy load.**

**To tie it:** tie a single sheet bend first, but don't pull it tight yet. Take one extra turn around both sides of the larger rope's bight with the smaller rope's running end, then tighten the whole knot.

## Detailed Version

**The real, shared lesson across the square knot's two failure modes and the single sheet bend's real limitation: a knot that looks correct can still be subtly wrong in a way that only shows up under load** — which is exactly why learning the specific, real failure signatures (a granny knot's un-parallel running ends, a thief knot's mismatched routing, a single sheet bend loosening after tension releases) matters as much as learning the correct tying steps themselves.
""",
    },
    {
        "title": "Knots for Making Loops — Bowline Family",
        "section": "reference",
        "tags": ["knots", "bowline", "rope"],
        "risk_level": "moderate",
        "body_markdown": """## Bowline — a Real, Easy-to-Untie Loop at a Rope's End

**To tie it:** pass the running end through whatever object you're attaching the loop to, forming a loop in the standing part. Pass the running end through that loop from underneath, around the standing part, then back through the loop from the top — it should come down through the loop running parallel to the rope coming back up through it. Pull tight.

## Bowline on a Bight — a Loop Mid-Rope (Not Just at the End)

**For when you need a loop somewhere other than a rope's actual end.** Real bonus: it won't slip and is easy to untie. (The same real technique also works at a rope's end by doubling a short section of rope first.) Form the loop the same way as a standard bowline using the doubled section, then pass the bight's end up through the loop, back down and around the entire knot, and tighten.

## ⚠️ French Bowline — a Real Emergency Rescue Sling

**Used as a sling for lifting a person — one loop goes around the body, under the arms.** **The person's own weight keeps both loops tight, so they genuinely can't fall out of the sling** — which is specifically why this knot is useful for lifting an unconscious person who can't help hold themselves in place.

**To tie it:** start as a simple bowline (loop in the standing part), pass the running end through that loop from underneath, then form a second separate loop. Pass the running end through this second loop (again from underneath), around the back of the standing part, and back through so it exits parallel to the looped section. Pull the standing part to tighten — this leaves 2 real loops.

## Speir Knot — a Real Quick-Release Fixed Loop

**Used when you need a fixed loop, a knot that won't slip, AND a fast release** — pulling the running end releases it quickly.

**To tie it:** pass the running end through a ring or around a pipe/post, bringing it back on the left side of the standing part. Place both hands palms-up under both rope parts, left hand higher, gripping the standing part with your left hand and the running end with your right. Move your left hand left and right hand right to form two bights. Twist your left hand a half turn toward your body, twisting that bight into a loop. Pass the other bight over the rope and down through that loop. Tighten by pulling the bight and the standing part together.

## Overhand Knot Fixed Loop — the Real Knot to Memorize for Recovery Gear

**A simple fixed loop tied directly into a bight anywhere along a rope — no working end required.** Useful for attaching clips, hooks, or other rope. **⚠️ Real drawback: it tends to jam tight once loaded and may need to be cut off afterward.** Despite that, **this is explicitly the one knot worth committing to memory for use with personnel-recovery equipment**, specifically because it can be tied anywhere along the rope's length.

## Detailed Version

**The real, life-safety reason the French bowline and overhand fixed loop get singled out: both are built for exactly the moment when the person relying on the knot cannot actively help (unconscious, or being hoisted by equipment) — which is why ease of tying under pressure, and the loop's own structural security once loaded, matter more here than in an ordinary utility knot.**
""",
    },
    {
        "title": "Hitches — Half Hitch, Timber Hitch, Clove Hitch, Sheepshank & Prusik",
        "section": "reference",
        "tags": ["knots", "hitches", "rope"],
        "risk_level": None,
        "body_markdown": """## Half Hitch — Simple, but Genuinely Not Very Secure

**To tie it:** pass the rope around a timber, bring the running end around the standing part, then back under itself. **⚠️ Real historical note: this used to be the Army's standard finishing/safety knot, but it tends to undo itself with no load on it — it's since been replaced by the overhand knot for that role** (see Essential Knots — Overhand, Round Turn & Figure-Eight). Use it only for temporarily securing a rope's free end, not as a load-bearing hitch.

## Two Half Hitches — a Real, Quick Upgrade

**To tie it:** pass the running end around the pole/timber, take a turn around the standing part and under the running end (that's the first half hitch), then pass the running end around the standing part and back under itself again.

## Timber Hitch — for Moving Heavy Timbers/Poles

**To tie it:** make a half hitch, then **twist the running end around itself at least one more time.** **⚠️ These extra turns must wrap around the running end itself, not the pole** — otherwise the knot won't actually tighten against the pole when loaded.

## Timber Hitch and Half Hitch Combined — a Tighter Grip for Lifting/Dragging

**To tie it:** pass the running end around the timber and back under the standing part to form a half hitch, then tie a separate timber hitch further along the same timber with the running end. **The real load-bearing logic: strain comes onto the half hitch, while the timber hitch prevents that half hitch from slipping** — the two work together rather than either alone.

## Clove Hitch — Fastens a Rope to a Timber/Pipe/Post, Tieable Anywhere on the Rope

**Mid-rope version:** make two turns close together, twist them so the two loops lie back-to-back, then slip both loops over the timber/pipe at once.
**End-of-rope version:** wrap the rope around the timber in 2 turns, so the first turn crosses the standing part and the running end comes up under itself on the second turn.

## Sheepshank — Shortens a Rope or Bypasses a Weak Spot (Never Tied at a Rope's End)

**To tie it:** make 2 bights in the rope so three parallel sections run alongside each other, then tie a half hitch in the standing part over the end of each bight.

## Prusik — a Real Load-Dependent Sliding Knot

**Ties a short rope around a longer one (e.g., a sling rope onto a climbing rope) so that the short rope slides freely with no tension, but grips and holds once tension is applied.** Can be tied with either a rope end (finished off with a bowline) or a bight. **The real, practical payoff: this nonslip-under-load behavior lets a person climb a fixed rope using footholds**, and it also works to anchor a rope, or the end of a traction splint, to a branch or ski pole.

## Detailed Version

**The real, repeated principle across the timber-hitch-plus-half-hitch combo and the Prusik: pairing two simple knots, each handling a different part of the real mechanical load, often produces a more secure result than either one alone** — the half hitch takes the strain while the timber hitch stops it slipping; the Prusik's sliding-vs-gripping behavior under load does mechanically what a human climber's own grip-and-release would do by hand.
""",
    },
    {
        "title": "Lashings — Square, Diagonal & Shear",
        "section": "reference",
        "tags": ["knots", "lashing", "shelter-building"],
        "risk_level": None,
        "body_markdown": """## Square Lashing — Secures One Pole at a Right Angle to Another

**Directly applicable to shelter and raft frames already covered elsewhere in this wiki** (see Building Snow Shelters — Snow Wall, Cave, Tree-Pit & More and Wooded-Area Shelters — Lean-To, Double Lean-To & Wigwam).

**To tie it:**
1. Start with a clove hitch around the main log, right under where the crosspiece will sit.
2. Wrap the rope around both poles — each turn goes OUTSIDE the previous turn around the crosspiece, and INSIDE the previous turn around the main log. Keep it tight. **3-4 turns are needed.**
3. Add 2-3 "frapping" turns between the crosspieces, pulling tight — **this is what actually binds the crosspiece firmly in place.**
4. Finish with a clove hitch back around the same pole where you started.

## Diagonal Lashing — an Alternative for the Same Right-Angle Job

**To tie it:**
1. Start with a clove hitch around both poles at their crossing point.
2. Take 3 turns around both poles, laid beside each other (not stacked on top of each other).
3. Take 3 more turns around both poles, this time crosswise over the first set.
4. Pull tight, then add a couple of frapping turns between the two poles around the lashing itself, keeping everything tight.
5. Finish with a clove hitch around the same pole you started on.

## Shear Lashing — Binds 2+ Poles in a Series (e.g., for an A-Frame or Tripod Leg)

**To tie it:**
1. Lay the poles parallel, loosely beside each other, and start with a clove hitch on an outer pole.
2. Wrap 7-8 loose turns of rope around the whole bundle.
3. Add frapping turns between each individual pole.
4. Finish with a clove hitch on the pole opposite from where you started.

## Detailed Version

**The real, shared thread across all three lashings: every one starts and ends with a clove hitch (because it's tieable anywhere and holds reliably on its own), and every one relies on frapping turns — not the initial wraps alone — to actually cinch the poles together tight.** Skipping the frapping step on any of these produces a loose, wobbly joint even if the wraps themselves were done correctly.
""",
    },
    {
        "title": "Making Rope — Fiber Types, Twisting & Braiding",
        "section": "reference",
        "tags": ["rope-making", "bushcraft", "survival-skills"],
        "risk_level": None,
        "body_markdown": """## Quick Version

**Knowing the real properties of natural vs. manmade rope — and how to actually make rope from scratch — lets you improvise the right cordage for a task rather than wasting time, energy, or material on the wrong one.**

## Natural Fiber Rope — Real Properties

**Made from plant/animal fibers** (grasses, sedge, hemp, cotton, manila, hair, leather, sinew), twisted or braided together. **Genuinely resistant to friction-generated heat, but destroyed easily by a sharp blade.** **Real way to cut it without a blade: abrade it vigorously against rock, concrete, metal, or wood** until the fibers give way. **Tends to be thicker and harder to tie knots in, and can break down over time if not kept clean.**

## Manmade Fiber Rope — Real Properties

**Made from polypropylene, nylon, Kevlar, etc.** — braided/twisted as one continuous strand with no fiber splices, which makes it genuinely strong. **Water and weather resistant, but — being essentially plastic — vulnerable to friction-heat and abrasion.** **Real improvised cutting method: saw it with a Kevlar-like material or paracord, generating enough friction heat to melt through it** (a knife, rock, or glass edge also works). **Easier to tie knots in than natural rope, but still needs UV protection (keep it out of direct sun) to avoid degradation.**

**Kernmantle rope** (a real manmade subtype — an outer sheath over inner core fibers) is especially strong and abrasion-resistant, commonly used for climbing/rappelling. **Static kernmantle doesn't stretch; dynamic kernmantle is designed to stretch and recover** — paracord is a real, common example of the static type.

## Real Tensile Strength Reference (1-inch-diameter, 3-lay rope)

| Fiber | Tensile Strength (lbs) |
|---|---|
| Green grass | 100-250 |
| Bark fiber | 500-1,500 |
| Palm fiber | 650-2,000 |
| Sedges | 2,000-2,500 |
| Money rope (lianas) | 560-700 |
| Lawyer vine (calamus), ½-inch | 1,200 |

**⚠️ Always plan around the LOWEST figure in a range, for safety.** **A real, useful rule of thumb: doubling a rope's diameter roughly quadruples its tensile strength; halving the diameter cuts strength to about a quarter.**

## Real Twisting Technique

1. Gather long, strong fibers (pre-tested for strength/pliability) into loosely held, even strands — **about 15-30 individual fibers per strand, twisted clockwise**, formed to roughly ⅛ inch diameter.
2. **Twist 2-4 of these strands together counterclockwise ("laying")**, while simultaneously keeping any not-yet-laid strands twisted clockwise — **each strand must stay equal in both twist and thickness.**
3. Repeat the same process at a larger scale: twisted strands become "lays," and lays become full rope. **Keep tension and twist even across every strand** — if one strand twists around another unevenly, the "lay" is faulty.
4. **For fine cord** (fishing line, snare line): keep strands especially uniform. Cords as thin as 1/32 inch, spun by hand, can hold a real breaking strength of 20-30+ pounds.
5. **Normally takes 2+ people to spin and lay rope**, but a real solo technique exists: roll the fiber between the flat of your hand and your thigh, feeding in new material with your free hand as you go — **slow for any real length, but genuinely doable alone.**

## Real Braiding Technique (when you don't have help to spin/lay rope)

**General rule for every braid: work from the outside in toward the center.**

**Three-plait braid** (makes flat rope, simple but less finished-looking than 4-strand):
1. Pass the right strand over the one to its left.
2. Pass the left strand over the one to its right.
3. Repeat, alternating left/right.

**Broad braid** (for wider bands — belts, shoulder straps):
1. Hold 6+ strands flat together.
2. Pass a center strand over the strand to its left.
3. Pass the strand second-from-center-left over, toward the right, over the first strand.
4. Weave the next strand (adjacent to the first) under-and-over.
5. Keep weaving alternating strands from left and right toward the center — **the finished braid should end up tight and close.**

**Finishing a broad braid:**
1. Fold one center strand back on itself.
2. Weave the strand it had enclosed back on itself too.
3. Fold back the strand from the opposite side and weave it between the already-braided strands — **every strand should fold back with a consistent under-over-under pattern, no uneven gaps.** If the weave is too tight to work loose ends through by hand, **a thin wood chisel-edge tool can gently open the strands enough to pass the ends through.**
4. Roll the finished braid under a bottle or similar round object for a smooth final finish.

## Whipping the Ends — Real Fray Prevention

**A cut rope end tends to untwist and should always be secured.** Whipping (tightly wrapping the end with small cord) is a real, clean method that doesn't bulk up the rope's diameter — it still threads through blocks/openings afterward. **⚠️ Real, important sequencing: place 2 whippings about 1-2 inches apart BEFORE cutting the rope between them** — this stops both resulting ends from immediately untwisting the instant they're separated.

## Detailed Version

**The real, unifying skill across twisting and braiding: both convert a pile of individually weak fibers into something far stronger by working at the right scale (strand, then lay, then rope) with even tension and consistent twist throughout — uneven technique at any one scale weakens the whole final rope, no matter how good the raw material was.**
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
                "source_url": ATP_SURVIVAL_PDF_URL,
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
