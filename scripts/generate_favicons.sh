#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

python -m pip install --upgrade pip
python -m pip install cairosvg pillow

python scripts/generate_favicons.py
