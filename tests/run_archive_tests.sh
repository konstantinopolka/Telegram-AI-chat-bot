#!/bin/bash
#
# Test runner for archive scanning functionality
# Usage: ./tests/run_archive_tests.sh [category]
#
# Categories:
#   unit        - Run unit tests only
#   integration - Run integration tests only
#   system      - Run system tests only
#   all         - Run all tests (default)
#   fast        - Run all except slow tests
#   slow        - Run only slow tests (real HTTP)

set -e  # Exit on error

# Set PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Archive Scanning Test Runner${NC}"
echo "================================"
echo ""

CATEGORY="${1:-all}"

case "$CATEGORY" in
    unit)
        echo -e "${YELLOW}Running Unit Tests...${NC}"
        python -m pytest tests/unit/test_archive_scanner.py \
                        tests/unit/test_scraping/test_archive_parser.py \
                        tests/unit/test_scraping/test_archive_scraper.py \
                        -v
        ;;
    
    integration)
        echo -e "${YELLOW}Running Integration Tests...${NC}"
        python -m pytest tests/integration/test_archive_scanner_integration.py \
                        tests/integration/scraping/test_archive_parser_integration.py \
                        tests/integration/scraping/test_archive_scraper_integration.py \
                        -m "not slow" \
                        -v
        ;;
    
    system)
        echo -e "${YELLOW}Running System Tests...${NC}"
        python -m pytest tests/integration/system/test_archive_system_integration.py \
                        -m "not slow" \
                        -v
        ;;
    
    fast)
        echo -e "${YELLOW}Running All Tests (excluding slow tests)...${NC}"
        python -m pytest tests/ -k "archive" -m "not slow" -v
        ;;
    
    slow)
        echo -e "${YELLOW}Running Slow Tests (real HTTP requests)...${NC}"
        python -m pytest tests/ -k "archive" -m "slow" -v
        ;;
    
    all)
        echo -e "${YELLOW}Running All Archive Tests...${NC}"
        python -m pytest tests/ -k "archive" -v
        ;;
    
    coverage)
        echo -e "${YELLOW}Running Tests with Coverage...${NC}"
        python -m pytest tests/ -k "archive" \
                        -m "not slow" \
                        --cov=src.archive_scanner \
                        --cov=src.scraping.archive_parser \
                        --cov=src.scraping.archive_scraper \
                        --cov-report=term-missing \
                        --cov-report=html \
                        -v
        echo ""
        echo -e "${GREEN}Coverage report generated: htmlcov/index.html${NC}"
        ;;
    
    *)
        echo -e "${RED}Unknown category: $CATEGORY${NC}"
        echo ""
        echo "Usage: $0 [category]"
        echo ""
        echo "Categories:"
        echo "  unit        - Unit tests only"
        echo "  integration - Integration tests only"
        echo "  system      - System tests only"
        echo "  all         - All tests (default)"
        echo "  fast        - All except slow tests"
        echo "  slow        - Only slow tests (real HTTP)"
        echo "  coverage    - Run with coverage report"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✓ Tests completed${NC}"
