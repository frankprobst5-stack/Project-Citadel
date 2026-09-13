from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os
import json
import requests

from scanner_config import (
    build_conventional_config,
    build_trunk_recorder_config,
    validate_channel_file_csv,
    validate_talkgroups_csv,
)
from transcription import is_safe_filename, list_recordings, transcribe_file

app = Flask(__name__)
app.url_map.strict_slashes = False

DB_PATH = "/app/citadel.db"

# Mealie pantry-check bridge (see /api/pantry-check below) -- server-to-
# server config, never exposed to the browser.
MEALIE_BASE_URL = os.environ.get("MEALIE_BASE_URL", "http://citadel-mealie:9000")
MEALIE_API_TOKEN = os.environ.get("MEALIE_API_TOKEN", "")

def init_db():
    """Automatically creates the database and layout tables on startup."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for Primary Inventory (Food, Fuel, PPE, Orchard, Livestock)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id TEXT PRIMARY KEY,
            category TEXT,
            desc TEXT,
            loc TEXT,
            qty INTEGER,
            exp TEXT
        )
    ''')

    # min_qty (low-stock threshold, real per-item data): added after this
    # table already had real rows in it, so CREATE TABLE IF NOT EXISTS above
    # is a no-op on an existing install -- has to be a real ALTER TABLE, not
    # just a wider CREATE statement, or an already-running Citadel would
    # never actually gain the column. Defaults to 0 ("not tracked") rather
    # than guessing a universal low-stock number: a homestead's quantities
    # span 50lbs-of-rice to 3-tourniquets to 12-chickens, and a single fixed
    # threshold would misfire constantly across that range.
    cursor.execute("PRAGMA table_info(inventory)")
    if "min_qty" not in [row[1] for row in cursor.fetchall()]:
        cursor.execute("ALTER TABLE inventory ADD COLUMN min_qty INTEGER DEFAULT 0")

    # Table for Botanical Garden Year-Over-Year Records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS garden (
            id TEXT PRIMARY KEY,
            year TEXT,
            season TEXT,
            crop TEXT,
            loc TEXT,
            type TEXT,
            var TEXT,
            fert TEXT,
            pest TEXT,
            yield TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize database tables immediately on boot loop
init_db()

# --- CORS MIDDLEWARE BYPASS ---
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
    return response
# --- CORE MEDIA VAULT SCANNING UTILITY ENGINE ---

def scan_media_folder(base_folder):
    """Scans subdirectories to extract categories and individual media files."""
    path = f"/app/{base_folder}"
    categories_data = {}
    
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        
    for entry in os.scandir(path):
        if entry.is_dir():
            sub_folder_name = entry.name
            files_list = [f for f in os.listdir(entry.path) if os.path.isfile(os.path.join(entry.path, f))]
            categories_data[sub_folder_name] = sorted(files_list)
            
    if not categories_data:
        root_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        categories_data["General Archive"] = sorted(root_files)
        
    return categories_data

# --- APP LANDING INTERFACE ROUTING ---

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/videos', methods=['GET'])
def list_videos():
    data = scan_media_folder('videos')
    return render_template('videos.html', categories=data)

@app.route('/mp3', methods=['GET'])
@app.route('/mp3s', methods=['GET'])
def list_mp3s():
    data = scan_media_folder('mp3s')
    return render_template('mp3.html', categories=data)

@app.route('/pdf', methods=['GET'])
@app.route('/pdfs', methods=['GET'])
def list_pdfs():
    data = scan_media_folder('pdfs')
    return render_template('pdf.html', categories=data)

# --- DYNAMIC OFFLINE FILE STREAMING ENDPOINTS ---

def _is_safe_category(category):
    """Rejects path separators/traversal so `category` can't escape its media folder."""
    return category not in ("", ".", "..") and os.sep not in category and "/" not in category

@app.route('/files/mp3/<category>/<filename>', methods=['GET'])
def stream_mp3(category, filename):
    if not _is_safe_category(category):
        return "Invalid category", 400
    safe_path = f"/app/mp3s/{category}"
    return send_from_directory(safe_path, filename)

@app.route('/files/pdfs/<category>/<filename>', methods=['GET'])
def stream_pdf(category, filename):
    if not _is_safe_category(category):
        return "Invalid category", 400
    safe_path = f"/app/pdfs/{category}"
    return send_from_directory(safe_path, filename)

@app.route('/files/videos/<category>/<filename>', methods=['GET'])
def stream_video(category, filename):
    if not _is_safe_category(category):
        return "Invalid category", 400
    safe_path = f"/app/videos/{category}"
    return send_from_directory(safe_path, filename)
# --- INVENTORY API ENDPOINTS ---

@app.route('/api/inventory/<category>', methods=['GET'])
def get_inventory(category):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE category = ? ORDER BY id DESC", (category,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/inventory', methods=['POST'])
def save_inventory_item():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        qty_sanitized = int(data.get('qty', 0))
    except (ValueError, TypeError):
        qty_sanitized = 0

    try:
        min_qty_sanitized = int(data.get('min_qty', 0))
    except (ValueError, TypeError):
        min_qty_sanitized = 0

    cursor.execute('''
        INSERT OR REPLACE INTO inventory (id, category, desc, loc, qty, exp, min_qty)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (str(data['id']), data['category'], data['desc'], data['loc'], qty_sanitized, data['exp'], min_qty_sanitized))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/inventory/<item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# --- BOTANICAL GARDEN API ENDPOINTS ---

@app.route('/api/garden/<year>/<season>', methods=['GET'])
def get_garden(year, season):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM garden WHERE year = ? AND season = ? ORDER BY id DESC", (year, season))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/garden', methods=['POST'])
def save_garden_item():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO garden (id, year, season, crop, loc, type, var, fert, pest, yield)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (str(data['id']), data['year'], data['season'], data['crop'], data['loc'], data['type'], data['var'], data['fert'], data['pest'], data['yield']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/api/garden/<item_id>', methods=['DELETE'])
def delete_garden_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM garden WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

# --- MEALIE PANTRY-CHECK BRIDGE ---
# The one piece of the Mealie recipe integration that's genuinely
# Citadel-specific: no recipe app knows about this homestead's own Food
# Inventory / Freezer Foods ledgers (the `inventory` table's `food` and
# `freezer` categories, same table logistics.html already reads/writes
# via /api/inventory above). This calls Mealie's own REST API server-to-
# server over citadel-net -- never from the browser -- since it needs
# Mealie's API token, which must stay off the client.
#
# Matching a recipe's structured ingredient food name against a ledger
# row's freeform `desc` text is necessarily a best-effort, case-
# insensitive substring match in both directions: both sides are typed
# independently by a person ("chicken breast" in Mealie vs. "Chicken
# Breasts - Freezer 2" in the ledger), so there's no shared ID to join
# on.
@app.route('/api/pantry-check', methods=['GET'])
def pantry_check():
    if not MEALIE_API_TOKEN:
        return jsonify({
            "status": "error",
            "detail": "MEALIE_API_TOKEN not configured -- generate one in Mealie's User Settings > API Tokens and set it in .env, then restart vault-api.",
        }), 400

    query = request.args.get("q", "").strip()
    slug = request.args.get("slug", "").strip()
    if not query and not slug:
        return jsonify({"status": "error", "detail": "pass ?q=<search text> or ?slug=<recipe slug>"}), 400

    headers = {"Authorization": f"Bearer {MEALIE_API_TOKEN}"}
    try:
        if not slug:
            search_res = requests.get(
                f"{MEALIE_BASE_URL}/api/recipes",
                params={"search": query, "perPage": 1},
                headers=headers,
                timeout=10,
            )
            search_res.raise_for_status()
            items = search_res.json().get("items", [])
            if not items:
                return jsonify({"status": "error", "detail": f"no recipe found matching {query!r}"}), 404
            slug = items[0]["slug"]

        recipe_res = requests.get(f"{MEALIE_BASE_URL}/api/recipes/{slug}", headers=headers, timeout=10)
        recipe_res.raise_for_status()
        recipe = recipe_res.json()
    except requests.RequestException as e:
        return jsonify({"status": "error", "detail": f"Mealie unreachable or failed: {e}"}), 502

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory WHERE category IN ('food', 'freezer')")
    pantry_rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    results = []
    for ing in recipe.get("recipeIngredient", []):
        food = ing.get("food") or {}
        food_name = (food.get("name") or "").strip()
        # Mealie's own `display` collapses to just the bare quantity when
        # `food` didn't parse (e.g. "1" instead of "1 bag Egg Noodles") --
        # originalText/note still hold the real freeform line in that case,
        # so prefer those over `display` when there's no structured food.
        if food_name:
            display = ing.get("display") or ing.get("originalText") or food_name
        else:
            display = ing.get("originalText") or ing.get("note") or ing.get("display") or "(unparsed ingredient)"
        if not food_name:
            results.append({"ingredient": display, "matched": False, "pantry_matches": []})
            continue
        needle = food_name.lower()
        matches = [
            row for row in pantry_rows
            if needle in (row.get("desc") or "").lower() or (row.get("desc") or "").lower() in needle
        ]
        results.append({
            "ingredient": display,
            "food_name": food_name,
            "matched": len(matches) > 0,
            "pantry_matches": [
                {"desc": m["desc"], "loc": m["loc"], "qty": m["qty"], "category": m["category"]}
                for m in matches
            ],
        })

    return jsonify({
        "status": "success",
        "recipe": {"name": recipe.get("name"), "slug": recipe.get("slug")},
        "ingredients": results,
        "missing_count": sum(1 for r in results if not r["matched"]),
    })

# --- PROJECT IBRIS LIVE SIGNAL DATA RELAY ROUTE ---
@app.route('/api/radar', methods=['GET'])
def get_live_radar_matrix():
    """Reads the output of the radar daemon script and serves it to the front-end sweep screen."""
    # POINTS DIRECTLY TO THE SHARED VOLUME PATHWAY MATRIX LANE
    json_path = "/app/project-ibris/radar_state.json"

    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({"timestamp": "SYNC_ERROR", "total_nodes": 0, "targets": []})

# --- TRUNKED RADIO SCANNER LIVE STATE RELAY ROUTE ---
@app.route('/api/scanner', methods=['GET'])
def get_scanner_state():
    """Reads whatever scanner_bridge.py (see that file, 2026-09-06) has
    written to the shared state file and serves it as-is. Same daemon-
    writes-JSON/API-reads-JSON shape as /api/radar above -- no daemon has
    ever connected in this environment (this sandbox can't run
    trunk-recorder at all, it needs real USB device passthrough for an
    RTL-SDR), so an honest "no_data" default comes back instead of a
    fabricated "listening" claim until one actually does. The default's
    shape matches scanner_bridge.py's ScannerState.to_json() exactly
    (systems/active_calls/recorders/decode_rates all real-empty, not
    just status/detail/transcripts as before 2026-09-06) so WayStation's
    UI never needs a schema-version check to know nothing's connected
    yet. WayStation (the comms app this cockpit launches) is the
    intended consumer, same pattern as the map-tiles integration -- there
    is no Citadel-side comms UI anymore, see ROADMAP.md."""
    json_path = "/app/scanner/scanner_state.json"
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({
        "status": "no_data",
        "updated_at": None,
        "detail": "No scanner decode daemon configured yet -- requires an RTL-SDR (or similar) dongle and a trunk-recorder/op25 config for your local trunked system.",
        "systems": [],
        "active_calls": [],
        "recorders": [],
        "decode_rates": [],
        "transcripts": [],
    })

SCANNER_DIR = "/app/scanner"
SCANNER_CONFIG_PATH = f"{SCANNER_DIR}/config.json"
SCANNER_TALKGROUPS_PATH = f"{SCANNER_DIR}/talkgroups.csv"
SCANNER_CHANNELS_PATH = f"{SCANNER_DIR}/channels.csv"

@app.route('/api/scanner/config', methods=['GET'])
def get_scanner_config():
    """Lets the setup UI (WayStation, not a page in this repo -- see
    ROADMAP.md) pre-populate the form with whatever's already configured,
    rather than being a write-only black box. Which CSV to read back is
    determined by the saved config's own system type, not guessed --
    trunked systems reference talkgroupsFile, conventional/conventionalP25
    reference channelFile (added 2026-09-06 for real conventional
    Sheriff/Fire/EMS setups)."""
    if not os.path.exists(SCANNER_CONFIG_PATH):
        return jsonify({"configured": False})
    with open(SCANNER_CONFIG_PATH, 'r') as f:
        config = json.load(f)
    csv_path = SCANNER_TALKGROUPS_PATH
    system = (config.get("systems") or [{}])[0]
    if "channelFile" in system:
        csv_path = SCANNER_CHANNELS_PATH
    csv_data = ""
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            csv_data = f.read()
    return jsonify({"configured": True, "config": config, "csv_data": csv_data})

@app.route('/api/scanner/config', methods=['POST'])
def save_scanner_config():
    """Turns operator-supplied setup into real trunk-recorder files. Both
    files are validated in full before either is written -- a partially
    written config (valid JSON, missing/corrupt CSV, or vice versa) is
    worse than refusing the write outright and saying why.

    `system_type` picks the real trunk-recorder system shape: "trunked"
    (control-channel-following, the original and only supported shape
    before 2026-09-06) or "conventional"/"conventionalP25" (fixed-frequency
    channels, added when a real operator brought real conventional
    Sheriff/Fire/EMS frequencies -- PANCOM, Donley County -- the trunked-
    only builder couldn't express. Whichever CSV file the chosen type
    doesn't use is left untouched from any previous config, not deleted --
    switching system_type and back shouldn't lose data."""
    data = request.json or {}
    csv_data = data.get("csv_data", "")
    system_type = data.get("system_type", "trunked")

    os.makedirs(SCANNER_DIR, exist_ok=True)

    if system_type == "trunked":
        valid, error = validate_talkgroups_csv(csv_data)
        if not valid:
            return jsonify({"status": "error", "detail": error}), 400
        try:
            config = build_trunk_recorder_config(
                short_name=data.get("short_name", ""),
                driver=data.get("driver", "osmosdr"),
                device=data.get("device"),
                center_hz=float(data.get("center_hz", 0)),
                rate_hz=float(data.get("rate_hz", 0)),
                gain=float(data.get("gain", 40)),
                control_channels_hz=data.get("control_channels_hz", []),
                ppm=data.get("ppm"),
            )
        except (ValueError, TypeError) as e:
            return jsonify({"status": "error", "detail": str(e)}), 400
        with open(SCANNER_TALKGROUPS_PATH, 'w') as f:
            f.write(csv_data)
    elif system_type in ("conventional", "conventionalP25"):
        valid, error = validate_channel_file_csv(csv_data)
        if not valid:
            return jsonify({"status": "error", "detail": error}), 400
        try:
            config = build_conventional_config(
                short_name=data.get("short_name", ""),
                system_type=system_type,
                driver=data.get("driver", "osmosdr"),
                device=data.get("device"),
                center_hz=float(data.get("center_hz", 0)),
                rate_hz=float(data.get("rate_hz", 0)),
                gain=float(data.get("gain", 40)),
                squelch=float(data.get("squelch", -50)),
                ppm=data.get("ppm"),
            )
        except (ValueError, TypeError) as e:
            return jsonify({"status": "error", "detail": str(e)}), 400
        with open(SCANNER_CHANNELS_PATH, 'w') as f:
            f.write(csv_data)
    else:
        return jsonify({"status": "error", "detail": f"Unknown system_type {system_type!r} -- must be 'trunked', 'conventional', or 'conventionalP25'."}), 400

    with open(SCANNER_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

    return jsonify({"status": "success", "config": config})

SCANNER_CALLS_DIR = f"{SCANNER_DIR}/calls"

@app.route('/api/scanner/recordings', methods=['GET'])
def get_scanner_recordings():
    """Real files trunk-recorder's own captureDir (scanner_config.py's
    "captureDir": "/app/calls", which lands here since vault-api and
    scanner share the same appdata/media-vault mount) actually has on
    disk. Honestly empty -- not an error -- until a real dongle and a
    running trunk-recorder have actually captured something; this
    sandbox has neither, so real usage never populates this without
    real hardware."""
    return jsonify(list_recordings(SCANNER_CALLS_DIR))

@app.route('/api/scanner/transcribe', methods=['POST'])
def transcribe_scanner_recording():
    """Transcribes one already-captured recording via the real
    whisper-server service (transcription.py), decided 2026-09-07 --
    verified live against the real running whisper container before
    this route existed. Takes a bare filename, not a path, and refuses
    anything containing a path separator -- this joins operator/caller-
    supplied input directly onto a real directory path, so path
    traversal (`../../etc/passwd`) has to be rejected outright rather
    than trusted."""
    data = request.json or {}
    filename = data.get("filename", "")
    if not is_safe_filename(filename):
        return jsonify({"status": "error", "detail": "invalid filename"}), 400

    file_path = os.path.join(SCANNER_CALLS_DIR, filename)
    try:
        text = transcribe_file(file_path)
    except FileNotFoundError:
        return jsonify({"status": "error", "detail": f"no such recording: {filename}"}), 404
    except requests.RequestException as e:
        return jsonify({"status": "error", "detail": f"whisper service unreachable or failed: {e}"}), 502

    return jsonify({"status": "success", "text": text})

# --- LOCAL WEATHER CAPTURE LIVE STATE RELAY ROUTE ---
@app.route('/api/weather', methods=['GET'])
def get_weather_state():
    """Same shape as /api/scanner and /api/radar: reads whatever a real local
    weather-capture daemon (a weather-station console poller, or a NOAA SAME
    weather-radio decoder) has written to the shared state file. Honest
    "no_data" default until one exists -- NWS's online alerts already cover
    this station's primary weather picture (see WayStation's nws.rs); this
    is specifically the offline/local-capture fallback. WayStation is the
    intended consumer, not a Citadel-side page -- see ROADMAP.md."""
    json_path = "/app/weather/weather_state.json"
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({
        "status": "no_data",
        "updated_at": None,
        "detail": "No local weather capture configured yet -- point this at a weather-station console API or a NOAA SAME weather-radio decoder.",
        "observation": None,
        "same_alerts": [],
    })

# --- MEDIA UPLOAD (PDF / VIDEO REFERENCE LIBRARY) ---

UPLOAD_KINDS = {
    'pdfs': {'exts': {'.pdf'}},
    'videos': {'exts': {'.mp4', '.mkv', '.webm', '.mov', '.avi'}},
}

@app.route('/api/media/<kind>', methods=['GET'])
def list_media(kind):
    """JSON version of the category->files listing /pdf and /videos already
    render as HTML, so a page like medical.html can show what's uploaded
    without scraping the human-facing pages."""
    if kind not in UPLOAD_KINDS:
        return jsonify({"error": "unknown kind"}), 404
    return jsonify(scan_media_folder(kind))

@app.route('/api/media/<kind>/<category>', methods=['POST'])
def upload_media(kind, category):
    if kind not in UPLOAD_KINDS:
        return jsonify({"error": "unknown kind"}), 404
    if not _is_safe_category(category):
        return jsonify({"error": "invalid category"}), 400
    if 'file' not in request.files:
        return jsonify({"error": "no file in request"}), 400

    upload = request.files['file']
    filename = upload.filename or ""
    if not is_safe_filename(filename):
        return jsonify({"error": "invalid filename"}), 400

    ext = os.path.splitext(filename)[1].lower()
    if ext not in UPLOAD_KINDS[kind]['exts']:
        return jsonify({"error": f"extension {ext} not allowed for {kind}"}), 400

    dest_dir = f"/app/{kind}/{category}"
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)
    upload.save(dest_path)
    return jsonify({"status": "success", "kind": kind, "category": category, "filename": filename})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

