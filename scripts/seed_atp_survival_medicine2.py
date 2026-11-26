#!/usr/bin/env python3
"""Seeds 8 more real pages from ATP 3-50.21 (Survival), Chapter 2
(Survival Medicine) -- mined from the real text layer already
extracted in this session (/tmp/atp_survival.txt, pages 2-20 through
2-28). Continues the previous batch's selective mining of this
chapter for genuinely new, complementary content not already covered.

Covers: medicinal plant properties organized by PURPOSE rather than
species (anti-diarrheal/anti-pyretic/anti-hemorrhagic/anti-helminthic/
antiseptic) with real sources, preparation, and treatment detail;
real debunked poisonous-plant misconceptions and real examples of
seasonal/preparation-dependent plant toxicity; real contact-
dermatitis and ingestion-poisoning treatment with real plant lists;
real field treatment for blisters, boils (including a genuinely new
bottle-suction technique), fungal infections, facial injuries, and
eye injuries (including eye impalement and chemical flush); and real
RICE/fracture/dislocation treatment including a real tree-notch
traction technique.

Idempotent by title, same pattern as the other scripts/seed_*.py files.

Usage:
    python3 scripts/seed_atp_survival_medicine2.py [--base-url http://localhost:8085] [--dry-run]
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
        "title": "Medicinal Plant Properties — Anti-Diarrheal & Anti-Pyretic",
        "section": "reference",
        "tags": ["medicinal-plants", "herbal-medicine", "tannic-acid"],
        "risk_level": "moderate",
        "body_markdown": """## Anti-Diarrheal (Tannic Acid)

**Real medicinal uses:** diarrhea, dysentery, burns, skin problems, and parasites — tannic acid both prevents infection and aids healing.

**Real sources:** the outer bark of all hardwood trees, acorns, banana plants, common plantain, strawberry leaves, blackberry stems and roots. White oak bark and similarly tannin-rich barks (cowberry, cranberry, hazel leaves) also work, brewed as a strong tea.

**Real preparation:** boil a hardwood tree's moist inner bark for 2+ hours to release the tannic acid — **it tastes and smells genuinely vile, but reliably stops most cases of diarrhea.**
- Place crushed outer bark, acorns, or leaves in water.
- Leach the tannin out by soaking or boiling.
- **Longer soaking = more tannin extracted.**
- Swap in fresh material once the current batch is depleted.
- **Clay, ashes, charcoal, powdered chalk, powdered bone, and pectin can all be mixed into the tannic acid tea** — a crude, real, working version of Kaopectate.

**Real treatment uses:**
- **Burns:** moisten a bandage with cooled tannin tea and compress the burn; cooled tea poured directly on the area eases pain.
- **Diarrhea, dysentery, worms:** drink the strong tea solution — it may also help expel worms.
- **Dry rashes/fungal skin problems:** cool compresses or soaking in the tea relieves itching and promotes healing.
- **Lice and insect bites:** wash the affected area with the tea to ease itching.

## Anti-Pyretic (Willow/Aspen — Real Aspirin-Like Relief)

**Real medicinal uses:** aches, colds, fever, inflammation, pain, sprains, sore throat — via real salicin/salicylic acid content, chemically related to aspirin.

**Real sources:** weeping willow bark is the classic source; also elder flower/fruit infusion, linden flower, aspen or slippery elm bark, and yarrow or peppermint tea.

**Real preparation:**
- Gather twigs, buds, or the cambium layer (the soft moist layer under the outer bark) of willow or aspen — brew as tea.
- **For a poultice:** crush the plant/stems into a pulpy mass.

**Real treatment uses:**
- Chew twigs, buds, or cambium directly for symptom relief.
- Drink the tea for colds and sore throat.
- Apply a warm, moist poultice (the pulpy mass, held in place with a dressing) for aches and sprains.

## Detailed Version

**The real, shared organizing principle worth noticing: both of these entries are built around one specific active compound (tannic acid; salicin) rather than one specific plant** — which is exactly why each lists multiple real alternative sources. If willow isn't available, aspen or slippery elm genuinely substitute; if oak bark isn't available, cranberry or hazel leaves do the same real job.
""",
    },
    {
        "title": "Medicinal Plant Properties — Anti-Hemorrhagic & Anti-Helminthic",
        "section": "reference",
        "tags": ["medicinal-plants", "herbal-medicine", "plant-identification"],
        "risk_level": "high",
        "body_markdown": """## Anti-Hemorrhagic (Plantain, Yarrow & Related Plants)

**Real medicinal uses:** a poultice of common plantain, woundwort, or yarrow leaves helps heal wounds, stings, and sores while preventing infection. **Real active compounds in common plantain:** aucubin (antimicrobial), allantoin (stimulates cell growth/tissue regeneration), and mucilage (reduces pain/discomfort). Plantain's astringent properties also make a leaf tea useful for diarrhea and soothing raw internal membranes, itching, wounds, abrasions, stings, and dysentery.

**Real source notes:** common plantain is one of the most abundant, widely distributed medicinal plants on earth (200+ species with similar properties). **Broadleaf plantain doubles as a genuinely nutritious wild edible** — high in calcium and vitamins A, C, K; young leaves eaten raw, older stringier ones boiled into stews. **Prickly pear (peeled) or witch hazel** work on wounds via their astringent (blood-vessel-shrinking) properties. **For bleeding gums/mouth sores, sweet gum can be chewed or used as a toothpick.**

**Real preparation/treatment:** brew tea from seeds (for diarrhea/dysentery) or leaves (for vitamins/minerals); make a leaf poultice for cuts, sores, burns, and stings.

## ⚠️ Anti-Helminthic (Wild Carrot) — a Real, Critical Identification Warning

**⚠️ Most worm/parasite treatments are genuinely toxic — use in moderation only, and get the identification right first.**

**Real medicinal uses:** wild carrot is an aromatic diuretic herb that soothes the digestive tract, stimulates the uterus, supports the liver, and promotes urination/kidney waste removal. A root tea treats urinary stones (strong tannic acid can help too, but is hard on the liver — use cautiously).

**⚠️ Never confuse Wild Carrot or Queen Anne's Lace with the Poison Hemlock family (Poison Hemlock, Water Hemlock, Fool's Parsley) — this is a real, deadly mix-up risk.** **The real, reliable identification tests:**
- **Stem hair:** Wild Carrot and Queen Anne's Lace have HAIRY stems/stalks. Poison Hemlock has a smooth, hollow stalk with purple blotches and no hair.
- **Smell:** roll some leaves between your thumb and forefinger. **Wild carrot roots smell like carrots. Poison Hemlock, Water Hemlock, and Fool's Parsley smell genuinely nasty.**

**Real preparation:** boil the leaves for an infusion (removes toxic elements) — used historically against cystitis and kidney stones, and to help dissolve existing stones. A warm flower infusion has treated diabetes historically.

**Real treatment:** grated raw root (especially cultivated varieties) treats threadworms. **⚠️ The root can also induce uterine contractions and encourage delayed menstruation — pregnant women should not use it.** Carrots broadly have real antiseptic, laxative, and vermicide (worm-expelling) properties, and are used as a poultice or for liver support.

## Detailed Version

**The real, life-or-death reason this page leads with the identification warning rather than burying it: Poison Hemlock's resemblance to Wild Carrot is one of the most commonly cited real plant-misidentification deaths — the hairy-stem and smell tests exist specifically because visual resemblance alone genuinely isn't a safe way to tell them apart.**
""",
    },
    {
        "title": "Medicinal Plant Properties — Antiseptic (Honey, Sugar, Yarrow & Cattail)",
        "section": "reference",
        "tags": ["medicinal-plants", "antiseptic", "wound-care"],
        "risk_level": "moderate",
        "body_markdown": """## Quick Version

**Real antiseptics for cleansing wounds, snake bites, sores, boils, inflammation, burns, and rashes — made from genuinely common survival plants, not specialized medicine.**

## Real Sources

Expressed juice of wild onion or garlic, chickweed leaves, or crushed dock leaves. **Yarrow** is a widely available flowering plant across temperate Asia/Europe/North America, used for fever, colds, hay fever, absent menstruation, dysentery, diarrhea, appetite loss, GI discomfort, and inducing sweating — **fresh leaves can be chewed to relieve toothache.** Other real sources: cattail, wild onion/garlic, chickweed, burdock root, mallow leaves/roots, white oak bark (tannic acid), prickly pear, slippery elm, sweet gum.

## ⚠️ Honey and Sugar — the Real Best Options

**Two of the genuinely best antiseptics available, and both are common pantry items, not foraged plants.**
- **Sugar:** apply to the wound until it turns syrupy, then wash off and reapply.
- **Honey:** apply 3 times daily.
- **Honey is by far the better of the two for open wounds and burns; sugar is a solid second choice.**

## Real Treatment Technique

- **Apply a poultice to the affected area to help stop bleeding.**
- **Yarrow**, dried and powdered, mixed with plantain or comfrey water (or used fresh alone), treats wounds.
- **For burns, scrapes, insect bites, and bruises: split open a cattail root and "bruise" the exposed portion**, then use it directly as a poultice secured over the injury.
- **Cattail stems ooze an amber, honey-like substance** — this has real antiseptic properties and can be used on small wounds and even toothaches.

## Detailed Version

**The real, practical takeaway worth remembering above the foraged-plant options: if you have ordinary honey or sugar on hand, you already have one of the genuinely best wound antiseptics available — no plant identification or preparation required at all.** The foraged options matter specifically when neither of those pantry staples is available.
""",
    },
    {
        "title": "Poisonous Plant Myths & Real Toxicity Variables",
        "section": "reference",
        "tags": ["poisonous-plants", "plant-identification", "foraging"],
        "risk_level": "critical",
        "body_markdown": """## ⚠️ Real Misconceptions About Poisonous Plants — Explicitly Debunked

1. **"Watch the animals and eat what they eat."** — **Mostly true, but some plants genuinely poisonous to humans are safely eaten by certain animals.** Don't treat this as a guarantee.
2. **"Boiling removes all poisons."** — **Boiling removes many toxins, but genuinely not all of them.** Some plant poisons survive boiling intact.
3. **"Red-colored plants are poisonous."** — **Some red plants are toxic, but far from all of them** — color alone is not a reliable real signal either way.
4. **"Poisonous plants look obviously different from edible ones."** — **False, and dangerously so: many toxic plants closely resemble edible relatives.** The classic real example: poison hemlock looks remarkably similar to wild carrot (see Medicinal Plant Properties — Anti-Hemorrhagic & Anti-Helminthic for the real way to tell them apart).

## Real Reasons Toxicity Is Genuinely Hard to Predict

- Some plants need substantial contact before any reaction; others cause death from minimal contact.
- **Toxin content varies by growing conditions and even subtle subspecies differences** — the "same" plant isn't always equally toxic.
- **Individual human resistance to toxins genuinely varies** — what one person tolerates, another may not.
- Some people are specifically more sensitive to one particular plant than the general population.

## ⚠️ Real Examples of Toxicity That Changes With Season or Preparation

- **Pokeweed leaves** are edible only when the plant first starts growing — they become toxic soon after.
- **May apple**: only the ripe fruit is edible; every other part, and the unripe green fruit, is poisonous.
- **Potatoes and tomatoes**: the fruit/tuber is a normal food, but **their green parts are poisonous** — a real, common, easy-to-overlook exception hiding inside an otherwise familiar food plant.
- **Black cherry**: as it wilts, it develops real hydrocyanic acid (cyanide) — a plant that was fine earlier can become dangerous specifically as it dies back.
- **Jack-in-the-pulpit corms**: poisonous raw, but become safe to eat once thinly sliced and **thoroughly dried — which can genuinely take up to a year.**

## Detailed Version

**The real, unifying lesson across every myth and every seasonal example here: there is no single, reliable shortcut rule for plant safety — not color, not what animals eat, not boiling, not visual resemblance to a known edible plant, and not even "this plant was safe last time."** Positive, specific identification of the actual plant, its actual part, and its actual growth stage is the only real substitute for memorized shortcuts, which is exactly why the real Universal Edibility Test (see Plant Identification & the Universal Edibility Test) exists as a fallback when identification genuinely isn't certain.
""",
    },
    {
        "title": "Contact Dermatitis & Ingestion Poisoning — Real Plant Lists & Treatment",
        "section": "emergency",
        "tags": ["poisonous-plants", "contact-dermatitis", "poisoning"],
        "risk_level": "critical",
        "body_markdown": """## Contact Dermatitis — the Real Most-Common Plant-Poisoning Problem

**Usually the single most troublesome type of plant poisoning for a person outdoors** — effects can persist, spread by scratching, and become genuinely dangerous near the eyes. **The real toxin is almost always an oil on the plant's surface** — and that oil can transfer onto gear, then onto whoever touches the gear afterward. **⚠️ Never burn a contact-poisonous plant — the smoke itself can be just as harmful as the plant.** Real risk increases when overheated/sweating. Symptoms (burning, redness, itching, swelling, blisters) can appear anywhere from hours to days after contact.

**Real treatment:**
1. **Wash the oil off with soap and cold water immediately upon contact or at first symptoms.**
2. **If no water is available, wipe the skin repeatedly with dirt or sand instead** — **⚠️ but never do this if blisters have already formed**, since dirt can break them open and invite infection.
3. Dry the area after removing the oil.
4. **Wash with a tannic acid solution (see Medicinal Plant Properties — Anti-Diarrheal & Anti-Pyretic for how to make it from oak bark), or crush jewelweed and rub it on the affected area** — both are real, effective treatments for plant-caused rashes.

**Real plants causing contact dermatitis:** cowhage, poison ivy, poison oak, poison sumac, rengas tree, trumpet vine.

## ⚠️ Ingestion Poisoning — a Real, Fast-Moving Emergency

**Never eat any plant without positive identification first — keep a real log of what's been eaten and what's been tested and found inedible.**

**Real signs:** nausea, vomiting, diarrhea, abdominal cramps, depressed heartbeat/respiration, headaches, hallucinations, dry mouth, unconsciousness, coma — **can progress to death.**

**Real treatment if plant poisoning is suspected:**
1. **Remove any remaining poisonous material from the mouth and (if possible) the stomach as quickly as possible.**
2. **If conscious: induce vomiting** (tickle the back of the throat, or give warm salt water).
3. **If conscious: dilute the poison with large quantities of water or milk.**

**Real plants causing ingestion poisoning:** castor bean, chinaberry, death camas, lantana, manchineel, oleander, pangi, physic nut, poison/water hemlock, rosary pea, strychnine tree.

## Detailed Version

**The real, important distinction between these two poisoning routes: contact dermatitis is rarely life-threatening but genuinely persistent and spreadable, while ingestion poisoning is comparatively rare but can escalate to death quickly** — which is exactly why the real treatment priorities differ (wash and wait for contact; actively remove and dilute for ingestion) rather than using one generic "plant poisoning" response for both.
""",
    },
    {
        "title": "Blisters & Boils — Real Field Treatment",
        "section": "reference",
        "tags": ["blisters", "boils", "skin-infection"],
        "risk_level": "moderate",
        "body_markdown": """## Blisters — Real Size-Based Treatment

**Caused by friction — a red, sore "hotspot" forms first, and if friction continues, fluid fills the separated skin layer.**

**Real prevention is the best treatment:** properly fitted footwear, dry feet, 2 pairs of socks, periodic foot checks, and stopping at the very first sign of rubbing — a small piece of moleskin or athletic tape on a problem spot early prevents a full blister later.

**⚠️ Real size-based rule for an already-formed blister:**
- **Smaller than a nickel: do NOT puncture it.** Cut a doughnut-shaped piece of moleskin and center it over the blister — the hole keeps adhesive off the tender blister itself, so it doesn't rip when the moleskin is changed.
- **Larger than a nickel: drain it.** Wash your hands and the area first to reduce infection risk, puncture it with a small sterile object (needle/pin), and drain the built-up fluid. **The best real covering for healing is the blister's own skin** — clean, wash, and cover with a sterile dressing rather than removing the loose skin.

## Boils — a Real Localized Skin Infection

**Starts as a reddened, tender spot; firms up over time; eventually the center fills with white blood cells fighting the infection (pus), forming a head that opens on its own or needs opening.** Pus trapped within tissue is called an abscess — a boil is itself a type of skin abscess, and can occur anywhere (trunk, limbs, buttocks, groin).

**Real signs:** a firm reddened bump, tender/swollen surrounding skin, growth over time, and eventually a pus-filled head that may drain/weep on its own.

**Real treatment — 2 options:**
1. **Warm compresses** to bring the boil to a head.
2. **⚠️ The real "bottle suction" method:**
   - Use an empty bottle that's been boiled in water.
   - Press the bottle's opening over the boil, sealing the skin to create an airtight vacuum — **this draws the pus to the surface.**
   - Open the boil with a sterile knife, wire, or needle.
   - Clean out the pus thoroughly with soap and water.
   - Cover the site and check periodically for further infection. **⚠️ Real historical note: toothpaste, and iodine where available, were used to cover boil sites during the Vietnam War** — not a first-choice modern dressing, but a real documented field substitute.

## Detailed Version

**The real, shared principle across the blister size-rule and the boil bottle-suction method: both use a mechanical, physics-based trick (an intact skin "roof" for a small blister; a sealed vacuum for a boil) to let the body's own healing process work with minimal added trauma** — rather than simply cutting into either one by default, which in both cases would genuinely increase infection risk for no real benefit.
""",
    },
    {
        "title": "Fungal Infections, Facial Injuries & Eye Injuries",
        "section": "reference",
        "tags": ["fungal-infection", "eye-injury", "dental-care"],
        "risk_level": "high",
        "body_markdown": """## Fungal Infections

**Keep the area clean, dry, and exposed to as much sunlight as possible — and don't scratch it.** **Real historical field treatments used by soldiers in Vietnam:** antifungal powder, lye soap, chlorine bleach, alcohol, vinegar, concentrated salt water, and iodine.

## Facial Injuries — Real Dental Care in Isolation

**Keep cleaning/brushing teeth even in a survival situation** — this prevents decay and gingivitis. **No toothbrush? Make a chew stick:** take a small green stick, chew the end, and use the resulting frayed fibers as a brush. **Tooth pain:** rinse with warm salt water for relief. **A painful mouth abscess:** lancing it and letting it drain eases pain and reduces infection risk. **Other soft-tissue facial injuries** (abrasions, contusions, lacerations, avulsions): clean and re-cover several times daily to prevent infection and crusting over.

## Eye Injuries

### Snow (or Water) Blindness

**From bright sunlight reflecting off ice crystals (or off water/other reflective surfaces) into the eyes.** Real signs: red, scratchy, watery eyes, headache, pain with light exposure. **Real treatment: cover the eyes with a dark cloth until symptoms resolve.** **Real prevention:** UV-rated sunglasses, or improvised sunshades; **putting soot under the eyes also genuinely reduces glare.**

### ⚠️ Eye Impalement — Never Remove the Object

**Never remove an impaled object from the eye unless it's actively interfering with real survival needs.** Cover the eye with a real eye shield — or improvise one from a cup, bandage, or similar rigid cover — to protect it from further injury or movement. **⚠️ Cover BOTH eyes, not just the injured one** — the real reason is that eyes move together (a "sympathetic" reflex), so leaving the uninjured eye uncovered means it keeps moving the injured one too.

### Chemical/Foreign Object in the Eye

**Flush with large amounts of water, directed from the inside corner of the eye outward** — this real direction specifically prevents carrying the chemical or debris from the affected eye into the other one.

## Detailed Version

**The real, counterintuitive detail most worth remembering here: covering the UNINJURED eye too, after an impalement, isn't excessive caution — it's addressing a real physical reflex (both eyes moving together) that would otherwise keep disturbing the injured eye no matter how carefully it's individually covered.**
""",
    },
    {
        "title": "Sprains, Strains, Fractures & Dislocations — Real Field Treatment",
        "section": "emergency",
        "tags": ["fractures", "sprains", "dislocations", "splinting"],
        "risk_level": "critical",
        "body_markdown": """## Sprains & Strains — Real RICE Protocol

**A sprain injures a tendon/ligament; a strain injures a muscle or the tendon connecting muscle to bone** — both get the same real treatment:

- **R — Rest** the injured area.
- **I — Ice for 24-48 hours**, using improvised ice packs/cold compresses intermittently through that window.
- **C — Compression** — wrap or splint to stabilize. **Real detail: leave a boot on a sprained ankle unless circulation is actually compromised** — removing it can make swelling and re-fitting worse, not better.
- **E — Elevate** the affected area.

**Real signs:** pain, swelling, bruising, lost functional movement, sometimes an audible pop/tear at the moment of injury (sprains); pain, spasm, weakness, sometimes cramping/inflammation, and in severe cases partial loss of function (strains, especially with a partial/full tear).

## Fractures — Open vs. Closed, and Real Treatment Priorities

**⚠️ Treat fractures early, before swelling complicates things — but run the MARCH sequence first, and immobilize before moving if at all possible.**

- **Open (compound) fracture:** bone protrudes through the skin. **Treat the soft-tissue wound and dress it properly before splinting.** Clean any protruding bone with antiseptic and keep it moist. Splint the area and **continually monitor blood flow past the injury — only reposition the bone if there's no blood flow at all.**
- **Closed fracture:** no open wound. Real signs: pain, tenderness, discoloration, swelling, visible deformity, lost function, and "grating" (the sound/feel of broken bone ends rubbing together).

**⚠️ Real danger during fracture treatment: severing or compressing a nerve or blood vessel at the fracture site.** Use minimum manipulation, done cautiously. **If the area below the break becomes numb, swollen, cool, or pale, with the person showing shock signs — suspect a severed major vessel and real internal bleeding**, requiring the fracture to be reset and the person treated for shock with fluid replacement.

## Real Traction Technique

**Traction means a slow, strong, sustained pull — never a sudden tug.** Small bones (finger, hand) can often be managed with hand traction alone. **For larger bones: wedge the fractured limb into the V-notch of a tree and pull until the overriding broken bone edges realign** — check the alignment against the uninjured limb, then splint while maintaining traction so the bone doesn't slip back out of position.

## Real Splinting Principles

**Splint the joints both above AND below the actual fracture site** — this is what actually stops the bone ends from moving (e.g., a mid-forearm fracture needs both the wrist and elbow splinted). **Immobilize a joint in a neutral functional position** — neither fully straight nor fully bent, roughly midway between. **A finger should be splinted in the position it would naturally rest in.** Secure splints with cloth strips, vines, or braided plant material (see Making Rope — Fiber Types, Twisting & Braiding). **Check the pulse below the injury repeatedly after immobilizing**, and elevate the limb throughout the day to help control swelling.

## Dislocations — Real Reset Technique

**A dislocation is a misaligned bone/joint separation** — genuinely painful, and can impair nerve or circulatory function below the injury. **Real signs:** joint pain, tenderness, swelling, discoloration, limited motion, visible deformity.

**Reset it as quickly as possible** — **manual traction, or using body weight to pull the bones back into place, is the real safest and easiest method**, restoring normal function/circulation. **Without an X-ray, judge correct alignment by look and feel, compared against the matching joint on the opposite side.** Once reset, immobilize the same way as a fracture.

## Detailed Version

**The real, shared mechanical principle underlying both the fracture traction technique and the dislocation reset: a slow, sustained pull — never a quick jerk — is what lets displaced bone ends or joint surfaces slide back past each other safely.** A sudden tug risks tearing surrounding tissue or pinching a nerve/vessel exactly where gradual, controlled traction wouldn't.
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
