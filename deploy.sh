#!/bin/bash
# Simple production deploy script
# Usage: ./deploy.sh

set -euo pipefail

# Variables
IMAGE="${REGISTRY:-ghcr.io/bucky-ops/auto-jips}:latest"
CONTAINER_NAME="ajips"
ENV_FILE="${1:-.prod.env}"

# Pull latest image
echo "Pulling image: $IMAGE"
docker pull "$IMAGE"

# Stop and remove existing container
if docker ps -a --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping existing container..."
    docker stop "${CONTAINER_NAME}" || true
    docker rm "${CONTAINER_NAME}" || true
fi

# Run new container
echo "Starting new container..."
docker run -d --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    -p 8000:8000 \
    --env-file "$ENV_FILE" \
    "$IMAGE"

echo "Deployment complete. Container running:"
docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"