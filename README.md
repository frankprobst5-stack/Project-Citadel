# Project Citadel

**A self-contained, offline-first home command center**: complete media library, secure notes, offline AI assistant (Ollama + Open WebUI), offline encyclopedia (Kiwix), home-school lessons (Kolibri), comprehensive homestead & emergency logistics tracking, and intelligent home automation — all running on your own hardware via Docker, with **zero external internet dependency**.

Everything runs locally on your own machine. When the internet goes down, your entire home command infrastructure stays up.

Free forever, licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later) — see [LICENSE](LICENSE) for the full text. (This covers Citadel's own code — the cockpit dashboard, the media-vault app, install scripts. The bundled services — Ollama, Open WebUI, Kiwix, Kolibri, Flatnotes — are pulled as pre-built container images and keep their own upstream licenses.)

---

## What You Get

### 🛡️ Command Cockpit Dashboard
A unified browser-based command center (port **8085**) with 13 integrated modules:

- **📡 Communications Hub** — Launches WayStation, the full EmComm dashboard (net control, ICS forms, mesh, Winlink, JS8Call, space weather)
- **🗺️ Tactical Map** — Offline vector map with real elevation data, no internet required
- **🎬 Digital Media Vault** — Self-hosted video, audio, and PDF library with category-based organization
- **🎓 Home Education Hub** — Cloud9 kid dashboard plus Kolibri, a full offline learning platform with thousands of lessons and student tracking
- **🍲 Recipes & Meal Planner** — Mealie: URL/photo recipe import, meal planning, shopping lists, plus a pantry-check bridge against your own Food Inventory/Freezer Foods ledgers
- **📚 Knowledge Base** — Offline wiki/encyclopedia access (Kiwix + .zim archives), morse code, phonetic alphabets, technical manuals
- **🌿 Homestead Logistics** — Multi-table inventory system for food, fuel, PPE, orchard/fruit trees, livestock, and botanical gardens (see below)
- **🩸 First Aid & Medical** — Offline emergency trauma protocols, surgical field manuals, medical reference charts
- **🧠 Offline AI Assistant** — Local Large Language Models (Ollama) for data analysis, writing, and computation — no cloud, no tracking
- **🏠 Home Monitor Matrix** — Smart home device registry and relay control (Project Vigil) for cameras and hardware relays. Solar/battery telemetry runs as a separate service but has no dashboard panel yet — see ROADMAP.md.
- **📝 Secure Notes** — Flatnotes markdown storage for sensitive documentation, asset inventories, and mission profiles
- **📟 Master Operations Handbook** — Full household operations manual
- **⚙️ System Settings** — Live service diagnostics and station identity

Plus a **live scratchpad** for quick tactical notes (auto-saved to browser storage).

### 📊 Homestead Logistics System

A production-grade inventory database (SQLite) for preparedness and homesteading:

**Inventory Ledgers:**
- **Food** — Track provisions, freeze-dried storage, shelf life, calorie indexes, expiration dates
- **Fuel** — Monitor gasoline reserves, diesel drums, propane levels, rotation schedules
- **PPE & Equipment** — Manage protective kits, gas mask canisters, respirator gear, inspection status
- **Orchard & Fruit Trees** — Log tree varieties, locations, pruning records, fertilization, seasonal health
- **Livestock & Animals** — Track breed counts, health logs, feeding requirements, production yields

**Botanical Garden Tracker:**
- Year-over-year crop database (2025–2028, extendable)
- Spring and Fall planting cycle records
- Per-crop logging: variety, plot location, planting type (seed/starter), fertilizers, pest pressures, total yield
- Search and filter by crop, variety, or plot
- Full CRUD interface with real-time updates

All data persists in a local SQLite database. **No cloud sync, no external dependencies.**

### 🏠 Smart Home Hub (Project Vigil)

An embedded **local-only IoT controller** for offline home automation:

- **Device Registry** — DIY smart devices (relays, cameras, sensors) register via HTTP heartbeat to `/api/register`
- **Relay Control** — Toggle connected devices on/off through the dashboard UI
- **Power Monitoring** — Solar/off-grid battery and bus telemetry, with real load-shedding automation on low battery
- **Hardware Support** — Includes ESP32 Arduino sketch (`esp32_relay_node.ino`) for building your own smart relay nodes
- **Persistent State** — Device registry saved to `vigil_grid_ledger.json`, survives reboots
- **Zero Internet** — All communication is LAN-local; works during internet outages

Example hardware registration:
```json
{
  "device_id": "LIVING_ROOM_SWITCH",
  "ip": "192.168.1.105",
  "type": "Smart Power Relay",
  "state": "OFF"
}
```

See `appdata/project-vigil/manual.html` for full integration docs.

---

## Requirements

- Docker and the `docker compose` plugin. Get Docker here if you don't have it: https://docs.docker.com/get-docker/
- Linux, macOS, or Windows.
- **Minimum hardware:** 4 GB RAM recommended. Lighter services (cockpit, vault-api, vigil, flatnotes, kiwix) run fine on modest hardware; Ollama and Kolibri benefit from more RAM.
- **Raspberry Pi:** Not yet officially supported (see [ROADMAP.md](ROADMAP.md)). Ollama (LLM) and Kolibri (education platform) are resource-heavy; tested only on desktop/laptop-class hardware so far.

---

## Installing

### Quick Start

1. **Download and unzip** this project to a folder on your machine.
2. **Run the installer for your platform:**
   - **Windows**: double-click `install.bat` (or run from Command Prompt/PowerShell)
   - **Linux / macOS**: open a terminal in the extracted folder and run `./install.sh`
3. **Wait for first startup** — Docker will pull container images (a few minutes on first run)
4. **Open your browser** to **http://localhost:8085**

Everything runs locally. Your entire home infrastructure is now up and running.

### First-Run Security Step: Change Mealie's Default Login

Mealie (the recipe manager) ships with self-signup disabled and a
publicly-documented default admin account: `changeme@example.com` /
`MyPassword`. Anyone who's read Mealie's own docs knows this login for
*every* fresh Citadel install, so change it immediately:

1. Open `http://localhost:8097`, log in with the default above.
2. Avatar (top right) → **Manage Your Account** → set your own email
   and password.

This is the one credential in Citadel that isn't obviously yours by
default — everything else has no login at all (see "Known Gaps" below
for what that means for exposing this beyond your own LAN).

### Configuration (Optional)

If any default ports are already in use on your machine, edit `.env` before running `install.sh`:

```dotenv
# Port mappings (host-side only; containers use their own internal ports)
COCKPIT_PORT=8085          # Main dashboard
OLLAMA_PORT=11500          # Offline AI (internal: 11434)
KOLIBRI_PORT=8081          # Home education
KIWIX_STORAGE_PATH=./appdata/kiwix-library  # Offline encyclopedias
```

See `.env.example` for all available options.

---

## Adding Your Content

### Media Library

Drop files into the appropriate folders inside `appdata/media-vault/`:

```
appdata/media-vault/
  videos/
    Documentary/
    Educational/
    Archive/
  mp3s/
    Audiobooks/
    Podcasts/
    Music/
  pdfs/
    Manuals/
    References/
    Plans/
```

Each subfolder becomes a category. Open the **Digital Media Vault** module in the cockpit to browse and stream.

### Offline Encyclopedia

Download `.zim` archives from https://library.kiwix.org (Wikipedia, wiktionary, wikihow, technical docs, etc.) and drop them into:
```
appdata/kiwix-library/
```

(Or configure `KIWIX_STORAGE_PATH` in `.env` to point elsewhere.)

Then access them via the **Knowledge Base** module.

### Home Education Lessons

Kolibri is a full learning platform. Once running, visit **http://localhost:8081** or click the **Home Education Hub** module to:
- Browse thousands of lessons (math, science, history, language, etc.)
- Track student progress
- Download content for offline use

### Homestead Logistics

Click the **Homestead Logistics** module in the cockpit to manage:
- Food, fuel, PPE inventory
- Orchard and livestock records
- Year-over-year botanical garden logs

All data is stored locally in SQLite. Export/backup `appdata/media-vault/citadel.db` if needed.

### Smart Home Devices

See `appdata/project-vigil/manual.html` for full hardware integration documentation. Quick summary:

1. Wire up a DIY smart device (ESP32 + relay recommended; sketch included)
2. Configure it to POST a registration packet to `http://<YOUR_CITADEL_IP>:8085/api/register`
3. Device appears in the **Home Monitor Matrix** module
4. Toggle on/off from the dashboard; Citadel sends commands back to your device

No cloud service, no vendor lock-in.

---

## Stopping / Restarting

```bash
# Stop all services
docker compose down

# Start everything back up
docker compose up -d

# View live logs
docker compose logs -f

# Restart a single service (e.g., vault-api)
docker compose restart citadel-vault-brain
```

---

## Ports Used

| Service | Port | Purpose |
|---|---|---|
| **Cockpit Dashboard** | 8085 | Main command center UI |
| **Kolibri** (Education) | 8081 | Home-school platform |
| **Project Vigil** (Home Hub) | 8082 | Device registry, relay control, solar/security telemetry, discovery |
| **Ollama** (Offline AI) | 11500 | Local LLM engine (internal: 11434) |
| **Open WebUI** (AI Chat) | 8090 | Multi-user AI chat interface |
| **Kiwix** (Encyclopedia) | 8095 | Offline wiki access |
| **Whisper** (Audio transcription) | 8096 | Local speech-to-text (also used by Mealie's Audio Provider) |
| **Mealie** (Recipes) | 8097 | Recipe manager & meal planner |
| **Flatnotes** (Secure Notes) | 8098 | Markdown note storage |
| **Cloud9** (Kid Dashboard) | 8099 | Homeschool dashboard for one kid's device |

If any port is already in use on your machine, edit `.env` **before running install.sh** and change the value. Example:

```dotenv
OLLAMA_PORT=11501  # Changed from 11500 if something else owns it
COCKPIT_PORT=8086  # Changed from 8085
```

---

## The Offline-First Architecture

Citadel is designed from the ground up to work **with or without the internet:**

### When Internet Is Down
- ✅ Dashboard available at `http://localhost:8085`
- ✅ Media vault (videos, audio, PDFs) fully accessible
- ✅ Offline AI (Ollama) responds normally
- ✅ Encyclopedia (Kiwix) fully searchable
- ✅ Education platform (Kolibri) continues lessons
- ✅ Smart home control (Project Vigil) unaffected
- ✅ Notes (Flatnotes) readable and editable
- ✅ Logistics database fully operational
- ✅ Serves other devices on your LAN (see below)

### When Internet Is Up
- Citadel still doesn't phone home; it's fully self-contained
- You *can* optionally configure external services (e.g., real Project IBRIS radar daemon), but nothing requires it

### Serving Other Devices on Your LAN

Citadel runs an internal HTTP server that other devices on your local network can access **even if your internet connection is down:**

- **Smart devices** can register and receive control commands at `http://<citadel-ip>:8085/api/register` and `http://<citadel-ip>:8085/api/toggle`
- **Laptops, tablets, phones** on your LAN can access the full dashboard at `http://<citadel-ip>:8085`
- **IoT sensors** can query the device registry at `http://<citadel-ip>:8085/api/grid`
- **Media streaming** to other devices works through the vault API at `/files/videos/`, `/files/mp3s/`, `/files/pdfs/`

This makes Citadel a true **network hub for your home** — a central command and data center that keeps functioning when the internet fails.

---

## Known Gaps & Roadmap

A few features are stubbed out but not yet implemented. See [ROADMAP.md](ROADMAP.md) for the full plan. Quick summary:

- **Radar tracking** — `vault-api` serves `/api/radar`, but it always returns an empty/sync-error result: no cockpit page currently has a panel for it, and the real Project IBRIS radar daemon (a separate repo — see ROADMAP.md Phase E) hasn't been bundled in yet. Worth noting its own repo already admits the radar output is demo/simulated data, not a real sensor feed, even once wired up.
- **Radio scanner & local weather** — `vault-api` serves honest live status (`/api/scanner`, `/api/weather`) plus a real setup API (`/api/scanner/config`) that turns an operator's own trunked-system data (free from RadioReference's public pages, digitalfrequencysearch.com, or OpenMHz — no paid subscription required) into a working `trunk-recorder` config. All of this is consumed and displayed by WayStation now, not a page in this repo (the old `comms.html` has been deleted — WayStation is the real comms replacement, launched from the Communications Hub tile). A real `trunk-recorder` service exists in `docker-compose.yml` under a `hardware` profile. Actual P25 decode and local weather capture both still need real RTL-SDR hardware — see ROADMAP.md Phase 2 for exactly what's left.
- **Raspberry Pi support** — Ollama and Kolibri are genuinely heavy; testing and documentation needed for Pi deployment.
- **Containerized vault-api** — Currently uses dev-mode Flask; should have a proper Dockerfile with pinned dependencies for reproducibility and offline startup.

None of these gaps affect the core functionality; they're genuine features to build, not bugs.

---

## Tech Stack

- **Frontend:** HTML5, CSS3, vanilla JavaScript (no build step, runs directly in nginx)
- **Backend:** Python 3.10 (Flask + SQLite, Ollama API, Project Vigil)
- **Reverse Proxy:** nginx (routing, CORS handling)
- **Container Runtime:** Docker + Docker Compose
- **Included Services:**
  - **Ollama** — Offline LLM inference
  - **Open WebUI** — AI chat interface
  - **Kiwix** — Encyclopedia/wiki server
  - **Kolibri** — Education platform
  - **Flatnotes** — Markdown note storage
  - **Project Vigil** — Home automation hub

---

## Contributing

Issues and pull requests welcome. This is a hobby project, not a commercial product — expect rough edges, and feel free to fork and make it your own under the terms of the GPL-3.0-or-later.

### Development Tips

- **Dashboard frontend** is pure HTML/CSS/JS in `appdata/cockpit/` — no build step
- **Vault API** logic is in `appdata/media-vault/app.py` — Flask-based, handles inventory/garden CRUD and media serving
- **Project Vigil** smart home logic is in `appdata/project-vigil/vigil_kernel.py` — device registry, relay control, solar/security telemetry, real automation, and hardware adapters (Tasmota/Shelly/ESPHome/Zigbee2MQTT) -- see its own top-of-file comment for what's verified against real hardware vs. written to spec awaiting field reports
- **Nginx routing** configured in `appdata/cockpit/nginx.conf` — proxy rules for all backend services

All changes are hot-reloaded or require a simple `docker compose restart <service>`.

---

## License

GNU General Public License v3.0 or later. See [LICENSE](LICENSE).

**Important:** This covers Citadel's own code (cockpit, media-vault, install scripts, Project Vigil integration). The bundled container services (Ollama, Open WebUI, Kiwix, Kolibri, Flatnotes) are pulled from upstream repositories and retain their own licenses.

---

## FAQ

**Q: Does Citadel require internet?**  
A: No. It runs entirely offline. If you have an internet connection, Citadel won't use it. If you lose internet, Citadel keeps working.

**Q: Can I access Citadel from other devices on my network?**  
A: Yes. From any device on your LAN, visit `http://<citadel-host-ip>:8085`. Smart home devices can register at `/api/register`. Everything works even if internet is down.

**Q: What if I already run Ollama locally?**  
A: Citadel's Ollama container is mapped to port 11500 by default (not 11434) to avoid conflicts. You can adjust `OLLAMA_PORT` in `.env`.

**Q: Can I export my logistics data?**  
A: The SQLite database is stored at `appdata/media-vault/citadel.db`. Back it up anytime. Standard SQLite tools can read it.

**Q: Is this meant to replace a commercial product like Project NOMAD?**  
A: Yes — Citadel was built explicitly as a free, self-hosted alternative. You own all your data; nothing is stored in the cloud.

**Q: Can I run this on Raspberry Pi?**  
A: Not officially tested yet. Ollama and Kolibri are heavy; Pi hardware would struggle. See [ROADMAP.md](ROADMAP.md) for the plan to split lightweight vs. resource-intensive services.
