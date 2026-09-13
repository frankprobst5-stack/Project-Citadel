"""Real unit tests for intercept_backend.py's read_recent_signals() --
pure file I/O and JSON-lines parsing, fully testable without any real
RTL-SDR hardware or a running rtl_433 process."""
import json
import os
import tempfile
import unittest

from intercept_backend import read_recent_signals


class ReadRecentSignalsTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".json")
        os.close(fd)

    def tearDown(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def _write_lines(self, *dicts):
        with open(self.path, "w", encoding="utf-8") as f:
            for d in dicts:
                f.write(json.dumps(d) + "\n")

    def test_missing_file_returns_empty_list_honestly(self):
        os.unlink(self.path)  # simulate "no daemon has written anything yet"
        self.assertEqual(read_recent_signals(self.path), [])

    def test_returns_newest_first(self):
        self._write_lines({"id": "1"}, {"id": "2"}, {"id": "3"})
        result = read_recent_signals(self.path)
        self.assertEqual([r["id"] for r in result], ["3", "2", "1"])

    def test_respects_max_signals_window(self):
        self._write_lines(*({"id": str(i)} for i in range(30)))
        result = read_recent_signals(self.path, max_signals=25)
        self.assertEqual(len(result), 25)
        self.assertEqual(result[0]["id"], "29")  # newest of the 30

    def test_one_malformed_line_does_not_discard_valid_ones(self):
        # Real bug fixed 2026-09-13: the original implementation's single
        # try/except around the whole parsing loop meant one bad line
        # wiped out every valid signal, not just itself.
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"id": "good_1"}) + "\n")
            f.write("{not valid json at all\n")
            f.write(json.dumps({"id": "good_2"}) + "\n")
        result = read_recent_signals(self.path)
        ids = [r["id"] for r in result]
        self.assertIn("good_1", ids)
        self.assertIn("good_2", ids)
        self.assertEqual(len(result), 2)

    def test_blank_lines_are_skipped(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(json.dumps({"id": "a"}) + "\n")
            f.write("\n")
            f.write("   \n")
            f.write(json.dumps({"id": "b"}) + "\n")
        result = read_recent_signals(self.path)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
