"""
Integration tests for bulk processing of Platypus Review issues.

This module contains tests for processing multiple review issues from the Platypus archive,
including extraction of all review links and batch processing using RepostingOrchestrator.
"""

import json
import time
import asyncio
import pytest
from typing import List, Dict, Any
from pathlib import Path
import requests
from bs4 import BeautifulSoup

from src.scraping.review_scraper import ReviewScraper
from src.reposting_orchestrator import RepostingOrchestrator
from src.telegraph_manager import TelegraphManager
from src.scraping.parser import Parser


class PlatypusArchiveExtractor(Parser):
    """
    Utility class for extracting all review links from Platypus archive.
    This functionality is specific to testing and not part of the main scraper.
    Inherits from Parser to reuse URL normalization and other utilities.
    """
    
    def __init__(self):
        self.base_archive_url = "https://platypus1917.org/platypus-review/"
        
    def extract_all_review_links(self) -> Dict[str, List[str]]:
        """
        Extract all review issue links organized by year.
        
        Returns:
            Dict with years as keys and lists of review URLs as values
        """
        try:
            response = requests.get(self.base_archive_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            review_links_by_year = {}
            
            # Find archive sections - each year is in div.dc-over-wrapper
            archive_sections = self._find_archive_sections(soup)
            
            for section in archive_sections:
                year, links = self._extract_year_and_links(section)
                if year and links:
                    review_links_by_year[year] = links
                    
            return review_links_by_year
            
        except Exception as e:
            print(f"Error extracting review links: {e}")
            return {}
    
    def _find_archive_sections(self, soup: BeautifulSoup) -> List:
        """Find all archive year sections - each in div.dc-over-wrapper"""
        # Find divs with class "dc-over-wrapper" that are direct children of "dc-four dc-columns"
        parent_divs = soup.find_all('div', class_='dc-four dc-columns')
        year_sections = []
        
        for parent in parent_divs:
            wrapper_divs = parent.find_all('div', class_='dc-over-wrapper', recursive=False)
            for wrapper in wrapper_divs:
                # Look for h2 with year inside this wrapper
                h2 = wrapper.find('h2')
                if h2 and h2.get_text(strip=True).isdigit():
                    year_sections.append(wrapper)
                    
        return year_sections
    
    def _extract_year_and_links(self, section_div) -> tuple:
        """Extract year and review links from a section div"""
        # Get year from h2 tag
        h2 = section_div.find('h2')
        if not h2:
            return None, []
            
        year = h2.get_text(strip=True)
        
        # Find all links in paragraphs within this section
        links = []
        for p in section_div.find_all('p'):
            for link in p.find_all('a', href=True):
                href = link['href']
                # Look for issue links: /category/pr/issue-XXX/
                if '/category/pr/issue-' in href:
                    # Use inherited normalize_url method
                    full_url = self.normalize_url(href, self.base_archive_url)
                    links.append(full_url)
                
        return year, links
    
    # Required abstract method implementations (not used for archive extraction)
    def parse_listing_page(self, html: str) -> List[str]:
        """Not used for archive extraction"""
        return []
    
    def parse_content_page(self, html: str, url: str) -> Dict[str, Any]:
        """Not used for archive extraction"""
        return {}
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Not used for archive extraction"""
        return ""
    
    def extract_content(self, soup: BeautifulSoup) -> str:
        """Not used for archive extraction"""
        return ""
    
    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Not used for archive extraction"""
        return {}
    
    def clean_content_for_publishing(self, content_div) -> str:
        """Not used for archive extraction"""
        return ""
        


class BulkProcessingStatistics:
    """Tracks statistics during bulk processing of reviews"""
    
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.total_reviews = 0
        self.successful_reviews = 0
        self.failed_reviews = 0
        self.failed_review_urls = []
        self.total_articles = 0
        self.successful_articles = 0
        self.failed_articles = 0
        self.telegraph_successes = 0
        self.telegraph_failures = 0
        self.over_60kb_articles = []
        self.processing_details = []
        self.errors = []
        
    def record_review_start(self, review_url: str):
        self.total_reviews += 1
        self.current_review_start_time = time.time()
        
    def record_review_success(self, review_data: Dict[str, Any]):
        self.successful_reviews += 1
        processing_time = time.time() - self.current_review_start_time
        self.processing_details.append({"processing_time": processing_time})
        
        # Count articles
        articles = review_data.get('articles', [])
        self.total_articles += len(articles)
        
        for article in articles:
            if article:  # Successfully processed
                self.successful_articles += 1
                # Check Telegraph status
                if article.get('telegraph_urls'):
                    self.telegraph_successes += 1
                else:
                    self.telegraph_failures += 1
                    
                # Check size for reporting
                content_size = len(article.get('content', '').encode('utf-8'))
                if content_size > 60 * 1024:  # 60KB
                    self.over_60kb_articles.append({
                        'title': article.get('title', 'Unknown'),
                        'url': article.get('original_url', ''),
                        'size_bytes': content_size,
                        'size_kb': round(content_size / 1024, 1),
                        'review_url': review_data.get('source_url', '')
                    })
            else:
                self.failed_articles += 1
                
    def record_review_failure(self, review_url: str, error: str):
        self.failed_reviews += 1
        self.failed_review_urls.append(review_url)
        self.errors.append(f"Failed to process {review_url}: {error}")
        
    def get_summary(self) -> Dict[str, Any]:
        return {
            'total_reviews': self.total_reviews,
            'successful_reviews': self.successful_reviews,
            'failed_reviews': self.failed_reviews,
            'total_articles': self.total_articles,
            'successful_articles': self.successful_articles,
            'failed_articles': self.failed_articles,
            'telegraph_successes': self.telegraph_successes,
            'telegraph_failures': self.telegraph_failures,
            'over_60kb_articles': self.over_60kb_articles,
            'processing_details': self.processing_details,
            'errors': self.errors
        }


class BulkReviewProcessor:
    """
    Integration tests for bulk review processing.
    Uses RepostingOrchestrator to process multiple reviews with statistics tracking.
    """
    
    def __init__(self):
        self.extractor = PlatypusArchiveExtractor()
        self.stats = BulkProcessingStatistics()
        
    async def test_extract_all_review_links(self):
        """Test extraction of all review links from archive"""
        print("Testing extraction of all review links...")
        
        links_by_year = self.extractor.extract_all_review_links()
        
        # Save results
        output_file = Path(__file__).parent.parent.parent / "platypus_review_links.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(links_by_year, f, indent=2, ensure_ascii=False)
            
        # Flatten for easy access
        all_links = []
        for year_links in links_by_year.values():
            all_links.extend(year_links)
            
        all_links_file = Path(__file__).parent.parent.parent / "platypus_all_issue_urls.json"
        with open(all_links_file, 'w', encoding='utf-8') as f:
            json.dump({"all_issue_urls": all_links}, f, indent=2, ensure_ascii=False)
            
        print(f"Extracted {len(all_links)} total review links")
        for year, links in links_by_year.items():
            print(f"  {year}: {len(links)} reviews")
            
        assert len(all_links) > 0, "Should extract some review links"
        return links_by_year
    
    async def test_process_recent_reviews(self, max_reviews: int = 5):
        """
        Test processing a limited number of recent reviews using RepostingOrchestrator.
        This is the main integration test that uses existing architecture.
        """
        print(f"Testing processing of {max_reviews} recent reviews...")
        
        # Get review links
        links_by_year = self.extractor.extract_all_review_links()
        
        # Get recent reviews (from latest years)
        recent_reviews = []
        for year in sorted(links_by_year.keys(), key=int, reverse=True):
            recent_reviews.extend(links_by_year[year])
            if len(recent_reviews) >= max_reviews:
                break
                
        recent_reviews = recent_reviews[:max_reviews]
        
        # Initialize components (mock/test versions)
        # Load Telegraph token from graph_bot.json
        graph_bot_file = Path(__file__).parent.parent.parent.parent / "graph_bot.json"
        try:
            with open(graph_bot_file, 'r') as f:
                graph_bot_data = json.load(f)
                access_token = graph_bot_data['access_token']
        except Exception as e:
            print(f"Warning: Could not load Telegraph token from graph_bot.json: {e}")
            access_token = "test_token"  # Fallback
            
        telegraph_manager = TelegraphManager(access_token=access_token)
        
        self.stats.reset()
        processed_reviews = []
        
        for review_url in recent_reviews:
            try:
                self.stats.record_review_start(review_url)
                
                # Create scraper for this review
                scraper = ReviewScraper(review_url)
                
                # Create orchestrator (with None for components we're not testing)
                orchestrator = RepostingOrchestrator(
                    review_scraper=scraper,
                    telegraph_manager=telegraph_manager,
                    db_session=None,  # Skip DB for testing
                    bot_handler=None,  # Skip bot for testing 
                    channel_poster=None  # Skip channel for testing
                )
                
                # Process the review using existing architecture
                review_result = await orchestrator.process_review_batch()
                
                if review_result:
                    # Convert Article object to dict for statistics
                    review_dict = {
                        'source_url': review_result.source_url,
                        'articles': [article.__dict__ if hasattr(article, '__dict__') else article for article in review_result.articles]
                    }
                    self.stats.record_review_success(review_dict)
                    processed_reviews.append(review_result)
                    print(f"✓ Successfully processed {review_url}")
                else:
                    self.stats.record_review_failure(review_url, "No articles returned")
                    print(f"✗ Failed to process {review_url}")
                    
            except Exception as e:
                self.stats.record_review_failure(review_url, str(e))
                print(f"✗ Error processing {review_url}: {e}")
                
        # Save results and statistics
        await self._save_test_results()
        
        # Assertions
        assert self.stats.successful_reviews > 0, "Should successfully process at least one review"
        assert len(processed_reviews) > 0, "Should have processed reviews"
        
        print(f"Test completed: {self.stats.successful_reviews}/{self.stats.total_reviews} reviews processed successfully")
        return processed_reviews
    
    async def test_telegraph_size_limits(self):
        """Test articles that exceed Telegraph size limits"""
        # This would use the over_60kb_articles from processing results
        large_articles = self.stats.over_60kb_articles
        
        if large_articles:
            print(f"Found {len(large_articles)} articles over 60KB:")
            for article in large_articles[:5]:  # Show first 5
                print(f"  - {article['title']} ({article['size_kb']}KB)")
                
        return large_articles
    
    async def _save_test_results(self):
        """Save test results and failed URLs for analysis"""
        results_file = Path(__file__).parent.parent.parent / "telegraph_test_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats.get_summary(), f, indent=2, ensure_ascii=False)
            
        if self.stats.failed_review_urls:
            failed_file = Path(__file__).parent.parent.parent / "failed_review_urls.json"
            with open(failed_file, 'w', encoding='utf-8') as f:
                json.dump({"failed_urls": self.stats.failed_review_urls}, f, indent=2)


# Standalone test functions for pytest compatibility
@pytest.mark.asyncio
async def test_extract_review_links():
    """Pytest-compatible test function"""
    processor = BulkReviewProcessor()
    return await processor.test_extract_all_review_links()

@pytest.mark.asyncio
async def test_process_reviews():
    """Pytest-compatible test function"""
    processor = BulkReviewProcessor()
    return await processor.test_process_recent_reviews(max_reviews=3)


# Main execution for manual testing
if __name__ == "__main__":
    async def main():
        processor = BulkReviewProcessor()
        
        print("=== Phase 1: Extract all review links ===")
        await processor.test_extract_all_review_links()
        
        print("\n=== Phase 2: Process recent reviews ===")
        await processor.test_process_recent_reviews(max_reviews=5)
        
        print("\n=== Phase 3: Analyze large articles ===")
        await processor.test_telegraph_size_limits()
        
        print("\n=== Test Summary ===")
        summary = processor.stats.get_summary()
        print(f"Total reviews processed: {summary['successful_reviews']}/{summary['total_reviews']}")
        print(f"Total articles processed: {summary['successful_articles']}/{summary['total_articles']}")
        print(f"Telegraph successes: {summary['telegraph_successes']}")
        print(f"Articles over 60KB: {len(summary['over_60kb_articles'])}")
    
    asyncio.run(main())
