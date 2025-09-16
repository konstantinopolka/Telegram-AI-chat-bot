#!/bin/bash

# Script to run bulk review processing tests
# Run this script from the tests/ directory

echo "🔄 Running Bulk Review Processing Tests..."
echo "========================================"

# Get the project root directory (parent of tests)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
echo "📁 Project root: $PROJECT_ROOT"

# Change to project root for proper imports
cd "$PROJECT_ROOT"

# Set up environment
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Install dependencies if needed
echo "📦 Installing test dependencies..."
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    echo "✓ Virtual environment activated"
else
    echo "⚠️  Virtual environment not found at $PROJECT_ROOT/venv/"
    echo "   You may need to create it with: python -m venv venv"
fi

pip install -r requirements/dev-requirements.txt

echo ""
echo "🧪 Running system integration tests..."
echo ""

# Run the specific system test
pytest tests/integration/system/test_bulk_review_processing.py -v -s

echo ""
echo "✅ Test run complete! Check the output files in project root:"
echo "  - platypus_review_links.json (all extracted review links by year)"
echo "  - platypus_all_issue_urls.json (flattened list of all review URLs)"
echo "  - telegraph_test_results.json (detailed processing statistics)"
echo "  - failed_review_urls.json (URLs that failed processing, if any)"
