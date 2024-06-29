#!/bin/sh
echo $POSTGRES_HOST
echo $POSTGRES_PORT

mqtt_server_ready () {
   while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
  echo "MQTT started"
}

until mqtt_server_ready; do
  >&2 echo 'MQTT not ready - sleeping'
done

>&2 echo 'MQTT ready - continue'

