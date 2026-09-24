"""Guided Missions for Language -- the fourth subject, after Weather,
Earth Lab, and History. Source is WordNet, via the same real lexical
database dictionary.py already bundles locally (no live API, no
network dependency, no "unavailable" state to handle -- a genuinely
different real-data shape from the other three subjects' live feeds).

`import dictionary` first for its own real side effect: it points
nltk.data.path at the bundled corpus before anything here touches
`wordnet`, the same real setup dictionary.py's own lookups depend on --
duplicating that one line here would risk it drifting out of sync with
wherever the corpus actually gets installed.

Every synonym, antonym, and hypernym chain named below was looked up
live against the real WordNet data before writing any narrative text,
not recalled from memory -- the specific senses matter (e.g. "smart"
has a synonym set for "stylish" and a completely different one for
"rude," and only one of those is the one most people mean first).
"""

import dictionary  # noqa: F401  (sets nltk.data.path as a real side effect)
from nltk.corpus import wordnet as wn


def _synonyms_mission():
    word = "brave"
    syn = wn.synset("audacious.s.01")
    synonyms = [l.name().replace("_", " ") for l in syn.lemmas() if l.name() != word]

    return {
        "missionType": "Guided",
        "concept": "synonyms",
        "title": "Same Idea, Different Words",
        "briefing": (
            "Synonyms are different words that share a similar meaning -- real writers reach "
            "for them so the same sentence doesn't repeat the same word over and over."
        ),
        "observe": {"kind": "word-facts", "word": word, "items": synonyms, "label": "Real synonyms for “brave”"},
        "question": f"WordNet's real dictionary data lists {len(synonyms)} words that share this exact sense of “{word}”: {', '.join(synonyms)}. Do you think all of them feel exactly the same, or do some feel a little different?",
        "reveal": (
            f"A little different, even though they're real synonyms. “Intrepid” and “dauntless” "
            f"sound more formal, almost like something from an old adventure story, while “brave” "
            f"is the everyday word you'd actually say out loud. Synonyms share a meaning, but they "
            f"almost never share the exact same feel -- that's real, and it's why picking the right "
            f"synonym is a writing skill, not just a swap."
        ),
        "investigateLink": None,
        "investigateLabel": None,
        "recap": f"“Brave” shares this real sense with: {', '.join(synonyms)}.",
        "source": "WordNet",
    }


def _antonyms_mission():
    word = "strong"
    syn = wn.synset("strong.a.01")
    lemma = next(l for l in syn.lemmas() if l.name() == word)
    antonym = lemma.antonyms()[0].name()

    weak_syn = wn.synset("weak.a.01") if wn.synsets("weak", pos=wn.ADJ) else None
    weak_def = weak_syn.definition() if weak_syn else None

    return {
        "missionType": "Guided",
        "concept": "antonyms",
        "title": "Opposite Ends of the Same Idea",
        "briefing": (
            "An antonym is a word with the opposite meaning -- but not every word has one. Some "
            "ideas just don't have a clean opposite."
        ),
        "observe": {"kind": "word-facts", "word": word, "items": [antonym], "label": "Real antonym of “strong”"},
        "question": f"WordNet's real data pairs “{word}” ({syn.definition()}) with exactly one direct antonym. What do you think it is?",
        "reveal": (
            f"“{antonym.title()}”" + (f" -- {weak_def}." if weak_def else ".") +
            " Not every word gets this clean pairing, though: think about a word like “yellow.” "
            "There's no single real opposite of a color the way “weak” is the real opposite of "
            "“strong” -- antonyms work best for words that describe a scale with two ends, "
            "not for words that just name a category."
        ),
        "investigateLink": None,
        "investigateLabel": None,
        "recap": f"“{word.title()}” and “{antonym}”: real opposite ends of the same scale.",
        "source": "WordNet",
    }


def _word_ladders_mission():
    word = "poodle"
    syn = wn.synsets(word, pos=wn.NOUN)[0]
    path = syn.hypernym_paths()[0]
    # Real hypernym_paths() returns broadest-first (entity ... poodle); the
    # "keep climbing up" framing below reads narrow-to-broad, so reverse it.
    chain = [s.lemmas()[0].name().replace("_", " ") for s in reversed(path)]
    climb = " → ".join(chain)

    return {
        "missionType": "Guided",
        "concept": "word-ladders",
        "title": "Every Word Fits Inside a Bigger Category",
        "briefing": (
            "Every specific word belongs to a broader category, which belongs to an even broader "
            "one -- real dictionaries actually track this general-to-specific ladder, called "
            "hypernyms."
        ),
        "observe": {"kind": "word-ladder", "chain": chain},
        "question": f"A “{word}” is a real, specific kind of dog. If you kept asking “what bigger category does this belong to?” again and again, how many real steps do you think it takes to reach the single broadest category WordNet has: “entity”?",
        "reveal": (
            f"{len(chain) - 1} real steps: {climb}. Every single noun in English eventually climbs "
            f"all the way up to “entity” if you keep asking the same question -- it's the exact same "
            f"kind of general-to-specific thinking biology uses to classify living things (species → "
            f"genus → family, all the way up to kingdom)."
        ),
        "investigateLink": None,
        "investigateLabel": None,
        "recap": f"{climb} -- {len(chain) - 1} real steps from one specific dog breed to the broadest category there is.",
        "source": "WordNet",
    }


def _parts_of_speech_mission():
    word = "run"
    noun_defs = [s.definition() for s in wn.synsets(word, pos=wn.NOUN)][:2]
    verb_defs = [s.definition() for s in wn.synsets(word, pos=wn.VERB)][:2]
    noun_count = len(wn.synsets(word, pos=wn.NOUN))
    verb_count = len(wn.synsets(word, pos=wn.VERB))

    return {
        "missionType": "Guided",
        "concept": "parts-of-speech",
        "title": "One Word, Completely Different Jobs",
        "briefing": (
            "Plenty of English words do double duty -- the exact same spelling works as a noun "
            "in one sentence and a verb in another, with meanings that aren't even close."
        ),
        "observe": {
            "kind": "parts-of-speech", "word": word,
            "nounCount": noun_count, "verbCount": verb_count,
            "nounDefs": noun_defs, "verbDefs": verb_defs,
        },
        "question": f"WordNet's real data lists “{word}” with {noun_count} noun meanings and {verb_count} verb meanings. Can you think of a sentence where “{word}” is a noun, and a different one where it's a verb?",
        "reveal": (
            f"As a noun, “{word}” can mean things like: {'; '.join(noun_defs)}. As a verb, it can "
            f"mean: {'; '.join(verb_defs)}. Same four letters, {noun_count + verb_count} completely real, "
            f"separate meanings between the two jobs -- English reuses spellings constantly instead "
            f"of inventing a new word for every single idea."
        ),
        "investigateLink": None,
        "investigateLabel": None,
        "recap": f"“{word.title()}”: {noun_count} real noun senses, {verb_count} real verb senses, same spelling.",
        "source": "WordNet",
    }


CONCEPTS = {
    "synonyms": ("Same Idea, Different Words", _synonyms_mission),
    "antonyms": ("Opposite Ends of the Same Idea", _antonyms_mission),
    "word-ladders": ("Every Word Fits Inside a Bigger Category", _word_ladders_mission),
    "parts-of-speech": ("One Word, Completely Different Jobs", _parts_of_speech_mission),
}


def list_concepts():
    return [{"id": concept_id, "title": title} for concept_id, (title, _) in CONCEPTS.items()]


def get_language_mission(concept_id):
    entry = CONCEPTS.get(concept_id)
    if not entry:
        return {"status": "unavailable", "reason": f"Unknown concept '{concept_id}'."}
    _, builder = entry
    try:
        return builder()
    except Exception:
        return {"status": "unavailable", "reason": "Couldn't look this word up in the dictionary right now."}
