"""Parent Tools v1 -- ROADMAP.md Phase 1, item 5, and the last piece
closing the loop the roadmap named: "a way to see a child's state, and to
assign work that My Day then surfaces." Built as a real recurring weekly
schedule (Mon-Fri blocks a parent lays out once), not one-off assignments
-- a real homeschool week repeats, and My Day's job is just to show
today's real weekday's blocks plus whether each one's been done today.

Real, deliberate scope: no login/auth. This is a trusted home-LAN family
tool, same threat model as every other Cloud9 feature (Kolibri and
Flatnotes both run with auth disabled too) -- a fake login would be
security theater, not real protection.
"""

import sqlite3
import time
from datetime import date

from paths import DATA_DIR

DB_FILE = DATA_DIR / "schedule.db"

WEEKDAYS = ("mon", "tue", "wed", "thu", "fri")


def _connect():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS blocks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weekday TEXT NOT NULL,
                order_index INTEGER NOT NULL,
                subject TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                link TEXT,
                duration_minutes INTEGER NOT NULL
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_blocks_weekday ON blocks (weekday, order_index)")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS completions (
                the_date TEXT NOT NULL,
                block_id INTEGER NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                completed_at REAL,
                PRIMARY KEY (the_date, block_id)
            )
            """
        )


_init_db()


def _row_to_block(row):
    return {
        "id": row[0],
        "weekday": row[1],
        "order": row[2],
        "subject": row[3],
        "title": row[4],
        "description": row[5],
        "link": row[6],
        "durationMinutes": row[7],
    }


def get_week():
    """The real, full recurring template, for the Parent Tools editor."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, weekday, order_index, subject, title, description, link, duration_minutes "
            "FROM blocks ORDER BY weekday, order_index"
        ).fetchall()
    week = {day: [] for day in WEEKDAYS}
    for row in rows:
        block = _row_to_block(row)
        if block["weekday"] in week:
            week[block["weekday"]].append(block)
    return week


def set_day(weekday, blocks):
    """Replaces one real weekday's blocks wholesale -- same "full re-save"
    pattern already used by Project Workshop's update_project, simpler
    and more robust than trying to diff/patch individual blocks."""
    if weekday not in WEEKDAYS:
        raise ValueError(f"Unknown weekday: {weekday}")
    with _connect() as conn:
        conn.execute("DELETE FROM blocks WHERE weekday = ?", (weekday,))
        conn.executemany(
            """
            INSERT INTO blocks (weekday, order_index, subject, title, description, link, duration_minutes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    weekday,
                    i,
                    b.get("subject") or "general",
                    b.get("title") or "Untitled",
                    b.get("description") or "",
                    b.get("link") or None,
                    int(b.get("durationMinutes") or 30),
                )
                for i, b in enumerate(blocks)
            ],
        )
    return get_week()[weekday]


def get_today():
    """Real Phase-1-completing data for My Day: today's actual weekday's
    blocks, merged with today's real completion state. Weekends
    correctly return an empty list -- no fake blocks on a day nothing
    was ever scheduled."""
    today = date.today()
    weekday = WEEKDAYS[today.weekday()] if today.weekday() < 5 else None
    today_str = today.isoformat()
    if not weekday:
        return {"date": today_str, "weekday": None, "blocks": []}

    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, weekday, order_index, subject, title, description, link, duration_minutes "
            "FROM blocks WHERE weekday = ? ORDER BY order_index",
            (weekday,),
        ).fetchall()
        done_rows = conn.execute(
            "SELECT block_id, done FROM completions WHERE the_date = ?", (today_str,)
        ).fetchall()
    done_map = {block_id: bool(done) for block_id, done in done_rows}

    blocks = []
    for row in rows:
        block = _row_to_block(row)
        block["done"] = done_map.get(block["id"], False)
        blocks.append(block)
    return {"date": today_str, "weekday": weekday, "blocks": blocks}


def set_block_done(the_date, block_id, done):
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO completions (the_date, block_id, done, completed_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (the_date, block_id) DO UPDATE SET
                done = excluded.done,
                completed_at = excluded.completed_at
            """,
            (the_date, block_id, 1 if done else 0, time.time() if done else None),
        )
