#!/usr/bin/env bash

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON_BIN="$REPO_ROOT/.venv/bin/python"

cd "$REPO_ROOT"

if [ ! -x "$PYTHON_BIN" ]; then
	PYTHON_BIN="python3"
fi

"$PYTHON_BIN" -m unittest discover -s tests -p 'test_*.py'
