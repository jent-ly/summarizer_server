#!/bin/sh
# courtesy of: https://github.com/docker/compose/issues/374#issuecomment-300671114

# wait for postgres to be ready before starting api

postgres_host=$1
postgres_port=$2

# wait for the postgres docker to be running
while ! pg_isready -h $postgres_host -p $postgres_port -q -U postgres; do
  >&2 echo "postgres is unavailable - retrying..."
  sleep 1
done

>&2 echo "postgres is up - starting api server..."

# start the server, this script overrides the Dockerfile's CMD
python3.7 ./summarizer_server/server.py