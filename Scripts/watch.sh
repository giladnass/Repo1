#!/bin/bash
# watch.sh -- Watch the source folder and convert new files as they arrive.
#
# Requires: fswatch (brew install fswatch)
#
# Usage:
#   chmod +x watch.sh
#   ./watch.sh
#   ./watch.sh --source ~/Dropbox/ToIngest --output ~/AI-Ingestion/02-converted
#
# To run as a background process that survives terminal close:
#   nohup ./watch.sh > ~/AI-Ingestion/watch.log 2>&1 &

set -euo pipefail

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

if ! command -v fswatch &>/dev/null; then
    echo "ERROR: fswatch not found. Install with: brew install fswatch"
    exit 1
fi

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found."
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Watching: ${SOURCE_DIR}"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Output:   ${OUTPUT_DIR}"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Press Ctrl+C to stop."

mkdir -p "${OUTPUT_DIR}"

fswatch -0 --event Created --event Renamed --event MovedTo "${SOURCE_DIR}" \
| while IFS= read -r -d '' file; do
    # Only process supported file types
    ext="${file##*.}"
    case "${ext,,}" in
        pdf|docx|epub|pptx|odt|rtf|html)
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] New file: ${file}"
            python3 "${INGEST_SCRIPT}" \
                --file "${file}" \
                --output "${OUTPUT_DIR}"
            ;;
        *)
            # Ignore other file types silently
            ;;
    esac
done
