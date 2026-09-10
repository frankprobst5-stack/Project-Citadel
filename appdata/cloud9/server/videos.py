import json
import uuid
from pathlib import Path

import yt_dlp

from paths import DATA_DIR, STATIC_DIR

DATA_FILE = DATA_DIR / "videos.json"
VIDEOS_DIR = STATIC_DIR / "videos"


def _load():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def list_videos(shelf):
    return _load().get(shelf, [])


def add_video(shelf, url, title):
    shelf_dir = VIDEOS_DIR / shelf
    shelf_dir.mkdir(parents=True, exist_ok=True)
    video_id = uuid.uuid4().hex
    out_template = str(shelf_dir / (video_id + ".%(ext)s"))

    ydl_opts = {
        "format": "18/best[acodec!=none][vcodec!=none]",
        "outtmpl": out_template,
        "quiet": True,
        "noplaylist": True,
        "js_runtimes": {"node": {}},
        "remote_components": ["ejs:github"],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = Path(ydl.prepare_filename(info)).name

    entry = {
        "id": video_id,
        "title": title or info.get("title", "Untitled"),
        "filename": filename,
    }
    data = _load()
    data.setdefault(shelf, []).append(entry)
    _save(data)
    return entry


def remove_video(shelf, video_id):
    data = _load()
    videos = data.get(shelf, [])
    match = next((v for v in videos if v["id"] == video_id), None)
    if not match:
        return False
    videos.remove(match)
    _save(data)
    file_path = VIDEOS_DIR / shelf / match["filename"]
    if file_path.exists():
        file_path.unlink()
    return True
