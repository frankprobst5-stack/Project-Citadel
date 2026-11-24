#!/usr/bin/env python3
"""Seeds 2 more real Emergency Now pages: Burns and Fractures/Sprains.

Both mined from the real Army First Aid manual already in the Vault
(Medical/FM-4-25-11-First_Aid.pdf, confirmed to have a real text layer
before transcribing anything) -- Chapter 3 (Burn Injuries) and Chapter
4 (Fractures) respectively.

Fracture splinting principles (splint in the position found, never
realign, immobilize the joint above and below, check circulation
before/after) are stable, current first-aid practice -- used directly
from the manual with no cross-check needed.

Burns needed one real correction, though: the military manual's own
procedure (remove the source, expose, dry dressing, no water/ointment)
is written for a combat-casualty context where evacuation may be
delayed -- it does NOT include the single most important civilian
first-aid step for an ordinary minor burn: cooling it under cool
running water for several minutes, which measurably limits how deep
the burn goes. Both are included here, clearly separated by which
situation each applies to -- using only the military manual would have
quietly dropped real civilian guidance that actually matters for the
common case.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_burns_fractures.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Burns — Minor and Severe",
        "tags": ["burns", "first-aid"],
        "risk_level": "high",
        "source_url": FIRST_AID_PDF_URL,
        "body_markdown": """## Quick Version

**Minor burn (small, doesn't involve a joint/face/genitals, skin not charred or leathery):**
1. **Cool it** under cool (not ice-cold) running water for about 10 minutes — this is the single most important step; it limits how deep the burn actually goes, and still helps up to an hour after the injury.
2. Gently clean with soap and water.
3. A thin layer of petroleum jelly or aloe is fine on a minor burn — loosely cover with a clean dressing.

**Severe burn, electrical burn, chemical burn, or a burn to the face/joints/genitals — call 911.**
1. **Eliminate the source first.** If clothing is on fire, roll the person on the ground to smother it (not if they're wearing synthetic fabric that could melt). For an electrical burn, don't touch the person until the power is confirmed off — use a dry, nonconductive object to move them if needed.
2. **Do not clean a severe burn** — cleaning can cause more skin damage. Cut away (don't pull) any clothing over the burn, but leave anything stuck to it alone.
3. Cover loosely with a clean, dry dressing. **Never apply grease or ointment, never break any blisters.**
4. **For chemical burns:** flush with large amounts of water if it's a liquid chemical. For a dry chemical, brush off loose particles first (not with your bare hand), then flush with water — but if only a small amount of water is available, don't apply any (a little water on some dry chemicals can trigger a reaction).

## Detailed Version

**Why cooling matters for minor burns, and why severe burns skip some of these steps:** cool running water actively draws heat out of the skin and slows the burn's progression — genuinely the most effective single thing you can do for an ordinary burn, and it's safe to do even an hour after the injury. For a severe burn headed to a hospital, cleaning and ointment are skipped specifically because they can complicate the wound a medical team will need to treat anyway — this isn't a contradiction, it's a different priority for a different severity.

**Electrical burns can look deceptively small on the surface** — check for both an entry and an exit wound; the exit point from a shock can be anywhere on the body regardless of where contact first occurred, and the real internal damage is often far worse than the visible skin injury suggests. High-voltage shock can also cause temporary unconsciousness or heart rhythm problems — treat any electrical burn as potentially more serious than it looks.

**White phosphorus** (a military/industrial hazard, not a household one) should be smothered with wet cloth or mud and kept wet to exclude air, which stops the particles from continuing to burn.
""",
    },
    {
        "title": "Fractures, Dislocations & Sprains — Splinting",
        "tags": ["fractures", "sprains", "first-aid"],
        "risk_level": "high",
        "source_url": FIRST_AID_PDF_URL,
        "body_markdown": """## Quick Version

**Signs of a fracture:** deformity, tenderness, swelling, pain, inability to move the part, a bone visibly out of place or protruding, bleeding, or discolored skin. **If you're not sure whether it's broken, treat it as a fracture anyway** — treating a sprain like a fracture costs little; treating a fracture like a sprain risks real injury.

**Do not:**
- Try to move the injured part to "test" whether it's broken — that risks real additional damage.
- Try to realign or straighten it — **splint it in the exact position you found it.**
- Push a protruding bone back under the skin — cover it with a clean dressing and leave it alone.
- Move someone with a suspected back or neck injury unless an immediate danger (fire, explosion) forces it.

**To splint:**
1. Gather splint material (boards, sticks, rolled magazines — anything rigid) long enough to extend past the joint above AND below the injury.
2. Pad the splint anywhere it touches a bony point (wrist, elbow, knee, ankle).
3. Place a splint on each side of the injury, secure with at least 4 ties (2 above, 2 below the injury site itself — never tie directly over the fracture), knots on the outside, away from the skin.
4. **Check circulation before and after splinting:** skin color, warmth, and how fast color returns when you press a nail bed. If it's noticeably paler, colder, or slower to refill than the uninjured side, the splint may be too tight — loosen and recheck.

## Detailed Version

A dislocation (joint out of place) and a sprain (torn connective tissue) get the same treatment as a closed fracture — splint and immobilize, don't try to diagnose which one it is in the field, since the first-aid response is identical either way.

An **open fracture** (bone breaks through the skin) is automatically a contaminated wound — cover it with a clean dressing before splinting, and treat the infection risk as real, not hypothetical.

The whole point of immobilizing is to stop sharp bone edges from moving further and cutting into surrounding tissue, blood vessels, or nerves — this is what actually prevents a closed fracture from becoming an open one, and what limits pain and shock. Checking circulation isn't optional busywork: numbness, tingling, or a cold/pale/bluish limb below the injury is a real sign of impaired blood flow that can threaten the limb itself, and that casualty needs to be evacuated and treated promptly, splint or no splint.
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
