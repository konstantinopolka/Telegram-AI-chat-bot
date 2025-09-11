# System Integration Tests

This directory contains system-level integration tests that test the entire workflow of the bot across multiple components.

## Structure

- `test_bulk_review_processing.py` - Main system integration test that:
  - Extracts all review links from Platypus archive
  - Processes multiple reviews using the RepostingOrchestrator
  - Tracks statistics and performance metrics
  - Tests Telegraph size limits and constraints

- `conftest.py` - Test configuration and fixtures
- `test_fixtures_platypus_links.py` - Legacy compatibility file

## Key Features

### PlatypusArchiveExtractor
- Extracts all review issue links from the Platypus archive
- Organizes links by year
- This functionality is specific to testing (not needed in main application)

### BulkProcessingStatistics
- Tracks comprehensive statistics during bulk processing
- Records processing times, success/failure rates
- Identifies articles over Telegraph size limits
- Generates detailed reports

### TestBulkReviewProcessing
- Uses existing RepostingOrchestrator architecture
- Processes reviews in batches with proper error handling
- Generates comprehensive test reports
- Compatible with pytest framework

## Usage

### Run via Script
```bash
# From the tests/ directory
cd tests/
./run_bulk_tests.sh
```

### Run via Pytest
```bash
# Run all system tests
pytest tests/integration/system/ -v

# Run specific test
pytest tests/integration/system/test_bulk_review_processing.py::test_extract_review_links -v

# Run with async support
pytest tests/integration/system/test_bulk_review_processing.py -v --asyncio-mode=auto
```

### Run Programmatically
```python
import asyncio
from tests.integration.system.test_bulk_review_processing import TestBulkReviewProcessing

async def main():
    tester = TestBulkReviewProcessing()
    await tester.test_extract_all_review_links()
    await tester.test_process_recent_reviews(max_reviews=3)

asyncio.run(main())
```

## Output Files

The tests generate several JSON files in the project root:
- `platypus_review_links.json` - All review links organized by year
- `platypus_all_issue_urls.json` - Flattened list of all review URLs  
- `telegraph_test_results.json` - Detailed processing statistics
- `failed_review_urls.json` - URLs that failed processing (if any)

## Integration with Existing Architecture

The tests reuse existing components:
- `ReviewScraper` for scraping individual reviews
- `RepostingOrchestrator` for the main processing workflow
- `TelegraphManager` for Telegraph article creation
- All existing validation and error handling

The only new functionality is:
- Archive extraction (specific to testing)
- Statistics tracking (for test reporting)
- Bulk processing coordination (test orchestration)

## Dependencies

See `requirements/dev-requirements.txt` for test-specific dependencies:
- pytest
- pytest-asyncio
- beautifulsoup4 (for archive parsing)
- requests (for HTTP calls)
