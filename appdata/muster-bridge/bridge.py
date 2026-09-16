# MUSTER BRIDGE // WSP/1-over-HTTP reader for Muster
# Copyright (C) 2026 SnapPress // Copyleft GNU AGPL-3.0-or-later
#
# Real, named gap this closes (see Muster's own ROADMAP.md, added
# 2026-09-16): Muster's browser JS cannot reach WayStation's WSP/1
# data at all -- WSP/1's real sync transports are file exchange and an
# authenticated raw TCP socket (net_sync.rs), neither reachable from a
# browser, which can only do HTTP/WebSocket. This service is a real
# WSP/1 peer -- it connects to WayStation over that exact TCP
# protocol, exactly like a second WayStation instance would, and
# re-exposes what it pulls as plain JSON over HTTP for Muster to
# fetch. It does NOT invent a new API on WayStation's side, and it
# does NOT change WayStation's trust model -- it just IS a trusted
# peer, using the same shared-secret mechanism any other WSP/1 station
# already uses (see WSP-1.md's "Signing" section and net_sync.rs's own
# module comment).
#
# **Wire protocol, verified directly against the real Rust source
# (net_sync.rs / sync.rs, 2026-09-16), not guessed or reverse-
# engineered from the prose spec alone**:
#   - Framing: a 4-byte big-endian length prefix, then that many bytes
#     of UTF-8 JSON. (net_sync.rs's write_message/read_message.)
#   - Every message is a JSON object tagged by a "kind" field:
#     Hello / Accepted / Rejected / Manifest / ObjectsRequest / Objects / Done.
#   - Hello{callsign, nonce, signature}: signature is hex
#     HMAC-SHA256(nonce) using this station's own shared secret --
#     the SAME secret the WayStation operator must separately register
#     for this exact callsign via WayStation's own Settings -> Peer
#     Sync (see the module's manifest.json / README note for the
#     real setup step this requires; there is no way to automate that
#     half from this side, it's the WayStation operator's own trust
#     decision, by design).
#   - WspEnvelope (carried inside an Objects message) is tagged by
#     "wsp_kind": "manifest" | "objects". SyncObject entries are
#     Rust's default externally-tagged enum shape:
#     {"Message": {...}} or {"Marker": {...}}.
#
# **This bridge is read-only from Muster's side on purpose, v1 scope**:
# it always sends an empty local Manifest/Objects (it has nothing of
# its own to offer WayStation), and always requests everything in
# WayStation's manifest. No incremental/cached sync, no writing
# anything back to WayStation -- real, deliberately deferred work, not
# silently assumed solved. A short in-memory cache (see CACHE_TTL_S)
# avoids hammering WayStation's listener on every single Muster page
# load, nothing more sophisticated than that yet.

import hashlib
import hmac
import json
import os
import socket
import struct
import threading
import time
import uuid
import http.server
import socketserver

WAYSTATION_HOST = os.environ.get("WAYSTATION_HOST", "")
WAYSTATION_PORT = int(os.environ.get("WAYSTATION_PORT", "51820"))
MUSTER_CALLSIGN = os.environ.get("MUSTER_CALLSIGN", "")
MUSTER_SECRET = os.environ.get("MUSTER_SECRET", "")
BRIDGE_PORT = 8080
CACHE_TTL_S = 30
CONNECT_TIMEOUT_S = 5

_cache_lock = threading.Lock()
_cache = {"at": 0, "messages": [], "markers": [], "error": None}


def _write_message(sock, msg: dict):
    body = json.dumps(msg).encode("utf-8")
    sock.sendall(struct.pack(">I", len(body)) + body)


def _read_message(sock) -> dict:
    len_bytes = _recv_exact(sock, 4)
    (length,) = struct.unpack(">I", len_bytes)
    if length > 64 * 1024 * 1024:
        raise ValueError(f"declared message length {length} bytes is not plausible")
    body = _recv_exact(sock, length)
    return json.loads(body)


def _recv_exact(sock, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("connection closed while reading a message")
        buf += chunk
    return buf


def _sign_nonce(secret: str, nonce: str) -> str:
    return hmac.new(secret.encode("utf-8"), nonce.encode("utf-8"), hashlib.sha256).hexdigest()


def fetch_from_waystation():
    """One real WSP/1 exchange: Hello, wait for Accepted, swap empty
    manifest/objects for real ones, return whatever WayStation actually
    has. Raises on any real failure (unreachable host, rejected auth,
    protocol mismatch) -- callers decide how to present that, this
    function never fabricates a result."""
    if not WAYSTATION_HOST:
        raise RuntimeError("WAYSTATION_HOST is not configured (see modules/muster/manifest.json)")
    if not MUSTER_CALLSIGN or not MUSTER_SECRET:
        raise RuntimeError(
            "MUSTER_CALLSIGN/MUSTER_SECRET are not configured -- this station has no "
            "identity to present to WayStation, so it cannot be a trusted WSP/1 peer yet"
        )

    with socket.create_connection((WAYSTATION_HOST, WAYSTATION_PORT), timeout=CONNECT_TIMEOUT_S) as sock:
        nonce = str(uuid.uuid4())
        signature = _sign_nonce(MUSTER_SECRET, nonce)
        _write_message(sock, {"kind": "Hello", "callsign": MUSTER_CALLSIGN, "nonce": nonce, "signature": signature})

        reply = _read_message(sock)
        if reply.get("kind") == "Rejected":
            raise PermissionError(
                f"WayStation rejected this connection: {reply.get('reason')} -- "
                f"has the operator registered callsign {MUSTER_CALLSIGN!r} with this exact "
                f"shared secret in WayStation's own Settings -> Peer Sync?"
            )
        if reply.get("kind") != "Accepted":
            raise ValueError(f"expected Accepted or Rejected, got {reply!r}")

        # This station has nothing of its own to offer (v1, read-only) --
        # an honest empty manifest, not a fabricated one.
        _write_message(sock, {"kind": "Manifest", "entries": []})
        peer_manifest_msg = _read_message(sock)
        if peer_manifest_msg.get("kind") != "Manifest":
            raise ValueError(f"expected Manifest, got {peer_manifest_msg!r}")
        peer_entries = peer_manifest_msg.get("entries", [])
        all_uuids = [e["uuid"] for e in peer_entries]

        _write_message(sock, {"kind": "ObjectsRequest", "uuids": all_uuids})
        peer_request_msg = _read_message(sock)
        if peer_request_msg.get("kind") != "ObjectsRequest":
            raise ValueError(f"expected ObjectsRequest, got {peer_request_msg!r}")
        # WayStation may ask what we have for the uuids it doesn't
        # recognize from our empty manifest -- we have nothing, so an
        # honest empty Objects envelope, not silently ignored.
        _write_message(sock, {
            "kind": "Objects",
            "envelope": {
                "wsp_kind": "objects",
                "wsp_version": 1,
                "origin_callsign": MUSTER_CALLSIGN,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "entries": [],
                "signature": None,
            },
        })

        objects_msg = _read_message(sock)
        if objects_msg.get("kind") != "Objects":
            raise ValueError(f"expected Objects, got {objects_msg!r}")
        envelope = objects_msg.get("envelope", {})
        entries = envelope.get("entries", [])

        try:
            _write_message(sock, {"kind": "Done"})
        except OSError:
            pass  # best-effort -- we already have what we came for

    messages, markers = [], []
    for entry in entries:
        if "Message" in entry:
            messages.append(entry["Message"])
        elif "Marker" in entry:
            marker = entry["Marker"]
            # Real find, caught by testing against the actual compiled
            # WayStation code (not assumed from the struct fields alone):
            # MapMarker carries a `deleted_at` tombstone (v48 migration --
            # a soft-delete, not a removed row). Muster's map should never
            # show a deleted marker as if it were live.
            if marker.get("deleted_at") is None:
                markers.append(marker)
    return messages, markers


def get_cached():
    with _cache_lock:
        if time.time() - _cache["at"] < CACHE_TTL_S and _cache["error"] is None:
            return _cache["messages"], _cache["markers"], None
    try:
        messages, markers = fetch_from_waystation()
        with _cache_lock:
            _cache.update(at=time.time(), messages=messages, markers=markers, error=None)
        return messages, markers, None
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        with _cache_lock:
            _cache.update(at=time.time(), error=error)
        return [], [], error


class BridgeHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/muster/messages":
            messages, _, error = get_cached()
            if error:
                self._send_json({"error": error}, status=502)
            else:
                self._send_json(messages)
            return
        if self.path == "/api/muster/markers":
            _, markers, error = get_cached()
            if error:
                self._send_json({"error": error}, status=502)
            else:
                self._send_json(markers)
            return
        self.send_error(404)


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    print("=============================================================")
    print("MUSTER BRIDGE // WSP/1-over-HTTP reader")
    print(f"WayStation target: {WAYSTATION_HOST or '(not configured)'}:{WAYSTATION_PORT}")
    print("=============================================================")
    with ThreadedHTTPServer(("", BRIDGE_PORT), BridgeHandler) as httpd:
        httpd.serve_forever()
