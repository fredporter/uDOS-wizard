#!/usr/bin/env bash

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SHARED_PYTHON_BIN="${UDOS_SHARED_PYTHON_BIN:-}"
USE_SHARED_RESOURCES="${UDOS_USE_SHARED_RESOURCES:-1}"
VENV_DIR="${UDOS_VENV_DIR:-$HOME/.udos/venv/wizard}"
PYTHON_BIN="$VENV_DIR/bin/python"
TEST_STATE_ROOT="${REPO_ROOT}/.tmp/state"

cd "$REPO_ROOT"
mkdir -p "$VENV_DIR"

export UDOS_STATE_ROOT="${UDOS_STATE_ROOT:-$TEST_STATE_ROOT}"
export WIZARD_STATE_ROOT="${WIZARD_STATE_ROOT:-$UDOS_STATE_ROOT/wizard}"
export UDOS_RENDER_ROOT="${UDOS_RENDER_ROOT:-$UDOS_STATE_ROOT/rendered}"
export WIZARD_RESULT_STORE_PATH="${WIZARD_RESULT_STORE_PATH:-$WIZARD_STATE_ROOT/orchestration-results.json}"
mkdir -p "$WIZARD_STATE_ROOT" "$UDOS_RENDER_ROOT"

if [ "$USE_SHARED_RESOURCES" = "1" ] && [ -z "$SHARED_PYTHON_BIN" ]; then
  FAMILY_HELPER="$REPO_ROOT/../scripts/lib/family-python.sh"
  if [ -f "$FAMILY_HELPER" ]; then
    # shellcheck source=/dev/null
    . "$FAMILY_HELPER"
    ensure_shared_python
    SHARED_PYTHON_BIN="${UDOS_SHARED_PYTHON_BIN:-}"
  fi
fi

if [ -n "$SHARED_PYTHON_BIN" ] && [ -x "$SHARED_PYTHON_BIN" ]; then
  PYTHON_BIN="$SHARED_PYTHON_BIN"
elif [ ! -x "$PYTHON_BIN" ]; then
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
