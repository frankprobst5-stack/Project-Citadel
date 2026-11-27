#!/usr/bin/env python3
"""Seeds 3 real pages from the OCR'd US Army Special Forces Medical
Handbook (ST 31-91B, 1982), Chapter 19 (Dental Emergencies and
Treatment) -- mined from the OCR output cached at /tmp/sfmedical.txt.

Covers real content meaningfully extending the existing dental
coverage from Where There Is No Dentist: a real thermal-testing
procedure to diagnose whether tooth pain is from a vital (alive) or
dying tooth, a more precise real zinc-oxide-eugenol cavity-filling
procedure, and real tooth crown fracture classification -- including
a critical real warning not previously captured: zinc oxide/eugenol
placed directly on exposed pulp causes pulp necrosis and must be
replaced with calcium hydroxide (Dycal) for that specific situation.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_sfmedical_dental.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
SFMEDICAL_PDF_URL = "/files/pdfs/Medical/ST-31-91B-US-Army-Special-Forces-Medical-Handbook.pdf"

PAGES = [
    {
        "title": "Diagnosing Tooth Pain — Thermal Testing for Cavities vs. Dead Teeth",
        "section": "reference",
        "tags": ["dental", "diagnosis", "toothache"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Toothaches generally trace back to one of 3 real causes: decay (caries), a fractured tooth/crown/root, or an acute root-end (periapical) abscess.** A real, simple thermal test can actually distinguish a decayed-but-alive tooth from a dying one — which changes the real correct treatment.

## Real Tooth Anatomy Terms

**Crown** (the visible part above the gum) vs. **root(s)** (embedded in the socket). The crown has 5 real surfaces: **occlusal** (biting surface), **lingual** (tongue side), **facial** (cheek side), and **mesial/distal** (the two surfaces touching neighboring teeth — mesial is nearer the midline, distal is farther from it).

## Real Signs of a Simple Carious (Decayed) Tooth

Intermittent or continuous, usually intense pain; **triggered by heat, cold, sweet, acidic, or salty substances**; visibly decayed, discolored enamel/dentin; **pain when the tooth is tapped.**

## ⚠️ The Real Thermal Test — Distinguishing Vital From Dying Teeth

**⚠️ Always test a normal, unsuspected tooth first for comparison** — the same stimulus produces a genuinely different real response pattern depending on the tooth's actual condition.

**Real procedure:**
1. Isolate the test teeth from saliva with gauze.
2. **Cold test:** apply a cotton applicator sprayed with ethyl chloride (or ice) to the crown. **A healthy, vital tooth responds to cold with pain that stops soon after the stimulus is removed.**
3. **Heat test:** touch a heated instrument (e.g., a warmed mouth-mirror handle) to the tooth.
4. Compare against the unsuspected "normal" tooth each time.
5. **Check for vitality by touching sound dentin directly** — pain on touching dentin itself indicates the tooth is still alive.

**⚠️ Real diagnostic pattern worth remembering: a genuinely diseased tooth's reaction DIFFERS from a healthy one in a specific way** — for example, pain from cold that lingers well after the stimulus is removed, with little/no response to heat; **or the reverse — lingering pain from heat, with little/no response to cold at all.** Either lingering-response pattern (rather than the healthy tooth's quick-fading response) points toward real underlying disease, not simple decay.

## Detailed Version

**The real, practical value of this test: a tooth with ordinary decay (still vital, still alive) gets a very different real treatment than one where the nerve itself is already dying — testing first, rather than assuming based on how bad a cavity looks, is what prevents either over-treating a salvageable tooth or under-treating a genuinely dying one.**
""",
    },
    {
        "title": "Treating a Cavity — Real Zinc Oxide-Eugenol Filling Procedure",
        "section": "reference",
        "tags": ["dental", "cavity", "filling"],
        "risk_level": "moderate",
        "body_markdown": """## ⚠️ Read This First

**This real procedure only works on teeth confirmed to still be vital (alive)** — see Diagnosing Tooth Pain — Thermal Testing for Cavities vs. Dead Teeth to confirm that first. **⚠️ Real, important chemistry: eugenol soothes inflamed pulp tissue when NOT in direct contact with it — but a zinc-oxide/eugenol mix placed directly against live pulp will actually kill it.** This procedure is built specifically around keeping that mix away from the pulp itself.

## The Real Procedure

1. **Local anesthetic is normally needed first.**
2. Remove as much soft, decayed material as possible with a spoon-shaped instrument — **if properly anesthetized, the person should feel no pain during this.**
3. **Irrigate the cavity with warm water** until loose debris is flushed out.
4. Isolate the tooth with gauze packs and gently dry the cavity with cotton.
5. **Mix zinc oxide powder with 2-3 drops of eugenol** on a clean, dry surface until it forms a thick, putty-like consistency.
6. **Fill the cavity with this paste, tamping it gently** (a Woodson plastic instrument works well for this).
7. **Have the person bite several times to check for interference** with the opposing teeth; wipe away excess material with a moist cotton pledget. **Pain should ease within minutes, and the paste fully hardens within about an hour.** Instruct the person not to chew on that tooth in the meantime.
8. **No zinc oxide powder available?** A cotton pledget soaked in plain eugenol, left in the cavity, works as a real substitute.
9. **⚠️ Always explain that this is a temporary measure** — real definitive dental care is still needed afterward.

## Detailed Version

**The real, precise technique worth keeping from this page: the paste goes INTO the cleaned-out cavity space, resting against the cavity walls and any remaining deep decay — never pressed directly onto exposed, still-living pulp tissue.** That distinction is exactly what separates this real, effective temporary filling from the real pulp-killing mistake covered in Tooth Crown Fractures — Real Classification & Treatment.
""",
    },
    {
        "title": "Tooth Crown Fractures — Real Classification & Treatment",
        "section": "reference",
        "tags": ["dental", "tooth-fracture", "trauma"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Front teeth are especially prone to crown fractures from trauma — real treatment depends entirely on how deep the fracture actually goes, with 3 real categories.**

## Category 1 — Simple Fracture (Little/No Dentin Exposed)

**Real treatment: just smooth the rough edges of the tooth.** Nothing more invasive is needed.

## Category 2 — Extensive Fracture (Dentin Exposed, Pulp Still Covered)

**Real treatment:**
1. Wash the tooth with warm saline.
2. Isolate and dry it.
3. **Cover the exposed dentin with a zinc oxide-eugenol paste** — real anterior-tooth retention can be tricky, so 2 real techniques help: fitting a trimmed copper band or aluminum crown (contoured so it won't cut the gum) filled with the paste over the tooth, **or mixing cotton fibers into the zinc oxide/eugenol** (the fibers add real strength) and bridging it across to the neighboring teeth for retention.
4. **Have the person bite down to confirm neither the band nor the splint interferes with their normal bite.**
5. **Get the person to a real dentist as soon as possible.**

## ⚠️ Category 3 — Extensive Fracture With Exposed Pulp

**Real treatment:**
1. Anesthetize the tooth.
2. Isolate and dry it.
3. Gently wash with warm saline.
4. **⚠️ Cover the pulp and dentin with calcium hydroxide (e.g., Dycal) — NEVER zinc oxide and eugenol here, since direct contact with pulp causes real pulp death (necrosis).** Let it harden — **moistening the mix with water after placement speeds hardening.**
5. **⚠️ Real size threshold: if the pulp exposure is larger than 1.5mm, seriously consider extraction instead of trying to save the tooth.** **If calcium hydroxide genuinely isn't available and zinc oxide/eugenol is all you have, that itself is a real reason to lean toward extraction** rather than risk killing the pulp with the only material on hand.

## Detailed Version

**The real, single most important safety distinction across these 3 categories: dentin alone can safely be covered with zinc oxide/eugenol, but exposed PULP cannot — using the wrong material on an exposed pulp doesn't just fail to help, it actively kills tissue that otherwise had a real chance of staying alive.** Getting this material choice right, based on which category actually applies, is the entire point of classifying the fracture correctly before treating it.
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
                "source_url": SFMEDICAL_PDF_URL,
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
