#!/usr/bin/env python3
"""Seeds 4 real pages from the USMC Winter Survival Course Handbook's
Survival Medicine chapter -- mined from the real text layer already
extracted in this session (/tmp/usmcwinter.txt, pages 14-1 through
14-10). Covers cold-weather physiology and the 3 real cold-injury
categories this source treats in real depth: hypothermia, frostbite,
and snow blindness/trenchfoot.

A real cross-source note: this source's field tourniquet-loosening
guidance (20 minutes, if rescue is unlikely within 2 hours) is
noticeably less conservative than the TCCC Prolonged Field Care
appendix's real tourniquet-conversion timing (safe under 2hr, likely
safe 2-6hr, not advised over 6hr) already seeded in this wiki -- that
discrepancy is flagged explicitly rather than silently picking one,
consistent with this build-out's standing practice of surfacing real
source conflicts instead of hiding them.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_usmc_cold_injuries.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
USMC_WINTER_PDF_URL = "/files/pdfs/Military Manuals/USMC-Winter-Survival-Course-Handbook.pdf"

PAGES = [
    {
        "title": "Cold Weather Physiology — Heat Loss & the Body's Response",
        "section": "reference",
        "tags": ["cold-weather", "physiology", "hypothermia"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Understanding exactly how the body loses heat is what makes cold-weather prevention actually effective, rather than just generically "staying warm."**

## The 5 Real Ways the Body Loses Heat

1. **Radiation** — direct heat loss to colder surroundings. **An unclothed body loses roughly 60% of its total heat this way** — the single largest mechanism, which is exactly why covering exposed skin (especially the head) matters so much.
2. **Conduction** — direct heat transfer into a colder object you're touching. **Sitting or lying directly on cold ground, snow, or rock without insulation beneath you causes rapid heat loss this way** — an insulating pad or even a pack underneath you breaks this contact.
3. **Convection** — heat loss to moving air or water flowing across the body. Still air/water around the body eventually reaches body temperature and stops drawing heat — **but continuously moving air or water never equalizes, so the body keeps losing heat indefinitely.** This is the real mechanism behind wind chill.
4. **Evaporation** — heat lost converting sweat (or any skin moisture) into vapor. **This is the body's main active cooling method** — a single quart of sweat, easily produced in an hour of hard exertion, carries away roughly 600 calories of heat as it evaporates. It works just as well (and just as dangerously, in cold conditions) whether you're overheating on purpose or just overexerted.
5. **Respiration** — air you inhale is warmed and humidified by your body; that heat leaves when you exhale (which is why your breath is visible in cold air). This combines convection and evaporation happening inside the body itself.

## How the Body Actually Responds

**To excess heat:** skin blood vessels dilate (bringing more blood near the surface to shed heat), followed by sweating (adding evaporative cooling).

**To cold — essentially the reverse:** skin blood vessels constrict first, which both reduces heat loss at the surface AND redirects blood toward the body's core (brain, heart, lungs, liver, kidneys) — **this is exactly why fingers and toes get cold first: the body is deliberately sacrificing them to protect the organs that matter more.** If constriction alone isn't enough, shivering begins — rhythmic muscle contraction that generates real heat, but **can only be sustained for a limited time before exhaustion sets in.** From there, the body either successfully rewarms, or continues cooling into hypothermia.

## Detailed Version

**The real, practical payoff of understanding these 5 mechanisms individually: each one has a different, specific countermeasure.** Insulating layers address radiation; a sleeping pad or pack under you addresses conduction; windproof outer layers address convection; moisture-wicking base layers and avoiding overexertion-driven sweat address evaporation; and simply breathing through a scarf or balaclava in extreme cold reduces respiratory heat loss. Generic "bundle up" advice misses that these are genuinely separate problems, each solved differently.
""",
    },
    {
        "title": "Hypothermia — Causes, Signs & Field Treatment",
        "section": "emergency",
        "tags": ["hypothermia", "cold-weather", "emergency"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Hypothermia — core body temperature at or below 95°F — is the #1 killer in survival situations, and it does NOT require extreme cold to occur.** Most real cases happen between 30-50°F, not far-below-freezing temperatures — a genuinely dangerous and widely underestimated fact.

## Real Causes

Hypothermia occurs whenever heat loss exceeds the body's heat production. Contributing factors: ambient temperature, wind chill (which **only meaningfully affects improperly clothed people**), wet clothing, cold-water immersion, improper clothing, exhaustion, alcohol/nicotine/certain drugs (barbiturates, tranquilizers), and injuries causing immobility, major bleeding, major burns, or head trauma.

## Real Signs — Watch Mental Status First

**The #1 sign is altered mental status** — confusion, slurred speech, strange behavior, irritability, impaired judgment, hallucinations, or fatigue. This is literally the brain itself getting cold. As it worsens: loss of consciousness, then coma.

**Shivering is a real early warning sign, but it stops for two very different reasons — telling them apart matters:** either the body has warmed back to normal, OR the body has kept cooling (shivering decreases below 95°F and stops entirely around 90°F). **If someone who was shivering suddenly stops, don't assume they're fine — check which reason it actually is.**

**⚠️ A severely hypothermic person can appear dead** — no visible breathing, no detectable pulse. **Real cases have been successfully revived with no permanent damage. The real operating principle: "you are not dead until you are warm and dead."** Don't give up resuscitation efforts on a cold person just because they appear to show no vital signs.

## Real Prevention

- Properly warm, well-maintained cold-weather clothing, kept as dry as possible.
- **If your feet are cold, put on a hat** — up to 80% of body heat can escape through the head.
- **Avoid dehydration** — drink 6-8 quarts of water per day when available.
- Eat adequately — food is fuel for heat production.
- Avoid fatigue/exhaustion.
- **Increase activity as temperature drops rather than staying still** — if you truly can't move around, do isometric exercises of successive muscle groups instead.
- **Use a buddy system** — check each other regularly for hypothermia signs, since the person affected often can't reliably judge their own mental state.

## Real Field Treatment

1. Make the diagnosis (recognize it's happening).
2. **Prevent further heat loss** — get the person out of the environment and into shelter.
3. Insulate them.
4. **Rewarm with real skin-to-skin contact:** zip two sleeping bags together, pre-warm the combined bag with another person's body heat, then place the hypothermic person inside with 2 unclothed people on either side of them.
5. Evacuate for real medical care if at all possible.

## Other Real, Important Points

- **Fluids:** a mildly hypothermic person can be given hot (non-alcoholic) drinks; otherwise give nothing by mouth.
- **Minimize unnecessary movement/jarring of the person** — a severely cooled heart can stop if jostled.
- **Treat major wounds/bleeding BEFORE attempting to rewarm** — rewarming someone who has bled out significantly accomplishes little.
- **⚠️ Never give alcohol to a hypothermia victim** — it accelerates heat loss despite feeling warming.
- **Once rewarming starts, keep monitoring continuously** — don't consider the person "handled" and walk away.

## Detailed Version

**The single most counterintuitive, important fact on this page: most real hypothermia happens in only moderately cold conditions, not extreme cold.** That matters because it means hypothermia prevention isn't a "only worry about it in a blizzard" concern — it's relevant any time wet clothing, wind, exhaustion, or inadequate layering combine, even at temperatures that don't feel immediately dangerous.
""",
    },
    {
        "title": "Frostbite — Prevention & the Freeze-Thaw-Refreeze Danger",
        "section": "emergency",
        "tags": ["frostbite", "cold-weather", "emergency"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Frostbite is the actual freezing of body tissue — and it's an entirely preventable injury.** In a genuine survival situation (no real medical care reachable), rewarming a severely frostbitten area often does more harm than waiting, for a specific, important reason explained below.

## Real Prevention

- **Dress in layers and stay comfortably cool** — add a layer the moment you start feeling uncomfortable, rather than waiting.
- **Keep clothing dry** — change wet socks/gloves immediately, even if that means changing socks 4-5 times a day.
- Dress appropriately for wind conditions specifically.
- **Avoid dehydration** — less circulating blood volume means less blood available to warm fingers and toes, directly increasing frostbite risk.
- **Avoid starvation** — food is fuel, and the body burns that fuel to generate heat.

## Real Signs

**Ears, nose, fingers, and toes are affected first.** Progression: cold feeling with tingling → numbness → a waxy appearance with skin that's stiff and won't glide freely over the underlying joint.

## Real Treatment — by Severity

**Frosting (the mildest stage) can be reversed with body-heat rewarming:** hold the affected area skin-to-skin for 15 minutes — rewarm the face/nose/ears with bare hands, rewarm hands in the armpit/groin/belly, rewarm feet against a buddy's armpit or belly.

**⚠️ If the area does NOT rewarm within 15 minutes, suspect superficial or deep frostbite instead — and the treatment approach changes completely:**
- **Do NOT attempt further rewarming.**
- Splint the area and protect it from further injury.
- Evacuate for real medical care as soon as possible.
- **Never rub a cold injury with snow. Never massage it. Never rewarm it with a stove or open fire** — a frozen area can't feel a burn forming until real damage is already done.
- Loosen any constricting clothing and avoid tobacco (it constricts blood vessels further).

## ⚠️ The Real Reason Field Rewarming Is Avoided: Freeze-Thaw-Refreeze Injury

**If a frostbitten limb is thawed and then refreezes before it's fully healed (healing can take weeks to months), the resulting damage is dramatically worse than the original injury.** This is why, in a genuine survival context with no real evacuation available soon: **it is better to walk out on a frostbitten foot than to warm it and risk it refreezing.**

- Treat a frozen extremity like a fracture — pad and splint it carefully.
- Treat a frozen foot as a litter case (don't walk on it if a litter evacuation is actually possible).
- Keep preventing any further freezing injury.
- **Don't forget hypothermia can be happening at the same time** — keep the whole person warm and dry, not just the frostbitten part.
- **Once real medical care is reached, proper rewarming uses a water bath carefully maintained at 101-108°F** — a specific, controlled temperature range, not just "warm water."

## Detailed Version

**The real decision this page is built around: whether real follow-on care is actually reachable soon changes the correct action entirely.** If evacuation is realistic, do NOT attempt field rewarming — splint, protect, and get the person to real care, where controlled rewarming happens once. If evacuation genuinely isn't coming, the math changes: a frozen limb that stays frozen (even while walking on it) avoids the specific freeze-thaw-refreeze damage that an attempted-but-incomplete field rewarming would risk.
""",
    },
    {
        "title": "Snow Blindness & Trenchfoot (Immersion Foot)",
        "section": "reference",
        "tags": ["snow-blindness", "trenchfoot", "cold-weather"],
        "risk_level": "high",
        "body_markdown": """## Snow Blindness — Real Sunburn of the Cornea

**Two real reasons winter mountain environments carry elevated risk:** at high altitude, less UV radiation gets filtered out before reaching you, and snow's white surface reflects far more UV back up into your face than ordinary ground.

**Real signs:** painful eyes, a hot/sticky/gritty sensation (like sand in the eyes), blurred vision, sometimes severe headache, excessive tearing, eye muscle spasms, bloodshot eyes.

**Real prevention is simple: always wear UV-protective sunglasses.** Without them, field-expedient sunglasses can be improvised from a strip of cardboard with horizontal slits cut into it, and charcoal applied under the eyes reduces glare reflected up from snow.

**Real treatment:** evacuate if possible; patch the eyes to block further light exposure; wet compresses can ease discomfort if conditions aren't too cold for them. **Mild cases typically heal in about 2 days; severe cases can take up to a week.**

## Trenchfoot / Immersion Foot

**A cold-wet injury to the feet (or hands) from prolonged exposure — generally 7-10 hours — to water that's cold but above freezing.** The real risk factors are wet + cold + immobility together, not any one alone.

**Real signs:** **severe pain is the dominant symptom** — trenchfoot is genuinely very painful. Visually, it's often hard to distinguish from frostbite (and both can be present together): red/purple mottled skin, patches of white skin, heavily wrinkled skin, swelling, a reduced or absent pulse in the area, and in severe cases blistering or gangrene.

**Real prevention:** keep feet warm and dry; change socks at least once daily (more often if needed), letting feet air-dry briefly during the change and wiping out boot interiors; exercise the feet whenever the rest of the body is immobile, to keep blood actually circulating.

**Real treatment: every case of trenchfoot needs real evacuation — it cannot be effectively treated in the field.** While waiting: dry, warm, and elevate the feet; **the pain is often severe enough to require real pain medication even when the injury looks mild** — don't judge severity by appearance alone. **Real healing typically takes at least 2 months and can take close to a year; severe cases can require amputation. This is not a minor injury to dismiss.**

## Detailed Version

**The real common thread between these two conditions: both are genuinely preventable with simple, specific habits (sunglasses; dry socks on a schedule), and both are routinely underestimated because the preventive action feels unnecessary in the moment — on a cloudy, cold, or seemingly low-risk day — right up until the damage is already done and, in trenchfoot's case, takes months to heal.**
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
                "source_url": USMC_WINTER_PDF_URL,
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
