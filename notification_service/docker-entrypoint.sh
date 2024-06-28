#!/bin/sh

#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

services_ready() {
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done
  echo "Database started"
  while ! nc -z $RABBIT_HOST $RABBIT_PORT; do
    sleep 0.1
  done
  echo "RabbitMQT started"
}


# We need this line to make sure that this container is started
# after the one with postgres, redis and elastic
until services_ready; do
  >&2 echo 'services is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'Services is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd

if [ "$RUN_MODE" = "GRPC" ]
then
  python -m src.main_grpc
else
  gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
fi
