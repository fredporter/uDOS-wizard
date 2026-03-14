#!/usr/bin/env bash

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

python3 -m unittest discover -s tests -p 'test_*.py'
