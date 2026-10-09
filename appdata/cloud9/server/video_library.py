"""Video Library -- a second real "Watch" shelf, separate from History
Library's (which is specifically history-focused). This one reads from
Frank's own already-downloaded, subject-sorted video folder
(/home/frank/Desktop/school videos on the host, real subfolders per
subject -- Ancient Egypt for Kids, Earth & Space Science, Engineering &
Technology, Life Science, Physical Science, a general "a closer look"
shelf, and Math), mounted read-only (see modules/education/
compose.fragment.yml). Same reasoning as history_library.py's own local
video section: this module only ever plays Frank's own files, never
fetches or writes anything -- current, actively-owned videos, not public
domain, so no scraping/downloading logic belongs here at all.

Categories are read live from the real folder structure rather than a
hardcoded list, so a new subject folder Frank adds later just shows up --
no code change needed.
"""

import re
from pathlib import Path

VIDEOS_DIR = Path("/app/school-videos")

_VIDEO_EXTENSIONS = (".mp4", ".webm", ".m4v", ".mkv")


def _category_title(dirname):
    # Real folder names are already mostly display-ready ("Earth & Space
    # Science"); only the one lowercase one ("a closer look") needs
    # title-casing to look intentional next to the others.
    if dirname.islower():
        return dirname.title()
    return dirname


def _category_id(dirname):
    return re.sub(r"[^a-z0-9]+", "-", dirname.lower()).strip("-")


def _video_title(filename):
    return Path(filename).stem


def list_categories():
    """Real, live-scanned list -- no hardcoded subject names, so a new
    folder Frank adds under the mount just shows up next sync."""
    if not VIDEOS_DIR.is_dir():
        return []
    categories = []
    for path in sorted(VIDEOS_DIR.iterdir()):
        if path.is_dir():
            categories.append({"id": _category_id(path.name), "title": _category_title(path.name), "dirname": path.name})
    return categories


def _category_dir(category_id):
    for cat in list_categories():
        if cat["id"] == category_id:
            return VIDEOS_DIR / cat["dirname"]
    return None


def list_videos(category_id):
    cat_dir = _category_dir(category_id)
    if not cat_dir or not cat_dir.is_dir():
        return []
    videos = []
    for path in sorted(cat_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in _VIDEO_EXTENSIONS:
            videos.append(
                {
                    "filename": path.name,
                    "title": _video_title(path.name),
                    "url": f"/api/video-library/videos/{category_id}/{path.name}",
                }
            )
    return videos


def resolve_video_path(category_id, filename):
    """Real path resolution with real traversal protection -- category_id
    must match a real, live-discovered subfolder (not an arbitrary path
    segment), and the resolved file must stay inside that exact folder."""
    cat_dir = _category_dir(category_id)
    if not cat_dir:
        return None
    candidate = (cat_dir / filename).resolve()
    try:
        candidate.relative_to(cat_dir.resolve())
    except ValueError:
        return None
    if not candidate.is_file():
        return None
    return candidate
