"""The Mission Engine -- ROADMAP.md Phase 2, the signature cross-subject
feature. A mission gives a real reason to pull several Labs together
instead of visiting them one at a time. Every task in a mission is a
real, already-built Cloud9 feature -- this doesn't invent new subject
content, it sequences what's already real and tracks doing it.

Real v1 scope, matching every other engine built this session: manual
checkboxes per task (same honest pattern as Project Workshop's checklist
and Parent Tools' schedule), not automatic cross-Lab completion
detection -- that's real, harder, separate work, not attempted here.
Every completed task logs through the shared Learning Event schema
(learning_engine.py), so My Day and the eventual Portfolio pick missions
up for free instead of needing their own plumbing.
"""

import sqlite3
import time

import learning_engine
from paths import DATA_DIR

DB_FILE = DATA_DIR / "missions.db"

# Real mission templates. Hardcoded data, same spirit as Math Lab's own
# content -- a real, simple source of truth, not a database table nobody
# but this file needs to edit yet.
MISSION_TEMPLATES = {
    "storm-approaching": {
        "title": "A Storm Is Approaching",
        "description": "The worked example from the real expansion plan -- pull Weather, Earth, Math, History, Writing, and Preparedness together around one real event.",
        "icon": "\U0001F32A️",
        "tasks": [
            {"id": "weather", "subject": "science", "title": "Examine the real radar and atmosphere", "description": "Check Current Conditions and Radar in Weather Labs -- what's really happening right now?", "link": "/weather-labs"},
            {"id": "earth", "subject": "geography", "title": "Locate the storm", "description": "Use Earth Lab to find where you are and what region a storm like this would be moving through.", "link": "/earth-lab"},
            {"id": "math", "subject": "math", "title": "Calculate speed, distance, and time", "description": "If a storm is moving at a certain speed, how long until it reaches a place a certain distance away? Work it out in Math Lab's sandbox.", "link": "/math-lab"},
            {"id": "history", "subject": "history", "title": "Investigate a historical storm", "description": "Weather Labs' own Mission Mode has a real Historical tab -- pull up a real storm from the past and see what happened.", "link": "/weather-labs"},
            {"id": "writing", "subject": "writing", "title": "Write a real weather bulletin", "description": "Write a short bulletin like a real meteorologist would -- what's happening, what to expect, what to do.", "link": "/?open=writing"},
            {"id": "preparedness", "subject": "life", "title": "Review the family severe-weather plan", "description": "Check or update the real family emergency kit and plan in Project Workshop.", "link": "/project-workshop"},
            {"id": "save", "subject": "journal", "title": "Save what you learned", "description": "Write a Learning Journal entry about the mission -- what you found out, what surprised you.", "link": "/learning-journal"},
        ],
    },
    "cooking": {
        "title": "Let's Cook Something",
        "description": "Life Lab's real second worked example -- math scaling, kitchen science, reading, writing, and the life skill itself, all in one real activity.",
        "icon": "\U0001F373",
        "tasks": [
            {"id": "scale", "subject": "math", "title": "Scale your recipe", "description": "Pick a real recipe in Math Lab's Recipe Scaler and scale it to the size you actually need -- watch every ingredient recalculate.", "link": "/math-lab"},
            {"id": "science", "subject": "science", "title": "Ask Ollie the kitchen science question", "description": "Something in your recipe is changing because of real chemistry -- why does baking powder make batter rise? Why does a raw egg turn solid when it's heated? Ask Ollie and find out the real why, not just the what.", "link": "/?open=ai_assist"},
            {"id": "reading", "subject": "reading", "title": "Read the whole recipe twice", "description": "Read every ingredient and every step before you start cooking. Look up any word you don't know in Dictionary.", "link": "/?open=dictionary"},
            {"id": "cook", "subject": "life", "title": "Cook it for real", "description": "With a parent, actually make the recipe. Track it as a real Project Workshop project -- ingredients, steps, and what you'd do differently next time.", "link": "/project-workshop"},
            {"id": "writing", "subject": "writing", "title": "Write your own recipe card", "description": "In your own words, write out the recipe like you're teaching someone else to make it.", "link": "/?open=writing"},
            {"id": "save", "subject": "journal", "title": "Save what you learned", "description": "Write a Learning Journal entry about cooking it -- what worked, what surprised you, what you'd change.", "link": "/learning-journal"},
        ],
    },
}


def _connect():
    return sqlite3.connect(DB_FILE)


def _init_db():
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS mission_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id TEXT NOT NULL,
                started_at REAL NOT NULL,
                completed_at REAL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS task_completions (
                run_id INTEGER NOT NULL,
                task_id TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0,
                completed_at REAL,
                PRIMARY KEY (run_id, task_id)
            )
            """
        )


_init_db()


def list_templates():
    return [
        {"id": tid, "title": t["title"], "description": t["description"], "icon": t["icon"], "taskCount": len(t["tasks"])}
        for tid, t in MISSION_TEMPLATES.items()
    ]


def _row_to_run(row, tasks_done):
    run_id, template_id, started_at, completed_at = row
    template = MISSION_TEMPLATES.get(template_id)
    if not template:
        return None
    tasks = []
    for task in template["tasks"]:
        tasks.append({**task, "done": tasks_done.get(task["id"], False)})
    done_count = sum(1 for t in tasks if t["done"])
    return {
        "id": run_id,
        "templateId": template_id,
        "title": template["title"],
        "description": template["description"],
        "icon": template["icon"],
        "startedAt": started_at,
        "completedAt": completed_at,
        "tasks": tasks,
        "doneCount": done_count,
        "taskCount": len(tasks),
    }


def start_mission(template_id):
    if template_id not in MISSION_TEMPLATES:
        raise ValueError(f"Unknown mission template: {template_id}")
    now = time.time()
    with _connect() as conn:
        cur = conn.execute(
            "INSERT INTO mission_runs (template_id, started_at) VALUES (?, ?)",
            (template_id, now),
        )
        run_id = cur.lastrowid
    return get_run(run_id)


def get_run(run_id):
    with _connect() as conn:
        row = conn.execute(
            "SELECT id, template_id, started_at, completed_at FROM mission_runs WHERE id = ?",
            (run_id,),
        ).fetchone()
        if not row:
            return None
        done_rows = conn.execute(
            "SELECT task_id, done FROM task_completions WHERE run_id = ?", (run_id,)
        ).fetchall()
    tasks_done = {task_id: bool(done) for task_id, done in done_rows}
    return _row_to_run(row, tasks_done)


def get_active_runs():
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, template_id, started_at, completed_at FROM mission_runs "
            "WHERE completed_at IS NULL ORDER BY started_at DESC"
        ).fetchall()
    return [r for r in (get_run(row[0]) for row in rows) if r]


def get_history(limit=10):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT id, template_id, started_at, completed_at FROM mission_runs "
            "WHERE completed_at IS NOT NULL ORDER BY completed_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [r for r in (get_run(row[0]) for row in rows) if r]


def complete_task(run_id, task_id, done):
    """Toggling a task real-logs through the shared Learning Event schema
    (ROADMAP.md Phase 1) so missions feed My Day/Portfolio the same way
    every other real activity does, not through separate plumbing."""
    run = get_run(run_id)
    if not run:
        return None
    task = next((t for t in run["tasks"] if t["id"] == task_id), None)
    if not task:
        return None

    now = time.time()
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO task_completions (run_id, task_id, done, completed_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT (run_id, task_id) DO UPDATE SET
                done = excluded.done,
                completed_at = excluded.completed_at
            """,
            (run_id, task_id, 1 if done else 0, now if done else None),
        )

    if done:
        learning_engine.record_activity(
            subject=task["subject"],
            activity="mission_task",
            concept=f"{run['templateId']}:{task_id}",
            source="cloud9-mission-engine",
            artifact=None,
            correct=None,
        )

    updated = get_run(run_id)
    if updated["doneCount"] == updated["taskCount"] and not updated["completedAt"]:
        with _connect() as conn:
            conn.execute("UPDATE mission_runs SET completed_at = ? WHERE id = ?", (now, run_id))
        updated = get_run(run_id)
    return updated
