"""Real tests for transcription.py's pure functions -- list_recordings
against a real temp directory with real files (not a mocked filesystem),
and transcribe_file's real-file-missing error path. The actual HTTP call
to whisper-server is live-verified separately (see ROADMAP.md's changelog
entry) since it needs the real running container -- not something a unit
test should depend on to pass.

Run with: python3 -m unittest appdata/media-vault/test_transcription.py
"""

import os
import tempfile
import unittest

from transcription import is_safe_filename, list_recordings, transcribe_file


class ListRecordingsTests(unittest.TestCase):
    def test_returns_an_empty_list_for_a_directory_that_does_not_exist_yet(self):
        # The real, honest state before any scanner has ever run --
        # nothing has created captureDir on disk at all.
        self.assertEqual(list_recordings("/tmp/does-not-exist-9f3ac2"), [])

    def test_returns_an_empty_list_for_a_real_but_empty_directory(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(list_recordings(d), [])

    def test_lists_real_files_with_size_and_mtime(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "20260907_120000_TG101.wav")
            with open(path, "wb") as f:
                f.write(b"fake wav bytes for size testing only, not asserting audio validity")
            recordings = list_recordings(d)
            self.assertEqual(len(recordings), 1)
            self.assertEqual(recordings[0]["filename"], "20260907_120000_TG101.wav")
            self.assertEqual(recordings[0]["size_bytes"], os.path.getsize(path))
            self.assertIsInstance(recordings[0]["modified_at"], float)

    def test_skips_subdirectories_not_just_files(self):
        with tempfile.TemporaryDirectory() as d:
            os.mkdir(os.path.join(d, "a_subdirectory"))
            with open(os.path.join(d, "real.wav"), "wb") as f:
                f.write(b"x")
            recordings = list_recordings(d)
            self.assertEqual([r["filename"] for r in recordings], ["real.wav"])

    def test_sorts_newest_first(self):
        with tempfile.TemporaryDirectory() as d:
            older = os.path.join(d, "older.wav")
            newer = os.path.join(d, "newer.wav")
            with open(older, "wb") as f:
                f.write(b"x")
            os.utime(older, (1000, 1000))
            with open(newer, "wb") as f:
                f.write(b"x")
            os.utime(newer, (2000, 2000))
            recordings = list_recordings(d)
            self.assertEqual([r["filename"] for r in recordings], ["newer.wav", "older.wav"])


class TranscribeFileTests(unittest.TestCase):
    def test_raises_file_not_found_rather_than_silently_returning_nothing(self):
        with self.assertRaises(FileNotFoundError):
            transcribe_file("/tmp/does-not-exist-9f3ac2.wav")


class IsSafeFilenameTests(unittest.TestCase):
    def test_accepts_a_real_looking_recording_filename(self):
        self.assertTrue(is_safe_filename("20260907_120000_TG101.wav"))

    def test_rejects_empty_string(self):
        self.assertFalse(is_safe_filename(""))

    def test_rejects_dot_and_dotdot(self):
        self.assertFalse(is_safe_filename("."))
        self.assertFalse(is_safe_filename(".."))

    def test_rejects_forward_slash_path_traversal(self):
        self.assertFalse(is_safe_filename("../../etc/passwd"))
        self.assertFalse(is_safe_filename("subdir/file.wav"))

    def test_rejects_backslash_path_traversal(self):
        self.assertFalse(is_safe_filename("..\\..\\windows\\system32"))


if __name__ == "__main__":
    unittest.main()
