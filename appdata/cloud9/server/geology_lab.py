"""Geology section of Science Lab. Checked PhET's full real catalog
first, same discipline as every other Science Lab section -- no
dedicated geology/rock-cycle simulation exists among their real sims, so
PhET isn't the right tool here. Video Library's existing "Earth & Space
Science" category (real Magic School Bus episodes on erosion, volcanoes,
the water cycle -- already built) covers this honestly, so Geology links
straight there instead of inventing a parallel video shelf, same move
already made for Biology.

The one new piece is a real Rock Classification activity -- well-
established, universally-known rock-type facts (granite is igneous,
limestone is sedimentary), not drawn from any single copyrighted source.
Zero new storage -- reuses the Mastery Engine under subject="geology".
"""

import mastery

ROCKS = [
    {"id": "granite", "name": "Granite", "rockType": "igneous", "fact": "Granite forms when melted rock (magma) cools slowly underground -- that slow cooling is why you can see its individual crystals."},
    {"id": "basalt", "name": "Basalt", "rockType": "igneous", "fact": "Basalt forms when lava cools quickly at the surface -- it's the most common rock in Earth's crust, especially under the oceans."},
    {"id": "obsidian", "name": "Obsidian", "rockType": "igneous", "fact": "Obsidian forms when lava cools so fast it doesn't even form crystals -- that's why it looks like real volcanic glass."},
    {"id": "sandstone", "name": "Sandstone", "rockType": "sedimentary", "fact": "Sandstone forms from real grains of sand, pressed and cemented together over a very long time."},
    {"id": "limestone", "name": "Limestone", "rockType": "sedimentary", "fact": "Limestone often forms from the real shells and skeletons of tiny sea creatures, compressed over millions of years."},
    {"id": "shale", "name": "Shale", "rockType": "sedimentary", "fact": "Shale forms from real mud and clay, pressed into thin layers -- it splits apart easily along those layers."},
    {"id": "marble", "name": "Marble", "rockType": "metamorphic", "fact": "Marble is limestone that got squeezed and heated underground until it changed into a harder, real crystalline rock."},
    {"id": "slate", "name": "Slate", "rockType": "metamorphic", "fact": "Slate is shale that got squeezed and heated until it changed -- that's why it splits into flat, smooth real sheets."},
    {"id": "gneiss", "name": "Gneiss", "rockType": "metamorphic", "fact": "Gneiss forms when existing rock gets squeezed and heated so much its minerals line up into real, visible bands."},
]

ROCK_TYPES = ["igneous", "sedimentary", "metamorphic"]


def get_rock_types():
    return ROCK_TYPES


def get_rocks():
    mastery_rows = {m["concept"]: m for m in mastery.get_all_for_subject("geology")}
    result = []
    for r in ROCKS:
        entry = dict(r)
        entry["mastery"] = mastery_rows.get(r["id"], {}).get("level", "new")
        result.append(entry)
    return result


def _rock_by_id(rock_id):
    for r in ROCKS:
        if r["id"] == rock_id:
            return r
    return None


def check_classification(rock_id, guess):
    import learning_engine

    rock = _rock_by_id(rock_id)
    if not rock:
        return None

    correct = guess == rock["rockType"]
    learning_engine.record_activity(
        "geology",
        "classify_rock",
        rock_id,
        source="cloud9-geology-lab",
        correct=correct,
        artifact=rock["rockType"],
    )
    return {
        "correct": correct,
        "rockType": rock["rockType"],
        "fact": rock["fact"] if correct else None,
    }
