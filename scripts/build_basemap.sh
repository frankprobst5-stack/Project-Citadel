#!/usr/bin/env bash
# Builds appdata/cockpit/tiles/comms_base.pmtiles (the Tactical Map's
# roads/labels/water vector layer) from an OpenStreetMap extract, for
# whatever region you actually live in -- not hardcoded to any one state.
#
# Uses the "protomaps-basemap" Planetiler profile (github.com/protomaps/
# basemaps), NOT generic Planetiler's default OpenMapTiles profile --
# found live 2026-09-13: map.html styles the basemap with
# protomaps-themes-base, which is built specifically for Protomaps' own
# tile schema (layer names like "roads", "places", "earth"). Generic
# Planetiler's default profile produces the different, superficially
# similar "OpenMapTiles" schema (layer names like "transportation",
# "place", "landcover") -- the data built and rendered without any
# error, but the style's layer definitions silently matched almost
# nothing (source-layer: "roads" against data that only had a
# "transportation" layer), so roads/labels never painted. Confirmed with
# a minimal from-scratch test page: the exact same file rendered
# perfectly with hand-written layers referencing the real layer names,
# proving the DATA was correct and the schema mismatch was the actual
# bug. No pre-built image exists for this profile, so this script builds
# it from source (Java/Maven, entirely inside Docker) the first time.
#
# Planetiler can resolve a short area name (e.g. "texas") to a download
# URL itself via Geofabrik's own index, but that index lookup has a
# short, non-configurable timeout and is a known source of flaky
# failures on slower connections -- found live 2026-09-13. Sidestepping
# it by downloading the .osm.pbf directly is more reliable, so this
# script takes the actual extract (a URL or a local file), not an area
# name.
#
# Usage:
#   ./build_basemap.sh <osm-pbf-url-or-local-path> [output-filename]
#
# Find your own region's extract at https://download.geofabrik.de --
# browse to your continent/country/state and copy the ".osm.pbf" link
# (right-click -> copy link, or just note the URL from the page).
#
# Examples:
#   ./build_basemap.sh https://download.geofabrik.de/north-america/us/texas-latest.osm.pbf
#   ./build_basemap.sh https://download.geofabrik.de/europe/germany-latest.osm.pbf germany_base.pmtiles
#   ./build_basemap.sh /home/me/downloads/already-fetched.osm.pbf
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <osm-pbf-url-or-local-path> [output-filename]" >&2
    echo "Find your region's .osm.pbf at https://download.geofabrik.de" >&2
    exit 1
fi

SOURCE="$1"
OUTPUT_NAME="${2:-comms_base.pmtiles}"
TILES_DIR="/home/frank/citadel/appdata/cockpit/tiles"
mkdir -p "$TILES_DIR"

# Planetiler's own docker run (below) writes into TILES_DIR as root
# (containers default to root, and TILES_DIR has no host-user write
# access set up for it) -- found live 2026-09-13: that left every file
# in here root-owned, so plain host-side commands (wget, mkdir) against
# this same directory failed outright with "Permission denied", and
# `sudo` isn't usable non-interactively here. Routing every write into
# TILES_DIR through a throwaway container instead sidesteps needing host
# write access at all, and stays consistent with how Planetiler already
# touches this directory. Used for every filesystem change below, not
# just the download, since the *directory itself* is root-owned, not
# just individual files in it.
DOCKER_TILES() { docker run --rm -v "$TILES_DIR:/data" -w /data alpine:latest "$@"; }

if [[ "$SOURCE" == http://* || "$SOURCE" == https://* ]]; then
    PBF_FILENAME="$(basename "$SOURCE")"
    PBF_PATH="$TILES_DIR/$PBF_FILENAME"

    # Found live 2026-09-13: a stale/wrong file already sitting at
    # PBF_PATH (e.g. left over from an earlier failed attempt) makes
    # `wget -c` silently resume by appending real bytes onto garbage --
    # wget only checks the byte offset, never the content, so the result
    # is a corrupted file that's the right SIZE but wrong DATA, and
    # everything downstream (Planetiler) processes it without complaint.
    # Rather than trust a leftover file, check what the server actually
    # reports before deciding whether resuming makes sense.
    EXPECTED_SIZE="$(curl -sIL "$SOURCE" | grep -i '^content-length:' | tail -1 | tr -d '\r' | awk '{print $2}')"
    SKIP_DOWNLOAD=false
    if [ -f "$PBF_PATH" ] && [ -n "$EXPECTED_SIZE" ]; then
        ACTUAL_SIZE="$(stat -c%s "$PBF_PATH")"
        if [ "$ACTUAL_SIZE" == "$EXPECTED_SIZE" ]; then
            echo "$PBF_PATH already matches the server's reported size ($EXPECTED_SIZE bytes) -- skipping re-download."
            SKIP_DOWNLOAD=true
        elif [ "$ACTUAL_SIZE" -gt "$EXPECTED_SIZE" ]; then
            echo "Existing $PBF_PATH is larger than the real extract -- removing stale file before downloading."
            DOCKER_TILES rm -f "/data/$PBF_FILENAME"
        fi
    fi

    if [ "$SKIP_DOWNLOAD" = false ]; then
        # BusyBox's wget (in the alpine image) doesn't reliably resume a
        # partial download against Geofabrik's redirects -- found live
        # 2026-09-13 ("wget: restart failed", then it silently restarted
        # from 0% instead of erroring). Harmless since the size gets
        # re-verified below either way, just slower than a real resume.
        echo "== Downloading $SOURCE =="
        DOCKER_TILES wget -c -O "/data/$PBF_FILENAME" "$SOURCE"

        if [ -n "$EXPECTED_SIZE" ]; then
            ACTUAL_SIZE="$(stat -c%s "$PBF_PATH")"
            if [ "$ACTUAL_SIZE" != "$EXPECTED_SIZE" ]; then
                echo "ERROR: downloaded file is ${ACTUAL_SIZE} bytes, server reported ${EXPECTED_SIZE} bytes." >&2
                echo "Refusing to build from a mismatched/corrupt download -- delete $PBF_PATH and re-run." >&2
                exit 1
            fi
        fi
    fi
else
    if [ ! -f "$SOURCE" ]; then
        echo "No such file: $SOURCE" >&2
        exit 1
    fi
    # Planetiler (below) only sees paths under TILES_DIR (that's the one
    # directory mounted into its container) -- a local file living
    # elsewhere has to be copied in first, not just referenced by path.
    PBF_FILENAME="$(basename "$SOURCE")"
    PBF_PATH="$TILES_DIR/$PBF_FILENAME"
    if [ "$(readlink -f "$SOURCE")" != "$(readlink -f "$PBF_PATH" 2>/dev/null || true)" ]; then
        echo "== Copying $SOURCE into $TILES_DIR =="
        docker run --rm -v "$TILES_DIR:/data" -v "$(dirname "$(readlink -f "$SOURCE")"):/src:ro" \
            alpine:latest cp "/src/$(basename "$SOURCE")" "/data/$PBF_FILENAME"
    fi
fi

# A real regional extract is always well over 1MB -- this is the same
# category of mistake that happened live 2026-09-13 (Planetiler silently
# fell back to its built-in Monaco demo default and produced a
# ~700KB/246-tile map instead of the intended state-wide one). Catching
# it here means a bad input fails loudly before burning CPU time on a
# build instead of silently producing a tiny, wrong map.
PBF_SIZE="$(stat -c%s "$PBF_PATH")"
if [ "$PBF_SIZE" -lt 1000000 ]; then
    echo "ERROR: $PBF_PATH is only ${PBF_SIZE} bytes -- too small to be a real regional extract." >&2
    echo "Refusing to build comms_base.pmtiles from this file." >&2
    exit 1
fi

# download_dir/tmpdir default to paths inside the container's own
# throwaway filesystem (only /data is mounted to the host), so every
# `docker run --rm` re-downloads natural_earth/water_polygons/
# lake_centerlines from scratch -- found live 2026-09-13: ~1.4GB and
# 30+ minutes wasted on a run that didn't even use the right OSM data.
# Pointing them at /data keeps that cache across re-runs.
DOCKER_TILES mkdir -p /data/.planetiler-cache /data/.planetiler-tmp

PROTOMAPS_IMAGE="protomaps-basemap:local"
if ! docker image inspect "$PROTOMAPS_IMAGE" >/dev/null 2>&1; then
    echo "== Building the protomaps-basemap image (one-time; no pre-built image is published) =="
    BUILD_DIR="$(mktemp -d)"
    git clone --depth 1 https://github.com/protomaps/basemaps.git "$BUILD_DIR/basemaps"
    docker build -t "$PROTOMAPS_IMAGE" "$BUILD_DIR/basemaps/tiles"
    rm -rf "$BUILD_DIR"
fi

CONTAINER_PBF="/data/$(basename "$PBF_PATH")"
echo "== Running Planetiler (protomaps-basemap profile) =="
docker run --rm -v "$TILES_DIR:/data" \
    "$PROTOMAPS_IMAGE" \
    --download --osm-path="$CONTAINER_PBF" \
    --download_dir=/data/.planetiler-cache \
    --tmpdir=/data/.planetiler-tmp \
    --force \
    --output="/data/$OUTPUT_NAME"

echo "Done: $TILES_DIR/$OUTPUT_NAME"
ls -lh "$TILES_DIR/$OUTPUT_NAME"
