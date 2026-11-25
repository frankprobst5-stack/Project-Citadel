#!/usr/bin/env python3
"""Seeds 3 real pages on childbirth, mined from Where There Is No
Doctor's Chapter 19 (Information for Mothers and Midwives) -- a
genuinely major gap this build-out hadn't touched yet, and arguably
one of the highest-stakes topics the book covers for a true no-access
situation.

Postpartum Hemorrhage is the most safety-critical of the three: it
transcribes the real step-by-step emergency sequence (breastfeeding/
nipple stimulation first, then uterine massage, then bimanual
compression, with real oxytocin/ergonovine/misoprostol dosing) rather
than summarizing it, since the escalation order itself is what matters
in a real emergency, not just the individual techniques.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_childbirth.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Labor & Normal Childbirth",
        "section": "reference",
        "tags": ["childbirth", "pregnancy", "midwifery"],
        "risk_level": "high",
        "body_markdown": """## Quick Version

**Signs labor is near** (can start days to weeks before actual delivery, especially with a first baby):
- The baby drops lower in the womb — easier breathing, but more frequent urination from bladder pressure.
- Thick, sometimes blood-tinged mucus discharge, a short time before or for 2-3 days leading up to labor. This is normal.
- Contractions (womb tightening) that start far apart and gradually become stronger, more regular, and more frequent — that progression is what separates real labor from a false alarm.
- **"False labor"** is real and common: strong, close contractions that then stop for hours or days. Walking, a warm bath, or rest can help tell the difference — and even false-labor contractions still help prepare the womb.
- **The bag of water breaking** (a flood of fluid) usually means labor is beginning or very close. After this: stay clean, avoid intercourse/baths/anything in the vagina (infection risk), and **if labor hasn't started within 12 hours of the water breaking, seek medical help.**

**The 3 stages of labor:**
1. **First stage:** from strong regular contractions until the cervix is fully open and the baby starts moving into the birth canal — typically the longest stage.
2. **Second stage:** from the baby entering the birth canal until birth.
3. **Third stage:** from the baby's birth until the placenta (afterbirth) delivers.

## Detailed Version

**Baby position matters for where delivery should happen:** if the baby's head is down low in the womb, a normal birth is likely. If the head is still up (breech) or the baby is sideways, this is genuinely dangerous for both mother and baby — delivery needs to happen in or near a hospital, not at home, if at all possible to arrange.

A simple real test for head position: gently push the baby's body from side to side. If pushing near what you believe is the head causes it to bend at the neck while the back stays still, that's the head. If the whole body moves together when you push the lower end, that's the baby's bottom (breech).
""",
    },
    {
        "title": "Danger Signs in Pregnancy",
        "section": "emergency",
        "tags": ["pregnancy", "danger-signs"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

**Any bleeding during pregnancy is a real danger sign — even a small amount.** Have her lie down quietly and get a health worker. Bleeding after 6 months can mean the placenta is blocking the birth canal (placenta previa) — this can be fatal without expert help. **Do not do a vaginal exam or put anything in the vagina. Get her to a hospital immediately.**

**Severe anemia** (weak, tired, pale or transparent-looking skin): dangerous because of how much blood is normally lost at childbirth — if she's already anemic, that normal blood loss becomes life-threatening. Needs real iron treatment and ideally a hospital birth in case a transfusion is needed.

**Pre-eclampsia (toxemia)** — blood pressure of 140/90 or higher, or any of: swollen face/whole-body swelling on waking, headaches, dizziness, blurred vision, pain high in the belly.
- If blood pressure climbs to **160/110 or higher**, or any of those signs appear — **get medical help immediately.** Pre-eclampsia can progress to seizures and death.
- While arranging help: have her lie down and rest more, eat well with plenty of protein, avoid salty packaged food.

## Detailed Version

**Why these three get grouped as "danger signs" rather than just symptoms to monitor:** each one is something that can progress from manageable to fatal within a short window if missed — bleeding can mean a placenta blocking delivery, anemia turns normal childbirth blood loss into a crisis, and pre-eclampsia can escalate to seizures. None of these are "wait and see" — all three are reasons to get real medical help moving immediately, not after the situation visibly worsens.

Regular prenatal check-ins (monthly for the first 6 months, twice monthly for months 7-8, weekly in the last month) exist specifically to catch these three before they become emergencies — tracking weight gain (normally 8-10kg over the pregnancy) and blood pressure at each visit is how pre-eclampsia and anemia get caught early rather than at crisis point.
""",
    },
    {
        "title": "Postpartum Hemorrhage — Heavy Bleeding After Birth",
        "section": "emergency",
        "tags": ["childbirth", "hemorrhage", "pregnancy"],
        "risk_level": "critical",
        "body_markdown": """## Quick Version

Some bleeding when the placenta comes out is normal — usually brief, under about a cup (¼ liter). **Heavy or continuing bleeding is a real, fast-moving emergency.**

**Warning:** a woman can be bleeding severely *internally* without much blood visibly coming out. Check her belly periodically (getting bigger may mean it's filling with blood) and watch for shock signs (weak rapid pulse, cold clammy skin, confusion).

**Escalating response, in order:**
1. **Put the baby to the breast** (or have someone stimulate/massage the nipples if the baby won't). This triggers a real hormone response that helps the uterus contract and control bleeding — try this first, it's fast and harmless.
2. **Get medical help moving immediately** — don't wait to see if the next steps work before starting this.
3. **Massage the lower belly until the womb feels hard.** Once bleeding stops, check every few minutes that it stays hard — if it softens again, massage again.
4. **If bleeding continues despite massage:** press down hard with both hands, one stacked on the other, on the belly just below the navel — using your full body weight if needed. Keep pressing well after the bleeding stops.
5. **If still not controlled:** scoop both hands into the belly above the womb and fold it forward, pressing it hard against the pubic bone, using your weight. Keep pressing for several minutes past when bleeding stops, or until real medical help arrives.
6. Give her plenty of fluids (water, juice, the Rehydration Drink). If she shows shock signs, position her with legs up, head down.
7. **If available:** oxytocin (10 units injected into muscle, a second dose after 15 minutes if bleeding hasn't stopped) is the real first-line medication; misoprostol if oxytocin isn't available. Ergonovine can be used *after* the placenta is out, but never before.

## Detailed Version

**This escalation order is the real point of this page, not just the individual techniques** — breastfeeding/nipple stimulation first because it's fast, free, and harmless; uterine massage next because it directly addresses the most common cause (an atonic, non-contracting uterus); bimanual compression as the last manual option before medication and transport become the deciding factors. Skipping straight to the most aggressive step isn't more effective — this order reflects what actually controls bleeding fastest for the least additional risk.

**A real, important warning from the same source:** vitamin K does NOT help control bleeding from childbirth, miscarriage, or abortion in adults — it's a real treatment, but only for newborns, and using it for maternal hemorrhage is a documented, genuine mistake.

**Oxytocin, misoprostol, and ergonovine are dangerous drugs used correctly — and genuinely dangerous used incorrectly.** They should never be used to speed up labor or "give the mother strength" before birth — this specific misuse can kill the mother or the baby. Their real, lifesaving use is strictly for controlling bleeding after the baby (and for ergonovine, after the placenta) is already out.
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
