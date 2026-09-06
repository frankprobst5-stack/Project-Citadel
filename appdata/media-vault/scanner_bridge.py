"""Turns trunk-recorder's real statusServer websocket messages into the
scanner_state.json shape WayStation's `/api/scanner` route already serves
as-is (see app.py's get_scanner_state -- it just relays whatever JSON sits
at /app/scanner/scanner_state.json, so this file is the only new piece
needed to make that route honestly return real data instead of the
"no_data" default).

Message shapes verified against trunk-recorder's own documentation
(trunkrecorder.com/docs/notes/STATUS-JSON, cross-checked against
docs/notes/STATUS-JSON.md in the robotastic/trunk-recorder repo -- both
gave the same field lists), not guessed at, matching every other
integration in this codebase (scanner_config.py's CONFIGURE.md schema,
WayStation's kiwix_search.rs OPDS/search-HTML parsing, etc.). Two message
types ("systems" and "rates") have real documented example payloads with
real values, quoted verbatim in this module's tests. Two others
("calls_active" and "recorders") only have documented field *names*, no
populated example -- their test fixtures below use those real field
names with illustrative values, which is stated here plainly rather than
implied to be a captured real payload.

ScannerState accumulates the latest known value for each message type
independently, mirroring trunk-recorder's own event model: "systems" and
"recorders" arrive once on connect, "calls_active"/"rates" arrive
continuously, and there's no single message that carries the whole
picture at once.
"""

import asyncio
import json
import time

# websockets is only needed for the live connection (run_bridge below),
# not for the pure parsing functions or ScannerState -- importing it
# lazily inside run_bridge means test_scanner_bridge.py's parsing tests
# never need the dependency installed at all, same reasoning
# scanner_config.py's own module docstring gives for staying Flask-free.


def parse_systems_message(msg):
    """Real documented shape:
    {"systems": [{"id": "0", "name": "SYS 1", "type": "p25", "sysid": "123",
                  "wacn": "456", "nac": "789012"}],
     "type": "systems", "instanceId": "", "instanceKey": ""}
    """
    return [
        {
            "id": s.get("id"),
            "name": s.get("name"),
            "type": s.get("type"),
            "sysid": s.get("sysid"),
            "wacn": s.get("wacn"),
            "nac": s.get("nac"),
        }
        for s in msg.get("systems", [])
    ]


def parse_calls_active_message(msg):
    """Real documented fields (STATUS-JSON.md): id, freq, sysNum, shortName,
    talkgroup, talkgrouptag, elapsed, length, state, phase2, conventional,
    encrypted, emergency, startTime, stopTime, freqList, recNum, srcNum,
    recState, analog, filename, statusfilename. Only the subset the
    Scanner UI's Active Talkgroups table actually needs is kept -- the
    rest (freqList, statusfilename, phase2, ...) is real but not surfaced
    yet, not dropped because it's unsupported, just not displayed.
    """
    return [
        {
            "id": c.get("id"),
            "freq": c.get("freq"),
            "system": c.get("shortName"),
            "talkgroup": c.get("talkgroup"),
            "talkgroup_tag": c.get("talkgrouptag"),
            "elapsed": c.get("elapsed"),
            "length": c.get("length"),
            "state": c.get("state"),
            "encrypted": c.get("encrypted"),
            "emergency": c.get("emergency"),
            "analog": c.get("analog"),
        }
        for c in msg.get("calls_active", [])
    ]


def parse_recorders_message(msg):
    """Real documented fields (STATUS-JSON.md): id, type, srcNum, recNum,
    count, duration, state, status_len, status_error, status_spike."""
    return [
        {
            "id": r.get("id"),
            "type": r.get("type"),
            "src_num": r.get("srcNum"),
            "rec_num": r.get("recNum"),
            "count": r.get("count"),
            "duration": r.get("duration"),
            "state": r.get("state"),
        }
        for r in msg.get("recorders", [])
    ]


def parse_rates_message(msg):
    """Real documented shape:
    {"rates": [{"id": "0", "decoderate": "39.333332"}],
     "type": "rates", "instanceId": "", "instanceKey": ""}
    """
    return [{"id": r.get("id"), "decode_rate": r.get("decoderate")} for r in msg.get("rates", [])]


class ScannerState:
    """Accumulates the latest known state from trunk-recorder's independent
    message stream. `status` only ever becomes "listening" once a real
    message has actually arrived -- constructing this class and never
    calling apply() leaves status at "no_data", the same honest default
    the route already returns when no daemon is running at all.
    """

    def __init__(self):
        self.status = "no_data"
        self.detail = None
        self.systems = []
        self.active_calls = []
        self.recorders = []
        self.decode_rates = []

    def apply(self, msg):
        msg_type = msg.get("type")
        if msg_type == "systems":
            self.systems = parse_systems_message(msg)
        elif msg_type == "calls_active":
            self.active_calls = parse_calls_active_message(msg)
        elif msg_type == "recorders":
            self.recorders = parse_recorders_message(msg)
        elif msg_type == "rates":
            self.decode_rates = parse_rates_message(msg)
        else:
            # A real message type this module doesn't handle yet (e.g.
            # "system", "call_start", "call_end", "recorder", "config") --
            # ignored rather than erroring, since trunk-recorder's own
            # docs list more message types than the Scanner UI currently
            # displays. Not silently wrong: nothing in `to_json()` claims
            # to reflect these.
            return
        self.status = "listening"

    def to_json(self):
        return {
            "status": self.status,
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) if self.status == "listening" else None,
            "detail": self.detail,
            "systems": self.systems,
            "active_calls": self.active_calls,
            "recorders": self.recorders,
            "decode_rates": self.decode_rates,
            # Real, honestly empty until Whisper.cpp transcription (a
            # separate, still-[PLANNED] backlog item) actually exists --
            # kept as a field so WayStation's existing transcript display
            # doesn't need a schema-version check to know it's absent.
            "transcripts": [],
        }


def write_scanner_state(state, path):
    with open(path, "w") as f:
        json.dump(state.to_json(), f, indent=2)


async def run_bridge(host, port, output_path, path="/server", ready_event=None, stop_event=None):
    """Runs a websocket SERVER that trunk-recorder connects to as a
    *client* -- confirmed from trunk-recorder's own real docs: "This
    setting configures Trunk Recorder to send status messages... to a
    server for processing." trunk-recorder does the connecting-out (and
    presumably its own reconnect-on-drop, being the client); this bridge
    just has to be listening and handle whatever real connection arrives.

    (An earlier draft of this function had the roles backwards -- had it
    shipped that way, this bridge would have sat there trying to dial out
    to trunk-recorder instead of accepting trunk-recorder's real inbound
    connection, and would never have received a single real message
    against actual hardware. Caught by re-reading the docs before writing
    the connection test, not by a failure in the field.)

    `ready_event`/`stop_event` exist only for tests, so a test can know
    the server socket is actually bound before connecting a client, and
    ask the server to shut down cleanly afterward -- a real deployment
    passes neither and the server just runs forever, same as this
    codebase's other long-running daemons.
    """
    import websockets.asyncio.server

    state = ScannerState()

    async def handler(ws):
        try:
            async for raw in ws:
                msg = json.loads(raw)
                state.apply(msg)
                write_scanner_state(state, output_path)
        finally:
            # The real trunk-recorder client disconnected (stopped,
            # crashed, or was reconfigured) -- marking that honestly
            # rather than leaving scanner_state.json silently frozen on
            # whatever the last message happened to say forever.
            state.status = "no_data"
            state.detail = "trunk-recorder disconnected from the status bridge."
            write_scanner_state(state, output_path)

    async with websockets.asyncio.server.serve(handler, host, port):
        if ready_event is not None:
            ready_event.set()
        if stop_event is not None:
            await stop_event.wait()
        else:
            await asyncio.Future()  # run forever


if __name__ == "__main__":
    import os
    import sys

    host = os.environ.get("SCANNER_BRIDGE_HOST", "0.0.0.0")
    port = int(os.environ.get("SCANNER_BRIDGE_PORT", "3010"))
    output_path = os.environ.get("SCANNER_STATE_PATH", "/app/scanner_state.json")
    print(f"scanner_bridge: listening on {host}:{port}, writing {output_path}", file=sys.stderr)
    asyncio.run(run_bridge(host, port, output_path))
