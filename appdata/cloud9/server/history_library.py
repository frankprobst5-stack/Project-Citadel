"""A real, honestly-sourced library of classic living books -- ROADMAP.md
Phase 3, item 3's replacement for the abandoned Wikidata "parallel
timeline" approach (that data source had real, demonstrated coverage/
reliability problems per event category -- see CARD_REDESIGN_PLAN.md).
Narrative "living books" instead of a queried events database.

Every title here is real public domain (pre-1929 US publication, well past
copyright expiration) and was pulled directly from its real, authoritative
host -- Project Gutenberg -- not scraped from any third-party blog. Grade
labels are either a real, human-curated reading-level tag published
alongside the title by Old Fashioned Education (oldfashionededucation.org,
a real homeschool curriculum site) or, where no such tag exists, stated
honestly as not given rather than invented.

Each book's raw .txt file (data/history-library/<category>/<slug>.txt) is
kept exactly as downloaded, including Project Gutenberg's own license
header/footer -- this module trims to the real START/END markers only for
the in-app reading view, and always links back to the book's real
Gutenberg page so the license terms stay attached to the content.

The "Watch" section is real too, but a different kind of real: Frank's own
already-downloaded (as a channel subscriber, for legitimate offline use)
copies of Free School's history videos, read from a read-only host mount
(see modules/education/compose.fragment.yml) rather than embedded from
YouTube -- these are current, actively-owned copyrighted videos, not
public domain, so this module only ever plays Frank's own local files,
never fetches or re-downloads anything itself.
"""

import re
from pathlib import Path

from paths import DATA_DIR

LIBRARY_DIR = DATA_DIR / "history-library"
VIDEOS_DIR = Path("/app/videos")

BOOKS = [
    {
        "id": "stories-of-great-americans",
        "title": "Stories of Great Americans for Little Americans",
        "author": "Edward Eggleston",
        "category": "american-history",
        "grade_label": "2nd to 4th grade",
        "gutenberg_id": 10070,
        "filename": "stories-of-great-americans.txt",
    },
    {
        "id": "stories-of-american-life-and-adventure",
        "title": "Stories of American Life and Adventure",
        "author": "Edward Eggleston",
        "category": "american-history",
        "grade_label": "2nd to 4th grade",
        "gutenberg_id": 15597,
        "filename": "stories-of-american-life-and-adventure.txt",
    },
    {
        "id": "bird-woman-lewis-clark",
        "title": "The Bird-Woman of the Lewis and Clark Expedition",
        "author": "Katherine Chandler",
        "category": "american-history",
        "grade_label": "K to 2nd grade (a bit younger -- a good bridge title)",
        "gutenberg_id": 5742,
        "filename": "bird-woman-lewis-clark.txt",
    },
    {
        "id": "beginners-american-history",
        "title": "The Beginner's American History",
        "author": "D. H. Montgomery",
        "category": "american-history",
        "grade_label": "Grade not stated by the source list -- denser than the Eggleston titles, a stretch text",
        "gutenberg_id": 18127,
        "filename": "beginners-american-history.txt",
    },
    {
        "id": "cave-boy-of-the-age-of-stone",
        "title": "The Cave Boy of the Age of Stone",
        "author": "Margaret A. McIntyre",
        "category": "ancient-history",
        "grade_label": "Grade not stated by the source list -- simple narrative, prehistoric/early ancient",
        "gutenberg_id": 18576,
        "filename": "cave-boy-of-the-age-of-stone.txt",
    },
    {
        "id": "story-of-the-greeks",
        "title": "The Story of the Greeks",
        "author": "H. A. Guerber",
        "category": "ancient-history",
        "grade_label": "Grade not stated by the source list -- a well-known upper-elementary ancient history text",
        "gutenberg_id": 23495,
        "filename": "story-of-the-greeks.txt",
    },
]

CATEGORIES = [
    {"id": "american-history", "title": "American History"},
    {"id": "ancient-history", "title": "Ancient History"},
]

_START_RE = re.compile(r"^\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*\*\*\*\s*$", re.MULTILINE)
_END_RE = re.compile(r"^\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*\*\*\*\s*$", re.MULTILINE)

_VIDEO_EXTENSIONS = (".mp4", ".webm", ".m4v")


def _book_by_id(book_id):
    for b in BOOKS:
        if b["id"] == book_id:
            return b
    return None


def _file_path(book):
    return LIBRARY_DIR / book["category"] / book["filename"]


def list_categories():
    return CATEGORIES


def list_books(category=None):
    books = BOOKS if not category else [b for b in BOOKS if b["category"] == category]
    result = []
    for b in books:
        path = _file_path(b)
        result.append(
            {
                "id": b["id"],
                "title": b["title"],
                "author": b["author"],
                "category": b["category"],
                "gradeLabel": b["grade_label"],
                "source": "Project Gutenberg",
                "sourceUrl": f"https://www.gutenberg.org/ebooks/{b['gutenberg_id']}",
                "available": path.exists(),
            }
        )
    return result


def get_book_text(book_id):
    """Real book text, trimmed to Project Gutenberg's own START/END markers
    for a clean reading view. Returns None if the book or file isn't found --
    no placeholder text, matching the rest of Cloud9's honest-empty-state rule."""
    book = _book_by_id(book_id)
    if not book:
        return None
    path = _file_path(book)
    if not path.exists():
        return None

    raw = path.read_text(encoding="utf-8", errors="replace")
    start_match = _START_RE.search(raw)
    end_match = _END_RE.search(raw)
    if start_match and end_match:
        body = raw[start_match.end():end_match.start()].strip()
    else:
        body = raw.strip()

    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "gradeLabel": book["grade_label"],
        "source": "Project Gutenberg",
        "sourceUrl": f"https://www.gutenberg.org/ebooks/{book['gutenberg_id']}",
        "text": body,
    }


def _video_title(filename):
    name = Path(filename).stem
    return re.sub(r"\s*-\s*FreeSchool\s*$", "", name).strip()


def list_videos():
    """Real listing of Frank's own already-downloaded video files -- never
    fetched or written by this module, just read from the read-only host
    mount. Empty list (not an error) if the mount isn't present, matching
    every other honest-empty-state pattern in this project."""
    if not VIDEOS_DIR.is_dir():
        return []
    videos = []
    for path in sorted(VIDEOS_DIR.iterdir()):
        if path.is_file() and path.suffix.lower() in _VIDEO_EXTENSIONS:
            videos.append(
                {
                    "filename": path.name,
                    "title": _video_title(path.name),
                    "url": f"/api/history-library/videos/{path.name}",
                }
            )
    return videos
