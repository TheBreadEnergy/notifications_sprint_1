#!/bin/sh

#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

mongo_ready () {
    while ! nc -z $MONGO_HOST $MONGO_PORT; do
      sleep 0.1
    done
    echo "MONGO started"
}

# We need this line to make sure that this container is started
# after the one with postgres, redis and elastic
until mongo_ready; do
  >&2 echo 'Mongo is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'Mongo is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd


gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000