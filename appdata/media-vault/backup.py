"""Real backup/restore logic for Citadel, added 2026-09-13.

Backs up everything under appdata/ plus .env by default, EXCLUDING a
known list of large/regenerable/downloaded content (Ollama models,
Kolibri's course library, the media vault's own video/audio/PDF
library, etc.) -- deliberately an exclude-list, not an include-list.
An include-list has already bitten this project once this session (the
.gitignore gap that left appdata/mealie/data/ untracked): a new module
added later automatically gets backed up under an exclude-list, but
would silently be skipped forever under an include-list unless someone
remembers to update it.

CRITICAL, found live 2026-09-13: `media-vault` is EXCLUDED from the
generic appdata_root walk entirely, on both backup and restore. Why:
vault-api's own container ALSO mounts that exact same host directory as
its own /app (its working directory, containing app.py, this file, and
everything else it runs from). The first version of this code walked
appdata_root generically and restored `media-vault` as just another
subdirectory -- which meant `shutil.rmtree()`-ing the SAME host
directory the running Flask process's own source code lives in and is
using as its cwd, mid-request. It failed with "Resource busy" partway
through and had already deleted backup.py and test_transcription.py
before failing. `citadel.db` and `notes-data` (the only real user data
actually inside media-vault -- everything else there is source code or
the already-excluded media library) are instead handled explicitly via
`extra_paths`, addressed through vault-api's existing dedicated mounts
for each (a single file replace and a single, purpose-built directory
replace -- neither is the process's own working directory, so neither
carries this risk).

Restore is the genuinely dangerous half regardless: it overwrites real,
live data. Every restore call is expected to have taken a fresh safety
snapshot of the CURRENT state first (see app.py's /api/backup/restore
route) so a bad restore is itself always recoverable, and every archive
is validated for path-traversal ("zip-slip") before anything is
extracted.
"""
import os
import shutil
import tarfile
from datetime import datetime, timezone

# Top-level directory names under appdata/ excluded entirely from the
# generic walk. `media-vault` is here for the reason explained above --
# not because its data doesn't matter, but because it needs different,
# safer handling (see extra_paths).
EXCLUDE_DIRS = {
    "ollama", "whisper-models", "open-webui", "kolibri_home",
    "kiwix-library", "kiwix", "backups", "media-vault",
}

# Specific subpaths (relative to appdata/) excluded even though their
# parent directory is otherwise included -- large media LIBRARIES or
# transient capture state, not ledger/config data. (Kept even though
# media-vault itself is now excluded above, in case that ever changes.)
EXCLUDE_SUBPATHS = {
    "media-vault/videos", "media-vault/mp3s", "media-vault/pdfs",
    "media-vault/scanner", "media-vault/weather", "media-vault/intercept",
    "cloud9/models", "cloud9/data/nltk_data",
    "cockpit/tiles",
}


def should_exclude(rel_path):
    """`rel_path` is relative to the appdata root, using '/' separators."""
    rel_path = rel_path.replace(os.sep, "/")
    top = rel_path.split("/", 1)[0]
    if top in EXCLUDE_DIRS:
        return True
    return any(rel_path == p or rel_path.startswith(p + "/") for p in EXCLUDE_SUBPATHS)


def create_backup(appdata_root, env_file_path, backup_dir, extra_paths=None, timestamp=None):
    """Creates a timestamped .tar.gz under backup_dir containing every
    file under appdata_root not matched by should_exclude(), plus
    env_file_path (if it exists) stored as top-level ".env", plus
    whatever's in `extra_paths` (a dict of {archive_name: real_path},
    each added under that exact archive name -- this is how
    media-vault's real data gets included without walking the
    overlapping-mount directory generically; see module docstring).
    Returns the created (filename, full_path, size_bytes)."""
    os.makedirs(backup_dir, exist_ok=True)
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    filename = f"citadel-backup-{timestamp}.tar.gz"
    filepath = os.path.join(backup_dir, filename)

    with tarfile.open(filepath, "w:gz") as tar:
        for root, dirs, files in os.walk(appdata_root):
            rel_root = os.path.relpath(root, appdata_root)
            rel_root = "" if rel_root == "." else rel_root

            def _kept(d):
                rel = f"{rel_root}/{d}" if rel_root else d
                return not should_exclude(rel)
            dirs[:] = [d for d in dirs if _kept(d)]

            for f in files:
                rel_path = f"{rel_root}/{f}" if rel_root else f
                if should_exclude(rel_path):
                    continue
                tar.add(os.path.join(root, f), arcname=f"appdata/{rel_path}")

        if os.path.exists(env_file_path):
            tar.add(env_file_path, arcname=".env")

        for arcname, real_path in (extra_paths or {}).items():
            if os.path.exists(real_path):
                tar.add(real_path, arcname=arcname)

    return filename, filepath, os.path.getsize(filepath)


def list_backups(backup_dir):
    """Newest first. Returns [] if backup_dir doesn't exist yet -- same
    honest-empty-default convention as everywhere else in this project."""
    if not os.path.isdir(backup_dir):
        return []
    entries = []
    for f in os.listdir(backup_dir):
        full_path = os.path.join(backup_dir, f)
        if os.path.isfile(full_path) and f.endswith(".tar.gz"):
            entries.append({
                "filename": f,
                "size_bytes": os.path.getsize(full_path),
                "created": datetime.fromtimestamp(
                    os.path.getmtime(full_path), tz=timezone.utc
                ).strftime("%Y-%m-%d %H:%M:%S UTC"),
            })
    entries.sort(key=lambda e: e["filename"], reverse=True)
    return entries


class UnsafeArchiveError(Exception):
    """Raised when a backup archive contains a path that would escape
    the intended extraction directory (a "zip-slip"/path-traversal
    attempt) -- whether from a corrupted file or a malicious one, this
    must never be silently extracted."""


def _validate_archive_members(tar):
    for member in tar.getmembers():
        norm = os.path.normpath(member.name)
        if norm.startswith("..") or os.path.isabs(norm):
            raise UnsafeArchiveError(f"unsafe path in archive: {member.name!r}")


def _chown_recursive(path, uid, gid):
    """Best-effort -- the restoring process runs as root inside its
    container (found live 2026-09-13: a real restore left every
    restored file/dir root-owned on the host, blocking the actual host
    user from editing them, or even reading them back for a future
    backup, without sudo -- same class of issue as this project's other
    Docker-creates-root-owned-paths bugs). Never raises: a chown failing
    on some exotic filesystem shouldn't fail the restore itself, which
    already did the part that actually matters."""
    try:
        os.chown(path, uid, gid)
    except OSError:
        pass
    if os.path.isdir(path) and not os.path.islink(path):
        for root, dirs, files in os.walk(path):
            for name in dirs:
                try:
                    os.chown(os.path.join(root, name), uid, gid)
                except OSError:
                    pass
            for name in files:
                try:
                    os.chown(os.path.join(root, name), uid, gid)
                except OSError:
                    pass


def restore_backup(archive_path, appdata_root, env_file_path, staging_dir, extra_paths=None, chown_to=None):
    """Extracts `archive_path` into a staging directory (validating
    every member's path first), then moves its appdata/* entries (any
    named in EXCLUDE_DIRS -- i.e. media-vault -- are skipped here too,
    defensively, even though create_backup never puts them there) into
    appdata_root, its top-level .env into env_file_path, and each
    `extra_paths` entry into its own real_path. Always cleans up the
    staging directory, even on failure. Raises UnsafeArchiveError before
    extracting anything if the archive contains a path-traversal
    attempt. `chown_to`, if given as an (uid, gid) tuple, is applied
    (best-effort) to everything actually restored, so files don't end up
    owned by whatever user the restoring process happened to run as."""
    if os.path.exists(staging_dir):
        shutil.rmtree(staging_dir)
    os.makedirs(staging_dir)

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            _validate_archive_members(tar)
            tar.extractall(path=staging_dir)

        staged_appdata = os.path.join(staging_dir, "appdata")
        if os.path.isdir(staged_appdata):
            os.makedirs(appdata_root, exist_ok=True)
            for item in os.listdir(staged_appdata):
                if item in EXCLUDE_DIRS:
                    continue
                src = os.path.join(staged_appdata, item)
                dst = os.path.join(appdata_root, item)
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                elif os.path.exists(dst):
                    os.remove(dst)
                shutil.move(src, dst)
                if chown_to:
                    _chown_recursive(dst, *chown_to)

        staged_env = os.path.join(staging_dir, ".env")
        if os.path.exists(staged_env):
            shutil.move(staged_env, env_file_path)
            if chown_to:
                _chown_recursive(env_file_path, *chown_to)

        for arcname, real_path in (extra_paths or {}).items():
            staged_extra = os.path.join(staging_dir, arcname)
            if not os.path.exists(staged_extra):
                continue
            if os.path.isdir(staged_extra):
                # real_path may itself be an active bind-mount point
                # (e.g. notes-data has its own dedicated mount) -- found
                # live 2026-09-13: rmtree-ing or moving something over
                # the mount-point directory ENTRY itself fails with
                # "Resource busy", since the kernel won't let you remove
                # a directory while something's mounted there. Clear its
                # CONTENTS instead and leave the mount point itself
                # untouched -- this works whether real_path is a mount
                # point or an ordinary directory.
                os.makedirs(real_path, exist_ok=True)
                for entry in os.listdir(real_path):
                    entry_path = os.path.join(real_path, entry)
                    if os.path.isdir(entry_path) and not os.path.islink(entry_path):
                        shutil.rmtree(entry_path)
                    else:
                        os.remove(entry_path)
                for entry in os.listdir(staged_extra):
                    shutil.move(os.path.join(staged_extra, entry), os.path.join(real_path, entry))
                if chown_to:
                    _chown_recursive(real_path, *chown_to)
            else:
                parent = os.path.dirname(real_path)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                if os.path.exists(real_path):
                    os.remove(real_path)
                shutil.move(staged_extra, real_path)
                if chown_to:
                    _chown_recursive(real_path, *chown_to)
    finally:
        shutil.rmtree(staging_dir, ignore_errors=True)
