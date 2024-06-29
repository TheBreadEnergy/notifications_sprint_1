#!/bin/sh

#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

postgres_redis_elastic_ready () {
  while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
    done
  echo "REDIS started"
  while ! nc -z $ELASTIC_HOST $ELASTIC_PORT; do
      sleep 0.1
    done
  echo "REDIS started"
  # Check that postgres is up and running on port `5432`:
}

# We need this line to make sure that this container is started
# after the one with postgres, redis and elastic
until postgres_redis_elastic_ready; do
  >&2 echo 'Elastic or redis is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'Elastic and redis is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd


gunicorn src.main:app  --preload --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000