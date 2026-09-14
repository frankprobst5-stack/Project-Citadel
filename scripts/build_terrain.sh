#!/usr/bin/env bash
# Builds appdata/cockpit/tiles/terrain/{z}/{x}/{y}.png (the Tactical
# Map's hillshade/elevation-profile layer) for whatever bounding box you
# need, by downloading pre-built terrarium-encoded elevation tiles
# instead of processing raw DEM data ourselves.
#
# Earlier version of this script downloaded raw USGS 3DEP GeoTIFFs and
# ran them through gdalwarp + rio-rgbify to produce terrarium tiles
# locally -- found live 2026-09-13: that pipeline hit a real rio-rgbify/
# GDAL version-compatibility bug (densify_pts=0 rejected by newer GDAL),
# and even after patching that, repeatedly got OOM-killed warping a
# statewide mosaic in parallel workers on a 15GB machine. This version
# sidesteps all of that: "elevation-tiles-prod" (originally a Mapzen
# project, still hosted as an AWS Open Data public dataset) already
# publishes the whole world pre-encoded in the exact terrarium PNG
# scheme map.html expects -- so building the local tileset is just
# "download the tiles for this bounding box," no GDAL/rio-rgbify/local
# DEM processing involved at all. Only tradeoff: this dataset is a
# multi-source blend last globally refreshed in 2017, so it's slightly
# coarser than fresh USGS data -- not visible at the zoom levels this
# hillshade layer actually uses.
#
# Tiles are written as PLAIN {z}/{x}/{y}.png FILES, not packed into a
# .pmtiles archive -- found live 2026-09-13: MapLibre's raster-dem
# tile-fetch path threw "dem dimension mismatch" on every tile when
# served through the pmtiles:// protocol, even though the tile bytes
# themselves were verified correct via direct extraction (the bug is in
# the pmtiles-js protocol layer's handling of raster-dem specifically --
# confirmed against MapLibre's own CHANGELOG, fixed upstream in v6.8.0,
# but that release dropped the classic single-file UMD bundle this
# project vendors in favor of an ESM+worker split, too large a migration
# to take on here). Plain static files sidestep the bug entirely and are
# the more common way to serve raster-dem tiles anyway.
#
# Usage:
#   ./build_terrain.sh <minLon,minLat,maxLon,maxLat> [max-zoom]
#
# Find your own bounding box at https://bboxfinder.com (draw a box over
# your area, copy the numbers in that exact minLon,minLat,maxLon,maxLat
# order). max-zoom defaults to 12 -- this source dataset has no more
# real detail above that anyway.
#
# Example (Texas + New Mexico + Arizona + Oklahoma):
#   ./build_terrain.sh -114.9,25.6,-93.0,37.1
set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <minLon,minLat,maxLon,maxLat> [max-zoom]" >&2
    echo "Find your bounding box at https://bboxfinder.com" >&2
    exit 1
fi

BBOX="$1"
MAX_Z="${2:-12}"

TILES_DIR="/home/frank/citadel/appdata/cockpit/tiles"
# WORKDIR lives OUTSIDE tiles/, not under it: tiles/ ends up root-owned
# (Planetiler's own docker run writes there as root, no host-user write
# access set up for it -- found live 2026-09-13, same issue documented
# in build_basemap.sh), so downloads land in a directory the host user
# actually owns, and only the very last step (moving the finished tree
# into tiles/) touches the root-owned directory, via a throwaway
# container.
WORKDIR="/home/frank/citadel/appdata/cockpit/.terrain-build"
STAGING="$WORKDIR/terrain"
rm -rf "$STAGING"
mkdir -p "$STAGING"

echo "== Downloading terrarium tiles (z0-${MAX_Z}) for bbox ${BBOX} =="
python3 - "$BBOX" "$MAX_Z" "$STAGING" <<'PYEOF'
import concurrent.futures, math, os, sys, urllib.request

bbox, max_z, staging = sys.argv[1], int(sys.argv[2]), sys.argv[3]
min_lon, min_lat, max_lon, max_lat = (float(v) for v in bbox.split(","))

def lonlat_to_tile(lon, lat, z):
    lat = max(min(lat, 85.0511), -85.0511)  # web mercator's valid range
    n = 2 ** z
    x = int((lon + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return max(0, min(n - 1, x)), max(0, min(n - 1, y))

# Only tiles actually inside the bbox get downloaded -- a bounding box
# far from square (like a four-state footprint) would otherwise waste
# real time and space filling in square-zoom-level corners no station
# location ever needs.
tiles = []
for z in range(0, max_z + 1):
    x0, y1 = lonlat_to_tile(min_lon, min_lat, z)  # SW corner -> larger y
    x1, y0 = lonlat_to_tile(max_lon, max_lat, z)  # NE corner -> smaller y
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            tiles.append((z, x, y))

print(f"{len(tiles)} tiles to fetch across z0-{max_z}")

BASE_URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"

def fetch(tile):
    z, x, y = tile
    url = BASE_URL.format(z=z, x=x, y=y)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return tile, r.read()
        except Exception:
            if attempt == 2:
                return tile, None
    return tile, None

done, missing = 0, 0
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
    for (z, x, y), data in pool.map(fetch, tiles):
        done += 1
        if data is None:
            missing += 1
            continue
        out_dir = os.path.join(staging, str(z), str(x))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, f"{y}.png"), "wb") as f:
            f.write(data)
        if done % 2000 == 0:
            print(f"  {done}/{len(tiles)} tiles fetched ({missing} missing so far)")

print(f"Done: {done - missing}/{len(tiles)} tiles written, {missing} missing (ocean/no-data tiles are expected to be missing)")
PYEOF

echo "== Installing into $TILES_DIR/terrain (root-owned; via a throwaway container) =="
docker run --rm -v "$TILES_DIR:/data" -v "$STAGING:/src:ro" \
    alpine:latest sh -c "rm -rf /data/terrain && cp -r /src /data/terrain"

echo "== Cleaning up intermediate files =="
rm -rf "$WORKDIR"

echo "Done: $TILES_DIR/terrain"
find "$TILES_DIR/terrain" -name '*.png' | wc -l | xargs echo "tile count:"
du -sh "$TILES_DIR/terrain"
