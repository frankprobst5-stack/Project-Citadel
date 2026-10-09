#!/usr/bin/env bash
# Real, periodic feed-fetch trigger for the Global Situation Monitor --
# same thin host-level wrapper pattern as news-scheduled.sh and
# backup-scheduled.sh: no real logic of its own, just triggers vault-
# api's own /api/situation/fetch-due endpoint (which decides which
# sources are actually due) and, once daily, the retention prune.
#
# Runs every 15 minutes via a systemd timer (see install.sh) -- lower
# urgency than News Archive's hazard sources (no 5-minute NWS-grade
# near-real-time need here), but frequent enough that a fast-moving
# story doesn't sit for hours before showing up on the timeline.

set -euo pipefail

CITADEL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$CITADEL_DIR/.env"
LOG_TAG="citadel-situation"

log() { echo "[$LOG_TAG] $(date -u +%Y-%m-%dT%H:%M:%SZ) $*"; }

DASHBOARD_PORT="8085"
VAULT_API_TOKEN=""
if [[ -f "$ENV_FILE" ]]; then
    port_line=$(grep -E "^COCKPIT_PORT=" "$ENV_FILE" 2>/dev/null || true)
    [[ -n "$port_line" ]] && DASHBOARD_PORT="${port_line#COCKPIT_PORT=}"
    token_line=$(grep -E "^VAULT_API_TOKEN=" "$ENV_FILE" 2>/dev/null || true)
    [[ -n "$token_line" ]] && VAULT_API_TOKEN="${token_line#VAULT_API_TOKEN=}"
fi

RESPONSE="$(curl -fsS -X POST -H "X-Vault-Token: ${VAULT_API_TOKEN}" "http://localhost:${DASHBOARD_PORT}/api/situation/fetch-due")" || {
    log "ERROR: fetch-due request failed — is Citadel running?"
    exit 1
}
log "fetch-due: $RESPONSE"

# Retention prune -- same once-daily cadence and reasoning as News
# Archive's own prune (see news-scheduled.sh).
if [[ "$(date -u +%H%M)" -ge "0310" && "$(date -u +%H%M)" -lt "0315" ]]; then
    PRUNE_RESPONSE="$(curl -fsS -X POST -H "X-Vault-Token: ${VAULT_API_TOKEN}" "http://localhost:${DASHBOARD_PORT}/api/situation/prune")" || true
    log "prune: $PRUNE_RESPONSE"
fi
