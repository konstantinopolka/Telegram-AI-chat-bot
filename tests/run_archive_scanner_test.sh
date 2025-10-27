#!/bin/bash

# Script to run real archive scanner integration test
# Tests ArchiveScanner with the actual Platypus Review archive
# Run this script from the tests/ directory or project root

echo "🔄 Running Archive Scanner Real-World Integration Test..."
echo "========================================"

# Get the project root directory
if [ -f "pytest.ini" ]; then
    PROJECT_ROOT="$(pwd)"
else
    PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

echo "📁 Project root: $PROJECT_ROOT"

# Change to project root for proper imports
cd "$PROJECT_ROOT"

# Set up environment
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Activate virtual environment if it exists
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    echo "✓ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found at $PROJECT_ROOT/venv/"
    echo "   You may need to create it with: python -m venv venv"
fi

# Check for required environment variables
if [ -z "$ARCHIVE_URL" ]; then
    echo "⚠️  Warning: ARCHIVE_URL not set in environment"
    echo "   Using default: https://platypus1917.org/platypus-review/"
fi

echo ""
echo "🧪 Running archive scanner integration test..."
echo "📡 Will make REAL HTTP requests to Platypus archive"
echo "💾 Will check against real database"
echo ""

# Run options
echo "Choose run mode:"
echo "  1) Run with pytest (recommended for CI/automated testing)"
echo "  2) Run standalone script (detailed output, saves JSON results)"
echo ""
read -p "Enter choice (1 or 2, default=2): " CHOICE
CHOICE=${CHOICE:-2}

if [ "$CHOICE" == "1" ]; then
    echo ""
    echo "Running with pytest..."
    pytest tests/test_archive_scanner_real.py -v -s --asyncio-mode=auto
    TEST_EXIT_CODE=$?
else
    echo ""
    echo "Running standalone script..."
    python tests/test_archive_scanner_real.py
    TEST_EXIT_CODE=$?
fi

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ Test completed successfully!"
    echo ""
    echo "📄 Check test results in: tests/archive_scanner_test_results.json"
else
    echo "❌ Test failed with exit code: $TEST_EXIT_CODE"
fi

echo ""
echo "ℹ️  This test:"
echo "   - Fetches real review URLs from https://platypus1917.org/platypus-review/"
echo "   - Checks which reviews exist in your database"
echo "   - Categorizes reviews as 'new' vs 'existing'"
echo "   - Verifies the functions used by RepostingOrchestrator"
echo ""
echo "ℹ️  Next step: Pass these URLs to ReviewOrchestrator for processing"

exit $TEST_EXIT_CODE
