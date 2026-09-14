#!/usr/bin/env bash
# CITADEL — one-line bootstrap for a brand-new machine, meant to be run
# straight from GitHub: curl -fsSL <raw-url-to-this-file> | bash
#
# Deliberately tiny and readable start to finish (no piped-in binaries,
# nothing beyond curl+unzip+cd) -- since piping a script straight into
# bash means trusting it sight-unseen, this stays short enough to
# actually read in the ten seconds before you run it. It does exactly
# one job: fetch this repo and hand off to the real installer
# (install.sh), which is the same script anyone downloading the zip by
# hand would run -- this file adds no install logic of its own.
set -e

REPO_URL="https://github.com/frankprobst5-stack/Project-Citadel"
ARCHIVE_URL="$REPO_URL/archive/refs/heads/main.zip"
DEST="${CITADEL_INSTALL_DIR:-$HOME/citadel}"

echo "============================================================"
echo " PROJECT CITADEL — one-line installer"
echo "============================================================"

if ! command -v curl >/dev/null 2>&1; then
    echo "curl isn't installed -- install it first (it ships by default on"
    echo "most Linux distros and macOS), then run this again."
    exit 1
fi

if [ -d "$DEST" ]; then
    echo "$DEST already exists -- if that's a previous Citadel install,"
    echo "just run its own install.sh again instead of this bootstrap:"
    echo "  cd $DEST && ./install.sh"
    echo "To install fresh somewhere else instead, set CITADEL_INSTALL_DIR:"
    echo "  CITADEL_INSTALL_DIR=~/citadel2 curl -fsSL <this-script-url> | bash"
    exit 1
fi

TMPZIP="$(mktemp -t citadel-XXXXXX.zip)"
trap 'rm -f "$TMPZIP"' EXIT

echo "Downloading Citadel from $REPO_URL ..."
curl -fsSL -o "$TMPZIP" "$ARCHIVE_URL"

echo "Extracting to $DEST ..."
# Only the PARENT needs to exist here, not $DEST itself -- the `mv`
# below renames GitHub's extracted Project-Citadel-main/ to $DEST, which
# only works as a rename if $DEST doesn't already exist (a real bug
# caught live: pre-creating $DEST with mkdir made `mv` nest the
# extracted folder INSIDE it instead of renaming it).
mkdir -p "$(dirname "$DEST")"
if command -v unzip >/dev/null 2>&1; then
    unzip -q "$TMPZIP" -d "$(dirname "$DEST")"
else
    # Alpine/minimal images sometimes lack unzip but always have python3
    # or bsdtar -- fall back rather than making unzip a hard requirement
    # for what's otherwise a curl-only bootstrap.
    if command -v bsdtar >/dev/null 2>&1; then
        bsdtar -xf "$TMPZIP" -C "$(dirname "$DEST")"
    elif command -v python3 >/dev/null 2>&1; then
        python3 -c "import zipfile,sys; zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$TMPZIP" "$(dirname "$DEST")"
    else
        echo "Need unzip, bsdtar, or python3 to extract the download -- install"
        echo "any one of those, then run this again."
        exit 1
    fi
fi
# GitHub's archive zip extracts to Project-Citadel-main/, not the plain
# $DEST name -- rename so CITADEL_HOST_PATH (written by install.sh) and
# every doc's "cd ~/citadel" instruction still point at a stable path.
mv "$(dirname "$DEST")/Project-Citadel-main" "$DEST"

echo ""
echo "Handing off to Citadel's own installer ($DEST/install.sh) ..."
echo ""
cd "$DEST"
chmod +x install.sh
exec ./install.sh
