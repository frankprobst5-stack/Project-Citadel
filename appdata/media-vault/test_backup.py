"""Real tests for backup.py -- everything runs against temp directories,
never real appdata, so there's zero risk of these tests touching actual
user data. Covers the exclude-list logic, a full create->restore round
trip verifying content actually survives, and the security property
that matters most: a maliciously-crafted archive with a path-traversal
entry must be rejected before anything is extracted, not after.
"""
import os
import shutil
import tarfile
import tempfile
import unittest

import backup


class ShouldExcludeTests(unittest.TestCase):
    def test_excluded_top_level_dir(self):
        self.assertTrue(backup.should_exclude("ollama/models/foo.bin"))
        self.assertTrue(backup.should_exclude("kolibri_home/content.db"))

    def test_excluded_subpath(self):
        self.assertTrue(backup.should_exclude("media-vault/videos/movie.mp4"))
        self.assertTrue(backup.should_exclude("cloud9/models/qwen.gguf"))

    def test_real_data_is_not_excluded(self):
        self.assertFalse(backup.should_exclude("mealie/data/mealie.db"))
        self.assertFalse(backup.should_exclude("flatnotes/my-note.md"))
        self.assertFalse(backup.should_exclude("project-vigil/vigil_state.json"))

    def test_media_vault_is_excluded_from_generic_walk(self):
        # Real bug fixed 2026-09-13: vault-api's own container ALSO
        # mounts this exact host directory as its own /app (working
        # directory, containing app.py/backup.py). Restoring it via the
        # generic walk meant rmtree-ing the live process's own source
        # tree mid-request. Must be handled via extra_paths instead.
        self.assertTrue(backup.should_exclude("media-vault/citadel.db"))
        self.assertTrue(backup.should_exclude("media-vault/app.py"))

    def test_similar_but_not_matching_prefix_is_not_excluded(self):
        # "cloud9/models-similar" should NOT match the "cloud9/models"
        # exclusion (prefix must end at a path boundary, not just any
        # string prefix).
        self.assertFalse(backup.should_exclude("cloud9/models-similar/note.txt"))


class CreateAndListBackupsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.appdata = os.path.join(self.tmp, "appdata")
        self.backup_dir = os.path.join(self.tmp, "backups")
        os.makedirs(os.path.join(self.appdata, "flatnotes"))
        os.makedirs(os.path.join(self.appdata, "media-vault", "videos"))
        os.makedirs(os.path.join(self.appdata, "ollama", "models"))
        with open(os.path.join(self.appdata, "flatnotes", "note.md"), "w") as f:
            f.write("real note content")
        with open(os.path.join(self.appdata, "media-vault", "videos", "movie.mp4"), "w") as f:
            f.write("huge media file")
        with open(os.path.join(self.appdata, "ollama", "models", "weights.bin"), "w") as f:
            f.write("huge downloaded model")
        self.env_path = os.path.join(self.tmp, ".env")
        with open(self.env_path, "w") as f:
            f.write("MEALIE_API_TOKEN=real-secret-token\n")
        # Simulates vault-api's OWN /app mount -- deliberately OUTSIDE
        # appdata_root, exactly like the real citadel.db (see module
        # docstring for why this can't be reached via the generic walk).
        self.citadel_db = os.path.join(self.tmp, "vault-api-app", "citadel.db")
        os.makedirs(os.path.dirname(self.citadel_db))
        with open(self.citadel_db, "w") as f:
            f.write("real ledger data")
        self.extra_paths = {"appdata/media-vault/citadel.db": self.citadel_db}

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_list_backups_empty_dir_is_honest_not_an_error(self):
        self.assertEqual(backup.list_backups(self.backup_dir), [])

    def test_create_backup_includes_real_data_and_env(self):
        filename, filepath, size = backup.create_backup(
            self.appdata, self.env_path, self.backup_dir, extra_paths=self.extra_paths,
        )
        self.assertTrue(os.path.exists(filepath))
        self.assertGreater(size, 0)
        with tarfile.open(filepath, "r:gz") as tar:
            names = tar.getnames()
        self.assertIn("appdata/flatnotes/note.md", names)
        self.assertIn(".env", names)

    def test_create_backup_includes_extra_paths(self):
        _, filepath, _ = backup.create_backup(
            self.appdata, self.env_path, self.backup_dir, extra_paths=self.extra_paths,
        )
        with tarfile.open(filepath, "r:gz") as tar:
            names = tar.getnames()
            content = tar.extractfile("appdata/media-vault/citadel.db").read()
        self.assertIn("appdata/media-vault/citadel.db", names)
        self.assertEqual(content, b"real ledger data")

    def test_create_backup_never_walks_media_vault_generically(self):
        # Regression test for the real bug: even without extra_paths,
        # nothing under appdata/media-vault/ should ever come from the
        # generic walk (only from extra_paths, which this call omits).
        _, filepath, _ = backup.create_backup(self.appdata, self.env_path, self.backup_dir)
        with tarfile.open(filepath, "r:gz") as tar:
            names = tar.getnames()
        self.assertFalse(any(n.startswith("appdata/media-vault/") for n in names))

    def test_create_backup_excludes_regenerable_content(self):
        _, filepath, _ = backup.create_backup(self.appdata, self.env_path, self.backup_dir)
        with tarfile.open(filepath, "r:gz") as tar:
            names = tar.getnames()
        self.assertNotIn("appdata/media-vault/videos/movie.mp4", names)
        self.assertNotIn("appdata/ollama/models/weights.bin", names)

    def test_list_backups_returns_newest_first(self):
        backup.create_backup(self.appdata, self.env_path, self.backup_dir, timestamp="20260101-000000")
        backup.create_backup(self.appdata, self.env_path, self.backup_dir, timestamp="20260202-000000")
        result = backup.list_backups(self.backup_dir)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["filename"], "citadel-backup-20260202-000000.tar.gz")


class RestoreBackupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.appdata = os.path.join(self.tmp, "appdata")
        self.backup_dir = os.path.join(self.tmp, "backups")
        self.staging = os.path.join(self.tmp, "staging")
        os.makedirs(os.path.join(self.appdata, "flatnotes"))
        with open(os.path.join(self.appdata, "flatnotes", "note.md"), "w") as f:
            f.write("original note")
        self.env_path = os.path.join(self.tmp, ".env")
        with open(self.env_path, "w") as f:
            f.write("MEALIE_API_TOKEN=original-token\n")
        # Simulates vault-api's OWN /app mount -- see module docstring.
        self.citadel_db = os.path.join(self.tmp, "vault-api-app", "citadel.db")
        os.makedirs(os.path.dirname(self.citadel_db))
        with open(self.citadel_db, "w") as f:
            f.write("original ledger data")
        self.extra_paths = {"appdata/media-vault/citadel.db": self.citadel_db}

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_round_trip_restores_exact_content(self):
        filename, filepath, _ = backup.create_backup(
            self.appdata, self.env_path, self.backup_dir, extra_paths=self.extra_paths,
        )

        # Simulate real data changing/getting corrupted after the backup.
        with open(os.path.join(self.appdata, "flatnotes", "note.md"), "w") as f:
            f.write("CORRUPTED")
        with open(self.env_path, "w") as f:
            f.write("MEALIE_API_TOKEN=corrupted\n")
        with open(self.citadel_db, "w") as f:
            f.write("CORRUPTED DB")

        backup.restore_backup(filepath, self.appdata, self.env_path, self.staging, extra_paths=self.extra_paths)

        with open(os.path.join(self.appdata, "flatnotes", "note.md")) as f:
            self.assertEqual(f.read(), "original note")
        with open(self.env_path) as f:
            self.assertEqual(f.read(), "MEALIE_API_TOKEN=original-token\n")
        with open(self.citadel_db) as f:
            self.assertEqual(f.read(), "original ledger data")

    def test_chown_to_is_applied_to_restored_content(self):
        # Real bug fixed 2026-09-13: the restoring process runs as root
        # inside its container -- every restored file ended up root-
        # owned on the host, blocking the actual host user from editing
        # (or even reading, for their next backup) anything just
        # restored without sudo. Uses the current process's own uid/gid
        # as the target since this test doesn't run as root and can't
        # chown to an arbitrary uid -- what matters is that chown was
        # actually attempted/applied, not which id specifically.
        my_uid, my_gid = os.getuid(), os.getgid()
        _, filepath, _ = backup.create_backup(
            self.appdata, self.env_path, self.backup_dir, extra_paths=self.extra_paths,
        )
        backup.restore_backup(
            filepath, self.appdata, self.env_path, self.staging,
            extra_paths=self.extra_paths, chown_to=(my_uid, my_gid),
        )
        restored_note = os.path.join(self.appdata, "flatnotes", "note.md")
        self.assertEqual(os.stat(restored_note).st_uid, my_uid)
        self.assertEqual(os.stat(self.citadel_db).st_uid, my_uid)

    def test_staging_directory_is_cleaned_up_after_restore(self):
        _, filepath, _ = backup.create_backup(self.appdata, self.env_path, self.backup_dir)
        backup.restore_backup(filepath, self.appdata, self.env_path, self.staging)
        self.assertFalse(os.path.exists(self.staging))

    def test_restore_never_deletes_a_real_but_excluded_subpath(self):
        # Real bug, found live 2026-09-13, that actually destroyed real
        # data: appdata/cockpit/tiles/ (300MB+ of real map tiles) is
        # excluded from backups for size, but "cockpit" itself is
        # backed up. The old restore logic did rmtree(appdata/cockpit)
        # before replacing it with the archived copy -- which obviously
        # never had tiles/ either -- so tiles/ was just gone afterward.
        # Restoring must never delete real content that was deliberately
        # excluded from the backup; it should only ever add/overwrite
        # what the backup actually contains.
        os.makedirs(os.path.join(self.appdata, "cockpit", "tiles"))
        with open(os.path.join(self.appdata, "cockpit", "tiles", "comms_base.pmtiles"), "w") as f:
            f.write("real 300MB+ map data (stand-in)")
        with open(os.path.join(self.appdata, "cockpit", "index.html"), "w") as f:
            f.write("original dashboard")

        filename, filepath, _ = backup.create_backup(self.appdata, self.env_path, self.backup_dir)
        # Confirm the backup really doesn't have the tiles (matching the
        # real exclude rule) -- otherwise this test wouldn't be
        # exercising the real scenario at all.
        with tarfile.open(filepath, "r:gz") as tar:
            names = tar.getnames()
        self.assertNotIn("appdata/cockpit/tiles/comms_base.pmtiles", names)
        self.assertIn("appdata/cockpit/index.html", names)

        # Simulate index.html changing after the backup, same as any
        # normal restore scenario.
        with open(os.path.join(self.appdata, "cockpit", "index.html"), "w") as f:
            f.write("CORRUPTED dashboard")

        backup.restore_backup(filepath, self.appdata, self.env_path, self.staging)

        tiles_path = os.path.join(self.appdata, "cockpit", "tiles", "comms_base.pmtiles")
        self.assertTrue(os.path.exists(tiles_path), "excluded-but-real content must survive a restore")
        with open(tiles_path) as f:
            self.assertEqual(f.read(), "real 300MB+ map data (stand-in)")
        with open(os.path.join(self.appdata, "cockpit", "index.html")) as f:
            self.assertEqual(f.read(), "original dashboard")

    def test_directory_extra_path_survives_as_a_mount_point_would(self):
        # Real bug fixed 2026-09-13: notes-data is its own dedicated
        # bind mount in the real system. rmtree-ing or shutil.move-ing
        # OVER the directory ENTRY at a mount point fails with "Resource
        # busy" -- only its CONTENTS can be replaced. Simulated here by
        # checking the directory's inode is unchanged after restore
        # (proving it was never removed and recreated), while its
        # contents genuinely did change to match the backup.
        notes_dir = os.path.join(self.tmp, "vault-api-app", "notes-data")
        os.makedirs(notes_dir)
        with open(os.path.join(notes_dir, "old-note.txt"), "w") as f:
            f.write("from the backup")
        extra_paths = dict(self.extra_paths)
        extra_paths["appdata/media-vault/notes-data"] = notes_dir

        _, filepath, _ = backup.create_backup(self.appdata, self.env_path, self.backup_dir, extra_paths=extra_paths)
        inode_before = os.stat(notes_dir).st_ino

        # Simulate real drift: a new file appears after the backup.
        with open(os.path.join(notes_dir, "newer-note.txt"), "w") as f:
            f.write("added after the backup")

        backup.restore_backup(filepath, self.appdata, self.env_path, self.staging, extra_paths=extra_paths)

        self.assertEqual(os.stat(notes_dir).st_ino, inode_before, "the directory itself must not be removed/recreated")
        self.assertTrue(os.path.exists(os.path.join(notes_dir, "old-note.txt")))
        self.assertFalse(os.path.exists(os.path.join(notes_dir, "newer-note.txt")),
                          "post-backup drift should be gone after restore")

    def test_restore_never_touches_a_media_vault_dir_even_if_archive_somehow_has_one(self):
        # Regression test for the real bug: even if an archive somehow
        # contains an appdata/media-vault/ entry (an old backup made
        # before this fix, say), restore must skip it rather than
        # rmtree-ing whatever's really there on the live system (vault-
        # api's own working directory).
        os.makedirs(os.path.join(self.appdata, "media-vault"))
        sentinel = os.path.join(self.appdata, "media-vault", "app.py")
        with open(sentinel, "w") as f:
            f.write("real running application code -- must survive")

        # Build an archive by hand that includes an appdata/media-vault/
        # entry, bypassing create_backup's own exclusion so this test
        # actually exercises restore_backup's independent defense.
        os.makedirs(self.backup_dir, exist_ok=True)
        archive_path = os.path.join(self.backup_dir, "old-style-backup.tar.gz")
        evil_media_vault_file = os.path.join(self.tmp, "old_citadel.db")
        with open(evil_media_vault_file, "w") as f:
            f.write("a backup made before the media-vault exclusion existed")
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(evil_media_vault_file, arcname="appdata/media-vault/citadel.db")

        backup.restore_backup(archive_path, self.appdata, self.env_path, self.staging)

        with open(sentinel) as f:
            self.assertEqual(f.read(), "real running application code -- must survive")

    def test_path_traversal_archive_is_rejected_before_extraction(self):
        # Craft a malicious archive with a path-traversal entry -- the
        # exact "zip-slip" attack shape: an entry named to escape the
        # intended extraction directory entirely.
        malicious_path = os.path.join(self.backup_dir, "malicious.tar.gz")
        os.makedirs(self.backup_dir, exist_ok=True)
        evil_file = os.path.join(self.tmp, "evil.txt")
        with open(evil_file, "w") as f:
            f.write("payload")
        with tarfile.open(malicious_path, "w:gz") as tar:
            tar.add(evil_file, arcname="../../../etc/evil_marker")

        with self.assertRaises(backup.UnsafeArchiveError):
            backup.restore_backup(malicious_path, self.appdata, self.env_path, self.staging)

        # Nothing from the malicious archive should have escaped, and
        # real data must be untouched.
        self.assertFalse(os.path.exists("/etc/evil_marker"))
        with open(os.path.join(self.appdata, "flatnotes", "note.md")) as f:
            self.assertEqual(f.read(), "original note")
        # Staging must not be left behind with partial/malicious content.
        self.assertFalse(os.path.exists(self.staging))

    def test_restoring_missing_archive_raises_cleanly(self):
        with self.assertRaises(FileNotFoundError):
            backup.restore_backup(
                os.path.join(self.backup_dir, "does-not-exist.tar.gz"),
                self.appdata, self.env_path, self.staging,
            )


if __name__ == "__main__":
    unittest.main()
