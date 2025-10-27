# Archive Scanner Real-World Integration Tests

## Overview

This test suite validates that `ArchiveScanner` correctly works with the **real Platypus Review archive** at https://platypus1917.org/platypus-review/

Unlike the unit tests (which use mocks), these tests:
- ✅ Make **real HTTP requests** to the Platypus archive
- ✅ Parse **real HTML** content
- ✅ Check against **real database** records
- ✅ Verify the exact workflow used by `RepostingOrchestrator`

## Test File

**`tests/test_archive_scanner_real.py`**

Contains 4 integration tests:

### 1. `test_archive_scanner_with_real_archive()`
- Scans the real Platypus archive page
- Categorizes reviews as new vs existing
- Verifies data structure and URL formats
- Most comprehensive test

### 2. `test_get_new_reviews_convenience_method()`
- Tests `get_new_reviews()` - the method called by `RepostingOrchestrator`
- Ensures it returns the correct Set[str] of URLs
- Validates URL formatting

### 3. `test_database_query_performance()`
- Measures performance of the bulk database query
- Ensures scan completes in < 10 seconds
- Validates efficient O(1) lookup approach

### 4. `test_archive_scanner_output_format()`
- Verifies output format matches what `RepostingOrchestrator` expects
- Checks type safety (Set[str])
- Validates all URLs are absolute

## Quick Start

### Run with Shell Script (Recommended)

```bash
# From project root or tests/ directory
./tests/run_archive_scanner_test.sh
```

The script offers two modes:
1. **pytest mode** - Standard pytest output, CI-friendly
2. **standalone mode** - Detailed output, saves JSON results

### Run Directly with pytest

```bash
# All tests
pytest tests/test_archive_scanner_real.py -v -s --asyncio-mode=auto

# Single test
pytest tests/test_archive_scanner_real.py::TestArchiveScannerReal::test_get_new_reviews_convenience_method -v -s
```

### Run as Standalone Script

```bash
python tests/test_archive_scanner_real.py
```

This mode:
- Provides detailed console output
- Shows progress for each test
- Saves results to `tests/archive_scanner_test_results.json`
- Returns exit code 0 on success, 1 on failure

## What Gets Tested

### Real HTTP Request
```python
scanner = ArchiveScanner(ARCHIVE_URL)
result = await scanner.scan_for_new_reviews()
```

- Fetches https://platypus1917.org/platypus-review/
- Parses real HTML using BeautifulSoup
- Extracts review URLs using CSS selectors

### Database Integration
```python
new_reviews = await scanner.get_new_reviews()
```

- Queries database for existing review URLs (bulk query)
- Identifies which archive URLs are new vs existing
- Returns only new URLs (as Set[str])

### RepostingOrchestrator Workflow
```python
# This is what RepostingOrchestrator.scan_and_process_new_reviews() does:
new_reviews_urls: Set[str] = await self.archive_scanner.get_new_reviews()
for review_url in new_reviews_urls:
    # Process each new review...
```

The test validates this exact pattern works with real data.

## Output

### Console Output (Standalone Mode)

```
============================================================
ARCHIVE SCANNER REAL-WORLD INTEGRATION TEST
============================================================

Archive URL: https://platypus1917.org/platypus-review/
Timestamp: 2025-10-27 14:30:00
============================================================

🧪 TEST 1: Full Archive Scan
----------------------------------------------------------------------
Testing ArchiveScanner with Real Archive
============================================================
Initializing ArchiveScanner for: https://platypus1917.org/platypus-review/

📡 Fetching review URLs from real archive...

============================================================
Archive Scan Results:
============================================================
Total reviews in archive: 150
New reviews found: 5
Existing reviews in DB: 145
============================================================

📝 Sample new review URLs (showing up to 5):
  1. https://platypus1917.org/category/pr/issue-150/
  2. https://platypus1917.org/category/pr/issue-149/
  ...

✅ Archive scan completed successfully!

...more tests...

📊 TEST SUMMARY
============================================================
✅ All tests passed!

Archive Statistics:
  Total reviews in archive: 150
  New reviews: 5
  Existing in DB: 145

📄 Results saved to: tests/archive_scanner_test_results.json
============================================================

✅ SUCCESS: All archive scanner tests passed!
```

### JSON Output File

**`tests/archive_scanner_test_results.json`**

```json
{
  "timestamp": "2025-10-27T14:30:00.123456",
  "archive_url": "https://platypus1917.org/platypus-review/",
  "total_reviews": 150,
  "new_reviews_count": 5,
  "existing_reviews_count": 145,
  "new_review_urls": [
    "https://platypus1917.org/category/pr/issue-150/",
    "https://platypus1917.org/category/pr/issue-149/",
    "https://platypus1917.org/category/pr/issue-148/",
    "https://platypus1917.org/category/pr/issue-147/",
    "https://platypus1917.org/category/pr/issue-146/"
  ],
  "existing_review_urls": [
    "https://platypus1917.org/category/pr/issue-1/",
    "https://platypus1917.org/category/pr/issue-2/",
    ...
  ],
  "tests_passed": true
}
```

## Environment Requirements

### Required Environment Variables

Set in `.env`:
```bash
ARCHIVE_URL=https://platypus1917.org/platypus-review/
ARCHIVE_LINK_SELECTORS=h2 > a[href^="https://platypus1917.org/category/pr/issue-"]
```

### Database

- Database must be running and accessible
- `Review` table must exist (via Alembic migrations)
- No special setup needed - test reads existing data

### Network

- Requires internet connection to fetch archive page
- Will fail if platypus1917.org is unreachable

## Use Cases

### 1. Validate ArchiveScanner Before Integration

Before using `RepostingOrchestrator`, verify `ArchiveScanner` works:

```bash
./tests/run_archive_scanner_test.sh
```

### 2. Check for New Reviews

See how many new reviews are available:

```bash
python tests/test_archive_scanner_real.py
# Check tests/archive_scanner_test_results.json
```

### 3. Debugging Archive Parsing Issues

If archive URLs aren't being detected:

```bash
pytest tests/test_archive_scanner_real.py::TestArchiveScannerReal::test_archive_scanner_with_real_archive -v -s
```

Look for:
- HTTP errors (404, 500)
- CSS selector mismatches
- URL format changes

### 4. Performance Validation

Ensure bulk queries are fast:

```bash
pytest tests/test_archive_scanner_real.py::TestArchiveScannerReal::test_database_query_performance -v -s
```

Should complete in < 10 seconds even with 150+ reviews.

## Comparison with Other Tests

### vs Unit Tests (`tests/unit/test_archive_scanner.py`)
- ❌ Unit tests: Use mocks, no real HTTP/DB
- ✅ **This test: Uses real archive + real database**

### vs System Tests (`tests/integration/system/test_archive_system_integration.py`)
- ❌ System tests: Mock the entire workflow end-to-end
- ✅ **This test: Real HTTP + Real DB, no ReviewOrchestrator processing**

### vs Bulk Review Processing (`test_bulk_review_processing.py`)
- ❌ Bulk tests: Process reviews through Telegraph API
- ✅ **This test: Only scan archive, don't process reviews**

## Next Steps

After these tests pass, you can:

1. **Run `RepostingOrchestrator`** to process new reviews:
   ```python
   orchestrator = RepostingOrchestrator()
   await orchestrator.scan_and_process_new_reviews()
   ```

2. **Set up scheduled scanning** (hourly/daily):
   ```python
   # Using APScheduler or cron
   scheduler.add_job(scan_and_process_new_reviews, 'interval', hours=1)
   ```

3. **Add user commands** (e.g., `/check_new_reviews`):
   ```python
   @bot.message_handler(commands=['check_new_reviews'])
   async def check_new_reviews(message):
       scanner = ArchiveScanner()
       new_reviews = await scanner.get_new_reviews()
       await bot.reply(message, f"Found {len(new_reviews)} new reviews!")
   ```

## Troubleshooting

### Test Fails with "Connection Error"
- Check internet connection
- Verify https://platypus1917.org/platypus-review/ is accessible
- Check firewall/proxy settings

### Test Fails with "No reviews found"
- Verify `ARCHIVE_LINK_SELECTORS` in `.env` matches current HTML structure
- Check if Platypus changed their archive page layout
- Run with `-s` flag to see detailed parsing output

### Test Fails with "Database Error"
- Ensure database is running
- Run Alembic migrations: `alembic upgrade head`
- Check database connection settings in `.env`

### All Reviews Marked as "Existing"
- This is normal if you've already processed all archive reviews
- Clear database to see "new" reviews, or wait for new issues to be published

## Related Files

- `src/archive_scanner.py` - Implementation being tested
- `src/scraping/archive_scraper.py` - HTTP fetching and parsing
- `src/scraping/archive_parser.py` - HTML parsing logic
- `src/reposting_orchestrator.py` - Uses ArchiveScanner
- `tests/unit/test_archive_scanner.py` - Unit tests with mocks
- `tests/integration/test_archive_scanner_integration.py` - Integration tests with mocked DB

## License

Same as main project.
