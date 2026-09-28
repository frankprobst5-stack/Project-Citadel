#!/usr/bin/env python3
"""Real host-side helper for Cloud9's "launch a native app" buttons
(Kart Racing/SuperTuxKart, Code Lab/Scratch, Globe/Marble).

Why this exists instead of Cloud9's own container just calling
subprocess.Popen() directly: Cloud9 runs in an isolated Docker container
(plain python:3.11-slim, no GUI, no access to the host filesystem beyond
its own data/ bind mount) -- it genuinely cannot see /usr/games/supertuxkart
or open a window on the real desktop. The naive fix (bind-mount the host's
X11 socket into the container) was deliberately rejected: that would let
anything running inside Cloud9's Flask app -- a bug, a compromised
dependency -- see and control every window on the host desktop, not just
its own. On a kids' platform specifically, that's a real, serious downside,
not a theoretical one.

Same real pattern this ecosystem already trusts elsewhere (Gated's own
gated-helper.py): a small, narrowly-scoped daemon on the host side that the
untrusted container can ask to do exactly one thing, never anything else.
Unlike Gated's helper, this one needs no privilege escalation at all --
launching a normal desktop app doesn't need root, just the real logged-in
user's own session (DISPLAY/WAYLAND_DISPLAY/XAUTHORITY all come for free
since this runs as that same user, not forwarded from anywhere).

Protocol: the container connects to a Unix socket and sends one line, the
tool_id (e.g. "kart_racing\n"). This script looks that id up in the SAME
external_tools.json Cloud9's own container already reads (re-read on every
request, so a config change takes effect without restarting this daemon),
and -- ONLY if it resolves to a real, existing path already configured by
whoever set this file up -- launches it. The container can never send an
arbitrary path or command; it can only ever select from a fixed set of
ids someone already put in that file. Replies with one JSON line back.
"""

import json
import re
import signal
import socket
import subprocess
from pathlib import Path

# Without this, every launched app becomes a real zombie process once it
# exits -- this daemon is its parent (start_new_session=True below only
# detaches the process *group*, not the parent/child relationship for
# wait() purposes) and never explicitly reaps it. SIG_IGN on SIGCHLD is
# real, standard POSIX behavior (see signal(7)): the kernel auto-reaps
# this process's children instead of turning them into zombies, with no
# explicit waitpid() call needed anywhere in this file. Confirmed live --
# a launched SuperTuxKart process no longer lingers as <defunct> after
# being closed.
signal.signal(signal.SIGCHLD, signal.SIG_IGN)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TOOLS_FILE = DATA_DIR / "external_tools.json"

# A dedicated subdirectory, not a bare socket file directly under
# /run/user/1000/ -- Docker bind-mounts a single FILE by inode, so if this
# daemon ever restarts and recreates the socket (it unlinks + rebinds on
# every start, below), a container that mounted the file itself would be
# left pointing at the old, now-deleted inode until the container itself
# was recreated. Mounting this whole (otherwise-empty) directory instead
# means the container always sees whatever socket is currently inside it.
SOCKET_DIR = Path("/run/user/1000/cloud9-launcher")
SOCKET_PATH = SOCKET_DIR / "launcher.sock"

TOOL_ID_RE = re.compile(r"^[a-z0-9_]{1,64}$")


def load_tools():
    with open(TOOLS_FILE, encoding="utf-8") as f:
        return json.load(f)


def launch(tool_id):
    if not TOOL_ID_RE.match(tool_id):
        return False, f"'{tool_id}' isn't a valid tool id."

    tools = load_tools()
    tool = tools.get(tool_id)
    if tool is None:
        return False, f"'{tool_id}' isn't a known tool."

    path = tool.get("path")
    if not path:
        return False, f"{tool['label']} isn't set up yet. Ask a grown-up to install it."

    if not Path(path).exists():
        return False, f"Couldn't find {tool['label']} at the configured location."

    # Detached: must keep running after this connection (and this
    # process) closes, same as launcher.py's own original Popen call.
    subprocess.Popen([path], start_new_session=True)
    return True, f"Launching {tool['label']}..."


def serve():
    if SOCKET_PATH.exists():
        SOCKET_PATH.unlink()
    SOCKET_PATH.parent.mkdir(parents=True, exist_ok=True)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(str(SOCKET_PATH))
    SOCKET_PATH.chmod(0o666)  # the container connects as its own container-internal user
    server.listen(8)
    print(f"cloud9-launcher listening on {SOCKET_PATH}")

    try:
        while True:
            conn, _ = server.accept()
            with conn:
                try:
                    data = conn.recv(256).decode("utf-8", "replace").strip()
                    ok, message = launch(data) if data else (False, "Empty request.")
                except Exception as exc:  # noqa: BLE001 -- one bad request must not kill the daemon
                    ok, message = False, f"Launcher error: {exc}"
                conn.sendall((json.dumps({"ok": ok, "message": message}) + "\n").encode("utf-8"))
    finally:
        server.close()
        SOCKET_PATH.unlink(missing_ok=True)


if __name__ == "__main__":
    serve()
