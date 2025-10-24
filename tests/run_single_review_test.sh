#!/bin/bash

# Script to run single review integration test
# Run this script from the tests/ directory or project root

echo "🔄 Running Single Review Integration Test..."
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
if [ -z "$TELEGRAPH_ACCESS_TOKEN" ]; then
    echo "⚠️  Warning: TELEGRAPH_ACCESS_TOKEN not set"
    echo "   Telegraph article creation will be skipped"
fi

echo ""
echo "🧪 Running single review integration test..."
echo ""

# Run the specific test with verbose output
pytest tests/test_single_review.py -v -s

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ Test completed successfully!"
else
    echo "❌ Test failed with exit code: $TEST_EXIT_CODE"
fi

echo ""
echo "To run with different review URL, edit TEST_REVIEW_URL in tests/test_single_review.py"

exit $TEST_EXIT_CODE
