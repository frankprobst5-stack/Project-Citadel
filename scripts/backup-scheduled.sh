#!/usr/bin/env bash
# Real, scheduled nightly backup — ROADMAP.md's own v2 backlog item.
#
# Real backup/restore already existed (Settings > Backups, Phase G) but was
# manual-click-only and landed on the same disk as everything else — a
# genuine single point of failure if that disk dies. This closes both real
# gaps named in the backlog: (1) a scheduled snapshot, and (2) an optional
# mirror step to a second physical drive or NAS path.
#
# Deliberately a thin host-level wrapper around the EXISTING, already-tested
# backup logic (backup.py's create_backup(), exposed as POST
# /api/backup/create) rather than a second implementation — this script
# only triggers that real endpoint and, if configured, mirrors the result.
# Runs via a systemd timer (see citadel-backup.timer/.service below), not
# cron — this project's own convention elsewhere (Undercroft's boot-console
# unit, its update-check timer) already prefers systemd units for anything
# host-level, one less scheduling mechanism to reason about.

set -euo pipefail

CITADEL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$CITADEL_DIR/.env"
LOG_TAG="citadel-backup"

log() { echo "[$LOG_TAG] $(date -u +%Y-%m-%dT%H:%M:%SZ) $*"; }

# Cockpit's own nginx already proxies /api/backup/* to vault-api
# (appdata/cockpit/nginx.conf) — vault-api itself has no port mapped
# directly to the host, so 8085 (the one real, documented entry point) is
# the correct address here, not a container-internal one.
DASHBOARD_PORT="8085"
if [[ -f "$ENV_FILE" ]]; then
    port_line=$(grep -E "^COCKPIT_PORT=" "$ENV_FILE" 2>/dev/null || true)
    [[ -n "$port_line" ]] && DASHBOARD_PORT="${port_line#COCKPIT_PORT=}"
fi

log "Triggering backup via http://localhost:${DASHBOARD_PORT}/api/backup/create"
RESPONSE="$(curl -fsS -X POST "http://localhost:${DASHBOARD_PORT}/api/backup/create")" || {
    log "ERROR: backup request failed — is Citadel running? (docker compose ps)"
    exit 1
}
log "Backup created: $RESPONSE"

# Optional off-machine mirror — real second gap named in the backlog. Only
# runs if BACKUP_MIRROR_PATH is actually set in .env; otherwise this script
# still did its real job (a scheduled on-disk snapshot) and exits cleanly.
MIRROR_PATH=""
if [[ -f "$ENV_FILE" ]]; then
    mirror_line=$(grep -E "^BACKUP_MIRROR_PATH=" "$ENV_FILE" 2>/dev/null || true)
    MIRROR_PATH="${mirror_line#BACKUP_MIRROR_PATH=}"
fi

if [[ -n "$MIRROR_PATH" ]]; then
    if [[ ! -d "$MIRROR_PATH" ]]; then
        log "WARNING: BACKUP_MIRROR_PATH ($MIRROR_PATH) doesn't exist or isn't mounted — skipping mirror this run, on-disk backup already succeeded above."
    elif ! command -v rsync >/dev/null 2>&1; then
        log "WARNING: rsync not installed on the host — skipping mirror. Install it (apt install rsync) to enable off-machine mirroring."
    else
        log "Mirroring $CITADEL_DIR/backups/ to $MIRROR_PATH"
        rsync -a --delete "$CITADEL_DIR/backups/" "$MIRROR_PATH/"
        log "Mirror complete."
    fi
else
    log "No BACKUP_MIRROR_PATH set in .env — on-disk backup only (see .env.example to enable off-machine mirroring)."
fi
