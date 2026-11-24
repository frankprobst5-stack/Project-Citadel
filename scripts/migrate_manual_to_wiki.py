#!/usr/bin/env python3
"""One-time migration: manual.html's real content -> real wiki_pages rows.

Run once, against the live stack, after wiki.html/the /api/wiki/* routes
exist (appdata/media-vault/wiki.py). Splits the handbook's own 9 real
<div class="section"> blocks (plus its intro) into 10 wiki pages, each
tagged, with each section's own cards/subsections kept as real markdown
headings -- not reworded, not summarized, the actual text from
manual.html as of 2026-11-24, just reformatted from HTML into the
markdown subset wiki.html's renderMarkdown() supports (headers, bullets,
numbered lists, bold/italic/inline code, fenced code blocks, pipe
tables, and [text](url) links).

Idempotent by title: re-running this skips any page whose title already
exists rather than creating a duplicate, so a half-finished or re-run
migration never doubles up.

Does NOT delete manual.html or its index.html card -- that's a separate,
deliberate step once these pages are confirmed to look right in the
wiki UI.

Usage:
    VAULT_API_TOKEN=... python3 scripts/migrate_manual_to_wiki.py [--base-url http://localhost:8085]
(defaults to reading VAULT_API_TOKEN out of ../.env if not set in the environment)
"""
import argparse
import os
import sys
from pathlib import Path

import requests

PAGES = [
    {
        "title": "Master Operations Handbook — Overview",
        "tags": ["overview", "manual"],
        "body_markdown": """**SECURITY CLASSIFICATION: LOCAL SOVEREIGN // OFF-GRID SURVIVABILITY INFRASTRUCTURE**

This document describes the real cockpit cards as they actually exist today (rewritten 2026-09-13, ROADMAP.md Phase F). Two rules kept it honest: nothing here is described as working unless it's actually been built and tested, and anything genuinely untested (usually because no real hardware exists yet to test it against) says so plainly rather than implying it just works.""",
    },
    {
        "title": "What You Need Before You Start",
        "tags": ["setup", "requirements"],
        "body_markdown": """Added 2026-09-14 -- this was missing entirely before, even though the buying guide for optional smart-home hardware further down existed. This is what you need to run Citadel **at all**, before any of that.

## Software

**Docker Desktop** (Windows/macOS) or **Docker Engine + the `docker compose` plugin** (Linux) -- [docs.docker.com/get-docker](https://docs.docker.com/get-docker/). On Windows this also enables WSL2, which may ask for a restart -- that's normal, not an error. After installing, make sure Docker is actually **running** (Docker Desktop's whale icon shows "running," not just installed) before continuing to the power-up protocol.

## Hardware -- corrected against real measured numbers, not a guess

Idle, Citadel's whole core fleet uses under 1 GB of RAM combined -- but the Off-Grid AI engine (Ollama) alone jumps to roughly **1.5 GB the moment it actually answers a question** (loading a small model into RAM), measured live on this project's own hardware. Budget by what you actually enable in the installer's module picker, not by "Citadel" as one thing:

| You enable | Realistic free RAM to budget (beyond your OS's own usage) |
|---|---|
| Just the lightweight tier (Home Monitor Matrix, Secure Notes, Knowledge Base) | ~1 GB |
| + Recipes and/or Whisper audio transcription | ~2 GB |
| + Off-Grid AI and/or Home Education (these two share one Ollama engine now, so enabling both doesn't double this cost) | ~4 GB, more for a larger model than the default `llama3.2:1b` |
| Everything at once (the installer's non-interactive default) | 8 GB+ free, 16 GB total system RAM is comfortable -- this exact combination froze a real 15 GB test machine when combined with normal desktop use |

Also want **~10 GB free disk space** for container images, plus room for your own media/notes/backups. If this machine is your daily driver, not a dedicated box, pick only the modules you actually want in the installer's picker -- Settings -> Modules also lets you turn any of this off later without reinstalling, no terminal needed.""",
    },
    {
        "title": "Emergency System Power-Up Protocol (After Outages)",
        "tags": ["recovery", "outage"],
        "body_markdown": """If the main server computer suffers a sudden power loss or manual reboot, follow these 3 basic recovery steps to restore the dashboard:

## Step 1: Open the System Command Line

Turn on the computer monitor, tap the **Ubuntu Terminal** app icon on the sidebar menu panel layout, or press `Ctrl + Alt + T` on the keyboard.

## Step 2: Advance to Core Control Directory

Type this exact path routing phrase into your screen prompt line and hit Enter:

```
cd ~/citadel
```

## Step 3: Ignite the Container Fleet

Type this and hit Enter:

```
docker compose up -d
```

This starts every module in your `.env` file's `COMPOSE_PROFILES` line -- by default, everything except two things that need real hardware plugged in first: `hardware` (an RTL-SDR radio dongle, for the Communications Hub's trunked-radio scanner and Project Intercept) and `camera` (a real webcam, for the Home Monitor Matrix's motion detector). Add either name to that line once you actually have the matching hardware. If a card is missing from your dashboard entirely, check that line first before assuming something's broken.

**Expected Confirmation:** Every enabled service prints green [Started] across the terminal line.""",
    },
    {
        "title": "Communications & Airwave Spectrum Modules",
        "tags": ["communications", "radio"],
        "body_markdown": """These cards handle radio and long-distance messaging.

## Card 1: Communications Hub

**What It Does:** Launches WayStation, the full EmComm command dashboard -- net control, ICS forms, mesh, Winlink, JS8Call, space weather, and cross-transport message routing. WayStation is a separate desktop app; this tile just opens it. It has its own hardware requirements for its ham-radio features (Digirig/TNC for packet, a SignaLink-style interface for HF digital modes, etc.) -- see WayStation's own documentation for what those actually are, not this page.

## Card 12: Project Intercept

**What It Does:** Passively decodes 433MHz ISM-band radio traffic -- wireless weather station sensors, tire-pressure monitors, and similar consumer devices -- using the real, open-source `rtl_433` decoder.

**Requires real hardware:** an RTL-SDR USB dongle, plus the `hardware` profile enabled in `.env`. Without a dongle plugged in, this card's page will honestly show nothing captured -- that's correct behavior, not a bug.

**Note:** a single RTL-SDR dongle can only run *one* thing at a time -- either this, or WayStation's trunked-radio scanner (which uses the same kind of dongle), not both simultaneously. Two dongles are needed to run both at once.""",
    },
    {
        "title": "Homestead Logistics, Storage, & Security Modules",
        "tags": ["homestead", "storage", "security"],
        "body_markdown": """These cards handle inventory, secure notes, physical automation, and encryption.

## Card 11: Note Storage Vault

**What It Does:** Your family's off-grid secure notepad (Flatnotes) -- markdown files saved directly to local disk, no cloud, no account.

## Card 10: Home Monitor Matrix (Project Vigil)

**What It Does:** A real, working device registry and relay controller, plus real automation: battery-threshold load-shedding and tripline-triggered perimeter lighting run continuously in the background, no manual intervention needed. Also has a real local network scanner ("Scan Now") that finds Tasmota/Shelly/ESPHome devices on your LAN via mDNS.

**Camera feeds:** real -- any device registered with a `stream_url` (e.g. an ESP32-CAM streaming MJPEG) shows a live feed directly on this page.

**Controlling real hardware:** supported for four real ecosystems -- Tasmota, Shelly (both generations), ESPHome, and Zigbee2MQTT -- each built against that project's own official API. Honest status: none of these four have been tested against real physical hardware yet (none owned as of this writing). If you're trying one, please report back what works.

**Motion-triggered lighting:** a real webcam motion detector (adapted from Project IBRIS) can report directly into this card's tripline field. Also untested against a real camera -- needs the `camera` profile and a real `/dev/video0` device.

**Not supported, and never will be:** Blink and SimpliSafe. Both are closed cloud ecosystems with no local API at all -- don't buy either expecting it to work here. See the Real Smart-Home Hardware Guide page for what to actually buy instead.

## Card 3: Digital Media Vault

**What It Does:** Centralized offline video, audio, and PDF library, organized by folder.

## Card 7: Homestead Logistics

**What It Does:** Nine real inventory ledgers -- Food, Fuel, PPE, Orchard, Livestock, Water, Office/School Supplies, Fertilizer/Pesticide, and Freezer -- each with low-stock and expiration alerts, plus a separate year-over-year Botanical Garden tracker. Also has a Recipe Pantry Check tool: look up any recipe and see which ingredients you already have in Food Inventory or Freezer.

## Card 6: Recipes & Meal Planner

**What It Does:** Mealie, a real, mature self-hosted recipe manager -- import recipes by URL or photo, build a weekly meal plan, generate a shopping list. Local AI (your own Ollama) can assist with ingredient parsing and photo import; performance depends on your hardware and is genuinely slow on modest CPUs with no GPU -- expect real delays, not instant results.

**First-time setup:** log in with Mealie's default account and change the password immediately -- see README.md for exact steps. This is the one login in all of Citadel that isn't automatically yours.

*(Being replaced by the Unified Wiki's own recipe section + URL import -- see the Wiki card. Once that transition is confirmed solid, Mealie itself will be retired.)*

## Card 13: Crypto Vault

**What It Does:** Two real, verified tools, both running entirely in your browser with nothing sent over any network: AES-256-GCM text encryption (the browser's own audited Web Crypto API, not a home-rolled cipher), and a real Shamir's Secret Sharing key splitter -- split a secret into N shards where any T of them reconstruct it, but fewer reveal nothing. Both round-trip-tested live before being added here.""",
    },
    {
        "title": "Local Knowledge Base & Education Modules",
        "tags": ["knowledge", "education"],
        "body_markdown": """These cards cover reference material, school, AI, and system administration.

## Card 5: Knowledge Base

**What It Does:** Offline Wikipedia/wiki archives (Kiwix), plus phonetic alphabets and Morse code reference material.

## Card 4: Home Education Hub

**What It Does:** Cloud9 (a kid-focused dashboard: homework helper, planner, dictionary, weather labs) plus a full Kolibri course library underneath it.

## Card 8: First Aid

**What It Does:** Offline emergency trauma protocols, surgical field manuals, and medication reference charts. A handful of sub-features on this page (pediatric dosing charts, step-by-step skill images, printable field cards) are honestly marked "not built yet" directly on the page itself -- check there for the current real status, not this page.

## Card 9: Off-Grid AI

**What It Does:** A local, fully offline chat interface running `llama3.2:1b` through Ollama -- no cloud, no API key, no data leaving this machine. Realistic expectation: on modest CPU-only hardware with no GPU, this runs at roughly 10-15 tokens/second -- usable, but noticeably slower than a cloud AI service. A small model was chosen deliberately to keep it usable at all on hardware like this; a beefier machine could run a larger, smarter model instead.

## Card 14: Master Operations Handbook

**What It Does:** This document -- now living here, in the Unified Wiki, instead of a static manual.html page.

## Card 15: System Settings

**What It Does:** Live reachability checks for every module, station identity, and build info. Configuration editing isn't wired up here yet -- real config still means editing `.env` directly and restarting containers.""",
    },
    {
        "title": "Card 2: Tactical Map",
        "tags": ["map"],
        "body_markdown": """Offline vector map (roads, place names) with real elevation data for your local region, plus a low-detail world view -- fully local, no internet tile server involved. Your own station marker (call sign, location name, grid locator, coordinates) is configured through `.env`'s `STATION_*` variables, not hardcoded in the page -- so this page itself never needs to carry your real address.""",
    },
    {
        "title": "Universal Family Fail-Safe Diagnostics",
        "tags": ["troubleshooting", "diagnostics"],
        "body_markdown": """Review these checks if a family member encounters an unexpected error on screen:

- **Symptom: A card is just missing from the dashboard** -- *Resolution:* Check `.env`'s `COMPOSE_PROFILES` line -- that card's module isn't in your enabled list (common for `hardware`/`camera`-gated cards without the matching real device). Add it and run `docker compose up -d` again.
- **Symptom: METRIC DROP (Red Disconnect Header Flashing)** -- *Resolution:* A background container has gone offline. Open your terminal, type `cd ~/citadel && docker compose restart`, and hit Enter.
- **Symptom: 502 Bad Gateway Error Web Block** -- *Resolution:* The nginx gateway is healthy, but the backend it's routing to hasn't answered yet. Give the container 30-45 seconds to finish starting, then hard-refresh (`Ctrl+F5`).
- **Symptom: Web Browser Page Returns "File Not Found"** -- *Resolution:* Confirm the address bar reads exactly `http://localhost:8085` (or your Citadel machine's real LAN IP, not `localhost`, if browsing from another device).""",
    },
    {
        "title": "Real Smart-Home Hardware Guide",
        "tags": ["hardware", "shopping"],
        "body_markdown": """What to actually buy if you want the Home Monitor Matrix (Card 10) or Project Intercept (Card 12) to control or capture real hardware, not just show empty registries. Every row below maps to something genuinely built in Citadel today -- nothing here is a wishlist for a feature that doesn't exist yet.

| Purpose | What to Buy | Why | Est. Price |
|---|---|---|---|
| 433MHz / Trunked Radio | Nooelec NESDR SMArt v5 (RTL2832U & R820T) or similar RTL-SDR dongle | Powers Project Intercept (Card 12) and WayStation's trunked-radio scanner. Remember: one dongle runs one of these at a time. | $35 - $45 |
| Smart Plug / Relay (Tasmota) | Any Tasmota-flashed smart plug (e.g. Sonoff S31, or a stock device reflashed with [Tasmota](https://tasmota.github.io/)) | Real local HTTP control, no cloud account. Register with `"protocol": "tasmota"` in Vigil. | $10 - $20 |
| Smart Plug / Relay (Shelly) | Shelly Plus 1 (Gen2) or a classic Shelly 1 (Gen1) | Real local HTTP/RPC control, no cloud account. Register with `"protocol": "shelly_gen1"` or `"shelly_gen2"` matching your model. | $10 - $25 |
| DIY Microcontroller (ESPHome) | Any ESP32 or ESP8266 dev board, flashed with [ESPHome](https://esphome.io/) and its `web_server:` component enabled | Real local REST control. Register with `"protocol": "esphome"` and the entity name from your ESPHome config. | $5 - $15 |
| Zigbee Sensors/Plugs | A Zigbee USB coordinator (e.g. Sonoff Zigbee 3.0 Dongle Plus) running [Zigbee2MQTT](https://www.zigbee2mqtt.io/), plus any Zigbee devices | Real MQTT-based control for battery sensors and plugs. Register with `"protocol": "zigbee2mqtt"` and your broker's address. | $15 - $30 (coordinator) + device cost |
| Camera Feed | ESP32-CAM board with an OV2640 lens, streaming MJPEG | Register with a real `stream_url` -- Vigil's device cards already render a live feed from this field. | $12 - $18 |
| Motion Detection Camera | Any real USB webcam | Powers the real (if untested-on-hardware) motion detector feeding Vigil's tripline. Needs `/dev/video0` and the `camera` profile. | $15 - $40 |
| Weatherproof Enclosure | Waterproof IP65 project box | Generic protection for any outdoor node above. | $10 - $20 |
| Backups | External hard drive or a mounted NAS share, kept offline/off-site when not actively backing up | Citadel's data all lives in `appdata/`. The installer sets up a real nightly backup automatically (Settings > Backups uses the same one) -- set `BACKUP_MIRROR_PATH` in `.env` to a drive like this to also get an off-machine copy of every scheduled backup, not just an on-disk one. | $60 - $90 |

**Explicitly not on this list, and never will be: Blink and SimpliSafe.** Both are closed cloud ecosystems with no supported local API -- Vigil cannot and will not control either, regardless of how they're registered.

## Give Devices a Real Address, Not a DHCP Guess

Every device above needs to know where Citadel is. Point it at `http://<hostname>.local:8085` (whatever your machine's real hostname is -- run `hostname` to check) instead of a raw IP address. This already works with zero extra setup on a normal desktop install: `avahi-daemon` is already running, and `.local` mDNS resolution just works. A raw DHCP-assigned IP can silently change after any router reboot or lease renewal, quietly breaking every device pointed at the old one -- the `.local` name doesn't have that problem.

**One real exception:** a minimal or headless install might not have `avahi-daemon` installed by default the way a desktop install does. If `<hostname>.local` doesn't resolve, install it directly: `sudo apt install avahi-daemon`, then try again.""",
    },
    {
        "title": "Local Reference & Server Care",
        "tags": ["reference", "maintenance"],
        "body_markdown": """## Real File Locations Worth Knowing

- **Your real configuration (ports, station info, API tokens):** `~/citadel/.env` -- never committed to git, this is where every real per-install value lives.
- **Secure Notes data:** `~/citadel/appdata/flatnotes`
- **Main dashboard layout:** `~/citadel/appdata/cockpit/index.html`
- **Full project status and what's still being worked on:** `~/citadel/ROADMAP.md`

## Controlled Server Power-Down Sequence

Before performing planned maintenance or a power/battery-bank swap, stop containers cleanly first:

```
cd ~/citadel && docker compose down && sudo shutdown -h now
```

**Expected Outcome:** All containers stop cleanly, data commits to disk, and the machine powers down without file corruption risk.""",
    },
]


def load_token(explicit_token):
    if explicit_token:
        return explicit_token
    env_token = os.environ.get("VAULT_API_TOKEN")
    if env_token:
        return env_token
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("VAULT_API_TOKEN="):
                return line.split("=", 1)[1].strip()
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:8085")
    parser.add_argument("--token", default=None, help="Overrides VAULT_API_TOKEN / .env lookup")
    args = parser.parse_args()

    token = load_token(args.token)
    if not token:
        print("No VAULT_API_TOKEN found (env var or ../.env). Aborting.", file=sys.stderr)
        sys.exit(1)

    headers = {"X-Vault-Token": token, "Content-Type": "application/json"}
    existing = requests.get(f"{args.base_url}/api/wiki/pages", headers=headers, timeout=10)
    existing.raise_for_status()
    existing_titles = {p["title"] for p in existing.json()}

    created, skipped = 0, 0
    for page in PAGES:
        if page["title"] in existing_titles:
            print(f"SKIP  (already exists): {page['title']}")
            skipped += 1
            continue
        res = requests.post(
            f"{args.base_url}/api/wiki/pages",
            headers=headers,
            json={
                "section": "manual",
                "title": page["title"],
                "body_markdown": page["body_markdown"],
                "tags": page["tags"],
                "source_url": None,
            },
            timeout=10,
        )
        if res.ok:
            print(f"CREATED: {page['title']}")
            created += 1
        else:
            print(f"FAILED  ({res.status_code}): {page['title']} -- {res.text}", file=sys.stderr)

    print(f"\n{created} created, {skipped} skipped (already present).")


if __name__ == "__main__":
    main()
