"""Real tests for scanner_bridge.py's parsing logic, run against trunk-
recorder's actual documented statusServer message shapes. "systems" and
"rates" fixtures below are the real documented example payloads, quoted
verbatim from trunkrecorder.com/docs/notes/STATUS-JSON. "calls_active"
and "recorders" fixtures use the real documented field *names* (no
populated example exists in trunk-recorder's docs) with illustrative
values -- see scanner_bridge.py's own module docstring for why that
distinction matters.

Run with: python3 -m unittest appdata/media-vault/test_scanner_bridge.py
"""

import json
import os
import tempfile
import unittest

from scanner_bridge import (
    ScannerState,
    parse_calls_active_message,
    parse_recorders_message,
    parse_rates_message,
    parse_systems_message,
    write_scanner_state,
)

# Verbatim from trunk-recorder's real docs.
REAL_SYSTEMS_MSG = json.loads(
    '{"systems": [{"id": "0", "name": "SYS 1", "type": "p25", "sysid": "123", '
    '"wacn": "456", "nac": "789012"}], "type": "systems", "instanceId": "", "instanceKey": ""}'
)

# Verbatim from trunk-recorder's real docs.
REAL_RATES_MSG = json.loads(
    '{"rates": [{"id": "0", "decoderate": "39.333332"}], "type": "rates", "instanceId": "", "instanceKey": ""}'
)

# Real documented field names, illustrative values (no populated example
# exists in trunk-recorder's own docs -- see module docstring).
CALLS_ACTIVE_MSG = {
    "type": "calls_active",
    "calls_active": [
        {
            "id": "12345",
            "freq": "854612500",
            "sysNum": "0",
            "shortName": "aep",
            "talkgroup": "3421",
            "talkgrouptag": "County Dispatch",
            "elapsed": "12",
            "length": "0",
            "state": "1",
            "encrypted": "0",
            "emergency": "0",
            "analog": "0",
        }
    ],
}

RECORDERS_MSG = {
    "type": "recorders",
    "recorders": [
        {"id": "0", "type": "p25", "srcNum": "0", "recNum": "0", "count": "142", "duration": "12.3", "state": "1"}
    ],
}


class ParseSystemsMessageTests(unittest.TestCase):
    def test_reads_the_real_documented_example(self):
        systems = parse_systems_message(REAL_SYSTEMS_MSG)
        self.assertEqual(systems, [{"id": "0", "name": "SYS 1", "type": "p25", "sysid": "123", "wacn": "456", "nac": "789012"}])

    def test_empty_systems_array_is_honestly_empty(self):
        self.assertEqual(parse_systems_message({"systems": [], "type": "systems"}), [])


class ParseRatesMessageTests(unittest.TestCase):
    def test_reads_the_real_documented_example(self):
        rates = parse_rates_message(REAL_RATES_MSG)
        self.assertEqual(rates, [{"id": "0", "decode_rate": "39.333332"}])


class ParseCallsActiveMessageTests(unittest.TestCase):
    def test_reads_the_documented_fields(self):
        calls = parse_calls_active_message(CALLS_ACTIVE_MSG)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["talkgroup"], "3421")
        self.assertEqual(calls[0]["talkgroup_tag"], "County Dispatch")
        self.assertEqual(calls[0]["system"], "aep")
        self.assertEqual(calls[0]["elapsed"], "12")

    def test_no_active_calls_is_honestly_empty(self):
        self.assertEqual(parse_calls_active_message({"calls_active": [], "type": "calls_active"}), [])


class ParseRecordersMessageTests(unittest.TestCase):
    def test_reads_the_documented_fields(self):
        recorders = parse_recorders_message(RECORDERS_MSG)
        self.assertEqual(len(recorders), 1)
        self.assertEqual(recorders[0]["type"], "p25")
        self.assertEqual(recorders[0]["count"], "142")
        self.assertEqual(recorders[0]["state"], "1")


class ScannerStateTests(unittest.TestCase):
    def test_a_fresh_state_is_honestly_no_data(self):
        state = ScannerState()
        as_json = state.to_json()
        self.assertEqual(as_json["status"], "no_data")
        self.assertIsNone(as_json["updated_at"])
        self.assertEqual(as_json["systems"], [])
        self.assertEqual(as_json["transcripts"], [], "must stay empty -- no transcription daemon exists yet")

    def test_applying_a_real_systems_message_flips_status_to_listening(self):
        state = ScannerState()
        state.apply(REAL_SYSTEMS_MSG)
        as_json = state.to_json()
        self.assertEqual(as_json["status"], "listening")
        self.assertIsNotNone(as_json["updated_at"])
        self.assertEqual(len(as_json["systems"]), 1)

    def test_message_types_accumulate_independently(self):
        # trunk-recorder's real event model: systems arrives once on
        # connect, calls_active arrives continuously -- applying one
        # must not erase data already known from the other.
        state = ScannerState()
        state.apply(REAL_SYSTEMS_MSG)
        state.apply(CALLS_ACTIVE_MSG)
        as_json = state.to_json()
        self.assertEqual(len(as_json["systems"]), 1, "systems must survive a later calls_active message")
        self.assertEqual(len(as_json["active_calls"]), 1)

    def test_an_unhandled_real_message_type_is_ignored_not_erroring(self):
        state = ScannerState()
        state.apply({"type": "config", "some": "future-field"})
        # Deliberately still no_data -- "config" isn't parsed into
        # anything yet, so nothing should claim otherwise.
        self.assertEqual(state.to_json()["status"], "no_data")


class WriteScannerStateTests(unittest.TestCase):
    def test_writes_real_json_a_flask_route_can_serve_as_is(self):
        state = ScannerState()
        state.apply(REAL_SYSTEMS_MSG)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "scanner_state.json")
            write_scanner_state(state, path)
            with open(path) as f:
                loaded = json.load(f)
            self.assertEqual(loaded["status"], "listening")
            self.assertEqual(loaded["systems"][0]["name"], "SYS 1")


if __name__ == "__main__":
    unittest.main()
