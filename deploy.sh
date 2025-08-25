#!/bin/bash

# Deploy script with registry push
set -e

VERSION=${1:-$(git describe --tags --always)}
REGISTRY=${DOCKER_REGISTRY:-"your-registry.com"}
IMAGE_NAME="${REGISTRY}/reposting_bot"

echo "Deploying version: $VERSION to registry: $REGISTRY"

# Build
./build.sh $VERSION

# Tag for registry
docker tag "reposting_bot:${VERSION}" "${IMAGE_NAME}:${VERSION}"
docker tag "reposting_bot:${VERSION}" "${IMAGE_NAME}:latest"

# Push to registry
docker push "${IMAGE_NAME}:${VERSION}"
docker push "${IMAGE_NAME}:latest"

echo "Deployed ${IMAGE_NAME}:${VERSION}"
