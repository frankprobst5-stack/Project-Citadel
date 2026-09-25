from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os
import json
import hmac
import requests
import threading

from scanner_config import (
    build_config,
    build_conventional_config,
    build_trunk_recorder_config,
    make_profile,
    validate_channel_file_csv,
    validate_talkgroups_csv,
)
from transcription import is_safe_filename, list_recordings, transcribe_file
import backup as backup_module
import modules_manager
import uuid
from datetime import datetime, timezone, timedelta
import news_feed_parser
import news_hazard_adapters
import news_nws_alerts
import news_location
import news_matcher

app = Flask(__name__)
app.url_map.strict_slashes = False

DB_PATH = "/app/citadel.db"

# Real fix for a live-reported vulnerability (2026-09-21, a real
# tester's own audit, verified directly against this file before fixing
# it): every route here had zero authentication, and this container has
# the host's own docker.sock mounted (see docker-compose.yml's own
# comment on that mount) -- an unauthenticated request to
# /api/modules/install can get root-equivalent control of the host, not
# hypothetically: the zip-install path validates path-safety inside the
# archive but never validates the *content* of the compose fragment it
# installs, and a service block with no `profiles:` key starts
# immediately and unconditionally on the next `docker compose up`.
#
# VAULT_API_TOKEN is generated once at install time (install.sh/
# install.bat), never a guessed or predictable default -- an empty
# token here means installs haven't been through the fixed installer
# yet, and every request is honestly rejected rather than silently
# trusting nothing, which would defeat the point.
#
# hmac.compare_digest, not `==`, for the same reason every other secret
# comparison in this codebase uses it (see db::verify_hmac equivalents
# elsewhere in this ecosystem) -- a timing side-channel on a home LAN is
# a real if minor risk, and the fix costs nothing.
VAULT_API_TOKEN = os.environ.get("VAULT_API_TOKEN", "")


@app.before_request
def _require_vault_token():
    # Real bug found live (2026-09-23, Frank's own report plus a
    # tester's): this ran unconditionally on every request, including
    # plain page loads (`/`, `/videos`, `/mp3`, `/pdf`) and file
    # streaming (`/files/...`) -- a normal browser navigation can never
    # attach a custom header, so the Digital Media Vault's own pages
    # 401'd immediately on load. The original tester's own threat model
    # (see the comment above) was always specifically about the *API* --
    # "/api/modules/install" and friends -- and the tester explicitly
    # said the dashboard/pages being open on the LAN was fine. Scoping
    # this to /api/ restores that original, agreed threat model instead
    # of accidentally locking out the whole vault UI.
    if request.method == "OPTIONS" or not request.path.startswith("/api/"):
        return None
    provided = request.headers.get("X-Vault-Token", "")
    if not VAULT_API_TOKEN or not hmac.compare_digest(provided, VAULT_API_TOKEN):
        return jsonify({"error": "Missing or invalid X-Vault-Token header."}), 401

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

    # News Archive & Local Log (ROADMAP.md DISCOVERY item, real build
    # 2026-09-16) -- schema translated from Masthead's own real, proven
    # MySQL design (github.com/frankprobst5-stack/masthead, private,
    # archived-but-reusable) into SQLite + this file's own conventions
    # (TEXT PRIMARY KEY, matching inventory/garden above), not invented
    # fresh. Summary-only by design -- this is a "last known state of the
    # world" reference/archive, not a full-article reading app the way
    # Masthead's own `body MEDIUMTEXT` column is, so rows stay small
    # (see news_feed_parser.py: `body` holds a feed's own summary, never
    # a scraped full article).
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_sources (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            feed_url TEXT NOT NULL UNIQUE,
            is_active INTEGER NOT NULL DEFAULT 1,
            fetch_interval_minutes INTEGER NOT NULL DEFAULT 720,
            last_fetched_at TEXT,
            next_due_at TEXT,
            last_error TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_articles (
            id TEXT PRIMARY KEY,
            source_id TEXT NOT NULL,
            dedupe_key TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            body TEXT,
            image_url TEXT,
            published_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            cap_event TEXT,
            cap_severity TEXT,
            cap_urgency TEXT,
            cap_certainty TEXT,
            cap_area_desc TEXT,
            cap_expires_at TEXT,
            cap_geocodes TEXT,
            latitude REAL,
            longitude REAL,
            UNIQUE(source_id, dedupe_key)
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_articles_published ON news_articles (published_at)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_news_articles_cap ON news_articles (cap_event, cap_expires_at)')

    # The manual "Local News Log" half -- hand-typed local reports for
    # exactly the window when no new syndicated news can arrive at all.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS local_log_entries (
            id TEXT PRIMARY KEY,
            entry_text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    # Small key/value store -- today only holds the cached NWS zone/county
    # codes (news_location.py), but a generic shape rather than a
    # single-purpose table since this is exactly the kind of "one more
    # small setting" need that comes up again.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
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
    Sheriff/Fire/EMS frequencies (a real county's PANCOM system) the
    trunked-only builder couldn't express. Whichever CSV file the chosen type
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

    # A direct write here is a manual, one-off config -- not tied to any
    # saved profile, so nothing should still claim to be "active" below.
    _set_active_profile_id(None)

    return jsonify({"status": "success", "config": config})

SCANNER_PROFILES_PATH = f"{SCANNER_DIR}/profiles.json"


def _load_profiles_store():
    """Saved scanner profiles, kept entirely separate from
    SCANNER_CONFIG_PATH/the two CSV files above -- those are the single
    live files trunk-recorder actually reads; this file is just storage
    until a profile is activated (see below)."""
    if not os.path.exists(SCANNER_PROFILES_PATH):
        return {"profiles": [], "active_profile_id": None}
    with open(SCANNER_PROFILES_PATH, 'r') as f:
        return json.load(f)


def _save_profiles_store(store):
    os.makedirs(SCANNER_DIR, exist_ok=True)
    with open(SCANNER_PROFILES_PATH, 'w') as f:
        json.dump(store, f, indent=2)


def _set_active_profile_id(profile_id):
    store = _load_profiles_store()
    if store.get("active_profile_id") == profile_id:
        return
    store["active_profile_id"] = profile_id
    _save_profiles_store(store)


@app.route('/api/scanner/profiles', methods=['GET'])
def list_scanner_profiles():
    """Saved scanner setups an operator can flip between without re-filling
    the whole setup form each time -- the real "like a Uniden BearCat"
    request from a storm-chaser field tester (2026-09-16, WayStation's own
    ROADMAP.md), deliberately not built during the field-test freeze and
    picked up now that it's lifted. `active_profile_id` tells the UI which
    saved profile (if any) matches what's actually live right now -- null
    means the live config was set directly (POST /api/scanner/config) or
    nothing's configured yet, not that something is broken."""
    return jsonify(_load_profiles_store())


@app.route('/api/scanner/profiles', methods=['POST'])
def save_scanner_profile():
    """Validates and stores a new named profile. Deliberately does NOT
    touch the live active config/CSV -- saving a profile is just storage,
    exactly like filling out the setup form without submitting it;
    activating one (see below) is the separate, explicit action that
    actually makes it live."""
    data = request.json or {}
    store = _load_profiles_store()
    existing_ids = {p["id"] for p in store["profiles"]}
    try:
        profile = make_profile(
            name=data.get("name", ""),
            system_type=data.get("system_type", "trunked"),
            short_name=data.get("short_name", ""),
            driver=data.get("driver", "osmosdr"),
            device=data.get("device"),
            center_hz=float(data.get("center_hz", 0)),
            rate_hz=float(data.get("rate_hz", 0)),
            gain=float(data.get("gain", 40)),
            csv_data=data.get("csv_data", ""),
            control_channels_hz=data.get("control_channels_hz", []),
            squelch=float(data.get("squelch", -50)),
            ppm=data.get("ppm"),
            existing_ids=existing_ids,
        )
    except (ValueError, TypeError) as e:
        return jsonify({"status": "error", "detail": str(e)}), 400

    store["profiles"].append(profile)
    _save_profiles_store(store)
    return jsonify({"status": "success", "profile": profile})


@app.route('/api/scanner/profiles/<profile_id>', methods=['DELETE'])
def delete_scanner_profile(profile_id):
    """Removes a saved profile. The live config/CSV trunk-recorder actually
    reads are left untouched even if this was the active profile --
    deleting the saved copy doesn't un-configure a scanner that's actually
    running, it just means that setup can't be re-activated by name later."""
    store = _load_profiles_store()
    remaining = [p for p in store["profiles"] if p["id"] != profile_id]
    if len(remaining) == len(store["profiles"]):
        return jsonify({"status": "error", "detail": f"No profile with id {profile_id!r}."}), 404
    store["profiles"] = remaining
    if store.get("active_profile_id") == profile_id:
        store["active_profile_id"] = None
    _save_profiles_store(store)
    return jsonify({"status": "success"})


@app.route('/api/scanner/profiles/<profile_id>/activate', methods=['POST'])
def activate_scanner_profile(profile_id):
    """Makes a saved profile the live config -- the one-tap "switch
    systems" action the field request actually asked for, instead of
    re-filling the whole setup form each time. Rebuilds the config fresh
    from the profile's own stored fields (via the same build_config
    dispatcher save_scanner_config uses) rather than replaying a config
    dict saved at profile-creation time, so a later change to e.g.
    STATUS_SERVER_URL applies to every profile the next time it's picked,
    not just ones saved after that change."""
    store = _load_profiles_store()
    profile = next((p for p in store["profiles"] if p["id"] == profile_id), None)
    if profile is None:
        return jsonify({"status": "error", "detail": f"No profile with id {profile_id!r}."}), 404

    system_type = profile["system_type"]
    try:
        config = build_config(
            short_name=profile["short_name"],
            system_type=system_type,
            driver=profile["driver"],
            device=profile.get("device"),
            center_hz=profile["center_hz"],
            rate_hz=profile["rate_hz"],
            gain=profile["gain"],
            control_channels_hz=profile.get("control_channels_hz"),
            squelch=profile.get("squelch", -50),
            ppm=profile.get("ppm"),
        )
    except (ValueError, TypeError) as e:
        return jsonify({"status": "error", "detail": str(e)}), 400

    os.makedirs(SCANNER_DIR, exist_ok=True)
    csv_path = SCANNER_CHANNELS_PATH if system_type in ("conventional", "conventionalP25") else SCANNER_TALKGROUPS_PATH
    with open(csv_path, 'w') as f:
        f.write(profile["csv_data"])
    with open(SCANNER_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

    store["active_profile_id"] = profile_id
    _save_profiles_store(store)
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

# --- BACKUP / RESTORE ---
# Real logic lives in backup.py (independently unit-tested, including a
# genuine path-traversal/"zip-slip" rejection test, and a regression
# test for the real mount-overlap data-loss bug found live 2026-09-13 --
# see that file's module docstring for the full story) -- these routes
# are thin wrappers. Mounted at container ROOT paths (docker-compose.yml
# has the full reasoning), deliberately NOT nested under /app, since
# /app is itself a bind mount of this exact appdata/media-vault
# directory.
CITADEL_APPDATA_ROOT = "/citadel-appdata"
CITADEL_ENV_PATH = "/citadel-appdata-env"
BACKUP_DIR = "/citadel-backups"
RESTORE_STAGING_DIR = "/citadel-restore-staging"

# citadel.db and notes-data are the only real user data actually inside
# appdata/media-vault (everything else there is source code, or the
# already-excluded video/audio/PDF library) -- addressed here through
# vault-api's OWN existing /app mount (safe: a single file replace and a
# single purpose-built directory replace, neither of which is the
# process's own working directory), never through CITADEL_APPDATA_ROOT's
# generic walk. See backup.py's module docstring for why that distinction
# is load-bearing, not stylistic.
BACKUP_EXTRA_PATHS = {
    "appdata/media-vault/citadel.db": "/app/citadel.db",
    "appdata/media-vault/notes-data": "/app/notes-data",
}


@app.route('/api/backup/create', methods=['POST'])
def api_create_backup():
    filename, _, size = backup_module.create_backup(
        CITADEL_APPDATA_ROOT, CITADEL_ENV_PATH, BACKUP_DIR, extra_paths=BACKUP_EXTRA_PATHS,
    )
    return jsonify({"status": "success", "filename": filename, "size_bytes": size})


@app.route('/api/backup/list', methods=['GET'])
def api_list_backups():
    return jsonify(backup_module.list_backups(BACKUP_DIR))


@app.route('/api/backup/download/<filename>', methods=['GET'])
def api_download_backup(filename):
    if not is_safe_filename(filename) or not filename.endswith(".tar.gz"):
        return jsonify({"error": "invalid filename"}), 400
    return send_from_directory(BACKUP_DIR, filename, as_attachment=True)


@app.route('/api/backup/delete/<filename>', methods=['DELETE'])
def api_delete_backup(filename):
    if not is_safe_filename(filename) or not filename.endswith(".tar.gz"):
        return jsonify({"error": "invalid filename"}), 400
    full_path = os.path.join(BACKUP_DIR, filename)
    if os.path.exists(full_path):
        os.remove(full_path)
    return jsonify({"status": "success"})


@app.route('/api/backup/restore', methods=['POST'])
def api_restore_backup():
    """Restores from either an uploaded .tar.gz (multipart field
    "file") or an existing on-server backup (form field "filename").
    Always creates a fresh safety-snapshot backup of the CURRENT state
    first -- a restore should never be a one-way door. Rejects (400,
    without touching anything) any archive backup_module.restore_backup
    flags as containing a path-traversal entry."""
    try:
        backup_module.create_backup(CITADEL_APPDATA_ROOT, CITADEL_ENV_PATH, BACKUP_DIR,
                                     extra_paths=BACKUP_EXTRA_PATHS, timestamp=None)
    except Exception as e:
        return jsonify({"status": "error", "detail": f"safety snapshot failed, aborting restore: {e}"}), 500

    cleanup_path = None
    if 'file' in request.files:
        upload = request.files['file']
        filename = upload.filename or ""
        if not is_safe_filename(filename) or not filename.endswith('.tar.gz'):
            return jsonify({"status": "error", "detail": "invalid backup file"}), 400
        archive_path = os.path.join(BACKUP_DIR, f"_restore_upload_{filename}")
        upload.save(archive_path)
        cleanup_path = archive_path
    else:
        filename = request.form.get('filename', '')
        if not is_safe_filename(filename) or not filename.endswith('.tar.gz'):
            return jsonify({"status": "error", "detail": "invalid filename"}), 400
        archive_path = os.path.join(BACKUP_DIR, filename)
        if not os.path.exists(archive_path):
            return jsonify({"status": "error", "detail": "backup not found"}), 404

    try:
        backup_module.restore_backup(archive_path, CITADEL_APPDATA_ROOT, CITADEL_ENV_PATH, RESTORE_STAGING_DIR,
                                      extra_paths=BACKUP_EXTRA_PATHS, chown_to=(1000, 1000))
        return jsonify({
            "status": "success",
            "detail": "Restored. A safety snapshot of the pre-restore state was taken first. "
                      "IMPORTANT: run 'docker compose restart' (no service name -- the whole fleet) now. "
                      "Found live: a restored directory can leave OTHER containers that also mount it "
                      "(e.g. cockpit) showing a stale/empty view until they're restarted too -- the data "
                      "itself is fine either way, but the dashboard can appear broken until you do this.",
        })
    except backup_module.UnsafeArchiveError as e:
        return jsonify({"status": "error", "detail": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500
    finally:
        if cleanup_path and os.path.exists(cleanup_path):
            os.remove(cleanup_path)


# Module system (Settings > Modules), added 2026-09-14 -- see
# modules_manager.py's own module docstring for the real design and the
# Docker-outside-of-Docker mechanics apply_compose() depends on.
CITADEL_MODULES_ROOT = "/citadel-modules-rw"
CITADEL_COMPOSE_PATH = "/citadel-compose-file"
CITADEL_HOST_PATH = os.environ.get("CITADEL_HOST_PATH", "")


@app.route('/api/modules', methods=['GET'])
def api_list_modules():
    return jsonify(modules_manager.list_modules(CITADEL_MODULES_ROOT, CITADEL_ENV_PATH))


@app.route('/api/modules/apply', methods=['POST'])
def api_apply_modules():
    """Body: {"profiles": ["vigil", "ai", ...]} -- the full list of
    profiles that should be enabled after this call (not a delta), so
    the caller (Settings' own checkbox list) always sends its complete
    current selection. Writes .env synchronously (fast, safe), then
    kicks off the real `docker compose up -d` in a background thread and
    returns immediately -- found live 2026-09-14 that running it
    synchronously doesn't work: ANY profile change also recreates
    cockpit (it reads COMPOSE_PROFILES at its own startup), and cockpit
    is the reverse proxy this very request came through, so the HTTP
    response gets severed by cockpit's own restart before the browser
    ever sees it -- confirmed live (curl got a bare connection reset,
    even though the apply had fully succeeded). Returning right after
    the .env write sidesteps that entirely: the browser gets a real,
    deliverable response, and the Settings UI just needs to expect a
    brief cockpit blip and re-poll GET /api/modules a few seconds later
    to confirm the new state actually took. A background failure has no
    request left to report to -- logged to stdout (`docker logs
    citadel-vault-brain`) instead of swallowed."""
    data = request.get_json(silent=True) or {}
    profiles = data.get("profiles")
    if not isinstance(profiles, list) or not all(isinstance(p, str) for p in profiles):
        return jsonify({"status": "error", "detail": "expected {\"profiles\": [list of strings]}"}), 400

    new_profiles = set(profiles)
    old_profiles = modules_manager.get_enabled_profiles(CITADEL_ENV_PATH)
    disabled_profiles = old_profiles - new_profiles
    modules_manager.set_enabled_profiles(CITADEL_ENV_PATH, new_profiles)

    def _apply_in_background():
        try:
            modules_manager.apply_compose(CITADEL_HOST_PATH, CITADEL_MODULES_ROOT, disabled_profiles)
        except RuntimeError as e:
            print(f"[modules] background apply_compose failed: {e}", flush=True)

    threading.Thread(target=_apply_in_background, daemon=True).start()
    return jsonify({
        "status": "applying",
        "detail": "Saved. Applying now in the background -- cockpit may blip "
                  "for a few seconds while it restarts to pick up the change. "
                  "Re-check the module list in a moment to confirm.",
    })


@app.route('/api/modules/install', methods=['POST'])
def api_install_module():
    """Multipart upload, field "file" -- a .zip of one modules/<name>/
    folder (manifest.json + compose.fragment.yml, optionally
    nginx.fragment.conf). Installs it disabled -- this only makes it
    show up in Settings' module list; a separate /api/modules/apply call
    (the same one the toggle UI already uses) actually enables and starts
    it. Runs sync_compose_include() + apply_compose() right after
    extracting specifically so a broken fragment (bad YAML, a real
    startup error) surfaces immediately as an install-time error instead
    of being deferred to whenever someone later tries to enable it."""
    if 'file' not in request.files:
        return jsonify({"status": "error", "detail": "no file uploaded"}), 400
    upload = request.files['file']
    filename = upload.filename or ""
    if not is_safe_filename(filename) or not filename.endswith('.zip'):
        return jsonify({"status": "error", "detail": "expected a .zip file"}), 400

    tmp_path = os.path.join(CITADEL_MODULES_ROOT, f"_upload_{filename}")
    upload.save(tmp_path)
    try:
        module_name = modules_manager.install_module_zip(tmp_path, CITADEL_MODULES_ROOT)
    except modules_manager.UnsafeModuleArchiveError as e:
        return jsonify({"status": "error", "detail": str(e)}), 400
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    try:
        modules_manager.sync_compose_include(CITADEL_COMPOSE_PATH, CITADEL_MODULES_ROOT)
    except RuntimeError as e:
        return jsonify({
            "status": "partial",
            "detail": f"Installed modules/{module_name}/, but couldn't update "
                      f"docker-compose.yml's include list: {e}",
        }), 500

    try:
        modules_manager.apply_compose(CITADEL_HOST_PATH, CITADEL_MODULES_ROOT)
    except RuntimeError as e:
        return jsonify({
            "status": "partial",
            "detail": f"Installed {module_name} and registered it, but applying "
                      f"failed (it's installed but not yet enabled, so this is "
                      f"safe to ignore until you're ready to enable it): {e}",
        })

    return jsonify({
        "status": "success",
        "detail": f"Installed {module_name}. It's disabled by default -- enable it "
                  f"from the module list above, same as any other module.",
        "name": module_name,
    })


# ---------------------------------------------------------------------
# News Archive & Local Log (ROADMAP.md DISCOVERY item, real build
# 2026-09-16). Real design decisions this section implements, worked
# through with Frank one at a time before any of this was written:
#   - Python port of Masthead's own proven logic, not PHP running
#     alongside vault-api (see news_hazard_adapters.py's own docstring).
#   - Location is fully automatic (STATION_LAT/STATION_LON, already set
#     for the Tactical Map) -- no second location field anywhere.
#   - Retention: regular articles kept 1 year, real hazard alerts
#     (cap_event set) never auto-pruned -- see api_news_prune below.
#   - Fetch schedule: per-source `fetch_interval_minutes` (720 = twice
#     daily for general news; hazard sources get a short interval when
#     seeded, see news-scheduled.sh) drives each source's own
#     `next_due_at`, checked by /api/news/fetch-due.
# ---------------------------------------------------------------------

def _station_coords():
    lat = os.environ.get("STATION_LAT", "")
    lon = os.environ.get("STATION_LON", "")
    try:
        return float(lat), float(lon)
    except ValueError:
        return None, None


def _get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/news/sources', methods=['GET'])
def api_list_news_sources():
    conn = _get_db()
    rows = conn.execute(
        "SELECT id, name, feed_url, is_active, fetch_interval_minutes, "
        "last_fetched_at, next_due_at, last_error FROM news_sources ORDER BY name"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/news/sources', methods=['POST'])
def api_add_news_source():
    """Body: {"name": "...", "feed_url": "...", "fetch_interval_minutes": 720}.
    New sources are immediately due (next_due_at = now), same reasoning
    as Masthead's own SourceService: a newly-added source shouldn't sit
    waiting a full interval before its first real fetch."""
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    feed_url = (data.get("feed_url") or "").strip()
    if not name or not feed_url:
        return jsonify({"error": "name and feed_url are both required"}), 400

    interval = data.get("fetch_interval_minutes")
    if not isinstance(interval, int) or interval < 1:
        interval = 720

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    conn = _get_db()
    try:
        conn.execute(
            "INSERT INTO news_sources (id, name, feed_url, is_active, "
            "fetch_interval_minutes, next_due_at, created_at) VALUES (?, ?, ?, 1, ?, ?, ?)",
            (str(uuid.uuid4()), name, feed_url, interval, now, now),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "a source with this feed_url already exists"}), 409
    finally:
        conn.close()
    return jsonify({"status": "success"})


@app.route('/api/news/sources/<source_id>', methods=['DELETE'])
def api_delete_news_source(source_id):
    conn = _get_db()
    conn.execute("DELETE FROM news_sources WHERE id = ?", (source_id,))
    conn.execute("DELETE FROM news_articles WHERE source_id = ?", (source_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


@app.route('/api/news/articles', methods=['GET'])
def api_list_news_articles():
    """?limit=50&offset=0 -- newest first. Location filtering happens
    here (not at ingest time) so a later station-location change
    re-scopes existing history instead of only affecting future
    fetches."""
    limit = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))

    conn = _get_db()
    lat, lon = _station_coords()
    county_fips, nws_zone_ugc = news_location.get_cached_zone_codes(conn)

    rows = conn.execute(
        "SELECT * FROM news_articles ORDER BY published_at DESC LIMIT ? OFFSET ?",
        (limit * 3 if (lat and lon) else limit, offset),
    ).fetchall()
    conn.close()

    articles = [dict(r) for r in rows]
    if lat and lon:
        articles = [a for a in articles if news_matcher.is_relevant_to_station(
            a, lat, lon, county_fips, nws_zone_ugc
        )]
    return jsonify(articles[:limit])


@app.route('/api/news/active-alerts', methods=['GET'])
def api_news_active_alerts():
    """Real hazard alerts only (cap_event set) that haven't expired yet
    and are relevant to this station's own location -- this is what the
    dashboard's red-dot indicator (index.html) polls."""
    conn = _get_db()
    lat, lon = _station_coords()
    county_fips, nws_zone_ugc = news_location.get_cached_zone_codes(conn)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    rows = conn.execute(
        "SELECT * FROM news_articles WHERE cap_event IS NOT NULL "
        "AND (cap_expires_at IS NULL OR cap_expires_at > ?) "
        "ORDER BY published_at DESC",
        (now,),
    ).fetchall()
    conn.close()

    alerts = [dict(r) for r in rows]
    if lat and lon:
        alerts = [a for a in alerts if news_matcher.is_relevant_to_station(
            a, lat, lon, county_fips, nws_zone_ugc
        )]
    return jsonify({"count": len(alerts), "alerts": alerts})


@app.route('/api/news/local-log', methods=['GET'])
def api_list_local_log():
    conn = _get_db()
    rows = conn.execute(
        "SELECT * FROM local_log_entries ORDER BY created_at DESC LIMIT 200"
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/news/local-log', methods=['POST'])
def api_add_local_log():
    data = request.get_json(silent=True) or {}
    text = (data.get("entry_text") or "").strip()
    if not text:
        return jsonify({"error": "entry_text is required"}), 400

    conn = _get_db()
    conn.execute(
        "INSERT INTO local_log_entries (id, entry_text, created_at) VALUES (?, ?, ?)",
        (str(uuid.uuid4()), text, datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


def _insert_articles(conn, source_id, items):
    inserted = 0
    for item in items:
        try:
            conn.execute(
                "INSERT INTO news_articles (id, source_id, dedupe_key, title, url, body, "
                "image_url, published_at, created_at, cap_event, cap_severity, cap_urgency, "
                "cap_certainty, cap_area_desc, cap_expires_at, cap_geocodes, latitude, longitude) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    str(uuid.uuid4()), source_id, item["dedupe_key"], item["title"], item["url"],
                    item.get("body"), item.get("image_url"), item["published_at"],
                    datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                    item.get("cap_event"), item.get("cap_severity"), item.get("cap_urgency"),
                    item.get("cap_certainty"), item.get("cap_area_desc"), item.get("cap_expires_at"),
                    item.get("cap_geocodes"), item.get("latitude"), item.get("longitude"),
                ),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            pass  # already have this one (source_id, dedupe_key) -- expected, not an error
    return inserted


@app.route('/api/news/fetch-due', methods=['POST'])
def api_news_fetch_due():
    """Real, periodic fetch -- called by scripts/news-scheduled.sh (a
    systemd timer, same real pattern as backup-scheduled.sh and
    health-check.sh). Only fetches sources whose own next_due_at has
    passed; the timer itself just needs to run often enough to catch
    the shortest real interval (hazard sources), not every source every
    time. NWS is handled separately below (news_nws_alerts.py), not as
    a regular RSS source -- see that module's own docstring for why."""
    conn = _get_db()
    now_dt = datetime.now(timezone.utc)
    now = now_dt.strftime("%Y-%m-%d %H:%M:%S")

    due = conn.execute(
        "SELECT * FROM news_sources WHERE is_active = 1 AND (next_due_at IS NULL OR next_due_at <= ?)",
        (now,),
    ).fetchall()

    results = []
    for source in due:
        source = dict(source)
        try:
            items = news_feed_parser.fetch_feed(source["feed_url"])
            adapter = news_hazard_adapters.adapter_for_feed_url(source["feed_url"])
            if adapter:
                items = [adapter(dict(item)) for item in items]
            inserted = _insert_articles(conn, source["id"], items)
            next_due = (now_dt + timedelta(
                minutes=source["fetch_interval_minutes"]
            )).strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                "UPDATE news_sources SET last_fetched_at = ?, next_due_at = ?, last_error = NULL WHERE id = ?",
                (now, next_due, source["id"]),
            )
            results.append({"source": source["name"], "fetched": len(items), "inserted": inserted})
        except Exception as e:
            conn.execute(
                "UPDATE news_sources SET last_error = ? WHERE id = ?",
                (str(e), source["id"]),
            )
            results.append({"source": source["name"], "error": str(e)})

    # NWS alerts: fetched every run (not gated by next_due_at) since this
    # is the one real life-safety-critical source, and the whole point of
    # the 5-15 minute scheduler cadence (see ROADMAP.md) is that these
    # need to be near-real-time, not on a per-source due schedule like
    # general news.
    lat, lon = _station_coords()
    if lat and lon:
        try:
            alerts = news_nws_alerts.fetch_active_alerts(lat, lon)
            inserted = _insert_articles(conn, "nws-direct", alerts)
            results.append({"source": "NWS Alerts (direct)", "fetched": len(alerts), "inserted": inserted})
        except Exception as e:
            results.append({"source": "NWS Alerts (direct)", "error": str(e)})

    conn.commit()
    conn.close()
    return jsonify({"status": "success", "results": results})


@app.route('/api/news/refresh-location', methods=['POST'])
def api_news_refresh_location():
    """Re-resolves and caches the real NWS county/zone codes from the
    current STATION_LAT/STATION_LON -- called by the scheduler
    periodically (station location rarely changes, but re-resolving is
    cheap and keeps this honest if it ever does)."""
    lat, lon = _station_coords()
    conn = _get_db()
    county_fips, nws_zone_ugc = news_location.refresh_and_cache_zone_codes(conn, lat, lon)
    conn.close()
    return jsonify({"county_fips": county_fips, "nws_zone_ugc": nws_zone_ugc})


@app.route('/api/news/prune', methods=['POST'])
def api_news_prune():
    """Real retention policy, worked through with Frank before any of
    this was built: regular articles kept 1 year, real hazard alerts
    (cap_event set) never auto-pruned -- these ARE the point of the
    feature (a real local hazard history), and realistic volume is low
    enough that keeping them all costs essentially nothing."""
    conn = _get_db()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%d %H:%M:%S")
    cur = conn.execute(
        "DELETE FROM news_articles WHERE cap_event IS NULL AND published_at < ?",
        (cutoff,),
    )
    deleted = cur.rowcount
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "deleted": deleted})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

