"""Local cache for Weather Labs' live observations -- the real design
decision for CARD_REDESIGN_PLAN.md's "still open" cache question, made
here 2026-09-20: SQLite, one row per successful fetch, kept long enough
to compute a real pressure trend (current vs. ~3h ago) and to answer
honestly when the network is down (last-known reading + its real age,
never silently relabeled as current).
"""

import json
import sqlite3
import time

from paths import DATA_DIR

DB_FILE = DATA_DIR / "weather_cache.db"

# Real 3-hour NWS pressure-trend convention -- comparing further back or
# forward would need query changes here, not just the caller.
TREND_WINDOW_SECONDS = 3 * 60 * 60
TREND_TOLERANCE_SECONDS = 45 * 60


def _connect():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fetched_at REAL NOT NULL,
                station TEXT NOT NULL,
                payload TEXT NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_observations_fetched_at ON observations (fetched_at)")


_init_db()


def save_observation(station, data):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO observations (fetched_at, station, payload) VALUES (?, ?, ?)",
            (time.time(), station, json.dumps(data)),
        )
        # Real housekeeping, not just the trend window -- keeps the file
        # from growing forever on a dashboard nobody ever restarts.
        conn.execute("DELETE FROM observations WHERE fetched_at < ?", (time.time() - 7 * 24 * 60 * 60,))


def get_latest():
    with _connect() as conn:
        row = conn.execute(
            "SELECT fetched_at, station, payload FROM observations ORDER BY fetched_at DESC LIMIT 1"
        ).fetchone()
    if not row:
        return None
    return {"fetched_at": row[0], "station": row[1], "payload": json.loads(row[2])}


def get_history(hours=24):
    """Every real cached observation from the last `hours` -- powers the
    instrument popovers' trend graphs. Deliberately returns whatever
    real points exist rather than padding/interpolating a smooth curve:
    a family that's only opened Weather Labs twice today gets two real
    points and an honest gap, not a fabricated line between them."""
    cutoff = time.time() - hours * 60 * 60
    with _connect() as conn:
        rows = conn.execute(
            "SELECT fetched_at, payload FROM observations WHERE fetched_at >= ? ORDER BY fetched_at ASC",
            (cutoff,),
        ).fetchall()
    return [{"fetched_at": ts, "payload": json.loads(payload)} for ts, payload in rows]


def get_near(seconds_ago, tolerance_seconds=TREND_TOLERANCE_SECONDS):
    """The observation closest to `seconds_ago` in the past, only if
    within `tolerance_seconds` of that target -- returns None rather
    than a misleading trend built from a reading that's really 6 hours
    old when we asked for 3."""
    target = time.time() - seconds_ago
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT fetched_at, station, payload FROM observations
            ORDER BY ABS(fetched_at - ?) ASC LIMIT 1
            """,
            (target,),
        ).fetchone()
    if not row or abs(row[0] - target) > tolerance_seconds:
        return None
    return {"fetched_at": row[0], "station": row[1], "payload": json.loads(row[2])}
