"""Turns operator-supplied scanner setup into real trunk-recorder config
files, decided 2026-09-05 -- the generic "last mile" for the trunked-radio
scanner backlog item. Trunked systems are inherently local (every county
runs different frequencies/talkgroups), so this can never be automatic the
way flight tracking is. What CAN be generic is this: accept whatever the
operator got hold of -- typed by hand off RadioReference's free (no
subscription needed) system pages, a CSV shared publicly on OpenMHz, or a
paid RadioReference export -- and turn it into files trunk-recorder
actually understands. All three sources produce (or can be typed into) the
same simple CSV shape, so one converter covers all of them.

Schema verified against trunk-recorder's own docs (CONFIGURE.md,
robotastic/trunk-recorder), not guessed at -- ver:2 top-level, a `sources`
array (SDR device config) and a `systems` array (control_channels +
talkgroupsFile per trunked system).

Pure functions, no Flask import -- keeps this testable without a running
server, and (someday) reusable if a second UI ever needs the same
conversion.
"""

import csv
import io
import re

REQUIRED_TALKGROUP_HEADERS = {"Decimal", "Mode", "Description"}
VALID_MODES = {"A", "D", "M", "T"}


def validate_talkgroups_csv(raw_csv_text):
    """Returns (is_valid, error_message). error_message is None on success.

    Deliberately permissive about extra columns -- a straight RadioReference
    export carries columns (Hex, Tag, Category) trunk-recorder doesn't need;
    rejecting those would punish the exact CSV operators are most likely to
    actually have. Only the columns trunk-recorder's docs mark required are
    enforced, and "Alpha Tag" is intentionally not required here even though
    trunk-recorder's docs list it as commonly present -- a system with no
    friendly talkgroup names yet (e.g. frequencies pulled from
    digitalfrequencysearch.com's free FCC-license data, no talkgroup names
    at all) should still produce a working, if less readable, config.
    """
    if not raw_csv_text or not raw_csv_text.strip():
        return False, "Talkgroups CSV is empty."

    reader = csv.DictReader(io.StringIO(raw_csv_text.strip()))
    if reader.fieldnames is None:
        return False, "Could not read a header row from the talkgroups CSV."

    headers = {h.strip() for h in reader.fieldnames}
    missing = REQUIRED_TALKGROUP_HEADERS - headers
    if missing:
        return False, f"Talkgroups CSV is missing required column(s): {', '.join(sorted(missing))}."

    rows = list(reader)
    if not rows:
        return False, "Talkgroups CSV has a header row but no talkgroup entries."

    for i, row in enumerate(rows, start=2):  # row 1 is the header
        decimal = (row.get("Decimal") or "").strip()
        if not decimal.isdigit():
            return False, f"Row {i}: \"Decimal\" must be a whole number, got {decimal!r}."
        mode = (row.get("Mode") or "").strip().upper()
        if mode and mode not in VALID_MODES:
            return False, f"Row {i}: \"Mode\" must be one of {sorted(VALID_MODES)}, got {mode!r}."

    return True, None


CHANNEL_FILE_REQUIRED_HEADERS = {"TG Number", "Frequency"}


def validate_channel_file_csv(raw_csv_text):
    """Returns (is_valid, error_message) for a conventional-system
    channelFile -- the counterpart to validate_talkgroups_csv() for
    trunked systems, decided 2026-09-06 when a real operator brought
    real conventional Sheriff/Fire/EMS frequencies (a real county's
    PANCOM system) that the trunked-only builder below couldn't express
    at all. Schema verified against trunk-recorder's own CONFIGURE.md,
    not guessed at: "TG Number" must be the first column, "Frequency" is
    the only other required one -- Tone/Alpha Tag/Description/Category/
    Tag/Enable/Signal Detector/Squelch are all real optional columns a
    plain frequency list (no talkgroup names yet) shouldn't be forced to
    provide, same reasoning validate_talkgroups_csv already applies.
    """
    if not raw_csv_text or not raw_csv_text.strip():
        return False, "Channel list CSV is empty."

    reader = csv.DictReader(io.StringIO(raw_csv_text.strip()))
    if reader.fieldnames is None:
        return False, "Could not read a header row from the channel list CSV."

    headers = [h.strip() for h in reader.fieldnames]
    if not headers or headers[0] != "TG Number":
        return False, "\"TG Number\" must be the first column in the channel list CSV."

    missing = CHANNEL_FILE_REQUIRED_HEADERS - set(headers)
    if missing:
        return False, f"Channel list CSV is missing required column(s): {', '.join(sorted(missing))}."

    rows = list(reader)
    if not rows:
        return False, "Channel list CSV has a header row but no channel entries."

    for i, row in enumerate(rows, start=2):  # row 1 is the header
        tg = (row.get("TG Number") or "").strip()
        if not tg.isdigit():
            return False, f"Row {i}: \"TG Number\" must be a whole number, got {tg!r}."
        freq = (row.get("Frequency") or "").strip()
        try:
            if float(freq) <= 0:
                raise ValueError
        except ValueError:
            return False, f"Row {i}: \"Frequency\" must be a positive number, got {freq!r}."

    return True, None


CONVENTIONAL_SYSTEM_TYPES = {"conventional", "conventionalP25"}

# Real trunk-recorder config field, decided 2026-09-06 alongside
# scanner_bridge.py: trunk-recorder is the websocket *client* here (its
# own docs: "configures Trunk Recorder to send status messages... to a
# server"), dialing out to this address -- "scanner-bridge" is the
# docker-compose service name scanner_bridge.py runs as, same
# container-name-as-hostname pattern already used for citadel-ollama,
# citadel-vault-brain, etc. on the shared citadel-net network. Without
# this field, real hardware would run and record calls but never emit a
# single status message -- config.json would look complete and still
# leave scanner_state.json silently stuck on "no_data" forever.
STATUS_SERVER_URL = "ws://scanner-bridge:3010/server"


def build_conventional_config(short_name, system_type, driver, device, center_hz, rate_hz, gain, squelch, ppm=None):
    """Builds a real trunk-recorder ver:2 config for a conventional (fixed-
    frequency, non-trunked) system -- e.g. individual Sheriff/Fire/EMS
    dispatch and tactical channels that each sit on their own frequency
    rather than following a control channel. Schema verified against
    trunk-recorder's own CONFIGURE.md: "channels"/"channelFile", and
    squelch is required for every conventional system, unlike trunked
    systems where it's optional. `system_type` picks analog FM demod
    ("conventional") vs P25 conventional decode ("conventionalP25") --
    a real per-system choice, since a source can only demodulate one way,
    even though a single real-world dispatch system (like PANCOM) may
    mix both kinds of channel across two separate system blocks sharing
    one source.
    """
    if not short_name or not short_name.strip():
        raise ValueError("short_name is required.")
    if system_type not in CONVENTIONAL_SYSTEM_TYPES:
        raise ValueError(f"system_type must be one of {sorted(CONVENTIONAL_SYSTEM_TYPES)}, got {system_type!r}.")
    if center_hz <= 0 or rate_hz <= 0:
        raise ValueError("center_hz and rate_hz must both be positive.")

    source = {
        "center": float(center_hz),
        "rate": float(rate_hz),
        "gain": float(gain),
        "driver": driver or "osmosdr",
        "digitalRecorders": 2,
    }
    if device:
        source["device"] = device
    if ppm is not None:
        source["ppm"] = float(ppm)

    system = {
        "shortName": short_name.strip()[:6],
        "type": system_type,
        "channelFile": "channels.csv",
        "squelch": float(squelch),
    }
    if system_type == "conventionalP25":
        system["modulation"] = "qpsk"

    return {
        "ver": 2,
        "sources": [source],
        "systems": [system],
        "captureDir": "/app/calls",
        "statusServer": STATUS_SERVER_URL,
    }


ALL_SYSTEM_TYPES = {"trunked"} | CONVENTIONAL_SYSTEM_TYPES


def validate_csv_for_system(system_type, csv_data):
    """Dispatches to whichever CSV shape a system_type actually uses --
    the same validation the direct-activation route already runs, reused
    here so a saved profile (see make_profile below) can never be broken
    in a way the direct path wouldn't also catch."""
    if system_type == "trunked":
        return validate_talkgroups_csv(csv_data)
    if system_type in CONVENTIONAL_SYSTEM_TYPES:
        return validate_channel_file_csv(csv_data)
    return False, f"Unknown system_type {system_type!r} -- must be one of {sorted(ALL_SYSTEM_TYPES)}."


def build_config(short_name, system_type, driver, device, center_hz, rate_hz, gain,
                  control_channels_hz=None, squelch=-50, ppm=None):
    """Dispatches to build_trunk_recorder_config or build_conventional_config
    by system_type -- one call site for both the direct-activation route and
    profile activation, so the two paths can't silently drift apart."""
    if system_type == "trunked":
        return build_trunk_recorder_config(
            short_name=short_name, driver=driver, device=device, center_hz=center_hz,
            rate_hz=rate_hz, gain=gain, control_channels_hz=control_channels_hz or [],
            ppm=ppm, squelch=squelch,
        )
    if system_type in CONVENTIONAL_SYSTEM_TYPES:
        return build_conventional_config(
            short_name=short_name, system_type=system_type, driver=driver, device=device,
            center_hz=center_hz, rate_hz=rate_hz, gain=gain, squelch=squelch, ppm=ppm,
        )
    raise ValueError(f"Unknown system_type {system_type!r} -- must be one of {sorted(ALL_SYSTEM_TYPES)}.")


def slugify_profile_name(name):
    """A real, storable id from an operator-typed profile name -- lowercase,
    non-alphanumeric runs collapsed to a single hyphen, so "PANCOM P25!"
    becomes "pancom-p25" rather than something with spaces or punctuation
    that would need escaping everywhere it's later used as a JSON key or
    URL path segment (DELETE/activate both address a profile by this id)."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return slug or "profile"


def unique_profile_id(name, existing_ids):
    """slugify_profile_name, with a numeric suffix if that slug is already
    taken -- two profiles named "PANCOM" (a trunked config today, a
    conventional one later) shouldn't collide and silently overwrite."""
    base = slugify_profile_name(name)
    candidate = base
    n = 2
    existing = set(existing_ids)
    while candidate in existing:
        candidate = f"{base}-{n}"
        n += 1
    return candidate


def make_profile(name, system_type, short_name, driver, device, center_hz, rate_hz, gain,
                  csv_data, control_channels_hz=None, squelch=-50, ppm=None, existing_ids=()):
    """Validates and builds a real, storable scanner profile -- the "like a
    Uniden BearCat" request from a real storm-chaser field tester
    (2026-09-16, WayStation's own ROADMAP.md): save several complete scanner
    setups (e.g. a trunked county system and a conventional Fire/EMS list)
    and flip between them without re-filling the whole setup form each
    time. Raises ValueError on anything that wouldn't also be accepted by
    the direct-activation path -- a saved profile that could never actually
    be activated is worse than refusing to save it. Returns a plain dict,
    not written to disk here -- storage is the Flask route's job, this
    stays pure and testable like the rest of this module."""
    if not name or not name.strip():
        raise ValueError("A profile name is required.")

    valid, error = validate_csv_for_system(system_type, csv_data)
    if not valid:
        raise ValueError(error)

    # Build once to confirm every other field is real and usable -- the
    # resulting config itself isn't stored on the profile; activation
    # rebuilds it fresh from these same fields, so the two paths can never
    # drift (e.g. a STATUS_SERVER_URL change automatically applies to every
    # already-saved profile the next time it's activated).
    build_config(
        short_name=short_name, system_type=system_type, driver=driver, device=device,
        center_hz=center_hz, rate_hz=rate_hz, gain=gain,
        control_channels_hz=control_channels_hz, squelch=squelch, ppm=ppm,
    )

    return {
        "id": unique_profile_id(name, existing_ids),
        "name": name.strip(),
        "system_type": system_type,
        "short_name": short_name,
        "driver": driver,
        "device": device,
        "center_hz": center_hz,
        "rate_hz": rate_hz,
        "gain": gain,
        "control_channels_hz": control_channels_hz or [],
        "squelch": squelch,
        "ppm": ppm,
        "csv_data": csv_data,
    }


def build_trunk_recorder_config(short_name, driver, device, center_hz, rate_hz, gain, control_channels_hz, ppm=None, squelch=-50):
    """Builds a real trunk-recorder ver:2 config dict -- not a guess at the
    shape, matches CONFIGURE.md's documented Source/System objects exactly.
    Raises ValueError on anything that would produce a config trunk-recorder
    can't actually use -- never silently write a broken file.
    """
    if not short_name or not short_name.strip():
        raise ValueError("short_name is required.")
    if not control_channels_hz:
        raise ValueError("At least one control channel frequency is required.")
    if center_hz <= 0 or rate_hz <= 0:
        raise ValueError("center_hz and rate_hz must both be positive.")

    source = {
        "center": float(center_hz),
        "rate": float(rate_hz),
        "gain": float(gain),
        "driver": driver or "osmosdr",
        "digitalRecorders": 2,
    }
    if device:
        source["device"] = device
    if ppm is not None:
        source["ppm"] = float(ppm)

    system = {
        "shortName": short_name.strip()[:6],
        "type": "p25",
        "control_channels": [int(f) for f in control_channels_hz],
        "modulation": "qpsk",
        "talkgroupsFile": "talkgroups.csv",
        "squelch": float(squelch),
    }

    return {
        "ver": 2,
        "sources": [source],
        "systems": [system],
        "captureDir": "/app/calls",
        "statusServer": STATUS_SERVER_URL,
    }
