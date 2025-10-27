#!/bin/bash

# Script to run ArchiveScanner integration test against real archive page
# Run this script from the tests/ directory or project root

echo "🔄 Running ArchiveScanner Integration Test (Real Archive)..."
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
    echo "⚠️  Warning: ARCHIVE_URL not set in .env"
    echo "   Using default: https://platypus1917.org/platypus-review/"
fi

echo ""
echo "🧪 Running ArchiveScanner integration test against live archive..."
echo ""

# Run the specific test with verbose output
pytest tests/integration/system/test_archive_scanner_real.py -v -s

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ Test completed successfully!"
    echo ""
    echo "📊 Summary:"
    echo "   - ArchiveScanner successfully fetched URLs from real archive"
    echo "   - scan_for_new_reviews() returned valid results"
    echo "   - get_new_reviews() returned valid URL set"
else
    echo "❌ Test failed with exit code: $TEST_EXIT_CODE"
fi

echo ""
echo "💡 Note: This test hits the live archive at ARCHIVE_URL"
echo "   and mocks database calls so no DB is required."

exit $TEST_EXIT_CODE
