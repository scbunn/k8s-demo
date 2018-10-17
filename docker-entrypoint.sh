#!/usr/bin/env sh
# ----------------------------------------------------------------------------
# docker entrypoint for demo app
# ----------------------------------------------------------------------------
set -e

if [[ "${1}" == "k8s" ]]; then
    echo "Starting demo app"
    exec gunicorn app:app --threads 4 -b 0.0.0.0:5000
else
    exec "$@"
fi
