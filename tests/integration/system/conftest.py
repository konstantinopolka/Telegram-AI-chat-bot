"""
Configuration and fixtures for system integration tests.
"""

import pytest
from pathlib import Path


@pytest.fixture
def project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def test_data_dir(project_root):
    """Get the test data directory"""
    return project_root / "test_data"


@pytest.fixture
def output_dir(project_root):
    """Get the output directory for test results"""
    output_dir = project_root / "test_output"
    output_dir.mkdir(exist_ok=True)
    return output_dir
