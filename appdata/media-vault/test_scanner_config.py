"""Real tests for scanner_config.py's pure conversion/validation logic --
the one part of the scanner subsystem that's actually testable without an
RTL-SDR or a running trunk-recorder instance. Stdlib unittest only, no new
dependency -- this repo doesn't have a test framework yet, and pytest would
be an odd first dependency to add for two files' worth of tests.

Run with: python3 -m unittest appdata/media-vault/test_scanner_config.py
"""

import unittest

from scanner_config import build_trunk_recorder_config, validate_talkgroups_csv

REAL_SHAPE_CSV = "Decimal,Mode,Description,Alpha Tag,Priority\n101,D,01 Dispatch,DCFD 01 Disp,1\n2227,D,Streetcar Yard,DC StcarYard,3\n"


class ValidateTalkgroupsCsvTests(unittest.TestCase):
    def test_accepts_the_real_documented_trunk_recorder_shape(self):
        ok, err = validate_talkgroups_csv(REAL_SHAPE_CSV)
        self.assertTrue(ok, err)
        self.assertIsNone(err)

    def test_accepts_extra_columns_a_real_radioreference_export_carries(self):
        csv_text = "Decimal,Hex,Alpha Tag,Mode,Description,Tag,Category,Priority\n101,065,DISP1,D,Dispatch 1,Law Dispatch,County PD,1\n"
        ok, err = validate_talkgroups_csv(csv_text)
        self.assertTrue(ok, err)

    def test_accepts_frequencies_with_no_alpha_tag_yet(self):
        # e.g. pulled from digitalfrequencysearch.com's free FCC-license
        # data, which has no talkgroup names at all -- still a real,
        # usable config, just less readable until names get added.
        csv_text = "Decimal,Mode,Description\n101,D,Unknown talkgroup 101\n"
        ok, err = validate_talkgroups_csv(csv_text)
        self.assertTrue(ok, err)

    def test_rejects_empty_input(self):
        ok, err = validate_talkgroups_csv("")
        self.assertFalse(ok)
        self.assertIn("empty", err)

    def test_rejects_missing_required_columns(self):
        ok, err = validate_talkgroups_csv("Alpha Tag\nDISP1\n")
        self.assertFalse(ok)
        self.assertIn("Decimal", err)
        self.assertIn("Mode", err)
        self.assertIn("Description", err)

    def test_rejects_a_header_only_csv_with_no_talkgroups(self):
        ok, err = validate_talkgroups_csv("Decimal,Mode,Description\n")
        self.assertFalse(ok)
        self.assertIn("no talkgroup entries", err)

    def test_rejects_a_non_numeric_decimal(self):
        ok, err = validate_talkgroups_csv("Decimal,Mode,Description\nabc,D,Bad row\n")
        self.assertFalse(ok)
        self.assertIn("Row 2", err)

    def test_rejects_an_invalid_mode(self):
        ok, err = validate_talkgroups_csv("Decimal,Mode,Description\n101,X,Bad mode\n")
        self.assertFalse(ok)
        self.assertIn("Row 2", err)


class BuildTrunkRecorderConfigTests(unittest.TestCase):
    def test_produces_the_real_documented_ver2_shape(self):
        config = build_trunk_recorder_config(
            short_name="test",
            driver="osmosdr",
            device="rtl=0",
            center_hz=857000000.0,
            rate_hz=8000000.0,
            gain=40,
            control_channels_hz=[855462500],
        )
        self.assertEqual(config["ver"], 2)
        self.assertEqual(len(config["sources"]), 1)
        self.assertEqual(config["sources"][0]["driver"], "osmosdr")
        self.assertEqual(config["sources"][0]["center"], 857000000.0)
        self.assertEqual(len(config["systems"]), 1)
        self.assertEqual(config["systems"][0]["type"], "p25")
        self.assertEqual(config["systems"][0]["control_channels"], [855462500])
        self.assertEqual(config["systems"][0]["talkgroupsFile"], "talkgroups.csv")

    def test_short_name_is_truncated_to_trunk_recorders_real_limit(self):
        config = build_trunk_recorder_config(
            short_name="waytoolongofaname",
            driver="osmosdr",
            device=None,
            center_hz=857000000.0,
            rate_hz=8000000.0,
            gain=40,
            control_channels_hz=[855462500],
        )
        self.assertEqual(len(config["systems"][0]["shortName"]), 6)

    def test_control_channels_round_trip_as_integers_not_floats(self):
        # trunk-recorder's own example uses bare integers for
        # control_channels -- a float here (855462500.0) is a real
        # config-shape mismatch a hardware-verified test would have caught.
        config = build_trunk_recorder_config(
            short_name="t", driver="osmosdr", device=None,
            center_hz=857e6, rate_hz=8e6, gain=40, control_channels_hz=[855462500.0],
        )
        self.assertIsInstance(config["systems"][0]["control_channels"][0], int)

    def test_rejects_blank_short_name(self):
        with self.assertRaises(ValueError):
            build_trunk_recorder_config(short_name="  ", driver="osmosdr", device=None, center_hz=1, rate_hz=1, gain=1, control_channels_hz=[100])

    def test_rejects_no_control_channels(self):
        with self.assertRaises(ValueError):
            build_trunk_recorder_config(short_name="t", driver="osmosdr", device=None, center_hz=1, rate_hz=1, gain=1, control_channels_hz=[])

    def test_rejects_non_positive_center_or_rate(self):
        with self.assertRaises(ValueError):
            build_trunk_recorder_config(short_name="t", driver="osmosdr", device=None, center_hz=0, rate_hz=1, gain=1, control_channels_hz=[100])
        with self.assertRaises(ValueError):
            build_trunk_recorder_config(short_name="t", driver="osmosdr", device=None, center_hz=1, rate_hz=-5, gain=1, control_channels_hz=[100])

    def test_device_and_ppm_are_optional(self):
        config = build_trunk_recorder_config(short_name="t", driver="osmosdr", device=None, center_hz=1, rate_hz=1, gain=1, control_channels_hz=[100])
        self.assertNotIn("device", config["sources"][0])
        self.assertNotIn("ppm", config["sources"][0])


if __name__ == "__main__":
    unittest.main()
