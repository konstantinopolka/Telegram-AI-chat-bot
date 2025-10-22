# Single Review Integration Test

## Overview

`test_single_review.py` is a comprehensive integration test that validates the complete workflow for processing a single review from start to finish.

## What It Tests

The test covers the entire review processing pipeline:

1. **Scraping** - Fetches review and all articles from a live URL
2. **Data Transformation** - Creates Article instances using ArticleFactory
3. **Telegraph Publishing** - Creates Telegraph articles (if token configured)
4. **Database Persistence** - Saves articles and review to database
5. **Data Verification** - Retrieves and validates all saved data

## Configuration

### Test Review URL

Edit the constant at the top of the test file to change the review being tested:

```python
# Test configuration - easily changeable
TEST_REVIEW_URL = "https://platypus1917.org/category/pr/issue-173/"
```

### Environment Variables

- `TELEGRAPH_ACCESS_TOKEN` - Optional, enables Telegraph article creation
- Database configuration variables (from `.env` file)

## Running the Test

### Method 1: Using the Helper Script (Recommended)

```bash
# From project root
./tests/run_single_review_test.sh
```

### Method 2: Using pytest

```bash
# From project root
export PYTHONPATH="$(pwd):$PYTHONPATH"
pytest tests/test_single_review.py -v -s
```

### Method 3: As Standalone Script

```bash
# From project root
python tests/test_single_review.py
```

## Test Output

The test provides detailed logging for each step:

```
==========================================
STEP 1: SCRAPING REVIEW AND ARTICLES
==========================================
✓ Scraped 8 articles
✓ Review ID: 173
✓ Source URL: https://platypus1917.org/category/pr/issue-173/

==========================================
STEP 2: CREATING ARTICLE INSTANCES
==========================================
✓ Created 8 Article instances
  Article 1: Introduction to Issue 173...
  Article 2: The Crisis of Capitalism...
  ...

==========================================
STEP 3: CREATING TELEGRAPH ARTICLES
==========================================
Creating Telegraph article 1/8: Introduction to Issue 173...
  ✓ Created 1 Telegraph page(s)
    Part 1: https://telegra.ph/...
...

==========================================
STEP 4: SAVING ARTICLES TO DATABASE
==========================================
Saving article 1/8: Introduction to Issue 173...
  ✓ Saved with ID: 1
✓ Successfully saved 8 articles to database

==========================================
STEP 5: CREATING AND SAVING REVIEW
==========================================
Created Review instance:
  ID: 173
  Source URL: https://platypus1917.org/category/pr/issue-173/
  Articles: 8
✓ Saved Review with ID: 173

==========================================
STEP 6: VERIFYING SAVED DATA
==========================================
✓ Successfully retrieved review from database
  Review ID: 173
  Articles: 8
  Article 1: ID=1, Title=Introduction to Issue 173...
  ...

==========================================
TEST COMPLETED SUCCESSFULLY!
==========================================
Summary:
  - Review ID: 173
  - Articles processed: 8
  - Telegraph articles created: 8
  - All data verified in database: ✓
==========================================
```

## What's NOT Tested

- Telegram bot posting (not yet implemented)
- Channel posting (not yet implemented)
- Error recovery for partial failures
- Concurrent processing

## Use Cases

### Testing Different Reviews

Change `TEST_REVIEW_URL` to test other reviews:

```python
TEST_REVIEW_URL = "https://platypus1917.org/category/pr/issue-172/"
```

### Testing Without Telegraph

Run the test without `TELEGRAPH_ACCESS_TOKEN` set to test everything except Telegraph creation:

```bash
unset TELEGRAPH_ACCESS_TOKEN
./tests/run_single_review_test.sh
```

### Development Workflow

1. Make changes to scraping, article creation, or database logic
2. Run this test to verify the entire pipeline still works
3. Check the detailed logs to identify any issues
4. Verify data in database manually if needed

## Prerequisites

1. Python virtual environment activated
2. All dependencies installed (`pip install -r requirements/dev-requirements.txt`)
3. Database configured and accessible
4. Optional: Telegraph access token for full testing

## Troubleshooting

### Import Errors

Make sure `PYTHONPATH` is set:

```bash
export PYTHONPATH="$(pwd):$PYTHONPATH"
```

### Database Connection Issues

Check your `.env` file has correct database configuration.

### Telegraph Creation Skipped

Set `TELEGRAPH_ACCESS_TOKEN` environment variable to enable Telegraph article creation.

### Test Timeout

Some reviews have many articles and can take time to process. This is normal for integration tests.

## Related Files

- `tests/run_single_review_test.sh` - Helper script to run the test
- `src/reposting_orchestrator.py` - Main orchestration logic
- `src/scraping/review_scraper.py` - Scraping implementation
- `src/article_factory.py` - Article instance creation
- `src/telegraph_manager.py` - Telegraph publishing
- `src/dao/repositories/` - Database repositories

## Future Enhancements

- Add support for testing Telegram bot posting when implemented
- Add support for testing channel posting when implemented
- Add performance benchmarking
- Add support for testing multiple reviews in batch
- Add support for testing error scenarios
