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
    echo "(Windows: this also installs/enables WSL2, which may ask you to restart"
    echo "your computer -- that's normal, just run this script again afterward.)"
    exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
    echo "Docker is installed, but the 'docker compose' plugin isn't available."
    echo "Update Docker Desktop, or install the compose plugin, then try again."
    exit 1
fi

# Real, live-found gap (2026-09-14): the two checks above only confirm the
# `docker` CLI and compose plugin exist on disk -- neither one talks to the
# daemon, so both pass even if Docker Desktop is installed but was never
# actually launched (a very common state for a first-time user, and a
# confusing one: without this check, the failure a novice would hit instead
# is `docker compose up -d` dying several steps later with a raw
# "Cannot connect to the Docker daemon" error and no guidance). `docker info`
# is the real, cheap way to confirm the daemon is actually reachable.
if ! docker info >/dev/null 2>&1; then
    echo "Docker is installed, but isn't running yet."
    echo "Start Docker Desktop (look for its whale icon -- Windows/macOS), or"
    echo "on Linux run: sudo systemctl start docker"
    echo "Then run this script again."
    exit 1
fi

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from the template (edit it later if you want to change ports)."
fi

# CITADEL_HOST_PATH: the real absolute path Citadel lives at on THIS
# machine, needed by vault-api's "one-click apply" module toggle
# (Settings > Modules, ROADMAP.md Phase B follow-up) -- see
# docker-compose.yml's own comment on vault-api's volumes and
# modules_manager.py's apply_compose() for why Docker-outside-of-Docker
# needs this project directory mounted at an IDENTICAL path on the host
# and inside vault-api's container. Always rewritten (not just on a
# fresh install, unlike COMPOSE_PROFILES above) because a moved or
# re-cloned install directory would otherwise leave a stale path behind
# that only fails later, confusingly, inside apply_compose().
CITADEL_HOST_PATH="$(pwd)"
if grep -q "^CITADEL_HOST_PATH=" .env 2>/dev/null; then
    sed -i "s#^CITADEL_HOST_PATH=.*#CITADEL_HOST_PATH=${CITADEL_HOST_PATH}#" .env
else
    echo "CITADEL_HOST_PATH=${CITADEL_HOST_PATH}" >> .env
fi

# Module picker (ROADMAP.md Phase B) -- every module here matches a real
# folder in modules/<name>/, each with its own manifest.json describing
# exactly what it is. This only runs on a truly fresh install (no
# COMPOSE_PROFILES line in .env yet) so re-running install.sh later
# (e.g. after a git pull) never silently resets a real running install's
# module selection back to some default -- that selection already lives
# in .env, which install.sh treats as existing config, not a template to
# regenerate.
#
# Skips the picker entirely in a non-interactive shell (`[ -t 0 ]` is
# false when stdin isn't a real terminal -- a CI runner, a `curl | bash`
# pipe, a Dockerfile RUN step) so automated installs never hang waiting
# on a prompt that can never be answered; those get every module enabled,
# matching this project's behavior before the module picker existed.
MODULE_NAMES=(vigil camera ai knowledge notes hardware audio education recipes)
if ! grep -q "^COMPOSE_PROFILES=" .env 2>/dev/null; then
    if [ -t 0 ]; then
        echo ""
        echo "Which optional modules do you want to run? (each is a separate"
        echo "Docker container, or a small group of them -- see modules/<name>/"
        echo "manifest.json for exactly what each one is.) Answer y/n for each;"
        echo "just press Enter to accept the suggested default."
        echo ""
        SELECTED=()
        for name in "${MODULE_NAMES[@]}"; do
            manifest="modules/$name/manifest.json"
            title="$name"
            requires_hw="false"
            if [ -f "$manifest" ]; then
                title=$(grep -o '"title"[[:space:]]*:[[:space:]]*"[^"]*"' "$manifest" | sed -E 's/.*"title"[[:space:]]*:[[:space:]]*"([^"]*)"/\1/')
                requires_hw=$(grep -o '"requires_hardware"[[:space:]]*:[[:space:]]*[a-z]*' "$manifest" | sed -E 's/.*: *//')
            fi
            # Hardware-dependent modules (a real RTL-SDR dongle, a real
            # webcam) default to "no" -- most people don't have the
            # device yet, and there's nothing this script can check for
            # that's more reliable than just asking honestly.
            default="y"
            prompt_suffix="[Y/n]"
            if [ "$requires_hw" = "true" ]; then
                default="n"
                prompt_suffix="[y/N] (needs real hardware passed through)"
            fi
            read -r -p "  $title ($name) $prompt_suffix: " answer
            answer="${answer:-$default}"
            if [[ "$answer" =~ ^[Yy] ]]; then
                SELECTED+=("$name")
            fi
        done
        PROFILES=$(IFS=,; echo "${SELECTED[*]}")
        if [ -z "$PROFILES" ]; then
            echo "COMPOSE_PROFILES=" >> .env
        else
            echo "COMPOSE_PROFILES=$PROFILES" >> .env
        fi
        echo ""
        echo "Selected modules: ${PROFILES:-(none)}"
    else
        echo "Non-interactive install detected -- enabling every module by"
        echo "default (edit COMPOSE_PROFILES in .env afterward for a lighter"
        echo "install, e.g. a Raspberry Pi)."
        echo "COMPOSE_PROFILES=vigil,ai,knowledge,notes,audio,education,recipes" >> .env
    fi
fi

# Pre-create bind-mount folders so Docker doesn't create them as root, which
# would block you from managing your own files later. Always creates every
# module's folders regardless of which ones were actually selected above --
# harmless (an unused empty folder costs nothing) and means enabling a
# module later via .env, without re-running this script, still works.
mkdir -p appdata/kiwix-library appdata/kolibri_home appdata/ollama appdata/open-webui appdata/flatnotes
mkdir -p appdata/media-vault/videos appdata/media-vault/mp3s appdata/media-vault/pdfs appdata/media-vault/notes-data
mkdir -p appdata/mealie/data appdata/whisper-models appdata/cloud9/data appdata/cloud9/models
mkdir -p backups

echo "Starting Citadel — this pulls a handful of container images the first"
echo "time, so it may take a few minutes..."
docker compose up -d

echo "============================================================"
echo " Citadel is up. Open your dashboard at:"
echo "   http://localhost:8085"
echo "============================================================"
