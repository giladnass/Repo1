#!/bin/bash
# watch.sh -- Watch the source folder and convert new files as they arrive.
#
# Requires: fswatch (brew install fswatch)
#
# Runs as a LaunchAgent for auto-start on login. See:
#   ~/Library/LaunchAgents/com.giladnass.ai-memory-watcher.plist
#
# Usage (manual):
#   ./watch.sh
#   ./watch.sh --source ~/Dropbox/ToIngest --output ~/AI-Ingestion/02-converted

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${HOME}/AI-Ingestion/01-source"
OUTPUT_DIR="${HOME}/AI-Ingestion/02-converted"
INGEST_SCRIPT="${SCRIPT_DIR}/ingest.py"

# Parse optional overrides
while [[ $# -gt 0 ]]; do
    case "$1" in
        --source) SOURCE_DIR="$2"; shift 2 ;;
        --output) OUTPUT_DIR="$2"; shift 2 ;;
        *) echo "Unknown argument: $1"; exit 1 ;;
    esac
done

notify() {
    local title="$1"
    local message="$2"
    local sound="${3:-}"
    if [[ -n "$sound" ]]; then
        osascript -e "display notification \"${message}\" with title \"${title}\" sound name \"${sound}\"" 2>/dev/null || true
    else
        osascript -e "display notification \"${message}\" with title \"${title}\"" 2>/dev/null || true
    fi
}

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# Notify on unexpected exit
trap 'notify "AI Memory Watcher" "Watcher stopped unexpectedly. Check ~/AI-Ingestion/watch-error.log" "Basso"' EXIT

if ! command -v fswatch &>/dev/null; then
    notify "AI Memory Watcher" "ERROR: fswatch not found. Install with: brew install fswatch" "Basso"
    log "ERROR: fswatch not found. Install with: brew install fswatch"
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    notify "AI Memory Watcher" "ERROR: python3 not found." "Basso"
    log "ERROR: python3 not found."
    exit 1
fi

mkdir -p "${OUTPUT_DIR}"

log "Watching: ${SOURCE_DIR}"
log "Output:   ${OUTPUT_DIR}"

notify "AI Memory Watcher" "Watcher started. Monitoring ${SOURCE_DIR}"

fswatch -0 --event Created --event Renamed --event MovedTo "${SOURCE_DIR}" \
| while IFS= read -r -d '' file; do
    ext="$(echo "${file##*.}" | tr '[:upper:]' '[:lower:]')"
    case "${ext}" in
        pdf|docx|epub|pptx|odt|rtf|html)
            log "New file: ${file}"
            if python3 "${INGEST_SCRIPT}" --file "${file}" --output "${OUTPUT_DIR}" 2>&1; then
                notify "AI Memory Watcher" "Converted: $(basename "${file}")"
            else
                notify "AI Memory Watcher" "Conversion failed: $(basename "${file}"). Check ~/AI-Ingestion/watch-error.log" "Basso"
                log "ERROR: conversion failed for ${file}"
            fi
            ;;
        *)
            ;;
    esac
done
