#!/usr/bin/env python3
"""Real host system metrics (CPU/RAM/disk/network) for the Master
Situation Board (added 2026-10-09). Runs as a persistent systemd
service on the HOST, not inside a container -- a container only sees
its own cgroup-limited view, not true host-wide usage, so this follows
the same "host-level daemon writes a JSON state file, a container-side
API reads it" pattern already established for scanner_bridge.py,
project-ibris's radar daemon, and the local weather-capture fallback
(see app.py's /api/scanner, /api/radar, /api/weather).

Writes appdata/media-vault/host-metrics/metrics_state.json every 5
seconds -- that directory is bind-mounted into vault-api at /app/
(same mount as everything else in appdata/media-vault/), so a new
/api/metrics route in app.py can serve it with the same honest
"no_data" default every other daemon-fed endpoint in this codebase
uses when the daemon isn't running yet.

CPU%: psutil.cpu_percent(interval=1) blocks for exactly 1 real second
to measure -- deliberate, not a sleep padding bug; psutil's own docs
are explicit that a 0-interval first call returns a meaningless 0.0.
Network rate is computed from two real byte-counter samples 5 seconds
apart (this loop's own interval), not an instantaneous value -- network
throughput has no meaningful instant reading, only a rate over a real
elapsed window.
"""
import json
import os
import time

import psutil

CITADEL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_DIR = os.path.join(CITADEL_DIR, "appdata", "media-vault", "host-metrics")
STATE_PATH = os.path.join(STATE_DIR, "metrics_state.json")
LOOP_SECONDS = 5


def _real_nic_name():
    """Picks the host's actual LAN-facing interface -- not loopback, not
    any Docker bridge/veth (this host runs well over a dozen of those,
    none of them the real network link). Not hardcoded to today's
    specific adapter name (a real USB WiFi dongle on this install) since
    that could change with different hardware later -- instead picks the
    first non-virtual interface that actually has an IPv4 address."""
    skip_prefixes = ("lo", "docker", "br-", "veth")
    for name, addrs in psutil.net_if_addrs().items():
        if name.startswith(skip_prefixes):
            continue
        if any(a.family.name == "AF_INET" for a in addrs):
            return name
    return None


def main():
    os.makedirs(STATE_DIR, exist_ok=True)
    nic = _real_nic_name()
    prev_net = psutil.net_io_counters(pernic=True).get(nic) if nic else None
    prev_time = time.time()

    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        now = time.time()
        net_up_bps = net_down_bps = None
        if nic:
            curr_net = psutil.net_io_counters(pernic=True).get(nic)
            if curr_net and prev_net:
                elapsed = max(now - prev_time, 0.001)
                net_up_bps = (curr_net.bytes_sent - prev_net.bytes_sent) / elapsed
                net_down_bps = (curr_net.bytes_recv - prev_net.bytes_recv) / elapsed
            prev_net = curr_net
        prev_time = now

        state = {
            "status": "ok",
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
            "cpu_percent": cpu_percent,
            "mem_used_bytes": mem.used,
            "mem_total_bytes": mem.total,
            "mem_percent": mem.percent,
            "disk_used_bytes": disk.used,
            "disk_total_bytes": disk.total,
            "disk_percent": disk.percent,
            "nic": nic,
            "net_up_bytes_per_sec": net_up_bps,
            "net_down_bytes_per_sec": net_down_bps,
        }
        tmp_path = STATE_PATH + ".tmp"
        with open(tmp_path, "w") as f:
            json.dump(state, f)
        os.replace(tmp_path, STATE_PATH)  # atomic -- never a reader sees a half-written file

        time.sleep(max(LOOP_SECONDS - 1, 1))  # cpu_percent(interval=1) already burned ~1s


if __name__ == "__main__":
    main()
