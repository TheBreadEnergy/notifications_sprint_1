#!/bin/sh

#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

postgres_ready () {
  # Check that postgres is up and running on port `5432`:
   while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
  echo "PostgreSQL started"

  while ! nc -z $CACHE_HOST $CACHE_PORT; do
      sleep 0.1
    done
  echo "REDIS started"
}

# We need this line to make sure that this container is started
# after the one with postgres, redis and elastic
until postgres_ready; do
  >&2 echo 'Postgres is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'Postgres is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
alembic upgrade head
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000