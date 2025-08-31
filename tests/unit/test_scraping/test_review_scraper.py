import pytest
from unittest.mock import Mock, patch, MagicMock
from src.scraping.review_scraper import ReviewScraper
from src.scraping.scraper import Scraper


class TestReviewScraper:
    """Test the ReviewScraper concrete implementation"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.base_url = "https://platypus1917.org/platypus-review/"
        self.scraper = ReviewScraper(self.base_url)
    
    def test_init(self):
        """Test ReviewScraper initialization"""
        assert self.scraper.base_url == self.base_url
        assert isinstance(self.scraper, Scraper)
        assert hasattr(self.scraper, 'fetcher')
        assert hasattr(self.scraper, 'parser')
    
    def test_get_listing_urls_success(self):
        """Test successful URL listing extraction"""
        mock_html = "<html>mock content</html>"
        expected_urls = ["https://platypus1917.org/2025/01/article1/", 
                        "https://platypus1917.org/2025/01/article2/"]
        
        with patch.object(self.scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(self.scraper.parser, 'parse_listing_page') as mock_parse:
            
            mock_fetch.return_value = mock_html
            mock_parse.return_value = expected_urls
            
            result = self.scraper.get_listing_urls()
            
            mock_fetch.assert_called_once_with(self.base_url)
            mock_parse.assert_called_once_with(mock_html)
            assert result == expected_urls
    
    def test_get_listing_urls_error_handling(self):
        """Test error handling in URL listing extraction"""
        with patch.object(self.scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(self.scraper, 'handle_scraping_error') as mock_error:
            
            mock_fetch.side_effect = Exception("Network error")
            
            result = self.scraper.get_listing_urls()
            
            assert result == []
            mock_error.assert_called_once()

    def test_get_content_data_success(self):
        """Test successful content data extraction"""
        article_url = "https://platypus1917.org/2025/01/article1/"
        mock_html = "<html>article content</html>"
        expected_content = {
            'title': 'Test Article',
            'content': '<p>Article content goes here</p>',
            'url': article_url
        }
        
        with patch.object(self.scraper.fetcher, 'validate_url') as mock_validate, \
             patch.object(self.scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(self.scraper.parser, 'parse_content_page') as mock_parse:
            
            mock_validate.return_value = True
            mock_fetch.return_value = mock_html
            mock_parse.return_value = expected_content
            
            result = self.scraper.get_content_data(article_url)
            
            mock_validate.assert_called_once_with(article_url)
            mock_fetch.assert_called_once_with(article_url)
            mock_parse.assert_called_once_with(mock_html, article_url)
            assert result == expected_content

    def test_get_content_data_invalid_url(self):
        """Test get_content_data with invalid URL"""
        article_url = "invalid-url"
        
        with patch.object(self.scraper.fetcher, 'validate_url') as mock_validate:
            mock_validate.return_value = False
            
            result = self.scraper.get_content_data(article_url)
            
            mock_validate.assert_called_once_with(article_url)
            assert result is None
    
    def test_scrape_single_article_success(self):
        """Test successful single article scraping"""
        article_url = "https://platypus1917.org/2025/01/article/"
        mock_html = "<html>article content</html>"
        expected_data = {
            'title': 'Test Article',
            'content': '<p>Content</p>',
            'original_url': article_url,
            'authors': ['Author'],
            'published_date': 'January 2025',
            'review_id': 173
        }
        
        with patch.object(self.scraper.fetcher, 'validate_url') as mock_validate, \
             patch.object(self.scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(self.scraper.parser, 'parse_content_page') as mock_parse, \
             patch.object(self.scraper, 'validate_content_data') as mock_validate_content:
            
            mock_validate.return_value = True
            mock_fetch.return_value = mock_html
            mock_parse.return_value = expected_data
            mock_validate_content.return_value = True
            
            result = self.scraper.scrape_single_article(article_url)
            
            mock_validate.assert_called_once_with(article_url)
            mock_fetch.assert_called_once_with(article_url)
            mock_parse.assert_called_once_with(mock_html, article_url)
            mock_validate_content.assert_called_once_with(expected_data)
            assert result == expected_data
    
    def test_scrape_single_article_invalid_url(self):
        """Test single article scraping with invalid URL"""
        article_url = "invalid-url"
        
        with patch.object(self.scraper.fetcher, 'validate_url') as mock_validate:
            mock_validate.return_value = False
            
            result = self.scraper.scrape_single_article(article_url)
            
            assert result is None
            mock_validate.assert_called_once_with(article_url)
    
    def test_scrape_single_article_invalid_content(self):
        """Test single article scraping with invalid content"""
        article_url = "https://platypus1917.org/2025/01/article/"
        mock_html = "<html>content</html>"
        content_data = {'title': '', 'content': '', 'original_url': article_url}
        
        with patch.object(self.scraper.fetcher, 'validate_url') as mock_validate, \
             patch.object(self.scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(self.scraper.parser, 'parse_content_page') as mock_parse, \
             patch.object(self.scraper, 'validate_content_data') as mock_validate_content:
            
            mock_validate.return_value = True
            mock_fetch.return_value = mock_html
            mock_parse.return_value = content_data
            mock_validate_content.return_value = False
            
            result = self.scraper.scrape_single_article(article_url)
            
            assert result is None
    
    def test_scrape_single_article_error_handling(self):
        """Test error handling in single article scraping"""
        article_url = "https://platypus1917.org/2025/01/article/"
        
        with patch.object(self.scraper.fetcher, 'validate_url') as mock_validate, \
             patch.object(self.scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(self.scraper, 'handle_scraping_error') as mock_error:
            
            mock_validate.return_value = True
            mock_fetch.side_effect = Exception("Fetch error")
            
            result = self.scraper.scrape_single_article(article_url)
            
            assert result is None
            mock_error.assert_called_once()
    
    def test_scrape_review_batch_success(self):
        """Test successful review batch scraping"""
        article_urls = [
            "https://platypus1917.org/2025/01/article1/",
            "https://platypus1917.org/2025/01/article2/"
        ]
        
        article_data_1 = {
            'title': 'Article 1',
            'content': '<p>Content 1</p>',
            'original_url': article_urls[0]
        }
        article_data_2 = {
            'title': 'Article 2', 
            'content': '<p>Content 2</p>',
            'original_url': article_urls[1]
        }
        
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(self.scraper, 'scrape_single_article') as mock_scrape:
            
            mock_get_urls.return_value = article_urls
            mock_scrape.side_effect = [article_data_1, article_data_2]
            
            result = self.scraper.scrape_review_batch()
            
            mock_get_urls.assert_called_once()
            assert mock_scrape.call_count == 2
            mock_scrape.assert_any_call(article_urls[0])
            mock_scrape.assert_any_call(article_urls[1])
            assert result == [article_data_1, article_data_2]
    
    def test_scrape_review_batch_no_urls(self):
        """Test review batch scraping when no URLs found"""
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls:
            mock_get_urls.return_value = []
            
            result = self.scraper.scrape_review_batch()
            
            assert result == []
    
    def test_scrape_review_batch_partial_success(self):
        """Test review batch scraping with some failed articles"""
        article_urls = [
            "https://platypus1917.org/2025/01/article1/",
            "https://platypus1917.org/2025/01/article2/",
            "https://platypus1917.org/2025/01/article3/"
        ]
        
        article_data_1 = {
            'title': 'Article 1',
            'content': '<p>Content 1</p>',
            'original_url': article_urls[0]
        }
        
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(self.scraper, 'scrape_single_article') as mock_scrape:
            
            mock_get_urls.return_value = article_urls
            # First succeeds, second and third fail
            mock_scrape.side_effect = [article_data_1, None, None]
            
            result = self.scraper.scrape_review_batch()
            
            assert len(result) == 1
            assert result[0] == article_data_1
    
    def test_scrape_review_batch_error_handling(self):
        """Test error handling in review batch scraping"""
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(self.scraper, 'handle_scraping_error') as mock_error:
            
            mock_get_urls.side_effect = Exception("Listing error")
            
            result = self.scraper.scrape_review_batch()
            
            assert result == []
            mock_error.assert_called_once()


class TestReviewScraperValidation:
    """Test ReviewScraper content validation"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scraper = ReviewScraper("https://example.com")
    
    def test_validate_content_data_valid(self):
        """Test content validation with valid data"""
        valid_data = {
            'title': 'Valid Article Title',
            'content': '<p>This is valid content with sufficient length for validation. It needs to be at least 100 characters long and contain paragraph tags.</p>',
            'original_url': 'https://example.com/article',
            'authors': ['Author Name'],
            'published_date': 'January 2025'
        }
        
        result = self.scraper.validate_content_data(valid_data)
        assert result is True
    
    def test_validate_content_data_missing_required_fields(self):
        """Test content validation with missing required fields"""
        invalid_data = {
            'title': 'Title',
            'content': '<p>Content</p>'
            # Missing 'original_url'
        }
        
        result = self.scraper.validate_content_data(invalid_data)
        assert result is False
    
    def test_validate_content_data_short_title(self):
        """Test content validation with too short title"""
        invalid_data = {
            'title': 'Hi',  # Too short
            'content': '<p>This is valid content with sufficient length for validation.</p>',
            'original_url': 'https://example.com/article'
        }
        
        result = self.scraper.validate_content_data(invalid_data)
        assert result is False
    
    def test_validate_content_data_short_content(self):
        """Test content validation with too short content"""
        invalid_data = {
            'title': 'Valid Title',
            'content': '<p>Short</p>',  # Too short
            'original_url': 'https://example.com/article'
        }
        
        result = self.scraper.validate_content_data(invalid_data)
        assert result is False
    
    def test_validate_content_data_no_paragraph_tags(self):
        """Test content validation without paragraph tags"""
        invalid_data = {
            'title': 'Valid Title',
            'content': 'This is content without paragraph tags and sufficient length.',
            'original_url': 'https://example.com/article'
        }
        
        result = self.scraper.validate_content_data(invalid_data)
        assert result is False


class TestReviewScraperUtilityMethods:
    """Test ReviewScraper utility methods"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scraper = ReviewScraper("https://example.com")
    
    def test_preview_content_summary_success(self):
        """Test successful content preview"""
        mock_urls = [f"https://example.com/article{i}/" for i in range(1, 8)]
        
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls:
            mock_get_urls.return_value = mock_urls
            
            result = self.scraper.preview_content_summary()
            
            expected = {
                'base_url': 'https://example.com',
                'total_articles': 7,
                'article_urls': mock_urls[:5],
                'has_more': True
            }
            assert result == expected
    
    def test_preview_content_summary_few_articles(self):
        """Test content preview with few articles"""
        mock_urls = ["https://example.com/article1/", "https://example.com/article2/"]
        
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls:
            mock_get_urls.return_value = mock_urls
            
            result = self.scraper.preview_content_summary()
            
            expected = {
                'base_url': 'https://example.com',
                'total_articles': 2,
                'article_urls': mock_urls,
                'has_more': False
            }
            assert result == expected
    
    def test_preview_content_summary_error(self):
        """Test content preview error handling"""
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(self.scraper, 'handle_scraping_error') as mock_error:
            
            error = Exception("Preview error")
            mock_get_urls.side_effect = error
            
            result = self.scraper.preview_content_summary()
            
            assert 'error' in result
            mock_error.assert_called_once_with(error, "preview content summary")
    
    def test_handle_scraping_error(self):
        """Test scraping error handling"""
        error = Exception("Test error")
        context = "test operation"
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            self.scraper.handle_scraping_error(error, context)
            
            expected_msg = f"ReviewScraper error in {context}: {error}"
            mock_print.assert_called_once_with(expected_msg)


class TestReviewScraperAbstractMethodImplementation:
    """Test that ReviewScraper properly implements all abstract methods"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.scraper = ReviewScraper("https://example.com")
    
    def test_implements_all_abstract_methods(self):
        """Test that all abstract methods are implemented"""
        abstract_methods = [
            'get_listing_urls',
            'scrape_single_article',
            'scrape_review_batch'
        ]
        
        for method_name in abstract_methods:
            assert hasattr(self.scraper, method_name)
            assert callable(getattr(self.scraper, method_name))
    
    def test_methods_return_correct_types(self):
        """Test that methods return expected types"""
        with patch.object(self.scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(self.scraper.parser, 'parse_listing_page') as mock_parse:
            
            mock_fetch.return_value = "<html></html>"
            mock_parse.return_value = []
            
            # get_listing_urls should return list
            result = self.scraper.get_listing_urls()
            assert isinstance(result, list)
        
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(self.scraper, 'scrape_single_article') as mock_scrape:
            
            mock_get_urls.return_value = []
            mock_scrape.return_value = None
            
            # scrape_review_batch should return list
            result = self.scraper.scrape_review_batch()
            assert isinstance(result, list)
