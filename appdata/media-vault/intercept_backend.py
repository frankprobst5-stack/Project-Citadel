# PROJECT INTERCEPT // 433MHz Signal Ledger API
# Licensed under the GNU General Public License v3.0 or later
# (GPL-3.0-or-later).
#
# Brought into Citadel 2026-09-13 (ROADMAP.md Phase E) from the
# standalone project-intercept repo, unchanged in shape (serves the
# last N lines of a real rtl_433 JSON-lines output file as JSON) except
# one real bug fixed: the original wrapped the whole per-line JSON.loads
# loop in one try/except, so a single malformed/partial line (realistic
# with rtl_433's real-world output, e.g. read mid-write) discarded every
# valid signal parsed before it, not just the bad one. Now each line is
# parsed independently -- one bad line is skipped, everything else
# still shows.
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 9095
LEDGER_FILE = os.environ.get("LEDGER_FILE", "airwaves_ledger.json")
MAX_SIGNALS = 25


def read_recent_signals(ledger_path, max_signals=MAX_SIGNALS):
    """Reads the last `max_signals` lines of a real rtl_433 JSON-lines
    output file, newest first. Returns an honest empty list if the file
    doesn't exist yet (no daemon/hardware running) -- same "no_data"
    honesty as every other daemon-writes/API-reads endpoint in this
    project (see /api/scanner, /api/weather). Skips individual malformed
    lines rather than discarding the whole batch over one bad line."""
    if not os.path.exists(ledger_path):
        return []
    signals = []
    with open(ledger_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[-max_signals:]
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            signals.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return signals


class InterceptDataServer(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Suppress console log spam

    def do_GET(self):
        if self.path.startswith("/api/intercept"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            signals = read_recent_signals(LEDGER_FILE)
            self.wfile.write(json.dumps(signals).encode("utf-8"))
        else:
            self.send_error(404)


if __name__ == "__main__":
    server = HTTPServer(("", PORT), InterceptDataServer)
    print(f"[INTERCEPT BACKEND] Core data listener active on port: {PORT}")
    server.serve_forever()
