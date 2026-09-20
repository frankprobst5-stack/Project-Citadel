"""The Cross-Subject Interactivity Engine's real backbone -- locked in
CARD_REDESIGN_PLAN.md: SQLite as the durable event log + tag registry,
Redis as the live pub/sub bus on top of it. SQLite is the source of
truth (always written); Redis is a best-effort broadcast for anything
that wants to react live -- a Redis outage never breaks a card, it just
means nothing is listening live at that moment.
"""

import json
import os
import sqlite3
import time

from paths import DATA_DIR

DB_FILE = DATA_DIR / "interactivity.db"
REDIS_URL = os.environ.get("REDIS_URL", "redis://citadel-cloud9-redis:6379/0")
REDIS_STREAM = "cloud9:events"

_redis_client = None
_redis_tried = False


def _get_redis():
    """Lazy, best-effort Redis connection -- tried once per process, never
    retried on every call (a down Redis shouldn't cost every request a
    fresh connect-timeout)."""
    global _redis_client, _redis_tried
    if _redis_tried:
        return _redis_client
    _redis_tried = True
    try:
        import redis

        client = redis.from_url(REDIS_URL, socket_connect_timeout=1, socket_timeout=1)
        client.ping()
        _redis_client = client
    except Exception:
        _redis_client = None
    return _redis_client


def _connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS content_tags (
                content_id TEXT NOT NULL,
                tag TEXT NOT NULL,
                PRIMARY KEY (content_id, tag)
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_content_tags_tag ON content_tags (tag)")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL NOT NULL,
                event_type TEXT NOT NULL,
                content_id TEXT NOT NULL,
                payload TEXT
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events (ts)")


_init_db()


def register_content(content_id, tags):
    """Upsert a content item's tags into the registry -- e.g. a country
    page tagged ["geography", "earth_lab", "africa"]. Safe to call every
    time the content is viewed, not just the first time."""
    with _connect() as conn:
        conn.execute("DELETE FROM content_tags WHERE content_id = ?", (content_id,))
        conn.executemany(
            "INSERT OR IGNORE INTO content_tags (content_id, tag) VALUES (?, ?)",
            [(content_id, tag) for tag in tags],
        )


def log_event(event_type, content_id, payload=None):
    """Write a real event to the durable SQLite log, then best-effort
    broadcast it on the Redis stream for anything subscribed live."""
    ts = time.time()
    payload_json = json.dumps(payload or {})
    with _connect() as conn:
        conn.execute(
            "INSERT INTO events (ts, event_type, content_id, payload) VALUES (?, ?, ?, ?)",
            (ts, event_type, content_id, payload_json),
        )

    client = _get_redis()
    if client is not None:
        try:
            client.xadd(
                REDIS_STREAM,
                {"event_type": event_type, "content_id": content_id, "payload": payload_json, "ts": str(ts)},
                maxlen=1000,
                approximate=True,
            )
        except Exception:
            pass


def get_recent_events(limit=10, event_type=None):
    query = "SELECT ts, event_type, content_id, payload FROM events"
    params = ()
    if event_type:
        query += " WHERE event_type = ?"
        params = (event_type,)
    query += " ORDER BY ts DESC LIMIT ?"
    params = params + (limit,)
    with _connect() as conn:
        rows = conn.execute(query, params).fetchall()
    return [
        {"ts": ts, "event_type": event_type, "content_id": content_id, "payload": json.loads(payload or "{}")}
        for ts, event_type, content_id, payload in rows
    ]


def get_tags_for_content(content_id):
    with _connect() as conn:
        rows = conn.execute("SELECT tag FROM content_tags WHERE content_id = ?", (content_id,)).fetchall()
    return [r[0] for r in rows]


def find_content_by_tag(tag, limit=20):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT DISTINCT content_id FROM content_tags WHERE tag = ? LIMIT ?", (tag, limit)
        ).fetchall()
    return [r[0] for r in rows]
