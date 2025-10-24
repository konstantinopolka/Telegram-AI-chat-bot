# Single Review Debug Scripts

These scripts help debug the review processing workflow for individual Platypus reviews.

## Scripts Available

### 1. `test_single_review_debug.py` (Manual)
The comprehensive debugging script that requires manual code editing to select reviews and modes.

**Usage:**
```bash
cd /home/sotnikov/projects/Bot
source venv/bin/activate
export PYTHONPATH="$(pwd):$PYTHONPATH"
python tests/integration/system/test_single_review_debug.py
```

**Features:**
- Full workflow debugging (uses complete ReviewOrchestrator)
- Step-by-step debugging with detailed breakdowns
- Saves results to JSON file for analysis
- Manual code editing required to change URLs/modes

### 2. `interactive_review_debug.py` (Interactive)
User-friendly interactive version with prompts for easy debugging.

**Usage:**
```bash
cd /home/sotnikov/projects/Bot
source venv/bin/activate  
export PYTHONPATH="$(pwd):$PYTHONPATH"
python tests/integration/system/interactive_review_debug.py
```

**Features:**
- Interactive URL selection from recent reviews
- Interactive mode selection (full workflow vs step-by-step)
- Uses the same underlying debugging functionality
- No code editing required

## Debug Modes

### Full Workflow Mode
- Processes the review exactly like production
- Uses ReviewOrchestrator with real Telegraph API
- Shows final processing results and timing
- Best for testing complete functionality

### Step-by-Step Mode
- Breaks down processing into discrete steps
- Shows detailed information at each stage
- Pauses between steps for inspection
- Best for identifying specific issues

## Debug Output

Both scripts provide:
- Article scraping results
- Schema creation details
- Telegraph processing status
- Database operation simulation
- Channel posting simulation
- Processing timing and statistics
- Saved JSON results for further analysis

## Common Debug Scenarios

1. **Content issues**: Use step-by-step mode to inspect scraped content
2. **Telegraph errors**: Full workflow mode shows Telegraph API responses
3. **Schema problems**: Step-by-step shows article schema creation details
4. **Performance testing**: Full workflow provides timing metrics

## Results File

Debug results are saved to: `tests/single_review_debug_results.json`

This file contains:
- Review metadata
- Processing statistics
- Telegraph URLs created
- Error information
- Timing data

## Structure

- `test_bulk_review_processing.py` - Main system integration test that:
  - Extracts all review links from Platypus archive
  - Processes multiple reviews using the ReviewOrchestrator
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
- Uses existing ReviewOrchestrator architecture
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
- `ReviewOrchestrator` for the main processing workflow
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
