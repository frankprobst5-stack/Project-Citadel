import nltk

from paths import DATA_DIR

nltk.data.path = [str(DATA_DIR / "nltk_data")]

from nltk.corpus import wordnet as wn  # noqa: E402

POS_LABELS = {
    "n": "noun",
    "v": "verb",
    "a": "adjective",
    "s": "adjective",
    "r": "adverb",
}


def lookup(word):
    word = word.strip().lower()
    if not word:
        return []
    seen = set()
    results = []
    for syn in wn.synsets(word):
        definition = syn.definition()
        pos = POS_LABELS.get(syn.pos(), syn.pos())
        key = (pos, definition)
        if key in seen:
            continue
        seen.add(key)
        results.append({"partOfSpeech": pos, "definition": definition})
    return results
