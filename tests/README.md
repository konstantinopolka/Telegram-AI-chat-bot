# Testing Guide

This directory contains all tests for the Bot project, organized into unit tests, integration tests, and system tests.

## 📁 Test Structure

```
tests/
├── unit/                           # Unit tests for individual components
│   ├── test_telegraph_manager.py   # Telegraph manager tests
│   └── test_scraping/              # Scraping module unit tests
│       ├── test_fetcher.py
│       ├── test_parser.py
│       ├── test_review_fetcher.py
│       ├── test_review_parser.py
│       └── test_review_scraper.py
├── integration/                    # Integration tests for component interactions
│   ├── scraping/                   # Scraping integration tests
│   │   ├── test_parser_integration.py
│   │   ├── test_review_fetcher_integration.py
│   │   └── test_review_parser_integration.py
│   └── system/                     # System-wide integration tests
│       ├── README.md
│       ├── conftest.py
│       ├── test_bulk_review_processing.py
│       └── test_fixtures_platypus_links.py
├── run_bulk_tests.sh              # Script for running system tests
├── test_single_article.py         # Standalone article test
└── *.json files                   # Test data and results
```

## 🛠️ Prerequisites

### 1. Python Environment Setup

Ensure you have Python 3.12+ and create a virtual environment:

```bash
# From project root
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
# Install test dependencies (includes base requirements)
pip install -r requirements/dev-requirements.txt

# Or install base requirements first, then dev
pip install -r requirements/base-requirements.txt
pip install -r requirements/dev-requirements.txt
```

### 3. Environment Variables

Make sure your environment variables are set (see `docker/database.env` for reference):
- Database configurations
- Telegraph API credentials
- Telegram bot tokens (for integration tests)

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run tests with coverage
pytest --cov=src

# Run specific test categories
pytest -m "not slow"        # Skip slow tests
pytest -m "integration"     # Only integration tests
pytest -m "system"          # Only system tests
```

### Test Categories

#### 1. Unit Tests
Test individual components in isolation:

```bash
# All unit tests
pytest tests/unit/ -v

# Specific component
pytest tests/unit/test_telegraph_manager.py -v
pytest tests/unit/test_scraping/ -v

# Specific test function
pytest tests/unit/test_scraping/test_parser.py::TestParser::test_parse_html -v
```

#### 2. Integration Tests
Test component interactions:

```bash
# All integration tests
pytest tests/integration/ -v

# Scraping integration tests
pytest tests/integration/scraping/ -v

# Specific integration test
pytest tests/integration/scraping/test_review_parser_integration.py -v
```

#### 3. System Tests
End-to-end workflow tests:

```bash
# Run via convenience script (recommended)
cd tests/
./run_bulk_tests.sh

# Or run directly with pytest
pytest tests/integration/system/ -v

# Run specific system test
pytest tests/integration/system/test_bulk_review_processing.py -v
```

### Standalone Tests

```bash
# Test single article processing
python tests/test_single_article.py

# Run specific test with custom parameters
pytest tests/test_single_article.py::test_process_specific_review -v
```

## 📊 Test Markers

Tests are organized using pytest markers (defined in `pytest.ini`):

- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.system` - System-wide tests  
- `@pytest.mark.slow` - Tests that take longer to run

### Using Markers

```bash
# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m "integration"

# Exclude system tests
pytest -m "not system"

# Combine markers
pytest -m "integration and not slow"
```

## 🔧 Test Configuration

### pytest.ini
The project uses a `pytest.ini` file with the following configuration:
- Test discovery patterns
- Async test support
- Marker definitions
- Default options (`-v --tb=short --strict-markers`)

### Async Tests
Tests use `pytest-asyncio` for async support:
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

## 📈 Test Output and Reports

### Generated Files
System tests generate several output files in the project root:

- `platypus_review_links.json` - All review links by year
- `platypus_all_issue_urls.json` - Flattened list of URLs
- `telegraph_test_results.json` - Processing statistics
- `failed_review_urls.json` - Failed processing URLs

### Understanding Output

```bash
# Run with detailed output
pytest tests/integration/system/ -v -s

# Generate coverage report
pytest --cov=src --cov-report=html
# View at htmlcov/index.html
```

## 🧪 Writing New Tests

### Test File Structure
```python
import pytest
from src.module_to_test import ComponentToTest

class TestComponentName:
    """Test class for ComponentName"""
    
    def setup_method(self):
        """Set up test fixtures for each test method"""
        self.component = ComponentToTest()
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        result = self.component.do_something()
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_async_functionality(self):
        """Test async functionality"""
        result = await self.component.async_method()
        assert result is not None
    
    @pytest.mark.integration
    def test_integration_scenario(self):
        """Integration test with multiple components"""
        pass
```

### Test Naming Conventions
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`
- Use descriptive names: `test_parse_content_page_integration`

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure PYTHONPATH is set correctly
   export PYTHONPATH="$(pwd):$PYTHONPATH"
   ```

2. **Async Test Failures**
   ```bash
   # Use asyncio mode
   pytest --asyncio-mode=auto
   ```

3. **Database Issues**
   ```bash
   # Check database setup and migrations
   alembic upgrade head
   ```

4. **Environment Variables**
   ```bash
   # Source environment file
   source docker/database.env
   ```

### Getting Help

- Check test logs and error messages carefully
- Use `-v` and `-s` flags for detailed output
- Run individual tests to isolate issues
- Check the `pytest.ini` configuration
- Verify all dependencies are installed

## 📚 Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- See `tests/integration/system/README.md` for system test details
- Check individual test files for specific component documentation

---

For questions about specific tests or to add new test cases, refer to the existing test files as examples and follow the established patterns.
