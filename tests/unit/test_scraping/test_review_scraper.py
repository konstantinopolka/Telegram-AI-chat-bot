import pytest
from unittest.mock import Mock, patch, MagicMock
from src.scraping.review_scraper import ReviewScraper
from src.scraping.scraper import Scraper
from src.scraping.constants import MIN_TITLE_LENGTH, MIN_CONTENT_LENGTH

@pytest.fixture
def review_scraper():
    return ReviewScraper("https://platypus1917.org/platypus-review/")

@pytest.fixture  
def simple_scraper():
    return ReviewScraper("https://example.com")

class TestReviewScraper:
    """Test the ReviewScraper concrete implementation"""
    
    def test_init(self, review_scraper):
        """Test ReviewScraper initialization"""
        assert review_scraper.base_url == "https://platypus1917.org/platypus-review/"
        assert isinstance(review_scraper, Scraper)
        assert hasattr(review_scraper, 'fetcher')
        assert hasattr(review_scraper, 'parser')
    
    def test_get_listing_urls_success(self, review_scraper):
        """Test successful URL listing extraction"""
        mock_html = "<html>mock content</html>"
        expected_urls = ["https://platypus1917.org/2025/01/article1/", 
                        "https://platypus1917.org/2025/01/article2/"]
        
        with patch.object(review_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(review_scraper.parser, 'parse_listing_page') as mock_parse:
            
            mock_fetch.return_value = mock_html
            mock_parse.return_value = expected_urls
            
            result = review_scraper.get_listing_urls()
            
            mock_fetch.assert_called_once_with(review_scraper.base_url)
            mock_parse.assert_called_once_with(mock_html)
            assert result == expected_urls
    
    def test_get_listing_urls_error_handling(self, review_scraper):
        """Test error handling in URL listing extraction"""
        with patch.object(review_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(review_scraper, 'handle_scraping_error') as mock_error:
            
            mock_fetch.side_effect = Exception("Network error")
            
            result = review_scraper.get_listing_urls()
            
            assert result == []
            mock_error.assert_called_once()

    def test_get_content_data_success(self, review_scraper):
        """Test successful content data extraction"""
        article_url = "https://platypus1917.org/2025/01/article1/"
        mock_html = "<html>article content</html>"
        expected_content = {
            'title': 'Test Article',
            'content': '<p>Article content goes here</p>',
            'url': article_url
        }
        
        with patch.object(review_scraper.fetcher, 'validate_url') as mock_validate, \
             patch.object(review_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(review_scraper.parser, 'parse_content_page') as mock_parse:
            
            mock_validate.return_value = True
            mock_fetch.return_value = mock_html
            mock_parse.return_value = expected_content
            
            result = review_scraper.get_content_data(article_url)
            
            mock_validate.assert_called_once_with(article_url)
            mock_fetch.assert_called_once_with(article_url)
            mock_parse.assert_called_once_with(mock_html, article_url)
            assert result == expected_content

    def test_get_content_data_invalid_url(self, review_scraper):
        """Test get_content_data with invalid URL"""
        article_url = "invalid-url"
        
        with patch.object(review_scraper.fetcher, 'validate_url') as mock_validate:
            mock_validate.return_value = False
            
            result = review_scraper.get_content_data(article_url)
            
            mock_validate.assert_called_once_with(article_url)
            assert result is None
    
    def test_scrape_single_article_success(self, review_scraper):
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
        
        with patch.object(review_scraper.fetcher, 'validate_url') as mock_validate, \
             patch.object(review_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(review_scraper.parser, 'parse_content_page') as mock_parse, \
             patch.object(review_scraper, 'validate_content_data') as mock_validate_content:
            
            mock_validate.return_value = True
            mock_fetch.return_value = mock_html
            mock_parse.return_value = expected_data
            mock_validate_content.return_value = True
            
            result = review_scraper.scrape_single_article(article_url)
            
            mock_validate.assert_called_once_with(article_url)
            mock_fetch.assert_called_once_with(article_url)
            mock_parse.assert_called_once_with(mock_html, article_url)
            mock_validate_content.assert_called_once_with(expected_data)
            assert result == expected_data
    
    def test_scrape_single_article_invalid_url(self, review_scraper):
        """Test single article scraping with invalid URL"""
        article_url = "invalid-url"
        
        with patch.object(review_scraper.fetcher, 'validate_url') as mock_validate:
            mock_validate.return_value = False
            
            result = review_scraper.scrape_single_article(article_url)
            
            assert result is None
            mock_validate.assert_called_once_with(article_url)
    
    def test_scrape_single_article_invalid_content(self, review_scraper):
        """Test single article scraping with invalid content"""
        article_url = "https://platypus1917.org/2025/01/article/"
        mock_html = "<html>content</html>"
        content_data = {'title': '', 'content': '', 'original_url': article_url}
        
        with patch.object(review_scraper.fetcher, 'validate_url') as mock_validate, \
             patch.object(review_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(review_scraper.parser, 'parse_content_page') as mock_parse, \
             patch.object(review_scraper, 'validate_content_data') as mock_validate_content:
            
            mock_validate.return_value = True
            mock_fetch.return_value = mock_html
            mock_parse.return_value = content_data
            mock_validate_content.return_value = False
            
            result = review_scraper.scrape_single_article(article_url)
            
            assert result is None
    
    def test_scrape_single_article_error_handling(self, review_scraper):
        """Test error handling in single article scraping"""
        article_url = "https://platypus1917.org/2025/01/article/"
        
        with patch.object(review_scraper.fetcher, 'validate_url') as mock_validate, \
             patch.object(review_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(review_scraper, 'handle_scraping_error') as mock_error:
            
            mock_validate.return_value = True
            mock_fetch.side_effect = Exception("Fetch error")
            
            result = review_scraper.scrape_single_article(article_url)
            
            assert result is None
            mock_error.assert_called_once()
    
    def test_scrape_review_batch_success(self, review_scraper):
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
        
        with patch.object(review_scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(review_scraper, 'scrape_single_article') as mock_scrape:
            
            mock_get_urls.return_value = article_urls
            mock_scrape.side_effect = [article_data_1, article_data_2]
            
            result = review_scraper.scrape_review_batch()
            
            mock_get_urls.assert_called_once()
            assert mock_scrape.call_count == 2
            mock_scrape.assert_any_call(article_urls[0])
            mock_scrape.assert_any_call(article_urls[1])
            assert result == [article_data_1, article_data_2]
    
    def test_scrape_review_batch_no_urls(self, review_scraper):
        """Test review batch scraping when no URLs found"""
        with patch.object(review_scraper, 'get_listing_urls') as mock_get_urls:
            mock_get_urls.return_value = []
            
            result = review_scraper.scrape_review_batch()
            
            assert result == []
    
    def test_scrape_review_batch_partial_success(self, review_scraper):
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
        
        with patch.object(review_scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(review_scraper, 'scrape_single_article') as mock_scrape:
            
            mock_get_urls.return_value = article_urls
            # First succeeds, second and third fail
            mock_scrape.side_effect = [article_data_1, None, None]
            
            result = review_scraper.scrape_review_batch()
            
            assert len(result) == 1
            assert result[0] == article_data_1
    
    def test_scrape_review_batch_error_handling(self, review_scraper):
        """Test error handling in review batch scraping"""
        with patch.object(review_scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(review_scraper, 'handle_scraping_error') as mock_error:
            
            mock_get_urls.side_effect = Exception("Listing error")
            
            result = review_scraper.scrape_review_batch()
            
            assert result == []
            mock_error.assert_called_once()


class TestReviewScraperValidation:
    """Test ReviewScraper content validation"""
    
    def test_validate_content_data_valid(self, simple_scraper):
        """Test content validation with valid data"""
        valid_data = {
            'title': 'Valid Article Title',
            'content': '<p>This is valid content with sufficient length for validation. It needs to be at least 100 characters long and contain paragraph tags.</p>',
            'original_url': 'https://example.com/article',
            'authors': ['Author Name'],
            'published_date': 'January 2025'
        }
        
        result = simple_scraper.validate_content_data(valid_data)
        assert result is True
    
    def test_validate_content_data_missing_required_fields(self, simple_scraper):
        """Test content validation with missing required fields"""
        invalid_data = {
            'title': 'Title',
            'content': '<p>Content</p>'
            # Missing 'original_url'
        }
        
        result = simple_scraper.validate_content_data(invalid_data)
        assert result is False
    
    @pytest.mark.parametrize(
        "title, expected_result",
        [
            ("Hi", False),  # Too short (< MIN_TITLE_LENGTH)
            ("", False),    # Empty title
            ("Test", False), # Exactly at minimum length - 1
            ("Valid", True), # At minimum length
            ("Valid Article Title", True), # Well above minimum
        ]
    )
    def test_validate_content_data_title_length(self, simple_scraper, title, expected_result):
        """Test content validation with various title lengths"""
        test_data = {
            'title': title,
            'content': '<p>' + 'x' * MIN_CONTENT_LENGTH + '</p>',  # Valid content
            'original_url': 'https://example.com/article'
        }
        
        result = simple_scraper.validate_content_data(test_data)
        assert result is expected_result
    
    @pytest.mark.parametrize(
        "content, expected_result",
        [
            ('<p>Short</p>', False),  # Too short (< MIN_CONTENT_LENGTH)
            ('', False),              # Empty content
            ('<p>' + 'x' * (MIN_CONTENT_LENGTH - 1) + '</p>', False),  # Just under minimum
            ('<p>' + 'x' * MIN_CONTENT_LENGTH + '</p>', True),         # At minimum
            ('<p>' + 'x' * (MIN_CONTENT_LENGTH + 50) + '</p>', True),  # Well above minimum
        ]
    )
    def test_validate_content_data_content_length(self, simple_scraper, content, expected_result):
        """Test content validation with various content lengths"""
        test_data = {
            'title': 'Valid Title',
            'content': content,
            'original_url': 'https://example.com/article'
        }
        
        result = simple_scraper.validate_content_data(test_data)
        assert result is expected_result
    
    def test_validate_content_data_no_paragraph_tags(self, simple_scraper):
        """Test content validation without paragraph tags"""
        invalid_data = {
            'title': 'Valid Title',
            'content': 'x' * MIN_CONTENT_LENGTH,  # Sufficient length but no <p> tags
            'original_url': 'https://example.com/article'
        }
        
        result = simple_scraper.validate_content_data(invalid_data)
        assert result is False


class TestReviewScraperUtilityMethods:
    """Test ReviewScraper utility methods"""
    
    def test_preview_content_summary_success(self, simple_scraper):
        """Test successful content preview"""
        mock_urls = [f"https://example.com/article{i}/" for i in range(1, 8)]
        
        with patch.object(simple_scraper, 'get_listing_urls') as mock_get_urls:
            mock_get_urls.return_value = mock_urls
            
            result = simple_scraper.preview_content_summary()
            
            expected = {
                'base_url': 'https://example.com',
                'total_articles': 7,
                'article_urls': mock_urls[:5],
                'has_more': True
            }
            assert result == expected
    
    def test_preview_content_summary_few_articles(self, simple_scraper):
        """Test content preview with few articles"""
        mock_urls = ["https://example.com/article1/", "https://example.com/article2/"]
        
        with patch.object(simple_scraper, 'get_listing_urls') as mock_get_urls:
            mock_get_urls.return_value = mock_urls
            
            result = simple_scraper.preview_content_summary()
            
            expected = {
                'base_url': 'https://example.com',
                'total_articles': 2,
                'article_urls': mock_urls,
                'has_more': False
            }
            assert result == expected
    
    def test_preview_content_summary_error(self, simple_scraper):
        """Test content preview error handling"""
        with patch.object(simple_scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(simple_scraper, 'handle_scraping_error') as mock_error:
            
            error = Exception("Preview error")
            mock_get_urls.side_effect = error
            
            result = simple_scraper.preview_content_summary()
            
            assert 'error' in result
            mock_error.assert_called_once_with(error, "preview content summary")
    
    def test_handle_scraping_error(self, simple_scraper):
        """Test scraping error handling"""
        error = Exception("Test error")
        context = "test operation"
        
        # Capture print output
        with patch('builtins.print') as mock_print:
            simple_scraper.handle_scraping_error(error, context)
            
            expected_msg = f"ReviewScraper error in {context}: {error}"
            mock_print.assert_called_once_with(expected_msg)


class TestReviewScraperAbstractMethodImplementation:
    """Test that ReviewScraper properly implements all abstract methods"""
    
    def test_implements_all_abstract_methods(self, simple_scraper):
        """Test that all abstract methods are implemented"""
        abstract_methods = [
            'get_listing_urls',
            'scrape_single_article',
            'scrape_review_batch'
        ]
        
        for method_name in abstract_methods:
            assert hasattr(simple_scraper, method_name)
            assert callable(getattr(simple_scraper, method_name))
    
    def test_methods_return_correct_types(self, simple_scraper):
        """Test that methods return expected types"""
        with patch.object(simple_scraper.fetcher, 'fetch_page') as mock_fetch, \
             patch.object(simple_scraper.parser, 'parse_listing_page') as mock_parse:
            
            mock_fetch.return_value = "<html></html>"
            mock_parse.return_value = []
            
            # get_listing_urls should return list
            result = simple_scraper.get_listing_urls()
            assert isinstance(result, list)
        
        with patch.object(simple_scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(simple_scraper, 'scrape_single_article') as mock_scrape:
            
            mock_get_urls.return_value = []
            mock_scrape.return_value = None
            
            # scrape_review_batch should return list
            result = simple_scraper.scrape_review_batch()
            assert isinstance(result, list)
        
        with patch.object(self.scraper, 'get_listing_urls') as mock_get_urls, \
             patch.object(self.scraper, 'scrape_single_article') as mock_scrape:
            
            mock_get_urls.return_value = []
            mock_scrape.return_value = None
            
            # scrape_review_batch should return list
            result = self.scraper.scrape_review_batch()
            assert isinstance(result, list)
