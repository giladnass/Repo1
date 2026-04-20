#!/bin/bash
# Wrapper for transcribe.py -- uses the AI-Ingestion venv automatically.
# Usage: ./transcribe.sh [same flags as transcribe.py]

VENV="${HOME}/AI-Ingestion/venv"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -f "${VENV}/bin/python" ]]; then
    echo "ERROR: venv not found at ${VENV}"
    echo "Run: python3 -m venv ${VENV} && ${VENV}/bin/pip install faster-whisper"
    exit 1
fi

"${VENV}/bin/python" "${SCRIPT_DIR}/transcribe.py" "$@"
