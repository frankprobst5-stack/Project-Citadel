"""Chemistry's real Molecule Builder -- ROADMAP.md Phase 3, item 4's
explicit sequencing rule: a molecule builder before any reaction
simulator, "for correctness reasons" (building a real molecule out of
real atoms is unambiguous; a simplified reaction simulator risks teaching
something subtly wrong). This is that builder -- nothing else from
Science Lab's chemistry section is attempted yet.

Real, well-established chemistry facts, not sourced from any single
copyrighted text -- these are universally-known atomic compositions
(water is 2 hydrogen + 1 oxygen, same fact in every real chemistry
reference). No new storage: reuses the existing Mastery Engine
(subject="chemistry") exactly like Word Lab and Math Lab already do,
through the one shared learning_engine.record_activity() call.
"""

import mastery

ELEMENTS = {
    "H": {"name": "Hydrogen", "atomicNumber": 1},
    "C": {"name": "Carbon", "atomicNumber": 6},
    "N": {"name": "Nitrogen", "atomicNumber": 7},
    "O": {"name": "Oxygen", "atomicNumber": 8},
    "Na": {"name": "Sodium", "atomicNumber": 11},
    "Cl": {"name": "Chlorine", "atomicNumber": 17},
}

MOLECULES = [
    {
        "id": "water",
        "name": "Water",
        "formula": "H2O",
        "atoms": {"H": 2, "O": 1},
        "fact": "What you drink, and most of your own body -- two hydrogen atoms bonded to one oxygen atom.",
    },
    {
        "id": "oxygen-gas",
        "name": "Oxygen Gas",
        "formula": "O2",
        "atoms": {"O": 2},
        "fact": "The real oxygen you breathe is two oxygen atoms bonded together, not a single atom floating around.",
    },
    {
        "id": "carbon-dioxide",
        "name": "Carbon Dioxide",
        "formula": "CO2",
        "atoms": {"C": 1, "O": 2},
        "fact": "What you breathe out, and what plants take back in -- one carbon atom bonded to two oxygen atoms.",
    },
    {
        "id": "carbon-monoxide",
        "name": "Carbon Monoxide",
        "formula": "CO",
        "atoms": {"C": 1, "O": 1},
        "fact": "One carbon, one oxygen -- just one fewer oxygen atom than carbon dioxide, but dangerous to breathe because it's colorless and odorless.",
    },
    {
        "id": "methane",
        "name": "Methane",
        "formula": "CH4",
        "atoms": {"C": 1, "H": 4},
        "fact": "Natural gas -- one carbon atom with four hydrogen atoms bonded around it.",
    },
    {
        "id": "ammonia",
        "name": "Ammonia",
        "formula": "NH3",
        "atoms": {"N": 1, "H": 3},
        "fact": "A real gas with a sharp smell, used in cleaning products and fertilizer -- one nitrogen atom bonded to three hydrogen atoms.",
    },
    {
        "id": "nitrogen-gas",
        "name": "Nitrogen Gas",
        "formula": "N2",
        "atoms": {"N": 2},
        "fact": "About 78% of the air around you right now -- two nitrogen atoms bonded together.",
    },
    {
        "id": "table-salt",
        "name": "Table Salt",
        "formula": "NaCl",
        "atoms": {"Na": 1, "Cl": 1},
        "fact": "Real table salt -- one sodium atom and one chlorine atom. Sodium alone is dangerously reactive and chlorine gas is toxic, but bonded together they're what you put on fries.",
    },
]


def get_elements():
    return [{"symbol": sym, **data} for sym, data in ELEMENTS.items()]


def get_molecules():
    mastery_rows = {m["concept"]: m for m in mastery.get_all_for_subject("chemistry")}
    result = []
    for mol in MOLECULES:
        entry = dict(mol)
        entry["mastery"] = mastery_rows.get(mol["id"], {}).get("level", "new")
        result.append(entry)
    return result


def _molecule_by_id(molecule_id):
    for m in MOLECULES:
        if m["id"] == molecule_id:
            return m
    return None


def check_molecule(molecule_id, built_atoms):
    """Real check: the submitted atom counts must exactly match the
    molecule's real formula -- no partial credit, same as getting a real
    chemical formula right or wrong. Logs through the shared Learning
    Event schema either way, so wrong attempts still feed the Mastery
    Engine (same honest pattern as every quiz in Math Lab/Word Lab)."""
    import learning_engine

    molecule = _molecule_by_id(molecule_id)
    if not molecule:
        return None

    cleaned = {sym: count for sym, count in (built_atoms or {}).items() if count}
    correct = cleaned == molecule["atoms"]

    learning_engine.record_activity(
        "chemistry",
        "build_molecule",
        molecule_id,
        source="cloud9-chemistry-lab",
        correct=correct,
        artifact=molecule["formula"],
    )

    return {
        "correct": correct,
        "formula": molecule["formula"],
        "fact": molecule["fact"] if correct else None,
    }
