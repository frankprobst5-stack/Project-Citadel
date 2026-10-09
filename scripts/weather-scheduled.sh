#!/usr/bin/env bash
# Real, periodic weather-fetch trigger for the Master Situation Board --
# same thin host-level wrapper pattern as news-scheduled.sh and
# situation-scheduled.sh. Every 20 minutes: conditions don't change fast
# enough to need News Archive's 5-minute cadence, and NWS's own station
# observations themselves typically update roughly hourly anyway.

set -euo pipefail

CITADEL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$CITADEL_DIR/.env"
LOG_TAG="citadel-weather"

log() { echo "[$LOG_TAG] $(date -u +%Y-%m-%dT%H:%M:%SZ) $*"; }

DASHBOARD_PORT="8085"
VAULT_API_TOKEN=""
if [[ -f "$ENV_FILE" ]]; then
    port_line=$(grep -E "^COCKPIT_PORT=" "$ENV_FILE" 2>/dev/null || true)
    [[ -n "$port_line" ]] && DASHBOARD_PORT="${port_line#COCKPIT_PORT=}"
    token_line=$(grep -E "^VAULT_API_TOKEN=" "$ENV_FILE" 2>/dev/null || true)
    [[ -n "$token_line" ]] && VAULT_API_TOKEN="${token_line#VAULT_API_TOKEN=}"
fi

RESPONSE="$(curl -fsS -X POST -H "X-Vault-Token: ${VAULT_API_TOKEN}" "http://localhost:${DASHBOARD_PORT}/api/weather/refresh")" || {
    log "ERROR: weather refresh request failed — is Citadel running?"
    exit 1
}
log "refresh: $RESPONSE"
