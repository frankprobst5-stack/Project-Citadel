#!/usr/bin/env bash
# pi-tier-picker — a manifest-driven module picker for Docker Compose stacks,
# with Raspberry Pi / ARM-aware defaults.
#
# Vendored from the standalone github.com/frankprobst5-stack/pi-tier-picker
# (extracted 2026-10-26 from this exact logic, previously hardcoded inline in
# install.sh). This is the generic tool, not a Citadel-specific fork -- update
# by copying pi-tier-picker.sh from that repo, don't hand-edit drift in here.
#
# Problem it solves: a self-hosted Compose stack with optional modules (each
# its own profile) wants to suggest sane defaults on low-RAM ARM boards
# without a maintainer having to hand-edit a hardcoded module list every time
# a module is added. Point it at a directory of modules, each with its own
# manifest.json, and it figures out the rest.
#
# Usage:
#   pi-tier-picker.sh [options]
#
# Options:
#   --modules-dir DIR     Directory containing one subdirectory per module,
#                          each with its own manifest.json. Default: "modules"
#   --non-interactive      Skip all prompts; apply the same default rules a
#                          prompt would have, silently. Also triggered
#                          automatically when stdin isn't a real terminal.
#   --quiet                Suppress the human-readable banner/prompts; only
#                          the final comma-separated profile list is printed.
#   -h, --help              Show this help text.
#
# Output: a single comma-separated list of selected module (profile) names,
# printed to stdout as the last line. Everything else (banner, prompts,
# per-module detection notes) goes to stderr, so `profiles=$(pi-tier-picker.sh)`
# captures only the result.
#
# Manifest schema (per module, modules/<name>/manifest.json):
#   {
#     "title": "Human-readable name",       // optional, falls back to <name>
#     "requires_hardware": false,            // optional, default false
#     "heavy_on_pi": false                   // optional, default false
#   }
#
# Default rules (a prompt can always be overridden by the person running it;
# these are only the *suggested* defaults, interactive or not):
#   requires_hardware=true           -> default "no" (most people don't have
#                                        the device yet, nothing else can
#                                        reliably detect that)
#   heavy_on_pi=true AND on ARM       -> default "no" (RAM-constrained)
#   otherwise                        -> default "yes"
#
# ARM detection is the standard, portable `uname -m` check (aarch64, armv7l,
# armv6l). Override it for testing with PI_TIER_PICKER_FORCE_ARM=true|false.

set -euo pipefail

MODULES_DIR="modules"
NON_INTERACTIVE="false"
QUIET="false"

while [ $# -gt 0 ]; do
    case "$1" in
        --modules-dir)
            MODULES_DIR="$2"
            shift 2
            ;;
        --non-interactive)
            NON_INTERACTIVE="true"
            shift
            ;;
        --quiet)
            QUIET="true"
            shift
            ;;
        -h|--help)
            sed -n '2,42p' "$0" | sed 's/^# \{0,1\}//'
            exit 0
            ;;
        *)
            echo "pi-tier-picker: unknown option: $1" >&2
            exit 1
            ;;
    esac
done

say() {
    if [ "$QUIET" != "true" ]; then
        echo "$@" >&2
    fi
}

if [ ! -d "$MODULES_DIR" ]; then
    echo "pi-tier-picker: modules directory not found: $MODULES_DIR" >&2
    exit 1
fi

# ARM / Raspberry-Pi-class detection. PI_TIER_PICKER_FORCE_ARM exists purely
# for testing (and for an operator who knows better than uname -m, same
# escape hatch Citadel's own install.sh gives via just answering "y" anyway).
if [ -n "${PI_TIER_PICKER_FORCE_ARM:-}" ]; then
    IS_ARM="$PI_TIER_PICKER_FORCE_ARM"
else
    IS_ARM="false"
    case "$(uname -m)" in
        aarch64|armv7l|armv6l) IS_ARM="true" ;;
    esac
fi

# Auto-discover modules: any subdirectory of MODULES_DIR containing a
# manifest.json, sorted for determinism. This is the one real difference
# from a hand-maintained array of module names — add a module by adding its
# directory, nothing else to remember to update. `-L` so a MODULES_DIR (or
# a module directory inside it) that's itself a symlink -- e.g. shared
# across repos -- still gets traversed; plain `find` won't descend through
# one by default (found the hard way, testing against a symlinked dir).
MODULE_NAMES=()
while IFS= read -r -d '' manifest; do
    MODULE_NAMES+=("$(basename "$(dirname "$manifest")")")
done < <(find -L "$MODULES_DIR" -mindepth 2 -maxdepth 2 -name manifest.json -print0 | sort -z)

if [ "${#MODULE_NAMES[@]}" -eq 0 ]; then
    echo "pi-tier-picker: no modules found under $MODULES_DIR (expected $MODULES_DIR/<name>/manifest.json)" >&2
    exit 1
fi

if [ "$NON_INTERACTIVE" != "true" ] && [ ! -t 0 ]; then
    NON_INTERACTIVE="true"
fi

say "============================================================"
say " pi-tier-picker"
say "============================================================"
if [ "$IS_ARM" = "true" ]; then
    say "ARM hardware detected (Raspberry Pi or similar) -- modules marked"
    say "\"heavy_on_pi\" default to 'no' below."
fi
if [ "$NON_INTERACTIVE" = "true" ]; then
    say "Non-interactive -- applying suggested defaults without prompting."
else
    say "Answer y/n for each module; press Enter to accept the default."
fi
say ""

json_field() {
    # Tiny, dependency-free JSON scalar read: good enough for this manifest's
    # flat string/bool fields, not a general JSON parser. A field that's
    # simply absent (most modules won't set heavy_on_pi, say) makes grep
    # exit 1 with no match -- `|| true` keeps that from tripping `set -e`
    # under `pipefail` and killing the whole picker over a normal, expected
    # case (found the hard way: it fails silently, no error message at all).
    local manifest="$1" field="$2" result
    result="$(grep -o "\"$field\"[[:space:]]*:[[:space:]]*\"\{0,1\}[^\",}]*\"\{0,1\}" "$manifest" 2>/dev/null \
        | sed -E "s/.*\"$field\"[[:space:]]*:[[:space:]]*\"?([^\",}]*)\"?.*/\1/" \
        | head -1)" || true
    printf '%s' "$result"
}

SELECTED=()
for name in "${MODULE_NAMES[@]}"; do
    manifest="$MODULES_DIR/$name/manifest.json"
    title="$(json_field "$manifest" title)"
    [ -z "$title" ] && title="$name"
    requires_hw="$(json_field "$manifest" requires_hardware)"
    heavy_on_pi="$(json_field "$manifest" heavy_on_pi)"

    default="y"
    prompt_suffix="[Y/n]"
    if [ "$requires_hw" = "true" ]; then
        default="n"
        prompt_suffix="[y/N] (needs real hardware)"
    elif [ "$heavy_on_pi" = "true" ] && [ "$IS_ARM" = "true" ]; then
        default="n"
        prompt_suffix="[y/N] (heavy on Pi-class hardware)"
    fi

    if [ "$NON_INTERACTIVE" = "true" ]; then
        answer="$default"
    else
        read -r -p "  $title ($name) $prompt_suffix: " answer
        answer="${answer:-$default}"
    fi

    if [[ "$answer" =~ ^[Yy] ]]; then
        SELECTED+=("$name")
    fi
done

PROFILES=$(IFS=,; echo "${SELECTED[*]}")
say ""
say "Selected: ${PROFILES:-(none)}"
echo "$PROFILES"
