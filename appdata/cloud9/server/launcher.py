import json
import socket

# Real architectural note (2026-09-27): this container has no GUI, no
# access to the host filesystem, and no display -- it genuinely cannot
# launch a native desktop app itself the way this file used to try to
# (subprocess.Popen() here would run *inside* this container, not on the
# real desktop). Bind-mounting the host's X11 socket into this container
# was deliberately rejected instead: that would let anything running in
# this Flask app see and control every window on the host desktop, not
# just its own -- a real security downside, worse on a kids' platform,
# not smaller. Real fix: talk to host-launcher/cloud9-launcher.py, a
# narrowly-scoped daemon running on the real host (same pattern Gated's
# own privileged helper already uses elsewhere in this ecosystem) that
# only ever launches one of the handful of pre-approved tools already
# named in external_tools.json -- this container can select an id, never
# supply an arbitrary path or command.
LAUNCHER_SOCKET = "/run/cloud9-launcher/launcher.sock"


def launch(tool_id):
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            sock.connect(LAUNCHER_SOCKET)
            sock.sendall((tool_id + "\n").encode("utf-8"))
            raw = sock.recv(4096).decode("utf-8", "replace")
        reply = json.loads(raw)
        return reply.get("ok", False), reply.get("message", "No response from the launcher.")
    except FileNotFoundError:
        return False, "The host launcher isn't running -- ask a grown-up to start it."
    except (ConnectionRefusedError, OSError):
        return False, "Couldn't reach the host launcher right now."
