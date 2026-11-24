#!/usr/bin/env python3
"""One-time migration: real files already in the Media Vault's own
videos/mp3s/pdfs folders -> real wiki_attachments rows, so they show up
in wiki.html's Media Library instead of only the old folder-scan gallery
pages (/videos, /mp3, /pdf).

This does NOT move, copy, or delete any real file -- every file stays
exactly where it already lives (appdata/media-vault/{videos,mp3s,pdfs}/
<category>/<filename>), same real path the existing stream_video/
stream_mp3/stream_pdf routes in app.py already serve. Only a catalog
row (kind, filename, title, tags, size_bytes) gets created, with
`filename` stored as "<category>/<basename>" so wiki.html's own
attachmentOpenUrl() can reconstruct the real streaming URL -- see that
function's own comment for the exact route shape it mirrors.

`kind` is set by which folder a file lives in (videos->video,
mp3s->audio, pdfs->pdf), not by sniffing the real file extension -- a
small number of real files under pdfs/ are actually .md checklists, not
PDFs, and this schema has no other kind for them; tagging them 'pdf'
reflects where they actually live today, honestly, rather than
inventing a kind that doesn't exist. `tags` is set to [category] so the
Media Library groups by the same folder structure the old gallery used.

Idempotent by (kind, filename): re-running skips any file whose exact
catalog entry already exists.

Usage:
    python3 scripts/backfill_media_to_wiki.py [--base-url http://localhost:8085] [--dry-run]
"""
import argparse
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
VAULT_ROOT = REPO_ROOT / "appdata" / "media-vault"

FOLDER_TO_KIND = {"videos": "video", "mp3s": "audio", "pdfs": "pdf"}


def load_token(explicit_token):
    if explicit_token:
        return explicit_token
    env_token = os.environ.get("VAULT_API_TOKEN")
    if env_token:
        return env_token
    env_file = REPO_ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("VAULT_API_TOKEN="):
                return line.split("=", 1)[1].strip()
    return None


def scan_real_files():
    """Yields (kind, category, basename, size_bytes) for every real file
    found -- same one-level-of-category-subfolder layout
    scan_media_folder() in app.py already assumes."""
    for folder, kind in FOLDER_TO_KIND.items():
        root = VAULT_ROOT / folder
        if not root.is_dir():
            continue
        for category_dir in sorted(root.iterdir()):
            if not category_dir.is_dir():
                continue
            for file_path in sorted(category_dir.iterdir()):
                if file_path.is_file():
                    yield kind, category_dir.name, file_path.name, file_path.stat().st_size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:8085")
    parser.add_argument("--token", default=None)
    parser.add_argument("--dry-run", action="store_true", help="List what would be created, create nothing")
    args = parser.parse_args()

    token = load_token(args.token)
    if not token:
        print("No VAULT_API_TOKEN found (env var or ../.env). Aborting.", file=sys.stderr)
        sys.exit(1)

    headers = {"X-Vault-Token": token, "Content-Type": "application/json"}

    existing_keys = set()
    if not args.dry_run:
        existing = requests.get(f"{args.base_url}/api/wiki/attachments", headers=headers, timeout=15)
        existing.raise_for_status()
        existing_keys = {(a["kind"], a["filename"]) for a in existing.json()}

    created, skipped, total_bytes = 0, 0, 0
    for kind, category, basename, size_bytes in scan_real_files():
        filename = f"{category}/{basename}"
        total_bytes += size_bytes
        if (kind, filename) in existing_keys:
            skipped += 1
            continue
        title = os.path.splitext(basename)[0]
        if args.dry_run:
            print(f"WOULD CREATE [{kind}] {filename} ({size_bytes:,} bytes)")
            created += 1
            continue
        res = requests.post(
            f"{args.base_url}/api/wiki/attachments",
            headers=headers,
            json={"kind": kind, "filename": filename, "title": title, "tags": [category], "size_bytes": size_bytes},
            timeout=15,
        )
        if res.ok:
            created += 1
        else:
            print(f"FAILED ({res.status_code}): [{kind}] {filename} -- {res.text}", file=sys.stderr)

    verb = "would create" if args.dry_run else "created"
    print(f"\n{created} {verb}, {skipped} skipped (already cataloged). {total_bytes / (1024**3):.2f} GB scanned total.")


if __name__ == "__main__":
    main()
