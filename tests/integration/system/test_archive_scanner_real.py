import asyncio
import pytest

from src.archive_scanner import ArchiveScanner
from src.dao import review_repository


@pytest.mark.asyncio
async def test_scan_for_new_reviews_real(monkeypatch):
    """Integration test: call scan_for_new_reviews() against the real archive page.

    The DB layer is monkeypatched so the test only verifies scraping + scanning logic
    and does not require a database.
    """

    async def _fake_get_all_source_urls():
        return set()

    # Patch out DB call so test doesn't need real DB
    monkeypatch.setattr(review_repository, "get_all_source_urls", _fake_get_all_source_urls)

    scanner = ArchiveScanner()

    result = await scanner.scan_for_new_reviews()

    assert isinstance(result, dict)
    assert result.get("total_count", 0) > 0, "Expected at least one URL from real archive"

    new_reviews = result.get("new_reviews")
    assert isinstance(new_reviews, set)
    assert len(new_reviews) > 0, "Expected new_reviews to be non-empty"

    # Check that at least one URL matches the archive issue pattern
    assert any("/category/pr/issue-" in url for url in new_reviews), "URLs should contain '/category/pr/issue-'"


@pytest.mark.asyncio
async def test_get_new_reviews_real(monkeypatch):
    """Integration test: ensure get_new_reviews() returns a non-empty set of URLs."""

    async def _fake_get_all_source_urls():
        return set()

    monkeypatch.setattr(review_repository, "get_all_source_urls", _fake_get_all_source_urls)

    scanner = ArchiveScanner()
    new_reviews = await scanner.get_new_reviews()

    assert isinstance(new_reviews, set)
    assert len(new_reviews) > 0
    assert any("/category/pr/issue-" in url for url in new_reviews)
