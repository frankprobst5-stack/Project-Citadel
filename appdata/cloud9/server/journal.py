import json
import uuid
from datetime import date

from paths import DATA_DIR

ENTRIES_FILE = DATA_DIR / "journal_entries.json"


def _load():
    if not ENTRIES_FILE.exists():
        return []
    with open(ENTRIES_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(entries):
    with open(ENTRIES_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def list_entries():
    entries = _load()
    return sorted(entries, key=lambda e: e["date"], reverse=True)


def add_entry(category, title, text):
    entries = _load()
    entry = {
        "id": uuid.uuid4().hex,
        "date": date.today().isoformat(),
        "category": category,
        "title": title,
        "text": text,
    }
    entries.append(entry)
    _save(entries)
    return entry


def delete_entry(entry_id):
    entries = _load()
    remaining = [e for e in entries if e["id"] != entry_id]
    if len(remaining) == len(entries):
        return False
    _save(remaining)
    return True
