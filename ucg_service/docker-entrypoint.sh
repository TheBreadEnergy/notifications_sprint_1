#!/bin/sh

#!/usr/bin/env sh


set -o errexit
set -o nounset

readonly cmd="$*"

# It is also possible to wait for other services as well: kafka
>&2 echo 'kafka is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd

gunicorn --worker-class gevent --workers 4 --bind 0.0.0.0:5001 src.main:app
