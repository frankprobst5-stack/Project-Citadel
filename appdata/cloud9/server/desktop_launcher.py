import threading
import time
import webbrowser

from app import app

HOST = "127.0.0.1"
PORT = 5057


def run_server():
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1.5)
    webbrowser.open(f"http://{HOST}:{PORT}")
    server_thread.join()
