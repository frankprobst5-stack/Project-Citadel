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
MODULE_NAMES=(vigil camera ai knowledge notes hardware audio education recipes muster)

# Real Raspberry Pi / ARM detection, ROADMAP.md Phase 1 -- `uname -m` is
# the standard, portable way to ask the kernel what CPU architecture this
# actually is, no /proc/cpuinfo string-matching needed. This only changes
# *suggested defaults* below, never blocks anything -- an operator with a
# beefy ARM server or a Pi they've decided to push hard can still say yes
# to everything, same as choosing "y" against a requires_hardware module
# they don't actually have yet.
IS_ARM="false"
case "$(uname -m)" in
    aarch64|armv7l|armv6l) IS_ARM="true" ;;
esac

if ! grep -q "^COMPOSE_PROFILES=" .env 2>/dev/null; then
    if [ -t 0 ]; then
        echo ""
        echo "Which optional modules do you want to run? (each is a separate"
        echo "Docker container, or a small group of them -- see modules/<name>/"
        echo "manifest.json for exactly what each one is.) Answer y/n for each;"
        echo "just press Enter to accept the suggested default."
        if [ "$IS_ARM" = "true" ]; then
            echo ""
            echo "ARM hardware detected (Raspberry Pi or similar) -- Ollama and"
            echo "Kolibri default to 'no' below, since together they can reserve"
            echo "over 5GB of RAM (see ROADMAP.md Phase 1). Say 'y' anyway if this"
            echo "board genuinely has the RAM to spare."
        fi
        echo ""
        SELECTED=()
        for name in "${MODULE_NAMES[@]}"; do
            manifest="modules/$name/manifest.json"
            title="$name"
            requires_hw="false"
            heavy_on_pi="false"
            if [ -f "$manifest" ]; then
                title=$(grep -o '"title"[[:space:]]*:[[:space:]]*"[^"]*"' "$manifest" | sed -E 's/.*"title"[[:space:]]*:[[:space:]]*"([^"]*)"/\1/')
                requires_hw=$(grep -o '"requires_hardware"[[:space:]]*:[[:space:]]*[a-z]*' "$manifest" | sed -E 's/.*: *//')
                heavy_on_pi=$(grep -o '"heavy_on_pi"[[:space:]]*:[[:space:]]*[a-z]*' "$manifest" | sed -E 's/.*: *//')
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
            elif [ "$heavy_on_pi" = "true" ] && [ "$IS_ARM" = "true" ]; then
                default="n"
                prompt_suffix="[y/N] (heavy -- see ROADMAP.md Phase 1)"
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
        if [ "$IS_ARM" = "true" ]; then
            echo "Non-interactive install detected on ARM hardware -- enabling"
            echo "every module EXCEPT Ollama/Kolibri by default (heavy on a Pi's"
            echo "shared RAM, see ROADMAP.md Phase 1). Edit COMPOSE_PROFILES in"
            echo ".env afterward to add them back if this board can carry it."
            echo "COMPOSE_PROFILES=vigil,knowledge,notes,audio,recipes,muster" >> .env
        else
            echo "Non-interactive install detected -- enabling every module by"
            echo "default (edit COMPOSE_PROFILES in .env afterward for a lighter"
            echo "install, e.g. a Raspberry Pi)."
            echo "COMPOSE_PROFILES=vigil,ai,knowledge,notes,audio,education,recipes,muster" >> .env
        fi
    fi

    # Remote-Ollama-host support, ROADMAP.md v2 backlog -- ollama itself
    # lives under its own "ollama-local" profile now (see
    # modules/ai/compose.fragment.yml), not bundled into "ai"/"education"
    # directly, specifically so it can be left out when a remote host is
    # configured. This only runs as part of the fresh-install picker above
    # (same guard, same "never silently touch an existing real install's
    # module selection" principle) -- add/remove "ollama-local" from
    # COMPOSE_PROFILES by hand afterward if this ever needs to change.
    JUST_SET_PROFILES="$(grep '^COMPOSE_PROFILES=' .env | cut -d= -f2-)"
    OLLAMA_REMOTE="$(grep '^OLLAMA_REMOTE_HOST=' .env 2>/dev/null | cut -d= -f2-)"
    if [[ "$JUST_SET_PROFILES" =~ (^|,)(ai|education)(,|$) ]]; then
        if [ -z "$OLLAMA_REMOTE" ]; then
            sed -i "s/^COMPOSE_PROFILES=.*/COMPOSE_PROFILES=${JUST_SET_PROFILES},ollama-local/" .env
            echo "-- Ollama/education modules selected, no remote host configured --"
            echo "   running Ollama locally (added the 'ollama-local' profile)."
        else
            echo "-- OLLAMA_REMOTE_HOST is set ($OLLAMA_REMOTE) -- Citadel's own local"
            echo "   Ollama container will NOT start; Off-Grid AI/Home Education will"
            echo "   use the remote one instead."
        fi
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

# Real bug, confirmed 2026-09-16 by an actual tester's fresh install
# (Mark, N2UGA): kiwix-serve is told to load `library.xml` (see
# modules/knowledge/compose.fragment.yml's `--library library.xml`),
# and on a fresh install that file doesn't exist at all -- not empty
# of books, genuinely missing -- so kiwix-serve errors out on startup
# and `restart: unless-stopped` just crash-loops it forever. Citadel
# deliberately doesn't ship any .zim content itself (real offline
# archives are often multi-GB and choosing what to download is meant
# to be the operator's own call) -- but it should still start cleanly
# with zero books instead of crash-looping. Verified directly against
# the real kiwix-serve image before writing this: a minimal empty
# library.xml (this exact real schema, not guessed) loads fine --
# "The library was successfully loaded," real HTTP 200, no crash.
if [ ! -f appdata/kiwix-library/library.xml ]; then
    cat > appdata/kiwix-library/library.xml <<'XMLEOF'
<?xml version="1.0" encoding="UTF-8" ?>
<library version="20110515">
</library>
XMLEOF
fi
mkdir -p backups

echo "Starting Citadel — this pulls a handful of container images the first"
echo "time, so it may take a few minutes..."

# Real bug, confirmed 2026-09-16 by an actual tester's report (the
# Windows installer's version of this same gap): this script used to
# print the "Citadel is up" success banner unconditionally, regardless
# of whether `docker compose up -d` actually succeeded -- on his
# machine a mount error meant containers were only *created*, never
# running, while the installer still claimed success. Checking the
# real exit status here, on both platforms, closes that gap instead of
# just on Windows.
if ! docker compose up -d; then
    echo "============================================================"
    echo " docker compose up -d failed -- Citadel is NOT running."
    echo " Scroll up for the real error from Docker, fix it, then run"
    echo " this script again (or just 'docker compose up -d' by hand)."
    echo "============================================================"
    exit 1
fi


# Scheduled nightly backups -- ROADMAP.md v2 backlog: real backup/restore
# already existed (Settings > Backups) but was manual-click-only. A
# user-level systemd timer (not a system one) so this never needs root,
# matching install.sh's existing no-sudo-required posture -- only `docker
# compose up -d` itself needs the operator to already be in the `docker`
# group, same as before this change. Best-effort throughout: a missing
# systemd, a `loginctl enable-linger` failure (needs polkit permission on
# some distros), or any of this failing outright still leaves Citadel
# itself fully up -- backups just stay manual-only, same as before.
if command -v systemctl >/dev/null 2>&1; then
    UNIT_DIR="$HOME/.config/systemd/user"
    mkdir -p "$UNIT_DIR"
    SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/scripts/backup-scheduled.sh"
    chmod +x "$SCRIPT_PATH" 2>/dev/null || true

    cat > "$UNIT_DIR/citadel-backup.service" <<EOF
[Unit]
Description=Citadel scheduled backup

[Service]
Type=oneshot
ExecStart=${SCRIPT_PATH}
EOF

    cat > "$UNIT_DIR/citadel-backup.timer" <<'EOF'
[Unit]
Description=Run Citadel's scheduled backup nightly

[Timer]
OnCalendar=daily
RandomizedDelaySec=30m
Persistent=true

[Install]
WantedBy=timers.target
EOF

    if systemctl --user daemon-reload 2>/dev/null && systemctl --user enable --now citadel-backup.timer 2>/dev/null; then
        loginctl enable-linger "$USER" 2>/dev/null || true
        echo "-- Nightly backup timer installed (systemctl --user status citadel-backup.timer)."
    else
        echo "-- Couldn't install the user-level backup timer (systemd --user unavailable in this"
        echo "   environment) -- backups still work manually via Settings > Backups, or run"
        echo "   scripts/backup-scheduled.sh yourself on whatever schedule you'd like."
    fi

    # Dead-container health check -- ROADMAP.md v2 backlog: this session had
    # two real container-corruption incidents, both root-caused to a single
    # memory-pressure freeze (less likely now thanks to Phase 6's real
    # per-container memory limits, but not impossible) -- catches a repeat
    # proactively rather than by accident during unrelated work. Every 15
    # minutes, not daily like backups -- a dead container is worth knowing
    # about the same hour it happens, not the next morning.
    HEALTH_SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/scripts/health-check.sh"
    chmod +x "$HEALTH_SCRIPT_PATH" 2>/dev/null || true

    cat > "$UNIT_DIR/citadel-health-check.service" <<EOF
[Unit]
Description=Citadel dead-container health check

[Service]
Type=oneshot
ExecStart=${HEALTH_SCRIPT_PATH}
EOF

    cat > "$UNIT_DIR/citadel-health-check.timer" <<'EOF'
[Unit]
Description=Run Citadel's dead-container health check periodically

[Timer]
OnBootSec=5m
OnUnitActiveSec=15m

[Install]
WantedBy=timers.target
EOF

    if systemctl --user daemon-reload 2>/dev/null && systemctl --user enable --now citadel-health-check.timer 2>/dev/null; then
        echo "-- Health check timer installed (systemctl --user status citadel-health-check.timer)."
    else
        echo "-- Couldn't install the user-level health-check timer -- run scripts/health-check.sh"
        echo "   yourself on whatever schedule you'd like instead."
    fi
fi

echo "============================================================"
echo " Citadel is up. Open your dashboard at:"
echo "   http://localhost:8085"
echo "============================================================"
