import json
from datetime import date

from paths import DATA_DIR

SCRATCHPAD_FILE = DATA_DIR / "scratchpad.json"
WRITING_FILE = DATA_DIR / "writing_paper.json"


def _load(path):
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_scratchpad():
    data = _load(SCRATCHPAD_FILE)
    today = date.today().isoformat()
    if data.get("date") != today:
        return ""
    return data.get("text", "")


def save_scratchpad(text):
    _save(SCRATCHPAD_FILE, {"text": text, "date": date.today().isoformat()})


def get_writing_paper():
    return _load(WRITING_FILE).get("text", "")


def save_writing_paper(text):
    _save(WRITING_FILE, {"text": text})
