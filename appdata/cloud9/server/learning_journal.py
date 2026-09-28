"""The real Learning Journal -- built exactly to CARD_REDESIGN_PLAN.md's
own "don't rebuild" finding: rather than invent new storage, this is a
Cloud9-native view over Flatnotes (`modules/notes/compose.fragment.yml`),
Citadel's own already-running markdown notes engine. Every entry is a
real Flatnotes note, tagged `#cloud9-learning-journal` so Flatnotes' own
full-text search can list them back out without touching any other real
note a family keeps in Flatnotes for something else.

No per-child scoping yet -- matches School Library's own honest "Everyone"
fallback, since Kolibri (the one real place Cloud9 already checked for
learner accounts) reports zero real learners on this instance. One shared
family journal until real per-child profiles exist somewhere in Citadel.
"""

import os
from datetime import datetime
from urllib.parse import quote

import requests

FLATNOTES_BASE_URL = os.environ.get("FLATNOTES_BASE_URL", "http://citadel-flatnotes:8080")
HEADERS = {"User-Agent": "Cloud9 Learning Journal (kids learning dashboard)"}
JOURNAL_TAG = "cloud9-learning-journal"


def _note_url(title):
    return f"{FLATNOTES_BASE_URL}/api/notes/{quote(title, safe='')}"


def _format_entry(note):
    content = (note.get("content") or "").replace(f"#{JOURNAL_TAG}", "").strip()
    title = "Untitled Entry"
    body = content
    if content.startswith("## "):
        first_line, _, rest = content.partition("\n")
        title = first_line[3:].strip() or title
        body = rest.strip()
    return {
        "id": note["title"],
        "title": title,
        "text": body,
        "lastModified": note["lastModified"],
    }


def list_entries():
    resp = requests.get(
        f"{FLATNOTES_BASE_URL}/api/search",
        params={"term": f"#{JOURNAL_TAG}", "sort": "lastModified", "order": "desc"},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    entries = []
    for result in resp.json():
        note_resp = requests.get(_note_url(result["title"]), headers=HEADERS, timeout=10)
        if note_resp.status_code == 404:
            continue  # real race: deleted between the search and this fetch
        note_resp.raise_for_status()
        entries.append(_format_entry(note_resp.json()))
    return entries


def add_entry(title, text):
    text = (text or "").strip()
    if not text:
        raise ValueError("Entry text is required.")
    title = (title or "").strip() or "Untitled Entry"

    # The real Flatnotes note title is just a unique storage key, never
    # shown to the child -- their own title lives inside the content.
    # Flatnotes titles become real filenames on disk and reject
    # <>:"/\|?* (confirmed live via a real 422), so no colons here even
    # though a timestamp reads more naturally with them.
    storage_title = "Learning Journal - " + datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    content = f"## {title}\n\n{text}\n\n#{JOURNAL_TAG}"

    resp = requests.post(
        f"{FLATNOTES_BASE_URL}/api/notes",
        json={"title": storage_title, "content": content},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    return _format_entry(resp.json())


def delete_entry(entry_id):
    resp = requests.delete(_note_url(entry_id), headers=HEADERS, timeout=10)
    return resp.status_code == 200
