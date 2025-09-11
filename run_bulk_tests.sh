#!/bin/bash

# Script to run bulk review processing tests

echo "🔄 Running Bulk Review Processing Tests..."
echo "========================================"

# Set up environment
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Install dependencies if needed
echo "📦 Installing test dependencies..."
source /home/sotnikov/projects/Bot/venv/bin/activate
pip install -r requirements/dev-requirements.txt

echo ""
echo "🧪 Running system integration tests..."
echo ""

# Run the specific system test
pytest tests/integration/system/test_bulk_review_processing.py -v -s

echo ""
echo "✅ Test run complete! Check the output files:"
echo "  - platypus_review_links.json (all extracted review links by year)"
echo "  - platypus_all_issue_urls.json (flattened list of all review URLs)"
echo "  - telegraph_test_results.json (detailed processing statistics)"
echo "  - failed_review_urls.json (URLs that failed processing, if any)"
