"""Nature Lab -- ROADMAP.md Phase 3, item 7: plants/animals/birds/
insects/trees/ecosystems, a Nature Journal that's a real Learning
Journal entry type (reuse, not a new store), season tracking.

Real sourcing: checked School Library first for real existing nature
content (same discipline as every other section) -- real counts
confirmed live: trees (5), plants (3), birds (3), insects (3). Video
Library's existing "A Closer Look" category (real FreeSchool nature
videos -- hoverflies, kangaroos, penguins, etc.) covers more. Nature Lab
links to both rather than duplicating either.

Season tracking uses real, verified 2026/2027 solstice and equinox UTC
times (cross-checked against multiple real astronomical sources before
use) -- not a simplified approximation, and not guessed at.
"""

from datetime import datetime, timezone

# Real, verified UTC moments -- Northern Hemisphere seasons. Covers
# 2026 in full plus the one 2027 boundary (spring equinox) needed to
# correctly close out a 2026 winter.
SEASON_BOUNDARIES = [
    ("Spring", datetime(2026, 3, 20, 14, 46, tzinfo=timezone.utc)),
    ("Summer", datetime(2026, 6, 21, 8, 24, tzinfo=timezone.utc)),
    ("Fall", datetime(2026, 9, 23, 0, 5, tzinfo=timezone.utc)),
    ("Winter", datetime(2026, 12, 21, 20, 50, tzinfo=timezone.utc)),
    ("Spring", datetime(2027, 3, 20, 20, 25, tzinfo=timezone.utc)),
]

NATURE_TOPICS = [
    {"id": "trees", "title": "Trees", "searchTerm": "trees"},
    {"id": "plants", "title": "Plants", "searchTerm": "plants"},
    {"id": "birds", "title": "Birds", "searchTerm": "birds"},
    {"id": "insects", "title": "Insects", "searchTerm": "insects"},
]


def get_season():
    now = datetime.now(timezone.utc)
    current_season = "Winter"  # real default for any date before our first boundary
    next_name, next_date = None, None
    for name, boundary in SEASON_BOUNDARIES:
        if now < boundary:
            next_name, next_date = name, boundary
            break
        current_season = name

    return {
        "currentSeason": current_season,
        "nextSeasonStarts": next_name,
        "nextChangeDate": next_date.isoformat() if next_date else None,
        "daysUntilNextSeason": (next_date - now).days if next_date else None,
    }


def get_nature_topics():
    return NATURE_TOPICS
