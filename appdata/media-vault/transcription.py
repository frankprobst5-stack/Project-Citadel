"""Offline audio transcription via a real Whisper.cpp service, decided
2026-09-07 -- the "offline audio transcription" Local AI backlog item.
Same "orchestrate, don't reimplement" treatment as Ollama/Kiwix: this
talks to a real `whisper-server` (the actual `whisper.cpp` project's own
HTTP server binary, apt-installed, verified live before writing any of
this -- real Ubuntu package `whisper.cpp` 1.8.3, real `/inference`
endpoint confirmed by hand with `curl` against the bundled Debian sample
WAV, returns `{"text": "..."}`) rather than reimplementing speech
recognition here.

Pure functions, no Flask import -- same testability reasoning as
scanner_config.py. `list_recordings` reads real files from trunk-
recorder's own `captureDir` (see scanner_config.py's STATUS_SERVER_URL
sibling constant reasoning -- this repo has no RTL-SDR dongle to
actually populate that directory yet, so an empty list is the honest
default, not a fabricated one).
"""

import os

import requests

WHISPER_URL = "http://whisper:8082/inference"
# Same real hardware-constrained timeout reasoning as ai_sitrep.rs's
# Ollama call: a base.en model transcribes roughly 10x realtime on this
# CPU (verified live: a real 53s clip took 5.3s), but a cold container
# start plus a long clip could still take a while -- generous rather
# than tight.
TRANSCRIBE_TIMEOUT_SECONDS = 60


def list_recordings(calls_dir):
    """Real directory listing of trunk-recorder's own captureDir --
    filename, size, and mtime for whatever audio files actually exist.
    Returns an empty list, not an error, when the directory doesn't
    exist yet (no scanner has ever run) or is empty (nothing captured
    yet) -- both are real, honest states, not failures. Sorted newest
    first, matching every other "recent activity" list in this project.
    """
    if not os.path.isdir(calls_dir):
        return []
    entries = []
    for name in os.listdir(calls_dir):
        path = os.path.join(calls_dir, name)
        if not os.path.isfile(path):
            continue
        stat = os.stat(path)
        entries.append({
            "filename": name,
            "size_bytes": stat.st_size,
            "modified_at": stat.st_mtime,
        })
    entries.sort(key=lambda e: e["modified_at"], reverse=True)
    return entries


def is_safe_filename(filename):
    """True only for a bare filename with no path separators -- rejects
    empty strings, `.`/`..`, and anything containing `/` or `\\`. This
    gets joined directly onto a real directory path by the caller, so a
    caller-supplied `../../etc/passwd` has to be refused outright here,
    not trusted.
    """
    if not filename or filename in (".", ".."):
        return False
    return "/" not in filename and "\\" not in filename


def transcribe_file(file_path, whisper_url=WHISPER_URL, timeout=TRANSCRIBE_TIMEOUT_SECONDS):
    """Posts a real audio file to the real whisper-server `/inference`
    endpoint and returns the transcribed text. Raises FileNotFoundError
    if the file doesn't exist (caller's job to turn that into a clean
    HTTP error, same division of responsibility as scanner_config.py's
    validators raising ValueError) and requests.RequestException if
    whisper-server itself is unreachable or errors -- never returns a
    fabricated transcript on failure.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    with open(file_path, "rb") as f:
        resp = requests.post(whisper_url, files={"file": f}, timeout=timeout)
    resp.raise_for_status()
    return resp.json()["text"].strip()
