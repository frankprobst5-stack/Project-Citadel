import json
import subprocess
from pathlib import Path

from paths import DATA_DIR

TOOLS_FILE = DATA_DIR / "external_tools.json"


def _load_tools():
    with open(TOOLS_FILE, encoding="utf-8") as f:
        return json.load(f)


def launch(tool_id):
    tools = _load_tools()
    tool = tools.get(tool_id)
    if tool is None:
        return False, f"'{tool_id}' isn't a known tool."

    path = tool.get("path")
    if not path:
        return False, f"{tool['label']} isn't set up yet. Ask a grown-up to install it."

    if not Path(path).exists():
        return False, f"Couldn't find {tool['label']} at the configured location."

    subprocess.Popen([path])
    return True, f"Launching {tool['label']}..."
