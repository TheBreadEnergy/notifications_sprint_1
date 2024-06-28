#!/bin/sh

#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

postgres_redis_elastic_ready () {
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
  echo "POSTGRES started"
  while ! nc -z $REDIS_HOST $REDIS_PORT; do
      sleep 0.1
    done
  echo "REDIS started"
  while ! nc -z $ELASTICSEARCH_HOST $ELASTICSEARCH_PORT; do
      sleep 0.1
    done
  echo "Elastic started"
  
}

# We need this line to make sure that this container is started
# after the one with postgres, redis and elastic
until postgres_redis_elastic_ready; do
  >&2 echo 'Postgres or elastic or redis is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
>&2 echo 'Postgres, elastic and redis is up - continuing...'

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd

curl -XPUT http://"${ELASTICSEARCH_HOST}":"${ELASTICSEARCH_PORT}"/_cluster/settings -H 'Content-Type: application/json' -d "@./schema/limitations.json"
curl -XPUT http://"${ELASTICSEARCH_HOST}":"${ELASTICSEARCH_PORT}"/movies -H 'Content-Type: application/json' -d "@./schema/movies.json"
curl -XPUT http://"${ELASTICSEARCH_HOST}":"${ELASTICSEARCH_PORT}"/genres -H 'Content-Type: application/json' -d "@./schema/genres.json"
curl -XPUT http://"${ELASTICSEARCH_HOST}":"${ELASTICSEARCH_PORT}"/persons -H 'Content-Type: application/json' -d "@./schema/persons.json"
python -m src.main