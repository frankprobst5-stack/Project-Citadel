#!/usr/bin/env bash
# Real, periodic dead-container health check — ROADMAP.md's own v2 backlog
# item. Real motivation: this session had two real container-corruption
# incidents, both root-caused to a single memory-pressure freeze (now less
# likely thanks to Phase 6's real per-container memory limits, but not
# impossible) — this exists to catch a repeat proactively, rather than
# stumbling into it by accident during unrelated work.
#
# Deliberately narrow scope, matching the backlog item's own "optional, low
# priority" framing: checks for Docker's own real "dead" status (a
# container whose process died during a resource-allocation failure, a
# distinct real state from a normal exit or a healthy "running" one — not
# guessed at, `docker ps`'s own documented status values), logs clearly
# either way, and writes a small status file so a dashboard could surface
# it later without needing to invent that integration today.

set -euo pipefail

CITADEL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATUS_FILE="$CITADEL_DIR/appdata/health-check-status.json"
LOG_TAG="citadel-health-check"

log() { echo "[$LOG_TAG] $(date -u +%Y-%m-%dT%H:%M:%SZ) $*"; }

DEAD_CONTAINERS="$(docker ps -a --filter "status=dead" --format "{{.Names}}" 2>&1)" || {
    log "ERROR: couldn't query Docker — is the daemon running?"
    exit 1
}

TIMESTAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
mkdir -p "$(dirname "$STATUS_FILE")"

if [[ -z "$DEAD_CONTAINERS" ]]; then
    log "OK — no dead containers found."
    cat > "$STATUS_FILE" <<EOF
{"status": "ok", "dead_containers": [], "checked_at": "$TIMESTAMP"}
EOF
else
    # Loud on purpose -- this is exactly the "caught proactively instead of
    # by accident" moment the backlog item asked for, so it goes to stderr
    # (visible via `systemctl status`/`journalctl`, not buried in a log
    # file nobody's watching) in addition to the status file.
    log "ALERT: dead container(s) found: $DEAD_CONTAINERS" >&2
    NAMES_JSON="$(echo "$DEAD_CONTAINERS" | awk 'BEGIN{ORS=""} {printf "%s\"%s\"", (NR>1?", ":""), $0}')"
    cat > "$STATUS_FILE" <<EOF
{"status": "alert", "dead_containers": [$NAMES_JSON], "checked_at": "$TIMESTAMP"}
EOF
fi
