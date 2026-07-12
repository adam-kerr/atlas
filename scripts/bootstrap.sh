#!/usr/bin/env sh
set -eu

command -v uv >/dev/null 2>&1 || {
  echo "uv is required: https://docs.astral.sh/uv/getting-started/installation/" >&2
  exit 1
}

uv sync --dev
uv run atlas doctor
uv run pytest
