"""The shared Learning Event schema -- ROADMAP.md's Phase 1, item 1. The
one real function every Lab is meant to call when a learner does
something worth remembering, instead of each Lab inventing its own
tracking. Real schema, from the roadmap: subject -> activity -> concept ->
difficulty -> source -> artifact -> completion -> mastery -> related
concepts.

This doesn't replace the existing Cross-Subject Interactivity Engine
(`interactivity.py`) -- it sits on top of it. `interactivity.py` stays the
real durable event log + Redis broadcast (already used by Earth Lab,
Weather Labs, This Day in History); this module is what makes logging to
it, and to the new Mastery Engine, one real call instead of two separate
ones every Lab has to remember to make correctly.
"""

import interactivity
import mastery


def record_activity(subject, activity, concept, source, difficulty=None, correct=None, artifact=None, related_concepts=None):
    """Real, single entry point for the shared Learning Event schema.

    subject: e.g. "math", "geography"
    activity: e.g. "times_table_quiz", "country_lookup"
    concept: the specific thing being practiced/learned, e.g. "7x8" or
        "addition_easy" -- granularity is the caller's real call, not
        prescribed here (an exact fact for Math's times tables, a skill
        tier for Math's timed challenges, a country code for Geography).
    source: what real, authoritative thing backs this (e.g. "cloud9-math-lab",
        a NOAA product name, a country data API) -- never left blank.
    correct: True/False if this was a practice attempt with a real right/
        wrong outcome; None if this activity has no such outcome (e.g.
        just viewing a country's page) -- only then does this feed the
        Mastery Engine, matching mastery.py's own real semantics.
    """
    content_id = f"{subject}:{concept}"
    tags = [subject, activity] + (related_concepts or [])
    interactivity.register_content(content_id, tags)

    payload = {
        "subject": subject,
        "activity": activity,
        "concept": concept,
        "difficulty": difficulty,
        "source": source,
        "artifact": artifact,
        "correct": correct,
        "related_concepts": related_concepts or [],
    }
    interactivity.log_event("learning_activity", content_id, payload=payload)

    mastery_result = None
    if correct is not None:
        mastery_result = mastery.record_attempt(subject, concept, correct)

    return {"logged": True, "mastery": mastery_result}
