"""Cloud9's own real front door onto Kolibri's content -- CARD_REDESIGN_PLAN.md's
locked "School Library" design: a clean grid of videos and exercises,
built directly on Kolibri's real REST API, with none of Kolibri's own
coach/admin chrome. Confirmed live against the actual running instance.

Real, load-bearing finding from building this: `/api/content/contentnode/
?kind=video` against a real, large library (100GB+, 21k+ videos) took
over 3 minutes and never completed against Kolibri's original 1024m
memory cap -- traced to the container being pinned at that ceiling, not
a slow query in general (the same request returned in ~10s once
modules/education/compose.fragment.yml's kolibri mem_limit was raised
to 2048m). Even at that speed, calling Kolibri live on every page view
would still make every family wait on it directly, so this module syncs
the full video/exercise list into a local SQLite cache
(data/school_library.db) and serves every real request from there --
fast regardless of Kolibri's own current load, with a real background
refresh instead of a live call per request.

Not yet built, named honestly rather than faked: progress/completion
checkmarks (attemptlog) -- confirmed live that the real endpoint exists
and returns 200, but this test instance has zero real learner accounts
yet, so its actual populated field shape couldn't be verified against
real data. Grade-level/subject filtering is a separate known gap (see
CARD_REDESIGN_PLAN.md) -- Kolibri's own `grade_levels`/`categories`
fields are opaque IDs with no live lookup table found yet.
"""

import json
import os
import sqlite3
import time

import requests

from paths import DATA_DIR

KOLIBRI_BASE_URL = os.environ.get("KOLIBRI_BASE_URL", "http://citadel-kolibri:8080")
# Browser-facing, not container-to-container -- same convention already
# used by cards.json's own existing "Full School Library" link, so this
# doesn't introduce a second, inconsistent way to reach Kolibri.
KOLIBRI_EXTERNAL_URL = os.environ.get("KOLIBRI_EXTERNAL_URL", "http://localhost:8081")
HEADERS = {"User-Agent": "Cloud9 School Library (kids learning dashboard)"}
DB_FILE = DATA_DIR / "school_library.db"

# Content rarely changes (an admin importing a new channel is a rare,
# deliberate action) -- re-syncing on every page view would just be
# needlessly hammering Kolibri. Real threshold, not a guess: long enough
# that normal daily use never re-triggers it, short enough that a newly
# imported channel shows up the same day.
SYNC_INTERVAL_SECONDS = 6 * 60 * 60


def _connect():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS content (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                thumbnail_url TEXT,
                video_url TEXT,
                duration INTEGER,
                channel_id TEXT,
                license_name TEXT,
                license_owner TEXT
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_content_kind ON content (kind)")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS sync_meta (key TEXT PRIMARY KEY, value TEXT)"
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS learners (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                full_name TEXT
            )
            """
        )


_init_db()


def _get_meta(key):
    with _connect() as conn:
        row = conn.execute("SELECT value FROM sync_meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def _set_meta(key, value):
    with _connect() as conn:
        conn.execute("INSERT OR REPLACE INTO sync_meta (key, value) VALUES (?, ?)", (key, value))


def _find_file_url(files, preset_contains):
    # Browser-facing (thumbnails/video play directly in the family's
    # browser), so this always uses the external URL, never the
    # container-to-container KOLIBRI_BASE_URL.
    for f in files or []:
        if preset_contains in (f.get("preset") or ""):
            return f"{KOLIBRI_EXTERNAL_URL}{f['storage_url']}"
    return None


def _fetch_kind(kind):
    resp = requests.get(
        f"{KOLIBRI_BASE_URL}/api/content/contentnode/",
        params={"kind": kind},
        headers=HEADERS,
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()


def sync_library(force=False):
    """Real fetch + cache refresh. Non-fatal on failure -- an unreachable
    Kolibri just means the library keeps showing whatever was cached
    last time, same honest degrade pattern as Weather Labs."""
    last_sync = _get_meta("last_sync")
    if not force and last_sync and (time.time() - float(last_sync)) < SYNC_INTERVAL_SECONDS:
        return

    rows = []
    for kind in ("video", "exercise"):
        nodes = _fetch_kind(kind)
        for n in nodes:
            files = n.get("files") or []
            rows.append(
                (
                    n["id"],
                    n["kind"],
                    n.get("title") or "(untitled)",
                    n.get("description") or "",
                    _find_file_url(files, "thumbnail"),
                    _find_file_url(files, "video") if kind == "video" else None,
                    n.get("duration"),
                    n.get("channel_id"),
                    n.get("license_name"),
                    n.get("license_owner"),
                )
            )

    with _connect() as conn:
        conn.execute("DELETE FROM content")
        conn.executemany(
            """
            INSERT INTO content (id, kind, title, description, thumbnail_url, video_url,
                                  duration, channel_id, license_name, license_owner)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )

    _sync_learners()
    _set_meta("last_sync", str(time.time()))


def _sync_learners():
    resp = requests.get(f"{KOLIBRI_BASE_URL}/api/auth/facilityuser/", headers=HEADERS, timeout=15)
    resp.raise_for_status()
    users = resp.json()
    with _connect() as conn:
        conn.execute("DELETE FROM learners")
        conn.executemany(
            "INSERT INTO learners (id, username, full_name) VALUES (?, ?, ?)",
            [(u["id"], u["username"], u.get("full_name") or u["username"]) for u in users],
        )


def get_content(kind, search=None, page=1, page_size=24):
    offset = (page - 1) * page_size
    query = "SELECT id, title, description, thumbnail_url, video_url, duration FROM content WHERE kind = ?"
    params = [kind]
    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
    count_query = query.replace(
        "SELECT id, title, description, thumbnail_url, video_url, duration", "SELECT COUNT(*)"
    )
    query += " ORDER BY title LIMIT ? OFFSET ?"

    with _connect() as conn:
        total = conn.execute(count_query, params).fetchone()[0]
        rows = conn.execute(query, params + [page_size, offset]).fetchall()

    items = [
        {
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "thumbnailUrl": r[3],
            "videoUrl": r[4],
            "duration": r[5],
            "kolibriUrl": f"{KOLIBRI_EXTERNAL_URL}/en/learn/#/topics/c/{r[0]}",
        }
        for r in rows
    ]
    return {"items": items, "total": total, "page": page, "pageSize": page_size}


def get_learners():
    with _connect() as conn:
        rows = conn.execute("SELECT id, username, full_name FROM learners ORDER BY full_name").fetchall()
    return [{"id": r[0], "username": r[1], "fullName": r[2]} for r in rows]


def get_status():
    last_sync = _get_meta("last_sync")
    with _connect() as conn:
        video_count = conn.execute("SELECT COUNT(*) FROM content WHERE kind = 'video'").fetchone()[0]
        exercise_count = conn.execute("SELECT COUNT(*) FROM content WHERE kind = 'exercise'").fetchone()[0]
    return {
        "lastSync": float(last_sync) if last_sync else None,
        "videoCount": video_count,
        "exerciseCount": exercise_count,
    }
