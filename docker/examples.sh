#!/bin/bash

# Example usage script for Docker versioning system
# This script demonstrates common workflows

echo "=== Telegram Bot Docker Versioning Examples ==="
echo ""

echo "1. Basic build with auto-versioning:"
echo "   cd docker && ./build.sh"
echo ""

echo "2. Build with specific version:"
echo "   cd docker && ./build.sh 1.2.3"
echo ""

echo "3. Generate environment and start:"
echo "   cd docker && ./generate-env.sh && docker-compose --env-file .env.docker up -d"
echo ""

echo "4. Check version of running container:"
echo "   docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}'"
echo ""

echo "5. View version info in application:"
echo "   docker run --rm reposting_bot:latest python -c \"from src.version import get_version_info; print(get_version_info())\""
echo ""

echo "6. Deploy to registry:"
echo "   cd docker && ./deploy.sh 1.2.3"
echo ""

echo "7. List all built versions:"
echo "   docker images | grep reposting_bot"
echo ""

echo "8. Rollback to previous version:"
echo "   docker-compose down"
echo "   docker tag reposting_bot:1.2.2 reposting_bot:latest"
echo "   docker-compose --env-file .env.docker up -d"
echo ""

echo "Current git info:"
echo "  Branch: $(git branch --show-current 2>/dev/null || echo 'not in git repo')"
echo "  Latest tag: $(git describe --tags --always 2>/dev/null || echo 'no tags')"
echo "  Commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'not in git repo')"
