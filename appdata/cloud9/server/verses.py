import json
from datetime import date

from paths import DATA_DIR

VERSES_FILE = DATA_DIR / "verses.json"


def get_verse_of_day():
    with open(VERSES_FILE, encoding="utf-8") as f:
        data = json.load(f)
    verses = data["verses"]
    index = date.today().toordinal() % len(verses)
    verse = verses[index]
    return {
        "reference": verse["reference"],
        "text": verse["text"],
        "translation": data["translation"],
    }
