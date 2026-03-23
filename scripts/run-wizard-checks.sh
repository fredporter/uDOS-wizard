#!/usr/bin/env bash

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="$REPO_ROOT/.venv"
PYTHON_BIN="$VENV_DIR/bin/python"

cd "$REPO_ROOT"

if [ ! -x "$PYTHON_BIN" ]; then
  if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 is required to create $VENV_DIR" >&2
    exit 1
  fi

  if ! python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
    echo "python3.11+ is required to bootstrap $VENV_DIR for uDOS-wizard" >&2
    exit 1
  fi

  python3 -m venv "$VENV_DIR"
  "$PYTHON_BIN" -m pip install --upgrade pip setuptools wheel
  "$PYTHON_BIN" -m pip install -e .
fi

if ! "$PYTHON_BIN" -c 'import wizard' >/dev/null 2>&1; then
  "$PYTHON_BIN" -m pip install -e .
fi

"$PYTHON_BIN" -m unittest discover -s tests -p 'test_*.py'
