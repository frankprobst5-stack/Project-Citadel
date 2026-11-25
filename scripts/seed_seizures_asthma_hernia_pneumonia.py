#!/usr/bin/env python3
"""Seeds 4 more real pages from Where There Is No Doctor: Seizures &
Epilepsy, Asthma, Hernia, and Pneumonia -- all mined from the real
text layer already extracted to /tmp/nodoctor.txt.

Seizure first aid (nothing in the mouth, ever -- not food, not an
object "to stop tongue-biting") is used directly; it matches current
guidance (the old "swallowing the tongue" myth this corrects against
is itself long-settled, not a recent change).

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_seizures_asthma_hernia_pneumonia.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Seizures & Epilepsy",
        "section": "emergency",
        "tags": ["seizures", "epilepsy"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**During a seizure:**
1. **Clear away anything hard or sharp nearby** so the person doesn't injure themselves while convulsing.
2. **Put nothing in their mouth — ever.** No food, no liquid, no medicine, no object to "stop them biting their tongue." This old idea is wrong and causes real injury (broken teeth, a blocked airway) — don't do it.
3. Let them sleep afterward if they become drowsy — that's normal.
4. **If a seizure lasts more than 15 minutes, this is a real emergency** — get medical help immediately.

**In a small child, high fever or severe dehydration are common causes** — cool a feverish child with water, and start rehydration if that's the likely cause. In a very ill person, consider meningitis, cerebral malaria, or poisoning. In a pregnant woman, consider eclampsia (see Danger Signs in Pregnancy). **Try to identify and treat the real cause, not just the seizure itself.**

## Detailed Version

**Epilepsy** causes recurring seizures in someone who otherwise seems healthy — episodes can be minutes, days, or months apart, and can range from brief "blanking out" to full convulsions with eyes rolling back. It's not contagious and not something caught from another person; it can run in families, follow brain injury at birth, high infant fever, or (less commonly) a parasitic brain cyst.

Real medicines (phenobarbital, phenytoin) can prevent seizures in epilepsy but don't cure it — they're typically a lifelong treatment, used at the lowest dose that actually controls seizures. **These specific medications should never be injected into a muscle** — IV injection by someone experienced is the only safe injectable route; otherwise they're given by mouth or, during a prolonged seizure, as a rectal (not intramuscular) dose under real medical guidance.
""",
    },
    {
        "title": "Asthma",
        "section": "reference",
        "tags": ["asthma", "respiratory"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Signs:** wheezing/hissing breath sounds (especially breathing out), the skin behind the collarbones and between ribs pulling in with each breath, and in severe cases blue lips/nails or swollen neck veins. Usually no fever.

**During an attack:**
- Move to the cleanest available air (leave a smoky or dusty room).
- Stay calm and keep the person calm — anxiety measurably worsens an attack.
- Give plenty of fluids — this helps loosen mucus.
- **Use a rescue inhaler (albuterol/salbutamol) as needed** — breathe it in as deeply as possible. A spacer attachment helps more of the dose actually reach the lungs.
- **Severe attack, not improving with the rescue inhaler:** oral steroid (prednisolone) is the next step, continued for several days — this needs real medical guidance on dosing. Epinephrine injection is a last-resort emergency option if no other medicine is available.
- If it isn't improving — get real medical help.

## Detailed Version

**Frequent attacks, or breathlessness during normal walking or mild exertion, is a sign the condition needs a daily controller inhaler** (an inhaled steroid), not just rescue treatment during attacks — using a controller consistently prevents attacks rather than just responding to them, and is both cheaper and safer long-term than constant emergency treatment.

**Real triggers worth controlling for:** allergens, cigarette smoke (including from someone else smoking nearby), smoke from indoor cooking fires, air pollution. Keeping animals outside the home, airing bedding in sunlight, and — if genuinely possible — relocating to cleaner air are all real, documented ways to reduce attack frequency, not just comfort measures.
""",
    },
    {
        "title": "Hernia",
        "section": "reference",
        "tags": ["hernia"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

A hernia is a tear in the muscle wall of the belly that lets a loop of gut push through, forming a lump under the skin — commonly from lifting something heavy or straining. Most common in the groin, especially in men.

**Real way to tell a hernia from a swollen lymph node in the same area:** a hernia lump gets noticeably bigger when the person coughs or lifts something; a swollen lymph node does not change size with coughing.

**Living with a hernia:** avoid heavy lifting; a truss (a simple padded support, worn against the groin) can help hold it in place.

**Lift correctly to prevent one:** bend the knees and lift with the legs, not the back.

## When a Hernia Becomes an Emergency

**If a hernia suddenly becomes large or painful:** lie down with feet higher than the head and gently press the bulge back in. If it won't go back in — that's a real emergency, get medical help.

**If it becomes very painful, causes vomiting, and the person can't have a bowel movement — this is dangerous and may need surgery.** Get medical help fast; in the meantime, treat it the same way as suspected appendicitis (rest, nothing by mouth, seek a hospital).

## Detailed Version

The reason an irreducible hernia (one that won't push back in) is dangerous: the trapped loop of gut can lose its blood supply, which is the same underlying mechanism behind the acute-abdomen emergency category — this is exactly why the recommended stopgap treatment mirrors appendicitis care rather than being treated as "just a hernia."
""",
    },
    {
        "title": "Pneumonia",
        "section": "reference",
        "tags": ["pneumonia", "respiratory", "illness"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Signs:** sudden chills then high fever, rapid shallow breathing (sometimes with grunting or wheezing, nostrils flaring with each breath), cough (often with yellow/green/rust-colored or slightly bloody mucus), chest pain, the person looks genuinely very ill. Note: newborns and very weak/elderly people can have severe pneumonia with little or no fever — don't rule it out just because fever is absent.

**A real, countable warning sign — fast breathing by age:**
- Newborn: more than 60 breaths/minute
- 2 months–1 year: more than 50 breaths/minute
- 1–5 years: more than 40 breaths/minute

(Don't count while the child is crying or right after crying — wait until they're calm.)

**Treatment:** antibiotics are genuinely life-or-death for pneumonia — penicillin, amoxicillin, cotrimoxazole, or erythromycin under real medical dosing guidance. Fever/pain control (acetaminophen is safer than aspirin for children under 12), plenty of fluids, and loosening mucus with fluids/steam.

## Detailed Version

**Pneumonia often follows another respiratory illness** — measles, whooping cough, flu, bronchitis, or an asthma attack — or comes after any serious illness that leaves someone weakened, especially babies and the elderly. A sick child whose breathing is fast AND shallow, more than anything else on this list, is the real signal to suspect pneumonia specifically.

If breathing is both rapid and *deep* (not shallow), that points toward dehydration or hyperventilation instead — a real, useful distinction for telling these apart without needing other equipment.
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
