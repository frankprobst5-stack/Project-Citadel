from flask import Flask, request, jsonify, render_template, send_from_directory
import sqlite3
import os
import json

app = Flask(__name__)
app.url_map.strict_slashes = False

DB_PATH = "/app/citadel.db"

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

    cursor.execute('''
        INSERT OR REPLACE INTO inventory (id, category, desc, loc, qty, exp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (str(data['id']), data['category'], data['desc'], data['loc'], qty_sanitized, data['exp']))
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
    """Reads whatever a real scanner-decode daemon (trunk-recorder/op25) has
    written to the shared state file and serves it. Same daemon-writes-JSON/
    API-reads-JSON shape as /api/radar above -- no daemon is wired into this
    stack yet (see ROADMAP.md Phase 2), so an honest "no_data" default comes
    back instead of a fabricated "listening" claim until one actually
    exists. WayStation (the comms app this cockpit launches) is the
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
        "transcripts": [],
    })

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

