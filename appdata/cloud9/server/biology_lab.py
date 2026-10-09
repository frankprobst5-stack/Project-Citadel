"""Biology section of Science Lab. Checked PhET first, same as every
other Science Lab section -- their real Biology sim list (Membrane
Transport, Natural Selection, Gene Expression Essentials, Neuron, Color
Vision, pH Scale, Molecule Polarity, Density) is middle/high-school and
up, nothing elementary-appropriate, so PhET isn't the right real tool
here. Video Library's existing "Life Science" category (real Magic
School Bus episodes, already built -- see video_library.py) already
covers this age range honestly, so Biology links straight there instead
of inventing a parallel video shelf.

The one new piece is a real Animal Classification activity -- well-
established, universally-known taxonomy facts (a dog is a mammal, a
shark is a fish), not drawn from any single copyrighted source. Zero new
storage -- reuses the Mastery Engine under subject="biology", same real
pattern as Chemistry's Molecule Builder.
"""

import mastery

ANIMALS = [
    {"id": "dog", "name": "Dog", "animalClass": "mammal", "fact": "Like all mammals, a dog is warm-blooded, has fur, and feeds its babies milk."},
    {"id": "whale", "name": "Whale", "animalClass": "mammal", "fact": "A whale lives its whole life in water but is still a real mammal -- warm-blooded, breathes air, and feeds its calves milk."},
    {"id": "robin", "name": "Robin", "animalClass": "bird", "fact": "Like all birds, a robin is warm-blooded, has feathers, and hatches from a hard-shelled egg."},
    {"id": "eagle", "name": "Eagle", "animalClass": "bird", "fact": "Like all birds, an eagle has feathers and a beak, and lays hard-shelled eggs."},
    {"id": "snake", "name": "Snake", "animalClass": "reptile", "fact": "Like all reptiles, a snake is cold-blooded and has dry, scaly skin."},
    {"id": "turtle", "name": "Turtle", "animalClass": "reptile", "fact": "Like all reptiles, a turtle is cold-blooded and has scaly skin, even under that shell."},
    {"id": "frog", "name": "Frog", "animalClass": "amphibian", "fact": "Like all amphibians, a frog starts life in water (as a tadpole) and can live on land as an adult."},
    {"id": "salamander", "name": "Salamander", "animalClass": "amphibian", "fact": "Like all amphibians, a salamander has moist skin and usually starts life in water."},
    {"id": "shark", "name": "Shark", "animalClass": "fish", "fact": "Like all fish, a shark is cold-blooded, lives in water, and breathes through gills."},
    {"id": "salmon", "name": "Salmon", "animalClass": "fish", "fact": "Like all fish, a salmon breathes through gills and has fins, not legs."},
    {"id": "ant", "name": "Ant", "animalClass": "insect", "fact": "Like all insects, an ant has six legs and a body split into three main parts."},
    {"id": "butterfly", "name": "Butterfly", "animalClass": "insect", "fact": "Like all insects, a butterfly has six legs -- and it completely transforms from a caterpillar through metamorphosis."},
]

CLASSES = ["mammal", "bird", "reptile", "amphibian", "fish", "insect"]


def get_classes():
    return CLASSES


def get_animals():
    mastery_rows = {m["concept"]: m for m in mastery.get_all_for_subject("biology")}
    result = []
    for a in ANIMALS:
        entry = dict(a)
        entry["mastery"] = mastery_rows.get(a["id"], {}).get("level", "new")
        result.append(entry)
    return result


def _animal_by_id(animal_id):
    for a in ANIMALS:
        if a["id"] == animal_id:
            return a
    return None


def check_classification(animal_id, guess):
    import learning_engine

    animal = _animal_by_id(animal_id)
    if not animal:
        return None

    correct = guess == animal["animalClass"]
    learning_engine.record_activity(
        "biology",
        "classify_animal",
        animal_id,
        source="cloud9-biology-lab",
        correct=correct,
        artifact=animal["animalClass"],
    )
    return {
        "correct": correct,
        "animalClass": animal["animalClass"],
        "fact": animal["fact"] if correct else None,
    }
