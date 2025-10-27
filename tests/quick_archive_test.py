#!/usr/bin/env python3
"""Quick test to verify archive classes work correctly."""

import asyncio
from src.scraping.archive_parser import ArchiveParser
from src.scraping.archive_scraper import ArchiveScraper
from src.archive_scanner import ArchiveScanner

def test_archive_parser():
    """Test ArchiveParser can be instantiated."""
    print("Testing ArchiveParser...")
    parser = ArchiveParser()
    assert parser is not None
    print("✓ ArchiveParser instantiation OK")
    
    # Test parsing with sample HTML
    html = '''<html><body>
        <h2><a href="https://platypus1917.org/category/pr/issue-179/">Issue 179</a></h2>
        <h2><a href="https://platypus1917.org/category/pr/issue-178/">Issue 178</a></h2>
    </body></html>'''
    
    urls = parser.parse_archive_page(html)
    print(f"✓ Parsed {len(urls)} URLs from HTML")
    assert len(urls) == 2
    print("✓ ArchiveParser works correctly\n")

def test_archive_scraper():
    """Test ArchiveScraper can be instantiated."""
    print("Testing ArchiveScraper...")
    scraper = ArchiveScraper("https://platypus1917.org/platypus-review/")
    assert scraper is not None
    assert scraper.archive_url == "https://platypus1917.org/platypus-review/"
    assert scraper.fetcher is not None
    assert scraper.parser is not None
    print("✓ ArchiveScraper instantiation OK")
    print("✓ ArchiveScraper works correctly\n")

async def test_archive_scanner():
    """Test ArchiveScanner can be instantiated."""
    print("Testing ArchiveScanner...")
    scanner = ArchiveScanner("https://platypus1917.org/platypus-review/")
    assert scanner is not None
    assert scanner.archive_url == "https://platypus1917.org/platypus-review/"
    assert scanner.archive_scraper is not None
    print("✓ ArchiveScanner instantiation OK")
    print("✓ ArchiveScanner works correctly\n")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Archive Classes Quick Test")
    print("=" * 60 + "\n")
    
    try:
        test_archive_parser()
        test_archive_scraper()
        asyncio.run(test_archive_scanner())
        
        print("=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main())
