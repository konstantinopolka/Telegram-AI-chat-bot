#!/bin/bash

# Docker Build and Version Management Script
set -e

# Get version from git tag or use default
VERSION=${1:-$(git describe --tags --always 2>/dev/null || echo "0.1.0")}
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo "Building Docker image with version: $VERSION"
echo "Build date: $BUILD_DATE"
echo "Git commit: $GIT_COMMIT"

# Set environment variables
export APP_VERSION=$VERSION
export BUILD_DATE=$BUILD_DATE
export GIT_COMMIT=$GIT_COMMIT
export BOT_IMAGE_TAG="${VERSION}-${GIT_COMMIT}"

# Generate .env.docker file with actual values
echo "Generating .env.docker..."
./generate-env.sh $VERSION

# Build and tag the image (we're already in docker folder)
echo "Building with docker-compose..."
docker-compose build --build-arg APP_VERSION=$VERSION \
                     --build-arg BUILD_DATE="$BUILD_DATE" \
                     --build-arg GIT_COMMIT=$GIT_COMMIT

# Tag additional versions
docker tag "reposting_bot:${VERSION}" "reposting_bot:${VERSION}-${GIT_COMMIT}"
docker tag "reposting_bot:${VERSION}" "reposting_bot:latest"

echo "Built images:"
docker images | grep reposting_bot

echo "To start the application:"
echo "  docker-compose --env-file .env.docker up -d"
echo ""
echo "To push to registry:"
echo "  docker push reposting_bot:${VERSION}"
echo "  docker push reposting_bot:latest"
