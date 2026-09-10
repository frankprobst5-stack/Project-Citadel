import sys
from pathlib import Path

if hasattr(sys, "_MEIPASS"):
    # Packaged (PyInstaller) build: bundled data lives wherever PyInstaller's
    # bootloader unpacked it (the "_internal" folder in onedir builds, or a
    # temp dir in onefile builds) - _MEIPASS is the official way to find it,
    # not a guessed/hardcoded folder name.
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
SERVER_DIR = BASE_DIR / "server"
STATIC_DIR = SERVER_DIR / "static"
