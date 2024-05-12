#!/bin/sh

#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd


gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000