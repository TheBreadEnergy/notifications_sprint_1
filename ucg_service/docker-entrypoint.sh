#!/bin/sh

#!/usr/bin/env sh


set -o errexit
set -o nounset

readonly cmd="$*"

kafka_ready () {
    while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
      sleep 0.1
    done
    echo "KAFKA started"
}

# We need this line to make sure that this container is started
# after the one with postgres, redis and elastic
until kafka_ready; do
  >&2 echo 'KAFKA is unavailable - sleeping'
done


# It is also possible to wait for other services as well: kafka
>&2 echo 'kafka is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd

gunicorn --worker-class gevent --workers 4 --bind 0.0.0.0:5001 src.main:app
