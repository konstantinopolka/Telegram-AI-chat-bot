"""
Tests for Archive Scanning Functionality
=========================================

This document describes the test suite for the archive scanning feature, which identifies
new Platypus Review issues by comparing the archive page with the database.

## Architecture Components Tested

1. **ArchiveParser** - Parses HTML to extract review URLs
2. **ArchiveScraper** - Fetches and scrapes archive page
3. **ArchiveScanner** - Business logic for identifying new reviews
4. **Repository Integration** - Database queries for existing reviews

## Test Structure

```
tests/
├── unit/
│   ├── test_archive_scanner.py           # ArchiveScanner business logic
│   └── test_scraping/
│       ├── test_archive_parser.py        # ArchiveParser unit tests
│       └── test_archive_scraper.py       # ArchiveScraper unit tests
├── integration/
│   ├── test_archive_scanner_integration.py  # Scanner + DB integration
│   └── scraping/
│       ├── test_archive_parser_integration.py   # Parser with real HTML
│       └── test_archive_scraper_integration.py  # Scraper workflow
└── integration/system/
    └── test_archive_system_integration.py   # End-to-end system tests
```

## Running Tests

### Run All Archive Tests

```bash
# Set PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Run all archive-related tests
pytest tests/ -k "archive" -v

# Run with coverage
pytest tests/ -k "archive" --cov=src --cov-report=html
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest tests/unit/test_archive_scanner.py -v
pytest tests/unit/test_scraping/test_archive_parser.py -v
pytest tests/unit/test_scraping/test_archive_scraper.py -v

# Integration tests
pytest tests/integration/test_archive_scanner_integration.py -v
pytest tests/integration/scraping/test_archive_parser_integration.py -v
pytest tests/integration/scraping/test_archive_scraper_integration.py -v

# System tests
pytest tests/integration/system/test_archive_system_integration.py -v

# Slow tests (with real HTTP requests)
pytest tests/ -k "archive" -m slow -v
```

### Run Tests by Functionality

```bash
# Test parsing only
pytest tests/ -k "parser" -v

# Test scraping only  
pytest tests/ -k "scraper" -v

# Test scanning only
pytest tests/ -k "scanner" -v
```

## Test Categories

### Unit Tests

**Purpose:** Test individual components in isolation with mocked dependencies.

#### test_archive_parser.py
- Tests HTML parsing logic
- Mocks HTTP requests
- Verifies selector filtering
- Tests error handling

```bash
pytest tests/unit/test_scraping/test_archive_parser.py -v
```

**Key Tests:**
- `test_parse_archive_page_success` - Successful URL extraction
- `test_parse_archive_page_empty` - Handles empty archive
- `test_parse_archive_page_filters_non_review_links` - URL filtering
- `test_parse_archive_page_logging` - Logging verification

#### test_archive_scraper.py
- Tests scraping workflow
- Mocks fetcher and parser
- Verifies duplicate removal (set conversion)
- Tests error propagation

```bash
pytest tests/unit/test_scraping/test_archive_scraper.py -v
```

**Key Tests:**
- `test_get_listing_urls_success` - Complete workflow
- `test_get_listing_urls_returns_set` - Duplicate removal
- `test_get_listing_urls_fetch_error` - Error handling
- `test_get_listing_urls_workflow` - Sequence verification

#### test_archive_scanner.py
- Tests business logic
- Mocks ArchiveScraper and database
- Tests categorization logic (new vs existing)
- Verifies bulk query optimization

```bash
pytest tests/unit/test_archive_scanner.py -v
```

**Key Tests:**
- `test_scan_for_new_reviews_success` - Identifies new reviews
- `test_check_reviews_in_db_bulk_query` - Bulk query approach
- `test_get_review_by_criteria_by_id_found_in_db` - Database lookup
- `test_logging_occurs` - Comprehensive logging

### Integration Tests

**Purpose:** Test component interactions with realistic data.

#### test_archive_parser_integration.py
- Uses realistic HTML from Platypus archive
- Real BeautifulSoup parsing (no mocks)
- Tests various HTML structures

```bash
pytest tests/integration/scraping/test_archive_parser_integration.py -v
```

**Key Tests:**
- `test_parse_realistic_archive_html` - Real HTML structure
- `test_parse_mixed_format_html` - HTML variations
- `test_parse_handles_malformed_html_gracefully` - Error tolerance
- `test_parse_real_world_scenario` - Production-like scenario

**Sample Output:**
```
test_parse_realistic_archive_html PASSED         [  20%]
test_parse_mixed_format_html PASSED              [  40%]
test_parse_minimal_html PASSED                   [  60%]
test_parse_empty_html PASSED                     [  80%]
test_parse_real_world_scenario PASSED            [ 100%]
```

#### test_archive_scraper_integration.py
- Tests fetcher + parser integration
- Mocks HTTP but uses real parsing
- Includes optional real HTTP test (marked slow)

```bash
# With mocked HTTP
pytest tests/integration/scraping/test_archive_scraper_integration.py -v

# Include real HTTP test
pytest tests/integration/scraping/test_archive_scraper_integration.py -m slow -v
```

**Key Tests:**
- `test_get_listing_urls_integration_mocked_fetch` - Complete workflow
- `test_fetcher_parser_integration` - Component interaction
- `test_real_http_request_to_archive` - Real HTTP (slow)
- `test_large_archive_integration` - Performance with 100+ URLs

#### test_archive_scanner_integration.py
- Tests ArchiveScanner + database repository
- Mocks database but uses real scanner logic
- Tests realistic scenarios

```bash
pytest tests/integration/test_archive_scanner_integration.py -v
```

**Key Tests:**
- `test_scan_workflow_integration` - Complete scan workflow
- `test_check_reviews_in_db_integration` - Database bulk query
- `test_performance_with_large_dataset` - 200 URL performance test
- `test_integration_with_realistic_scenario` - Production scenario

### System Tests

**Purpose:** End-to-end testing of complete workflows.

#### test_archive_system_integration.py
- Tests complete system from HTTP to database
- Simulates real user scenarios
- Includes optional real HTTP test

```bash
# With mocked HTTP
pytest tests/integration/system/test_archive_system_integration.py -v

# Include real HTTP test
pytest tests/integration/system/test_archive_system_integration.py -m slow -v
```

**Key Tests:**
- `test_complete_archive_scan_workflow` - Full workflow
- `test_incremental_update_scenario` - Multiple scans over time
- `test_performance_characteristics` - 300 URL performance
- `test_real_archive_end_to_end` - Real HTTP (slow)
- `test_data_flow_through_system` - Data transformation tracing

**Sample Output:**
```
test_complete_archive_scan_workflow PASSED       [  16%]
test_error_recovery_workflow PASSED              [  33%]
test_incremental_update_scenario PASSED          [  50%]
test_performance_characteristics PASSED          [  66%]
test_data_flow_through_system PASSED             [ 100%]
```

## Test Markers

Tests use pytest markers for organization:

```python
@pytest.mark.slow          # Real HTTP requests (skip by default)
@pytest.mark.integration   # Integration tests
@pytest.mark.system        # System-level tests
@pytest.mark.asyncio       # Async tests (all scanner tests)
```

**Usage:**
```bash
# Skip slow tests
pytest tests/ -k "archive" -m "not slow"

# Only integration tests
pytest tests/ -k "archive" -m "integration"

# Only system tests
pytest tests/ -k "archive" -m "system"
```

## Test Coverage

Run with coverage report:

```bash
# Generate coverage report
pytest tests/ -k "archive" --cov=src.archive_scanner \
                            --cov=src.scraping.archive_parser \
                            --cov=src.scraping.archive_scraper \
                            --cov-report=html

# View report
open htmlcov/index.html
```

**Expected Coverage:**
- ArchiveParser: >95%
- ArchiveScraper: >90%
- ArchiveScanner: >90%

## Common Test Scenarios

### Testing New Review Detection

```python
# Scenario: 5 reviews in archive, 2 already in DB
archive_urls = {issue-179, issue-178, issue-177, issue-176, issue-175}
db_urls = {issue-175, issue-176}

# Expected result:
new_reviews = {issue-179, issue-178, issue-177}  # 3 new
existing_reviews = {issue-175, issue-176}        # 2 existing
```

### Testing Empty Database

```python
# Scenario: First scan, no reviews in database yet
archive_urls = {issue-179, issue-178, issue-177}
db_urls = {}  # Empty database

# Expected result:
new_reviews = {issue-179, issue-178, issue-177}  # All new
existing_reviews = {}
```

### Testing All Reviews Processed

```python
# Scenario: All reviews already in database
archive_urls = {issue-179, issue-178, issue-177}
db_urls = {issue-179, issue-178, issue-177}  # All exist

# Expected result:
new_reviews = {}  # None new
existing_reviews = {issue-179, issue-178, issue-177}
```

## Performance Tests

### Bulk Query Optimization

```python
# Unit test verifies single bulk query (not N queries)
mock_repo.get_all_source_urls.call_count == 1  # ✅ Efficient

# NOT this (inefficient):
for url in archive_urls:
    mock_repo.get_by_url(url)  # ❌ N queries
```

### Large Dataset Performance

```python
# System test with 300 URLs should complete in <1 second
assert elapsed < 1.0  # Verifies bulk query efficiency
```

## Debugging Failed Tests

### Common Issues

1. **Import Errors**
   ```bash
   # Solution: Set PYTHONPATH
   export PYTHONPATH="$(pwd):$PYTHONPATH"
   ```

2. **Async Test Failures**
   ```bash
   # Ensure pytest-asyncio is installed
   pip install pytest-asyncio
   ```

3. **Real HTTP Tests Timing Out**
   ```bash
   # Skip slow tests
   pytest tests/ -k "archive" -m "not slow"
   ```

### Verbose Output

```bash
# See detailed test output
pytest tests/unit/test_archive_scanner.py -v -s

# See logging output
pytest tests/unit/test_archive_scanner.py -v -s --log-cli-level=DEBUG
```

### Run Single Test

```bash
# Run specific test function
pytest tests/unit/test_archive_scanner.py::TestArchiveScanner::test_scan_for_new_reviews_success -v
```

## Continuous Integration

Add to CI pipeline:

```yaml
# .github/workflows/test.yml
- name: Run Archive Tests
  run: |
    export PYTHONPATH="$(pwd):$PYTHONPATH"
    pytest tests/ -k "archive" -m "not slow" --cov=src --cov-report=xml
```

## Future Test Additions

Potential areas for additional testing:

1. **Database Integration Tests** - Real database operations (not just mocks)
2. **Concurrency Tests** - Multiple simultaneous scans
3. **Error Recovery** - Network failures, partial results
4. **Caching Tests** - If caching is added to ArchiveScanner
5. **Month-based Lookup** - When `get_review_by_criteria(month=...)` is implemented

## Related Documentation

- Main testing guide: `tests/README.md`
- System integration tests: `tests/integration/system/README.md`
- Review scraping tests: `tests/unit/test_scraping/test_review_scraper.py`
- Database guide: `docs/database_guide.md`

## Questions?

- Check main README: `README.md`
- Review architecture: `docs/RESTRUCTURING_SUMMARY.md`
- See Copilot instructions: `.github/copilot-instructions.md`
"""