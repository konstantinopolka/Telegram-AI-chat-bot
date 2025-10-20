"""
Debug script for testing a single Platypus Review issue processing.

This script allows step-by-step debugging of the complete workflow:
1. Review scraping (article extraction)
2. Article schema creation and validation  
3. Telegraph article generation
4. Database operations (mocked)
5. Channel posting (mocked)

Default test review: https://platypus1917.org/category/pr/issue-178/
"""


import json
import os
import time
import asyncio
import pytest
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass
import sys

# Add project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.scraping.review_scraper import ReviewScraper
from src.reposting_orchestrator import RepostingOrchestrator  
from src.telegraph_manager import TelegraphManager
from src.dao.models import Article, Review
from src.article_factory import article_factory


class MockTelegraphManager:
    """Mock Telegraph manager for testing without real API calls"""
    
    def __init__(self):
        self.test_mode = True
        
    async def create_article(self, article: Article) -> List[str]:
        """Mock article creation that returns fake URLs"""
        print(f"   📝 [MOCK] Creating Telegraph article for: {article.title}")
        print(f"   📏 Content length: {len(article.content)} characters")
        
        # Simulate the splitting logic
        content_length = len(article.content)
        if content_length > 60000:
            # Mock multi-part article
            num_parts = (content_length // 60000) + 1
            urls = [f"https://telegra.ph/mock-{article.title.lower().replace(' ', '-')}-part-{i+1}" 
                   for i in range(num_parts)]
            print(f"   📄 [MOCK] Created {num_parts} Telegraph pages (content too large)")
        else:
            # Mock single article
            urls = [f"https://telegra.ph/mock-{article.title.lower().replace(' ', '-')}"]
            print(f"   📄 [MOCK] Created 1 Telegraph page")
            
        for url in urls:
            print(f"      🔗 {url}")
            
        return urls


@dataclass
class SingleReviewDebugResults:
    """Container for debug results from single review processing"""
    review_url: str
    review_id: Optional[int] = None
    scraping_success: bool = False
    articles_found: int = 0
    articles_processed: int = 0
    telegraph_urls: List[str] = None
    processing_time: float = 0.0
    errors: List[str] = None
    raw_review_data: Dict[str, Any] = None
    processed_review: Optional[Review] = None
    
    def __post_init__(self):
        if self.telegraph_urls is None:
            self.telegraph_urls = []
        if self.errors is None:
            self.errors = []


class SingleReviewDebugger:
    """
    Debug utility for processing a single review with detailed logging and inspection.
    Uses the existing RepostingOrchestrator workflow for realistic testing.
    """
    
    def __init__(self, review_url: str = "https://platypus1917.org/category/pr/issue-178/"):
        self.review_url = review_url
        self.results = SingleReviewDebugResults(review_url=review_url)
        
        # Initialize components
        self._setup_components()
        
    def _setup_components(self):
        """Initialize all the components needed for processing"""
        print(f"🔧 Setting up components for review: {self.review_url}")
        
        # Initialize scraper
        self.review_scraper = ReviewScraper(self.review_url)
        
        # Initialize Telegraph manager with test mode
        # Check if we have real credentials or use test mode
        access_token = os.getenv('TELEGRAPH_ACCESS_TOKEN')
        if not access_token or access_token == "test_token":
            print("   ⚠️  Using test mode - no real Telegraph articles will be created")
            # Create a mock Telegraph manager for testing
            self.telegraph_manager = MockTelegraphManager()
        else:
            print("   📡 Using real Telegraph API")
            self.telegraph_manager = TelegraphManager(access_token=access_token)
        
        # Mock database session and other components for testing
        self.db_session = None  # Would be real DB session in production
        self.bot_handler = None  # Would be real bot handler in production
        self.channel_poster = None  # Would be real channel poster in production
        
        # Initialize orchestrator with all components
        self.orchestrator = RepostingOrchestrator(
            review_scraper=self.review_scraper,
            telegraph_manager=self.telegraph_manager,
            db_session=self.db_session,
            bot_handler=self.bot_handler,
            channel_poster=self.channel_poster
        )
        
        print("✅ Component setup complete")

    async def debug_full_workflow(self) -> SingleReviewDebugResults:
        """
        Run the complete workflow with detailed debugging output.
        This mirrors the production workflow exactly.
        """
        print(f"\n🚀 Starting full workflow debug for review: {self.review_url}")
        start_time = time.time()
        
        try:
            # Step 1: Process the review batch using orchestrator
            print("\n=== STEP 1: Review Batch Processing ===")
            processed_review = await self.orchestrator.process_review_batch()
            
            # Record results
            self.results.processed_review = processed_review
            self.results.processing_time = time.time() - start_time
            
            if processed_review:
                self.results.scraping_success = True
                self.results.review_id = processed_review.id
                self.results.articles_found = len(processed_review.articles)
                self.results.articles_processed = len([a for a in processed_review.articles if a.telegraph_urls])
                
                # Collect all telegraph URLs
                for article in processed_review.articles:
                    if article.telegraph_urls:
                        self.results.telegraph_urls.extend(article.telegraph_urls)
                        
                print(f"✅ Review processing complete!")
                print(f"   Review ID: {self.results.review_id}")
                print(f"   Articles found: {self.results.articles_found}")
                print(f"   Articles with Telegraph URLs: {self.results.articles_processed}")
                print(f"   Total Telegraph URLs: {len(self.results.telegraph_urls)}")
            else:
                self.results.errors.append("Review processing returned None")
                print("❌ Review processing failed")
                
        except Exception as e:
            error_msg = f"Full workflow error: {str(e)}"
            self.results.errors.append(error_msg)
            print(f"❌ {error_msg}")
            
        self.results.processing_time = time.time() - start_time
        print(f"\n⏱️  Total processing time: {self.results.processing_time:.2f} seconds")
        
        return self.results

    async def debug_step_by_step(self) -> SingleReviewDebugResults:
        """
        Debug each step individually with detailed inspection points.
        Useful for identifying exactly where issues occur.
        """
        print(f"\n🔍 Starting step-by-step debug for review: {self.review_url}")
        start_time = time.time()
        
        try:
            # Step 1: Test scraping
            print("\n=== STEP 1: Raw Review Scraping ===")
            raw_review_data = await self._debug_scraping()
            
            if not raw_review_data:
                self.results.errors.append("Scraping failed - no data returned")
                return self.results
                
            # Step 2: Test article schema creation  
            print("\n=== STEP 2: Article Schema Creation ===")
            articles = await self._debug_article_creation(raw_review_data)
            
            # Step 3: Test Telegraph processing
            print("\n=== STEP 3: Telegraph Processing ===") 
            await self._debug_telegraph_processing(articles)
            
            # Step 4: Mock database operations
            print("\n=== STEP 4: Database Operations (Mocked) ===")
            await self._debug_database_operations(articles)
            
            # Step 5: Mock channel posting
            print("\n=== STEP 5: Channel Posting (Mocked) ===")
            await self._debug_channel_posting(articles)
            
            # Final results compilation
            self._compile_final_results(raw_review_data, articles)
            
        except Exception as e:
            error_msg = f"Step-by-step debug error: {str(e)}"
            self.results.errors.append(error_msg)
            print(f"❌ {error_msg}")
            
        self.results.processing_time = time.time() - start_time
        print(f"\n⏱️  Total processing time: {self.results.processing_time:.2f} seconds")
        
        return self.results

    async def _debug_scraping(self) -> Optional[Dict[str, Any]]:
        """Debug the scraping step"""
        try:
            print(f"   📥 Scraping review from: {self.review_url}")
            raw_review_data = self.review_scraper.scrape_review_batch()
            
            if raw_review_data:
                self.results.scraping_success = True
                self.results.review_id = raw_review_data.get('review_id')
                self.results.raw_review_data = raw_review_data
                
                articles = raw_review_data.get('articles', [])
                self.results.articles_found = len(articles)
                
                print(f"   ✅ Scraping successful!")
                print(f"      Review ID: {self.results.review_id}")
                print(f"      Articles found: {len(articles)}")
                
                # Show article titles
                for i, article in enumerate(articles, 1):
                    title = article.get('title', 'No title')
                    content_len = len(article.get('content', ''))
                    print(f"      {i}. {title} ({content_len} chars)")
                    
                return raw_review_data
            else:
                print("   ❌ Scraping returned no data")
                return None
                
        except Exception as e:
            error_msg = f"Scraping error: {str(e)}"
            self.results.errors.append(error_msg)
            print(f"   ❌ {error_msg}")
            return None

    async def _debug_article_creation(self, raw_review_data: Dict[str, Any]) -> List[Article]:
        """Debug article schema creation"""
        try:
            print("   📝 Creating Article schemas from raw data...")
            articles = article_factory.from_scraper_data(raw_review_data)
            
            print(f"   ✅ Created {len(articles)} Article schemas")
            
            # Validate each article
            for i, article in enumerate(articles, 1):
                print(f"      {i}. {article.title}")
                print(f"         Authors: {article.authors}")
                print(f"         Content length: {len(article.content)} chars")
                print(f"         Published: {article.published_date}")
                
            return articles
            
        except Exception as e:
            error_msg = f"Article creation error: {str(e)}"
            self.results.errors.append(error_msg)
            print(f"   ❌ {error_msg}")
            return []

    async def _debug_telegraph_processing(self, articles: List[Article]):
        """Debug Telegraph processing for each article"""
        try:
            print("   📡 Processing articles for Telegraph...")
            
            for i, article in enumerate(articles, 1):
                print(f"   Processing article {i}/{len(articles)}: {article.title}")
                
                try:
                    telegraph_urls = await self.telegraph_manager.create_telegraph_articles(article)
                    if telegraph_urls:
                        article.telegraph_urls = telegraph_urls
                        self.results.telegraph_urls.extend(telegraph_urls)
                        print(f"      ✅ Created {len(telegraph_urls)} Telegraph page(s)")
                        for url in telegraph_urls:
                            print(f"         📄 {url}")
                    else:
                        print(f"      ❌ Telegraph creation failed")
                        
                except Exception as e:
                    error_msg = f"Telegraph error for '{article.title}': {str(e)}"
                    self.results.errors.append(error_msg)
                    print(f"      ❌ {error_msg}")
                    
            self.results.articles_processed = len([a for a in articles if a.telegraph_urls])
            print(f"   ✅ Telegraph processing complete: {self.results.articles_processed}/{len(articles)} successful")
            
        except Exception as e:
            error_msg = f"Telegraph processing error: {str(e)}"
            self.results.errors.append(error_msg)
            print(f"   ❌ {error_msg}")

    async def _debug_database_operations(self, articles: List[Article]):
        """Debug database operations (mocked for testing)"""
        try:
            print("   💾 Database operations (mocked)...")
            
            for article in articles:
                # In production, this would save to actual database
                print(f"      📝 [MOCK] Saving article: {article.title}")
                
            print("   ✅ Database operations complete (mocked)")
            
        except Exception as e:
            error_msg = f"Database error: {str(e)}"
            self.results.errors.append(error_msg)
            print(f"   ❌ {error_msg}")

    async def _debug_channel_posting(self, articles: List[Article]):
        """Debug channel posting (mocked for testing)"""
        try:
            print("   📢 Channel posting (mocked)...")
            
            for article in articles:
                if article.telegraph_urls:
                    # In production, this would post to actual Telegram channel
                    print(f"      📨 [MOCK] Posting to channel: {article.title}")
                    print(f"         URLs: {', '.join(article.telegraph_urls)}")
                    
            print("   ✅ Channel posting complete (mocked)")
            
        except Exception as e:
            error_msg = f"Channel posting error: {str(e)}"
            self.results.errors.append(error_msg)
            print(f"   ❌ {error_msg}")

    def _compile_final_results(self, raw_review_data: Dict[str, Any], articles: List[Article]):
        """Compile final results"""
        self.results.raw_review_data = raw_review_data
        
        # Create Review schema for results
        if articles:
            self.results.processed_review = Review(
                id=self.results.review_id,
                source_url=self.review_url,
                articles=articles,
                created_at=raw_review_data.get('created_at')
            )

    def save_debug_results(self, filename: str = "single_review_debug_results.json"):
        """Save debug results to JSON file"""
        results_dict = {
            'review_url': self.results.review_url,
            'review_id': self.results.review_id,
            'scraping_success': self.results.scraping_success,
            'articles_found': self.results.articles_found,
            'articles_processed': self.results.articles_processed,
            'telegraph_urls': self.results.telegraph_urls,
            'processing_time': self.results.processing_time,
            'errors': self.results.errors,
            'raw_review_data': self.results.raw_review_data,
        }
        
        # Add processed review info if available
        if self.results.processed_review:
            results_dict['processed_review'] = {
                'id': self.results.processed_review.id,
                'source_url': self.results.processed_review.source_url,
                'articles_count': len(self.results.processed_review.articles),
                'articles': [
                    {
                        'title': article.title,
                        'authors': article.authors,
                        'telegraph_urls': article.telegraph_urls or [],
                        'content_length': len(article.content)
                    }
                    for article in self.results.processed_review.articles
                ]
            }
            
        output_path = Path(__file__).parent.parent.parent / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Debug results saved to: {output_path}")

    def print_summary(self):
        """Print a summary of the debug results"""
        print(f"\n📊 DEBUG SUMMARY")
        print(f"{'='*50}")
        print(f"Review URL: {self.results.review_url}")
        print(f"Review ID: {self.results.review_id}")
        print(f"Scraping Success: {'✅' if self.results.scraping_success else '❌'}")
        print(f"Articles Found: {self.results.articles_found}")
        print(f"Articles Processed: {self.results.articles_processed}")
        print(f"Telegraph URLs: {len(self.results.telegraph_urls)}")
        print(f"Processing Time: {self.results.processing_time:.2f}s")
        print(f"Errors: {len(self.results.errors)}")
        
        if self.results.errors:
            print("\n❌ ERRORS:")
            for i, error in enumerate(self.results.errors, 1):
                print(f"   {i}. {error}")
                
        if self.results.telegraph_urls:
            print("\n📄 TELEGRAPH URLS:")
            for i, url in enumerate(self.results.telegraph_urls, 1):
                print(f"   {i}. {url}")


# Pytest compatible functions
@pytest.mark.asyncio
async def test_single_review_full_workflow():
    """Pytest-compatible test for full workflow"""
    debugger = SingleReviewDebugger()
    results = await debugger.debug_full_workflow()
    debugger.print_summary()
    
    # Assertions for testing
    assert results.scraping_success, "Review scraping should succeed"
    assert results.articles_found > 0, "Should find at least one article"
    
    return results

@pytest.mark.asyncio 
async def test_single_review_step_by_step():
    """Pytest-compatible test for step-by-step debugging"""
    debugger = SingleReviewDebugger()
    results = await debugger.debug_step_by_step()
    debugger.print_summary()
    
    # Assertions for testing
    assert results.scraping_success, "Review scraping should succeed"
    assert results.articles_found > 0, "Should find at least one article"
    
    return results


# Main execution for manual testing and debugging
if __name__ == "__main__":
    async def main():
        print("🔍 Single Review Debug Script")
        print("=" * 50)
        
        # Option 1: Use default review
        print("\n🎯 Option 1: Debug default review (issue-178)")
        debugger_default = SingleReviewDebugger()
        
        # Option 2: Debug a custom review (uncomment to use)
        # custom_url = "https://platypus1917.org/category/pr/issue-173/"
        # print(f"\n🎯 Option 2: Debug custom review ({custom_url})")
        # debugger_custom = SingleReviewDebugger(custom_url)
        
        # Choose debugging mode
        print("\n🔧 Select debugging mode:")
        print("1. Full workflow (uses RepostingOrchestrator)")
        print("2. Step-by-step (detailed debugging)")
        
        # For manual debugging, you can uncomment the mode you want:
        
        # Mode 1: Full workflow
        print(f"\n🚀 Running Full Workflow Debug...")
        results = await debugger_default.debug_full_workflow()
        
        # Mode 2: Step-by-step (uncomment to use instead)
        # print(f"\n🔍 Running Step-by-Step Debug...")
        # results = await debugger_default.debug_step_by_step()
        
        # Print results
        debugger_default.print_summary()
        
        # Save results
        debugger_default.save_debug_results()
        
        print(f"\n✅ Debug session complete!")
        
        # Debugging breakpoint - you can set breakpoints here in your debugger
        # to inspect variables and results
        print("🔍 [DEBUG POINT] Set breakpoints here to inspect results")
        
    # Run the async main function
    asyncio.run(main())
