#!/bin/sh
set -eu

is_true() {
    case "${1:-}" in
        1|true|TRUE|True|yes|YES|y|Y|on|ON)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

sync_python_requirements() {
    requirements_file="/app/requirements.txt"
    requirements_marker="/tmp/my_fastapi_service_requirements.sha256"

    if [ ! -f "$requirements_file" ]; then
        return
    fi

    current_hash="$(sha256sum "$requirements_file" | awk '{print $1}')"
    installed_hash=""
    if [ -f "$requirements_marker" ]; then
        installed_hash="$(cat "$requirements_marker" 2>/dev/null || true)"
    fi

    if [ "$current_hash" != "$installed_hash" ]; then
        echo "requirements changed; syncing python dependencies."
        python3 -m pip install -r "$requirements_file"
        printf '%s' "$current_hash" > "$requirements_marker"
    else
        echo "requirements unchanged; skipping dependency sync."
    fi
}

sync_python_requirements

if is_true "${DB_ENABLED:-0}"; then
    echo "DB_ENABLED=${DB_ENABLED} detected; checking database connection."
    python3 tools/check_db_connection.py
else
    echo "DB_ENABLED=${DB_ENABLED:-0} detected; skipping database connection check."
fi

if [ "${ENVIRONMENT:-local}" = "prod" ] && is_true "${DB_ENABLED:-0}"; then
    echo "ENVIRONMENT=${ENVIRONMENT:-local} detected; running aerich upgrade."
    aerich upgrade
else
    echo "ENVIRONMENT=${ENVIRONMENT:-local} detected; skipping aerich upgrade."
fi

if [ -n "${UVICORN_RELOAD:-}" ]; then
    if is_true "${UVICORN_RELOAD}"; then
        exec uvicorn app:app --reload --host 0.0.0.0 --port 8000
    fi
    exec uvicorn app:app --host 0.0.0.0 --port 8000
fi

if [ "${ENVIRONMENT:-local}" = "prod" ]; then
    exec uvicorn app:app --host 0.0.0.0 --port 8000
fi

exec uvicorn app:app --reload --host 0.0.0.0 --port 8000
