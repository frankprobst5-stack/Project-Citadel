#!/usr/bin/env bash
# Real, periodic feed-fetch trigger for the News Archive & Local Log
# feature — same thin host-level wrapper pattern as backup-scheduled.sh
# and health-check.sh: this script has no real logic of its own, it just
# triggers vault-api's own /api/news/fetch-due endpoint (which decides
# which sources are actually due) and, once daily, the retention prune.
#
# Runs every 5 minutes via a systemd timer (see install.sh) — that's the
# real cadence hazard sources need (per ROADMAP.md's own fetch-schedule
# decision), not because every run does real work: fetch-due itself is a
# no-op for any source whose next_due_at hasn't passed yet, so a general
# news source set to twice-daily only actually fetches twice a day even
# though this script runs every 5 minutes.

set -euo pipefail

CITADEL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$CITADEL_DIR/.env"
LOG_TAG="citadel-news"

log() { echo "[$LOG_TAG] $(date -u +%Y-%m-%dT%H:%M:%SZ) $*"; }

DASHBOARD_PORT="8085"
if [[ -f "$ENV_FILE" ]]; then
    port_line=$(grep -E "^COCKPIT_PORT=" "$ENV_FILE" 2>/dev/null || true)
    [[ -n "$port_line" ]] && DASHBOARD_PORT="${port_line#COCKPIT_PORT=}"
fi

RESPONSE="$(curl -fsS -X POST "http://localhost:${DASHBOARD_PORT}/api/news/fetch-due")" || {
    log "ERROR: fetch-due request failed — is Citadel running?"
    exit 1
}
log "fetch-due: $RESPONSE"

# Retention prune -- real policy already decided (see ROADMAP.md): once
# daily is plenty, this isn't time-sensitive the way fetching is. A
# simple hour-of-day check keeps this in the same 5-minute timer instead
# of needing a second one just for this.
if [[ "$(date -u +%H%M)" -ge "0300" && "$(date -u +%H%M)" -lt "0305" ]]; then
    PRUNE_RESPONSE="$(curl -fsS -X POST "http://localhost:${DASHBOARD_PORT}/api/news/prune")" || true
    log "prune: $PRUNE_RESPONSE"
fi
