#!/bin/bash
set -euo pipefail

IMAGE_REPO="gcr.io/alpine-gasket-242504/summarizer-server"
PG_PASSWORD=${1:-}
DD_API_KEY=${2:-}
DEPLOY_SHA=${3:-}

if [ -z "$PG_PASSWORD" ] || [ -z "$DD_API_KEY" ] || [ -z "$DEPLOY_SHA" ]; then
  echo "Usage: ./deploy.sh <postgres_password> <datadog_api_key> <travis_sha>"
  exit 1
fi

echo "Step 1: pull image and bring down server"

gcloud beta compute --project "alpine-gasket-242504" ssh --zone "us-central1-a" "jently-docker-instance-2" \
--command "gcloud docker -- pull $IMAGE_REPO:$DEPLOY_SHA && \
gcloud docker -- tag $IMAGE_REPO:$DEPLOY_SHA $IMAGE_REPO:latest && \
docker-compose -f docker-compose.prod.yml down"

echo "Step 2: copy docker-compose"

gcloud compute scp docker-compose.prod.yml jently-docker-instance-2:~

echo "Step 3: bring up server"

gcloud beta compute --project "alpine-gasket-242504" ssh --zone "us-central1-a" "jently-docker-instance-2" \
--command "ENV=prod DD_API_KEY=$DD_API_KEY HOST=$$HOST POSTGRES_PASSWORD=$PG_PASSWORD \
  docker-compose -f docker-compose.prod.yml up -d"
