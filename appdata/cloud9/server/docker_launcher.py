# Container-specific entry point, added for the Citadel Docker deployment
# (not part of the upstream Cloud9 repo). desktop_launcher.py binds
# 127.0.0.1 and opens a local browser window, both correct for the
# original one-laptop desktop-app use case but wrong here: other devices
# on the LAN need to reach this over the network, and there's no display
# in the container for webbrowser.open() to do anything with.
from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5057, debug=False, use_reloader=False)
