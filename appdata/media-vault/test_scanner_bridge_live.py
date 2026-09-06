"""Real websocket server/connection tests for scanner_bridge.py's
run_bridge(), against a real local test client -- not trunk-recorder
itself (this sandbox can't run trunk-recorder at all, it needs real USB
device passthrough for an RTL-SDR), but a genuine TCP websocket
connection all the same, playing trunk-recorder's real role: dialing
*out* to the bridge as a client and pushing real message shapes, exactly
as trunk-recorder's own docs describe ("configures Trunk Recorder to
send status messages... to a server"). Proves the server's
accept/receive/write/disconnect-handling plumbing genuinely works, not
just its message-parsing logic (already covered, dependency-free, in
test_scanner_bridge.py).

Requires the `websockets` package -- not part of this repo's base test
run for exactly that reason (test_scanner_config.py's own docstring
explains the "no new dependency" bar for the always-run suite; this file
is the deliberate, labeled exception, run separately).

Run with: python3 -m unittest test_scanner_bridge_live.py
"""

import asyncio
import json
import os
import tempfile
import unittest

import websockets

from scanner_bridge import run_bridge

REAL_SYSTEMS_MSG = {
    "systems": [{"id": "0", "name": "SYS 1", "type": "p25", "sysid": "123", "wacn": "456", "nac": "789012"}],
    "type": "systems",
    "instanceId": "",
    "instanceKey": "",
}

CALLS_ACTIVE_MSG = {
    "type": "calls_active",
    "calls_active": [
        {"id": "1", "freq": "854612500", "sysNum": "0", "shortName": "aep", "talkgroup": "3421", "talkgrouptag": "County Dispatch", "elapsed": "12"}
    ],
}


class RunBridgeAsARealWebsocketServerTests(unittest.IsolatedAsyncioTestCase):
    async def test_a_real_client_connecting_like_trunk_recorder_updates_real_state(self):
        # A fixed port rather than an ephemeral one: run_bridge is
        # fire-and-forget by design (matching a real long-running
        # daemon), so it doesn't hand back the bound port for a test to
        # discover -- adding that just for testability would be a more
        # invasive API change than picking one unlikely-to-collide port.
        with tempfile.TemporaryDirectory() as tmp:
            output_path = os.path.join(tmp, "scanner_state.json")
            ready = asyncio.Event()
            stop = asyncio.Event()
            port = 31010
            server_task = asyncio.create_task(run_bridge("127.0.0.1", port, output_path, ready_event=ready, stop_event=stop))
            await asyncio.wait_for(ready.wait(), timeout=5)

            # Plays trunk-recorder's real role: a client dialing OUT to
            # the configured statusServer address and pushing messages.
            async with websockets.connect(f"ws://127.0.0.1:{port}/server") as client:
                await client.send(json.dumps(REAL_SYSTEMS_MSG))
                await client.send(json.dumps(CALLS_ACTIVE_MSG))
                await asyncio.sleep(0.2)  # let the server process both

            await asyncio.sleep(0.2)  # let the server's disconnect handler run
            stop.set()
            await server_task

            with open(output_path) as f:
                state = json.load(f)
            self.assertEqual(state["systems"][0]["name"], "SYS 1")
            self.assertEqual(state["active_calls"][0]["talkgroup"], "3421")
            # The client (playing trunk-recorder) disconnected before the
            # server was told to stop -- state must reflect that honestly,
            # not stay frozen on "listening" after the real link dropped.
            self.assertEqual(state["status"], "no_data")
            self.assertIn("disconnected", state["detail"])


if __name__ == "__main__":
    unittest.main()
