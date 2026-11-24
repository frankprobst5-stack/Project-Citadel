"""Unified content wiki -- replaces three separate systems with one:

- The Media Vault's own folder-scan (`scan_media_folder`) has no
  metadata beyond a filename; `wiki_attachments` is a real table so a
  video/pdf/audio file can carry a title, section, and tags.
- Mealie (a whole separate container + its own SQLite DB) becomes
  `wiki_pages` rows with section='recipe' -- see `extract_recipe_jsonld`
  below for the link-paste-and-scrape feature that was the one Mealie
  feature actually worth keeping.
- The hand-written static `manual.html` ("Master Operations Handbook")
  becomes `wiki_pages` rows with section='manual' -- editable from the
  UI and, for the first time, actually searchable (today `/api/search`
  doesn't touch it at all).

Every function here takes an open `sqlite3.Connection` rather than
reaching for `DB_PATH` itself, same reasoning as every `_conn`-style
split in this ecosystem's other codebases: it's what makes this module
testable with a throwaway in-memory database instead of needing a live
Flask app or real appdata.
"""
import json
import re
import sqlite3
import uuid
from datetime import datetime, timezone

import requests


def create_wiki_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wiki_pages (
            id TEXT PRIMARY KEY,
            section TEXT NOT NULL,
            title TEXT NOT NULL,
            body_markdown TEXT NOT NULL,
            tags TEXT,
            recipe_meta TEXT,
            source_url TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wiki_attachments (
            id TEXT PRIMARY KEY,
            page_id TEXT,
            kind TEXT NOT NULL,
            filename TEXT NOT NULL,
            title TEXT,
            tags TEXT,
            size_bytes INTEGER,
            added_at TEXT NOT NULL
        )
    ''')
    conn.commit()


# --- Pages: CRUD -------------------------------------------------------

def _row_to_page(row):
    page = dict(row)
    page["tags"] = json.loads(page["tags"]) if page.get("tags") else []
    page["recipe_meta"] = json.loads(page["recipe_meta"]) if page.get("recipe_meta") else None
    return page


def list_wiki_pages(conn, section=None):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if section:
        cursor.execute("SELECT * FROM wiki_pages WHERE section = ? ORDER BY title ASC", (section,))
    else:
        cursor.execute("SELECT * FROM wiki_pages ORDER BY section ASC, title ASC")
    return [_row_to_page(r) for r in cursor.fetchall()]


def get_wiki_page(conn, page_id):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wiki_pages WHERE id = ?", (page_id,))
    row = cursor.fetchone()
    return _row_to_page(row) if row else None


def upsert_wiki_page(conn, page_id, section, title, body_markdown, tags=None, recipe_meta=None, source_url=None):
    if not section or not str(section).strip():
        raise ValueError("a wiki page needs a real section")
    if not title or not str(title).strip():
        raise ValueError("a wiki page needs a real title")
    now = datetime.now(timezone.utc).isoformat()
    tags_json = json.dumps(tags or [])
    recipe_meta_json = json.dumps(recipe_meta) if recipe_meta is not None else None
    cursor = conn.cursor()
    if page_id:
        cursor.execute(
            "SELECT created_at FROM wiki_pages WHERE id = ?", (page_id,)
        )
        existing = cursor.fetchone()
        created_at = existing[0] if existing else now
        cursor.execute(
            """
            INSERT OR REPLACE INTO wiki_pages
                (id, section, title, body_markdown, tags, recipe_meta, source_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (page_id, section, title, body_markdown, tags_json, recipe_meta_json, source_url, created_at, now),
        )
    else:
        page_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO wiki_pages
                (id, section, title, body_markdown, tags, recipe_meta, source_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (page_id, section, title, body_markdown, tags_json, recipe_meta_json, source_url, now, now),
        )
    conn.commit()
    return get_wiki_page(conn, page_id)


def delete_wiki_page(conn, page_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wiki_pages WHERE id = ?", (page_id,))
    cursor.execute("DELETE FROM wiki_attachments WHERE page_id = ?", (page_id,))
    conn.commit()


def search_wiki_pages(conn, query):
    """Real title/body/tag substring search -- the same kind of plain
    LIKE match `_search_vault`/`_search_baneward` already use in
    app.py, so this slots into `/api/search` without a different
    search engine or index to keep in sync."""
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    like = f"%{query}%"
    cursor.execute(
        "SELECT * FROM wiki_pages WHERE title LIKE ? OR body_markdown LIKE ? OR tags LIKE ? ORDER BY title ASC",
        (like, like, like),
    )
    return [_row_to_page(r) for r in cursor.fetchall()]


# --- Attachments --------------------------------------------------------

def _row_to_attachment(row):
    attachment = dict(row)
    attachment["tags"] = json.loads(attachment["tags"]) if attachment.get("tags") else []
    return attachment


def list_wiki_attachments(conn, page_id=None):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if page_id:
        cursor.execute("SELECT * FROM wiki_attachments WHERE page_id = ? ORDER BY added_at DESC", (page_id,))
    else:
        cursor.execute("SELECT * FROM wiki_attachments ORDER BY added_at DESC")
    return [_row_to_attachment(r) for r in cursor.fetchall()]


def search_wiki_attachments(conn, query):
    """Real filename/title/tag search over wiki_attachments -- replaces
    app.py's old _search_vault (which searched scan_media_folder() and
    linked to the now-retired /pdf and /videos gallery page routes).
    Covers all three real kinds (video/audio/pdf), where _search_vault
    only ever covered pdfs and videos, never mp3s."""
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    like = f"%{query}%"
    cursor.execute(
        "SELECT * FROM wiki_attachments WHERE filename LIKE ? OR title LIKE ? OR tags LIKE ? ORDER BY added_at DESC",
        (like, like, like),
    )
    return [_row_to_attachment(r) for r in cursor.fetchall()]


def add_wiki_attachment(conn, kind, filename, page_id=None, title=None, tags=None, size_bytes=None):
    if kind not in ("video", "audio", "pdf", "image"):
        raise ValueError(f"unknown attachment kind {kind!r} -- must be video/audio/pdf/image")
    attachment_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO wiki_attachments (id, page_id, kind, filename, title, tags, size_bytes, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (attachment_id, page_id, kind, filename, title, json.dumps(tags or []), size_bytes, now),
    )
    conn.commit()
    return {"id": attachment_id, "page_id": page_id, "kind": kind, "filename": filename, "title": title,
            "tags": tags or [], "size_bytes": size_bytes, "added_at": now}


def delete_wiki_attachment(conn, attachment_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wiki_attachments WHERE id = ?", (attachment_id,))
    conn.commit()


# --- Recipe import: paste a link, get a structured recipe --------------
#
# schema.org/Recipe JSON-LD is the mechanism recipe sites embed for
# Google's own rich-snippet search results -- it's why a recipe search
# on Google shows the star rating, time, and photo right in the result.
# Because it's an SEO standard rather than a per-site hack, one parser
# covers most modern recipe blogs with zero site-specific code, and
# zero new pip dependencies (this container only runtime-imports
# packages baked in at build time, see Dockerfile's own comment on
# why -- no BeautifulSoup/lxml needed for this, just stdlib json + re
# over the handful of <script type="application/ld+json"> blocks any
# page has). Sites that don't embed it return None, honestly -- paste
# the recipe in by hand rather than a guessed, wrong extraction.

_JSONLD_BLOCK_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)

_ISO8601_DURATION_RE = re.compile(
    r"P(?:\d+Y)?(?:\d+M)?(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
)


def _iter_jsonld_objects(html):
    """Every JSON-LD object on the page, flattening `@graph` wrappers
    and top-level arrays -- both real, common shapes (WordPress SEO
    plugins especially favor `@graph`)."""
    for raw in _JSONLD_BLOCK_RE.findall(html):
        try:
            parsed = json.loads(raw.strip())
        except (json.JSONDecodeError, ValueError):
            continue
        candidates = parsed if isinstance(parsed, list) else [parsed]
        for item in candidates:
            if not isinstance(item, dict):
                continue
            if "@graph" in item and isinstance(item["@graph"], list):
                for sub in item["@graph"]:
                    if isinstance(sub, dict):
                        yield sub
            else:
                yield item


def _is_recipe_type(item):
    t = item.get("@type")
    if isinstance(t, list):
        return "Recipe" in t
    return t == "Recipe"


def _flatten_instructions(raw):
    """`recipeInstructions` shows up as a plain string, a list of
    strings, a list of HowToStep dicts, or HowToSection dicts nesting
    their own `itemListElement` -- all four are real, seen on real
    sites, so all four are handled rather than just the common case."""
    if raw is None:
        return []
    if isinstance(raw, str):
        # Some sites put the whole method as one newline-separated string.
        return [line.strip() for line in raw.splitlines() if line.strip()]
    if not isinstance(raw, list):
        return []
    steps = []
    for entry in raw:
        if isinstance(entry, str):
            steps.append(entry.strip())
        elif isinstance(entry, dict):
            if entry.get("@type") == "HowToSection" and isinstance(entry.get("itemListElement"), list):
                steps.extend(_flatten_instructions(entry["itemListElement"]))
            else:
                text = entry.get("text") or entry.get("name")
                if text:
                    steps.append(str(text).strip())
    return [s for s in steps if s]


def _first_image_url(raw):
    if raw is None:
        return None
    if isinstance(raw, str):
        return raw
    if isinstance(raw, list) and raw:
        return _first_image_url(raw[0])
    if isinstance(raw, dict):
        return raw.get("url")
    return None


def parse_iso8601_duration(value):
    """'PT1H30M' -> '1h 30m'. Returns None for anything that doesn't
    look like an ISO 8601 duration rather than guessing."""
    if not value or not isinstance(value, str):
        return None
    match = _ISO8601_DURATION_RE.fullmatch(value.strip())
    if not match or not any(match.groups()):
        return None
    hours, minutes, seconds = (int(g) if g else 0 for g in match.groups())
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if not parts and seconds:
        parts.append(f"{seconds}s")
    return " ".join(parts) if parts else None


def extract_recipe_jsonld(html):
    """Returns a structured recipe dict from a page's own JSON-LD, or
    None if the page has no schema.org Recipe block."""
    for item in _iter_jsonld_objects(html):
        if not _is_recipe_type(item):
            continue
        ingredients = item.get("recipeIngredient") or item.get("ingredients") or []
        if isinstance(ingredients, str):
            ingredients = [ingredients]
        return {
            "title": item.get("name") or "Untitled Recipe",
            "ingredients": [str(i).strip() for i in ingredients if str(i).strip()],
            "instructions": _flatten_instructions(item.get("recipeInstructions")),
            "servings": item.get("recipeYield"),
            "total_time": parse_iso8601_duration(item.get("totalTime")),
            "prep_time": parse_iso8601_duration(item.get("prepTime")),
            "cook_time": parse_iso8601_duration(item.get("cookTime")),
            "image": _first_image_url(item.get("image")),
        }
    return None


def recipe_to_markdown(recipe):
    """Renders the structured dict into a plain markdown body, so a
    scraped recipe reads/edits the same as a hand-written one -- the
    structured fields in `recipe_meta` are what the recipe-specific UI
    renders from, this body is the fallback/searchable/printable form."""
    lines = []
    meta_bits = [b for b in (recipe.get("servings") and f"Servings: {recipe['servings']}",
                              recipe.get("prep_time") and f"Prep: {recipe['prep_time']}",
                              recipe.get("cook_time") and f"Cook: {recipe['cook_time']}",
                              recipe.get("total_time") and f"Total: {recipe['total_time']}") if b]
    if meta_bits:
        lines.append(" · ".join(meta_bits))
        lines.append("")
    lines.append("## Ingredients")
    lines.extend(f"- {i}" for i in recipe.get("ingredients", []))
    lines.append("")
    lines.append("## Instructions")
    lines.extend(f"{n}. {step}" for n, step in enumerate(recipe.get("instructions", []), start=1))
    return "\n".join(lines)


def import_recipe_from_url(url, timeout=10):
    """Fetches `url` and extracts a recipe from its JSON-LD. Raises
    ValueError (caller turns this into a 4xx, not a 5xx) when the page
    has no recognizable Recipe markup -- never fabricates a partial or
    guessed result."""
    response = requests.get(url, timeout=timeout, headers={"User-Agent": "CitadelWiki/1.0"})
    response.raise_for_status()
    recipe = extract_recipe_jsonld(response.text)
    if recipe is None:
        raise ValueError("couldn't find a recipe on that page -- it may not use the standard recipe markup most sites embed")
    return recipe
