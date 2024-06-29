#!/bin/sh

#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

postgres_redis_minio_ready () {
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
  echo "POSTGRES started"
  while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
    done
  echo "REDIS started"
  while ! nc -z $MINIO_ENDPOINT_HOST $MINIO_ENDPOINT_PORT; do
      sleep 0.1
    done
  echo "MINIO started"
  # Check that postgres is up and running on port `5432`:
}

# We need this line to make sure that this container is started
# after the one with postgres, redis and elastic
until postgres_redis_minio_ready; do
  >&2 echo 'Postgres or redis or minio is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'Postgres and redis and minio is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd

gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000