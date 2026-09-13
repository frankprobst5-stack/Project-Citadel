#!/usr/bin/env bash
# CITADEL — one-step installer for a fresh machine.
set -e

cd "$(dirname "$0")"

echo "============================================================"
echo " PROJECT CITADEL — Installer"
echo "============================================================"

if ! command -v docker >/dev/null 2>&1; then
    echo "Docker isn't installed. Install Docker Desktop (or Docker Engine on"
    echo "Linux) first, then run this script again: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
    echo "Docker is installed, but the 'docker compose' plugin isn't available."
    echo "Update Docker Desktop, or install the compose plugin, then try again."
    exit 1
fi

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from the template (edit it later if you want to change ports)."
fi

# Pre-create bind-mount folders so Docker doesn't create them as root, which
# would block you from managing your own files later.
mkdir -p appdata/kiwix-library appdata/kolibri_home appdata/ollama appdata/open-webui appdata/flatnotes
mkdir -p appdata/media-vault/videos appdata/media-vault/mp3s appdata/media-vault/pdfs appdata/media-vault/notes-data
mkdir -p appdata/mealie/data appdata/whisper-models appdata/cloud9/data appdata/cloud9/models

echo "Starting Citadel — this pulls a handful of container images the first"
echo "time, so it may take a few minutes..."
docker compose up -d

echo "============================================================"
echo " Citadel is up. Open your dashboard at:"
echo "   http://localhost:8085"
echo "============================================================"
