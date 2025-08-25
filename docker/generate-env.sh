#!/bin/bash

# Generate .env.docker with actual values
# This script creates environment variables with resolved values

# Get actual values
VERSION=${1:-$(git describe --tags --always 2>/dev/null || echo "1.0.0")}
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

echo "Generating .env.docker with:"
echo "  APP_VERSION=$VERSION"
echo "  BUILD_DATE=$BUILD_DATE"
echo "  GIT_COMMIT=$GIT_COMMIT"

# Create .env.docker file with actual values
cat > .env.docker << EOF
# Docker Image Versioning (Generated on $(date))
APP_VERSION=$VERSION
BUILD_DATE=$BUILD_DATE
GIT_COMMIT=$GIT_COMMIT
POSTGRES_VERSION=17
EOF

echo "Generated .env.docker successfully!"
