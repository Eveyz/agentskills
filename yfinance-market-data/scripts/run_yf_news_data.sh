#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/yf_news_data.py"
UV_PROJECT_ROOT="${UV_PROJECT_ROOT:-/home/znz/project/hedgefund}"
CONDA_ENV_NAME="${CONDA_ENV_NAME:-finance}"

if [[ -n "${VIRTUAL_ENV:-}" && -x "$VIRTUAL_ENV/bin/python" ]]; then
    exec "$VIRTUAL_ENV/bin/python" "$PYTHON_SCRIPT" "$@"
fi

if [[ -x "$UV_PROJECT_ROOT/.venv/bin/python" ]]; then
    exec "$UV_PROJECT_ROOT/.venv/bin/python" "$PYTHON_SCRIPT" "$@"
fi

if command -v uv >/dev/null 2>&1 && [[ -d "$UV_PROJECT_ROOT" ]]; then
    exec uv run --project "$UV_PROJECT_ROOT" python "$PYTHON_SCRIPT" "$@"
fi

if command -v conda >/dev/null 2>&1; then
    exec conda run -n "$CONDA_ENV_NAME" python "$PYTHON_SCRIPT" "$@"
fi

echo "No compatible Python runtime found. Tried \$VIRTUAL_ENV, $UV_PROJECT_ROOT/.venv, uv project $UV_PROJECT_ROOT, and conda env $CONDA_ENV_NAME." >&2
exit 1
