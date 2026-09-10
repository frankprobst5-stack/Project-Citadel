import json
import uuid

from paths import DATA_DIR

NOTES_FILE = DATA_DIR / "planner_notes.json"


def _load():
    if not NOTES_FILE.exists():
        return []
    with open(NOTES_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2)


def list_notes():
    return _load()


def add_note(date, text, author):
    notes = _load()
    note = {"id": uuid.uuid4().hex, "date": date, "text": text, "author": author}
    notes.append(note)
    _save(notes)
    return note


def update_note(note_id, text, author):
    notes = _load()
    for note in notes:
        if note["id"] == note_id:
            note["text"] = text
            note["author"] = author
            _save(notes)
            return note
    return None


def delete_note(note_id):
    notes = _load()
    remaining = [n for n in notes if n["id"] != note_id]
    if len(remaining) == len(notes):
        return False
    _save(remaining)
    return True
