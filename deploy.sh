#!/bin/bash
set -euo pipefail

IMAGE_REPO="gcr.io/alpine-gasket-242504/summarizer-server"
PG_PASSWORD=${1:-}
DEPLOY_SHA=${2:-}

if [ -z "$PG_PASSWORD" ] || [ -z "$DEPLOY_SHA" ]; then
  echo "Usage: ./deploy.sh <postgres_password> <travis_sha>"
  exit 1
fi

echo "Step 1: pull image and bring down server"

gcloud beta compute --project "alpine-gasket-242504" ssh --zone "us-central1-a" "jently-docker-instance-2" \
--command "gcloud docker -- pull $IMAGE_REPO:$DEPLOY_SHA && \
gcloud docker -- tag $IMAGE_REPO:$DEPLOY_SHA $IMAGE_REPO:latest && \
docker-compose -f docker-compose.prod.yml down"

echo "Step 2: copy files"

gcloud compute scp docker-compose.prod.yml jently-docker-instance-2:~
gcloud compute scp summarizer_server/nginx.conf summarizer_server/nginx_default.conf jently-docker-instance-2:~/summarizer_server/

echo "Step 3: bring up server"

gcloud beta compute --project "alpine-gasket-242504" ssh --zone "us-central1-a" "jently-docker-instance-2" \
--command "POSTGRES_PASSWORD=$PG_PASSWORD docker-compose -f docker-compose.prod.yml up -d"
