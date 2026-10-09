"""The shared Mastery Engine -- ROADMAP.md's Phase 1, item 2. One real
table, keyed by (subject, concept), instead of every Lab inventing its own
New/Learning/Almost/Mastered tracker. Math Lab is the first real consumer
(wired in learning_engine.py); every future Lab with practice-style
content (Word Lab's spelling, Geography facts, History dates) is meant to
call `record_attempt` the same way, not build a second copy of this.

Real, honest v1 scope: this is a simple streak-based level, not proper
spaced repetition (no SM-2, no per-learner forgetting curve). Good enough
to make "what needs review" a real, non-empty answer for My Day; a real
smarter scheduler is named as open follow-on work in ROADMAP.md.
"""

import sqlite3
import time

from paths import DATA_DIR

DB_FILE = DATA_DIR / "mastery.db"

LEVELS = ("new", "learning", "almost", "mastered")

# Streak needed to reach each level. Index matches LEVELS.
_STREAK_THRESHOLDS = {"new": 0, "learning": 1, "almost": 3, "mastered": 5}

# How long a concept stays "not due" once it reaches a given level -- a
# mastered fact is checked back in on less often than one still being
# learned. new/learning are always due (0 = due immediately).
_REVIEW_INTERVAL_SECONDS = {
    "new": 0,
    "learning": 0,
    "almost": 2 * 24 * 60 * 60,
    "mastered": 7 * 24 * 60 * 60,
}


def _connect():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mastery (
                subject TEXT NOT NULL,
                concept TEXT NOT NULL,
                level TEXT NOT NULL,
                correct_streak INTEGER NOT NULL DEFAULT 0,
                last_practiced REAL NOT NULL,
                next_review REAL NOT NULL,
                PRIMARY KEY (subject, concept)
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_mastery_next_review ON mastery (next_review)")


_init_db()


def _level_for_streak(streak):
    level = "new"
    for candidate in LEVELS:
        if streak >= _STREAK_THRESHOLDS[candidate]:
            level = candidate
    return level


def record_attempt(subject, concept, correct):
    """Real, honest update: a correct answer grows the streak and can level
    a concept up; a wrong answer resets the streak and demotes a level
    that was previously almost/mastered, since that's a real sign it needs
    more practice again -- never silently kept at a level it just failed."""
    now = time.time()
    with _connect() as conn:
        row = conn.execute(
            "SELECT level, correct_streak FROM mastery WHERE subject = ? AND concept = ?",
            (subject, concept),
        ).fetchone()

        if correct:
            streak = (row[1] if row else 0) + 1
            level = _level_for_streak(streak)
            next_review = now + _REVIEW_INTERVAL_SECONDS[level]
        else:
            streak = 0
            level = "learning" if row and row[0] in ("almost", "mastered") else "new"
            next_review = now  # a miss means it's due again right away

        conn.execute(
            """
            INSERT INTO mastery (subject, concept, level, correct_streak, last_practiced, next_review)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (subject, concept) DO UPDATE SET
                level = excluded.level,
                correct_streak = excluded.correct_streak,
                last_practiced = excluded.last_practiced,
                next_review = excluded.next_review
            """,
            (subject, concept, level, streak, now, next_review),
        )
    return {"subject": subject, "concept": concept, "level": level, "correctStreak": streak}


def get_due_reviews(limit=10, subject=None):
    """Concepts genuinely due for review right now -- what My Day surfaces
    across all subjects, and what a single Lab (e.g. Word Lab's spelling
    practice mode) can ask for scoped to just its own subject."""
    now = time.time()
    with _connect() as conn:
        if subject:
            rows = conn.execute(
                """
                SELECT subject, concept, level, correct_streak, last_practiced, next_review
                FROM mastery
                WHERE next_review <= ? AND subject = ?
                ORDER BY next_review ASC
                LIMIT ?
                """,
                (now, subject, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT subject, concept, level, correct_streak, last_practiced, next_review
                FROM mastery
                WHERE next_review <= ?
                ORDER BY next_review ASC
                LIMIT ?
                """,
                (now, limit),
            ).fetchall()
    return [
        {
            "subject": r[0],
            "concept": r[1],
            "level": r[2],
            "correctStreak": r[3],
            "lastPracticed": r[4],
            "nextReview": r[5],
        }
        for r in rows
    ]


def get_all_for_subject(subject):
    """Every real concept tracked for one subject, regardless of whether
    it's due -- what a Lab like Word Lab uses to know which words in its
    own list are new/untouched versus already have real progress, so a
    practice session can prioritize sensibly instead of guessing."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT concept, level, correct_streak, next_review FROM mastery WHERE subject = ?",
            (subject,),
        ).fetchall()
    return {
        r[0]: {"level": r[1], "correctStreak": r[2], "nextReview": r[3]}
        for r in rows
    }


def get_summary():
    """Per-subject counts by level -- real input for Parent Tools/Portfolio
    later, not used by My Day directly."""
    with _connect() as conn:
        rows = conn.execute(
            "SELECT subject, level, COUNT(*) FROM mastery GROUP BY subject, level"
        ).fetchall()
    summary = {}
    for subject, level, count in rows:
        summary.setdefault(subject, {}).setdefault(level, 0)
        summary[subject][level] = count
    return summary
