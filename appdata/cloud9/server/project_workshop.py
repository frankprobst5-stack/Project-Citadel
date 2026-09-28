"""Project Workshop -- same real-reuse pattern as the Learning Journal:
one Flatnotes note per project, tagged `#cloud9-project-workshop`, real
markdown structure (materials list, a real `- [ ]` checklist, notes,
photo attachments via Flatnotes' own real attachments API) instead of a
second data store. v1 scope, named honestly: goal, materials, checklist,
notes, and photos. "AI help" and a running per-project dated journal are
real, planned v2 work, not built here.

Same honest single-shared-workshop reasoning as the Learning Journal: no
per-child scoping yet, since Kolibri (the one place Cloud9 already
checked) reports zero real learner accounts.
"""

import os
from datetime import datetime
from urllib.parse import quote

import requests

FLATNOTES_BASE_URL = os.environ.get("FLATNOTES_BASE_URL", "http://citadel-flatnotes:8080")
HEADERS = {"User-Agent": "Cloud9 Project Workshop (kids learning dashboard)"}
PROJECT_TAG = "cloud9-project-workshop"

_SECTION_MATERIALS = "### Materials"
_SECTION_CHECKLIST = "### Checklist"
_SECTION_NOTES = "### Notes"
_SECTION_PHOTOS = "### Photos"


def _note_url(title):
    return f"{FLATNOTES_BASE_URL}/api/notes/{quote(title, safe='')}"


def _parse_content(content):
    content = content or ""
    lines = content.split("\n")

    title = "Untitled Project"
    start = 0
    if lines and lines[0].strip().startswith("## "):
        title = lines[0].strip()[3:].strip() or title
        start = 1

    goal = ""
    status = "active"
    materials = []
    checklist = []
    notes_lines = []
    photos = []
    section = None

    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("**Goal:**"):
            goal = stripped[len("**Goal:**"):].strip()
            continue
        if stripped.startswith("**Status:**"):
            status = stripped[len("**Status:**"):].strip().lower() or "active"
            continue
        if stripped == _SECTION_MATERIALS:
            section = "materials"
            continue
        if stripped == _SECTION_CHECKLIST:
            section = "checklist"
            continue
        if stripped == _SECTION_NOTES:
            section = "notes"
            continue
        if stripped == _SECTION_PHOTOS:
            section = "photos"
            continue
        if stripped.startswith(f"#{PROJECT_TAG}"):
            continue

        if section == "materials" and stripped.startswith("- "):
            materials.append(stripped[2:].strip())
        elif section == "checklist" and (stripped.lower().startswith("- [ ]") or stripped.lower().startswith("- [x]")):
            done = stripped.lower().startswith("- [x]")
            text = stripped[5:].strip()
            checklist.append({"text": text, "done": done})
        elif section == "notes":
            notes_lines.append(line)
        elif section == "photos" and stripped:
            photos.append(stripped)

    return {
        "title": title,
        "goal": goal,
        "materials": materials,
        "checklist": checklist,
        "notes": "\n".join(notes_lines).strip(),
        "photos": photos,
        "status": status,
    }


def _serialize_content(fields):
    lines = ["## " + (fields.get("title") or "Untitled Project"), ""]
    if fields.get("goal"):
        lines += ["**Goal:** " + fields["goal"], ""]
    lines += [_SECTION_MATERIALS]
    lines += ["- " + m for m in fields.get("materials") or []]
    lines += ["", _SECTION_CHECKLIST]
    lines += [
        "- [" + ("x" if item.get("done") else " ") + "] " + (item.get("text") or "")
        for item in fields.get("checklist") or []
    ]
    lines += ["", _SECTION_NOTES]
    if fields.get("notes"):
        lines.append(fields["notes"])
    lines += ["", _SECTION_PHOTOS]
    lines += fields.get("photos") or []
    lines += ["", "**Status:** " + (fields.get("status") or "active"), "", "#" + PROJECT_TAG]
    return "\n".join(lines)


def _get_note(storage_title):
    resp = requests.get(_note_url(storage_title), headers=HEADERS, timeout=10)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def list_projects():
    resp = requests.get(
        f"{FLATNOTES_BASE_URL}/api/search",
        params={"term": f"#{PROJECT_TAG}", "sort": "lastModified", "order": "desc"},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    summaries = []
    for result in resp.json():
        note = _get_note(result["title"])
        if not note:
            continue
        fields = _parse_content(note.get("content"))
        done = sum(1 for item in fields["checklist"] if item["done"])
        summaries.append({
            "id": note["title"],
            "title": fields["title"],
            "goal": fields["goal"],
            "status": fields["status"],
            "checklistDone": done,
            "checklistTotal": len(fields["checklist"]),
            "lastModified": note["lastModified"],
        })
    return summaries


def get_project(project_id):
    note = _get_note(project_id)
    if not note:
        return None
    fields = _parse_content(note.get("content"))
    fields["id"] = note["title"]
    fields["lastModified"] = note["lastModified"]
    return fields


def create_project(title, goal, materials, checklist):
    title = (title or "").strip() or "Untitled Project"
    storage_title = "Project - " + datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    content = _serialize_content({
        "title": title,
        "goal": (goal or "").strip(),
        "materials": [m.strip() for m in (materials or []) if m.strip()],
        "checklist": [
            {"text": item.strip(), "done": False}
            for item in (checklist or [])
            if item.strip()
        ],
        "notes": "",
        "photos": [],
        "status": "active",
    })
    resp = requests.post(
        f"{FLATNOTES_BASE_URL}/api/notes",
        json={"title": storage_title, "content": content},
        headers=HEADERS,
        timeout=10,
    )
    resp.raise_for_status()
    note = resp.json()
    fields = _parse_content(note["content"])
    fields["id"] = note["title"]
    fields["lastModified"] = note["lastModified"]
    return fields


def update_project(project_id, fields):
    content = _serialize_content(fields)
    resp = requests.patch(
        _note_url(project_id),
        json={"newContent": content},
        headers=HEADERS,
        timeout=10,
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    note = resp.json()
    result = _parse_content(note["content"])
    result["id"] = note["title"]
    result["lastModified"] = note["lastModified"]
    return result


def delete_project(project_id):
    resp = requests.delete(_note_url(project_id), headers=HEADERS, timeout=10)
    return resp.status_code == 200


def add_photo(project_id, filename, file_bytes, content_type):
    note = _get_note(project_id)
    if not note:
        return None
    resp = requests.post(
        f"{FLATNOTES_BASE_URL}/api/attachments",
        files={"file": (filename, file_bytes, content_type)},
        headers=HEADERS,
        timeout=20,
    )
    resp.raise_for_status()
    uploaded_filename = resp.json()["filename"]

    fields = _parse_content(note.get("content"))
    fields["photos"].append(uploaded_filename)
    return update_project(project_id, fields)


def get_photo(filename):
    """Proxies a real Flatnotes attachment's bytes back through Cloud9,
    same reasoning as School Library playing Kolibri video natively in
    Cloud9 -- the child's browser never needs to know Flatnotes exists."""
    resp = requests.get(
        f"{FLATNOTES_BASE_URL}/api/attachments/{quote(filename, safe='')}",
        headers=HEADERS,
        timeout=15,
    )
    if resp.status_code != 200:
        return None, None
    return resp.content, resp.headers.get("Content-Type", "application/octet-stream")
