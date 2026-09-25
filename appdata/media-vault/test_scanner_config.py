"""Real tests for scanner_config.py's pure conversion/validation logic --
the one part of the scanner subsystem that's actually testable without an
RTL-SDR or a running trunk-recorder instance. Stdlib unittest only, no new
dependency -- this repo doesn't have a test framework yet, and pytest would
be an odd first dependency to add for two files' worth of tests.

Run with: python3 -m unittest appdata/media-vault/test_scanner_config.py
"""

import unittest

from scanner_config import (
    build_config,
    build_conventional_config,
    build_trunk_recorder_config,
    make_profile,
    slugify_profile_name,
    unique_profile_id,
    validate_channel_file_csv,
    validate_csv_for_system,
    validate_talkgroups_csv,
)

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
        self.assertEqual(
            config["statusServer"], "ws://scanner-bridge:3010/server",
            "without this, real hardware would run and record but never emit a single status message",
        )
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


# Real PANCOM channel-list shape (a real Texas county, not named here --
# see 2026-09-12's ROADMAP.md note about not committing identifying
# location data) brought from a real RadioReference county page,
# 2026-09-06, not invented. TG Number is a synthetic per-channel index
# (trunk-recorder's conventional channelFile requires one; these
# frequencies don't have real talkgroup numbers the way a trunked system
# would). Frequencies/tones are real (public-record RadioReference data,
# not sensitive by themselves); place/agency names are genericized.
REAL_CONVENTIONAL_CSV = (
    "TG Number,Frequency,Tone,Alpha Tag,Description\n"
    "1,155.7750,114.8,Sheriff Disp,County Sheriff Dispatch\n"
    "2,154.1450,156.7,VFD Tactical 1,VFD Tactical 1\n"
)


class ValidateChannelFileCsvTests(unittest.TestCase):
    def test_accepts_the_real_documented_shape(self):
        ok, err = validate_channel_file_csv(REAL_CONVENTIONAL_CSV)
        self.assertTrue(ok, err)
        self.assertIsNone(err)

    def test_accepts_a_frequency_with_no_tone_or_alpha_tag_yet(self):
        # e.g. VFD Tactical 2 (154.1375 MHz), listed as plain analog with
        # no PL tone at all in the real county data.
        ok, err = validate_channel_file_csv("TG Number,Frequency\n3,154.1375\n")
        self.assertTrue(ok, err)

    def test_rejects_empty_input(self):
        ok, err = validate_channel_file_csv("")
        self.assertFalse(ok)
        self.assertIn("empty", err)

    def test_rejects_tg_number_not_being_the_first_column(self):
        ok, err = validate_channel_file_csv("Frequency,TG Number\n154.1375,1\n")
        self.assertFalse(ok)
        self.assertIn("first column", err)

    def test_rejects_missing_frequency_column(self):
        ok, err = validate_channel_file_csv("TG Number,Tone\n1,114.8\n")
        self.assertFalse(ok)
        self.assertIn("Frequency", err)

    def test_rejects_a_non_numeric_tg_number(self):
        ok, err = validate_channel_file_csv("TG Number,Frequency\nabc,154.1375\n")
        self.assertFalse(ok)
        self.assertIn("Row 2", err)

    def test_rejects_a_non_positive_frequency(self):
        ok, err = validate_channel_file_csv("TG Number,Frequency\n1,0\n")
        self.assertFalse(ok)
        self.assertIn("Frequency", err)


class BuildConventionalConfigTests(unittest.TestCase):
    def test_produces_the_real_documented_ver2_shape_for_p25_conventional(self):
        config = build_conventional_config(
            short_name="pancom", system_type="conventionalP25", driver="osmosdr", device="rtl=0",
            center_hz=155e6, rate_hz=2400000.0, gain=40, squelch=-60,
        )
        self.assertEqual(config["ver"], 2)
        self.assertEqual(config["systems"][0]["type"], "conventionalP25")
        self.assertEqual(config["systems"][0]["channelFile"], "channels.csv")
        self.assertEqual(config["systems"][0]["squelch"], -60.0)
        self.assertEqual(config["systems"][0]["modulation"], "qpsk")
        self.assertEqual(config["statusServer"], "ws://scanner-bridge:3010/server")

    def test_analog_conventional_has_no_modulation_field(self):
        # trunk-recorder's docs don't list modulation as applying to
        # plain analog "conventional" systems -- only conventionalP25/DMR.
        config = build_conventional_config(
            short_name="pancom", system_type="conventional", driver="osmosdr", device=None,
            center_hz=155e6, rate_hz=2400000.0, gain=40, squelch=-60,
        )
        self.assertNotIn("modulation", config["systems"][0])

    def test_rejects_an_unknown_system_type(self):
        with self.assertRaises(ValueError):
            build_conventional_config(short_name="t", system_type="smartnet", driver="osmosdr", device=None, center_hz=1, rate_hz=1, gain=1, squelch=-50)

    def test_rejects_blank_short_name(self):
        with self.assertRaises(ValueError):
            build_conventional_config(short_name="  ", system_type="conventional", driver="osmosdr", device=None, center_hz=1, rate_hz=1, gain=1, squelch=-50)

    def test_rejects_non_positive_center_or_rate(self):
        with self.assertRaises(ValueError):
            build_conventional_config(short_name="t", system_type="conventional", driver="osmosdr", device=None, center_hz=0, rate_hz=1, gain=1, squelch=-50)

    def test_device_and_ppm_are_optional(self):
        config = build_trunk_recorder_config(short_name="t", driver="osmosdr", device=None, center_hz=1, rate_hz=1, gain=1, control_channels_hz=[100])
        self.assertNotIn("device", config["sources"][0])
        self.assertNotIn("ppm", config["sources"][0])


class ValidateCsvForSystemTests(unittest.TestCase):
    def test_dispatches_trunked_to_talkgroups_validation(self):
        ok, err = validate_csv_for_system("trunked", REAL_SHAPE_CSV)
        self.assertTrue(ok, err)

    def test_dispatches_conventional_to_channel_file_validation(self):
        ok, err = validate_csv_for_system("conventional", REAL_CONVENTIONAL_CSV)
        self.assertTrue(ok, err)

    def test_dispatches_conventionalp25_to_channel_file_validation(self):
        ok, err = validate_csv_for_system("conventionalP25", REAL_CONVENTIONAL_CSV)
        self.assertTrue(ok, err)

    def test_rejects_an_unknown_system_type(self):
        ok, err = validate_csv_for_system("smartnet", REAL_SHAPE_CSV)
        self.assertFalse(ok)
        self.assertIn("smartnet", err)


class BuildConfigDispatchTests(unittest.TestCase):
    def test_dispatches_trunked_to_the_real_trunked_shape(self):
        config = build_config(
            short_name="test", system_type="trunked", driver="osmosdr", device=None,
            center_hz=857e6, rate_hz=8e6, gain=40, control_channels_hz=[855462500],
        )
        self.assertEqual(config["systems"][0]["type"], "p25")
        self.assertEqual(config["systems"][0]["talkgroupsFile"], "talkgroups.csv")

    def test_dispatches_conventional_to_the_real_conventional_shape(self):
        config = build_config(
            short_name="pancom", system_type="conventionalP25", driver="osmosdr", device=None,
            center_hz=155e6, rate_hz=2400000.0, gain=40, squelch=-60,
        )
        self.assertEqual(config["systems"][0]["channelFile"], "channels.csv")
        self.assertEqual(config["systems"][0]["modulation"], "qpsk")

    def test_rejects_an_unknown_system_type(self):
        with self.assertRaises(ValueError):
            build_config(short_name="t", system_type="smartnet", driver="osmosdr", device=None, center_hz=1, rate_hz=1, gain=1)


class SlugifyProfileNameTests(unittest.TestCase):
    def test_lowercases_and_hyphenates(self):
        self.assertEqual(slugify_profile_name("PANCOM P25!"), "pancom-p25")

    def test_collapses_repeated_separators(self):
        self.assertEqual(slugify_profile_name("  Fire & EMS  "), "fire-ems")

    def test_falls_back_when_nothing_alphanumeric_survives(self):
        self.assertEqual(slugify_profile_name("!!!"), "profile")


class UniqueProfileIdTests(unittest.TestCase):
    def test_returns_the_plain_slug_when_unused(self):
        self.assertEqual(unique_profile_id("PANCOM", existing_ids=set()), "pancom")

    def test_appends_a_numeric_suffix_on_collision(self):
        self.assertEqual(unique_profile_id("PANCOM", existing_ids={"pancom"}), "pancom-2")

    def test_keeps_incrementing_past_multiple_collisions(self):
        self.assertEqual(unique_profile_id("PANCOM", existing_ids={"pancom", "pancom-2", "pancom-3"}), "pancom-4")


class MakeProfileTests(unittest.TestCase):
    def test_builds_a_real_storable_trunked_profile(self):
        profile = make_profile(
            name="AEP Utility", system_type="trunked", short_name="aep",
            driver="osmosdr", device=None, center_hz=857e6, rate_hz=8e6, gain=40,
            csv_data=REAL_SHAPE_CSV, control_channels_hz=[855462500],
        )
        self.assertEqual(profile["id"], "aep-utility")
        self.assertEqual(profile["name"], "AEP Utility")
        self.assertEqual(profile["system_type"], "trunked")
        self.assertEqual(profile["csv_data"], REAL_SHAPE_CSV)

    def test_builds_a_real_storable_conventional_profile(self):
        profile = make_profile(
            name="PANCOM", system_type="conventionalP25", short_name="pancom",
            driver="osmosdr", device="rtl=0", center_hz=155e6, rate_hz=2400000.0,
            gain=40, csv_data=REAL_CONVENTIONAL_CSV, squelch=-60,
        )
        self.assertEqual(profile["id"], "pancom")
        self.assertEqual(profile["squelch"], -60)

    def test_rejects_a_blank_name(self):
        with self.assertRaises(ValueError):
            make_profile(
                name="  ", system_type="trunked", short_name="t", driver="osmosdr",
                device=None, center_hz=1, rate_hz=1, gain=1, csv_data=REAL_SHAPE_CSV,
                control_channels_hz=[100],
            )

    def test_rejects_an_invalid_csv_before_ever_building_a_config(self):
        with self.assertRaises(ValueError):
            make_profile(
                name="Bad", system_type="trunked", short_name="t", driver="osmosdr",
                device=None, center_hz=1, rate_hz=1, gain=1, csv_data="",
                control_channels_hz=[100],
            )

    def test_rejects_fields_that_would_also_fail_direct_activation(self):
        # No control channels for a trunked system -- build_trunk_recorder_config
        # itself would reject this; make_profile must reject it too, not save
        # a profile that could never actually be activated.
        with self.assertRaises(ValueError):
            make_profile(
                name="Broken", system_type="trunked", short_name="t", driver="osmosdr",
                device=None, center_hz=1, rate_hz=1, gain=1, csv_data=REAL_SHAPE_CSV,
                control_channels_hz=[],
            )

    def test_avoids_colliding_with_an_existing_id(self):
        profile = make_profile(
            name="PANCOM", system_type="conventionalP25", short_name="pancom",
            driver="osmosdr", device=None, center_hz=155e6, rate_hz=2400000.0,
            gain=40, csv_data=REAL_CONVENTIONAL_CSV, squelch=-60,
            existing_ids={"pancom"},
        )
        self.assertEqual(profile["id"], "pancom-2")


if __name__ == "__main__":
    unittest.main()
