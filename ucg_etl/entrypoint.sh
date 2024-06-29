#!/bin/sh

set -o errexit
set -o nounset

readonly cmd="$*"

ch_kafka_ready () {
  # Check that postgres is up and running on port `5432`:
  while ! nc -z $CH_HOST $CH_PORT; do
      sleep 0.1
    done
  echo " Clickhouse started"

  while ! nc -z $KAFKA_HOST $KAFKA_PORT; do
      sleep 0.1
    done
  echo "Kafka started"
}


until ch_kafka_ready; do
  >&2 echo 'kafka and clickhouse is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'kafka and clickhouse is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd

python -m src.main