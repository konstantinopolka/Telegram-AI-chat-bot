"""
Unit tests for TelegraphManager with environment variable configuration.
"""
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
from bs4 import BeautifulSoup
from src.telegraph_manager import TelegraphManager


@pytest.fixture(autouse=True)
def reset_telegraph_singleton():
    """Reset TelegraphManager singleton before each test."""
    TelegraphManager.reset_instance()
    yield
    TelegraphManager.reset_instance()


class TestTelegraphManager:
    
    @patch.dict(os.environ, {
        'TELEGRAPH_ACCESS_TOKEN': 'test_env_token',
        'TELEGRAPH_SHORT_NAME': 'test_short_name',
        'TELEGRAPH_AUTHOR_NAME': 'Test Author',
        'TELEGRAPH_AUTHOR_URL': 'https://test.com'
    })
    @patch('src.telegraph_manager.Telegraph')
    def test_init_with_environment_variables(self, mock_telegraph):
        """Test initialization using environment variables."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph.return_value = mock_telegraph_instance
        
        manager = TelegraphManager()
        
        # Should use environment variable token
        mock_telegraph.assert_called_with(access_token='test_env_token')
        assert manager.access_token == 'test_env_token'
        assert manager.short_name == 'test_short_name'
        assert manager.author_name == 'Test Author'
        assert manager.author_url == 'https://test.com'
    
    @patch.dict(os.environ, {}, clear=True)  # Clear all env vars
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"access_token": "json_token"}')
    def test_init_with_json_fallback(self, mock_file, mock_exists, mock_telegraph):
        """Test fallback to JSON file when env vars are not available."""
        mock_exists.return_value = True
        mock_telegraph_instance = MagicMock()
        mock_telegraph.return_value = mock_telegraph_instance
        
        manager = TelegraphManager()
        
        # Should fall back to JSON file
        mock_exists.assert_called_with('graph_bot.json')
        mock_telegraph.assert_called_with(access_token='json_token')
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    def test_init_create_new_account(self, mock_exists, mock_telegraph):
        """Test creating new account when no credentials available."""
        mock_exists.return_value = False
        mock_telegraph_instance = MagicMock()
        mock_telegraph_instance.create_account.return_value = {
            'access_token': 'new_token',
            'short_name': 'konstantinopolka',
            'author_name': 'Platypus Review'
        }
        mock_telegraph.return_value = mock_telegraph_instance
        
        with patch('builtins.open', mock_open()) as mock_file:
            manager = TelegraphManager()
            
            # Should create new account
            mock_telegraph_instance.create_account.assert_called_once()
            # Should save to JSON file
            mock_file.assert_called_with('graph_bot.json', 'w', encoding='utf-8')
    
    @patch('src.telegraph_manager.Telegraph')
    def test_init_with_provided_token(self, mock_telegraph):
        """Test initialization with explicitly provided access token."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph.return_value = mock_telegraph_instance
        
        manager = TelegraphManager(access_token='provided_token')
        
        # Should use provided token
        mock_telegraph.assert_called_with(access_token='provided_token')
        assert manager.access_token == 'provided_token'
    
    @patch.dict(os.environ, {'TELEGRAPH_ACCESS_TOKEN': 'env_token'})
    @patch('src.telegraph_manager.Telegraph')
    def test_provided_token_overrides_env(self, mock_telegraph):
        """Test that provided token takes precedence over environment variable."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph.return_value = mock_telegraph_instance
        
        manager = TelegraphManager(access_token='override_token')
        
        # Should use provided token, not env var
        mock_telegraph.assert_called_with(access_token='override_token')
        assert manager.access_token == 'override_token'
    
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    @patch('builtins.open', mock_open())
    def test_split_content(self, mock_exists, mock_telegraph):
        """Test content splitting functionality."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph_instance.create_account.return_value = {
            'access_token': 'test_token',
            'short_name': 'test',
            'author_name': 'Test Author'
        }
        mock_telegraph.return_value = mock_telegraph_instance
        mock_exists.return_value = False
        
        manager = TelegraphManager(access_token='test_token')
        
        # Test with small content that doesn't need splitting
        small_content = '<p>Small content</p>'
        chunks = manager.split_content(small_content)
        assert len(chunks) == 1
        assert chunks[0] == small_content
        
        # Test with large content that needs splitting
        large_block = '<p>' + 'A' * 25000 + '</p>'
        large_content = large_block + large_block + large_block  # Total > 50000 chars
        chunks = manager.split_content(large_content)
        assert len(chunks) > 1
    
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    @patch('builtins.open', mock_open())
    def test_split_content_handles_all_allowed_tags(self, mock_exists, mock_telegraph):
        """Test that split_content properly handles all tags from ALLOWED_TAGS."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph_instance.create_account.return_value = {
            'access_token': 'test_token',
            'short_name': 'test',
            'author_name': 'Test Author'
        }
        mock_telegraph.return_value = mock_telegraph_instance
        mock_exists.return_value = False
        
        manager = TelegraphManager(access_token='test_token')
        
        # Test content with various allowed tags
        complex_content = '''
        <p>This is a <strong>paragraph</strong> with <em>inline</em> elements and <a href="https://example.com">links</a>.</p>
        <blockquote>This is a blockquote with <code>code</code> inside.</blockquote>
        <ul>
            <li>List item with <b>bold</b> text</li>
            <li>Another item with <i>italic</i> and <u>underlined</u> text</li>
        </ul>
        <ol>
            <li>Numbered list item</li>
        </ol>
        <pre>Code block content</pre>
        <img src="https://example.com/image.jpg" alt="Test image">
        <hr>
        <p>Text with <s>strikethrough</s> and line<br>break.</p>
        '''
        
        chunks = manager.split_content(complex_content)
        
        # Should have at least one chunk
        assert len(chunks) >= 1
        
        # Combine all chunks to verify no content is lost
        combined_content = ''.join(chunks)
        soup = BeautifulSoup(combined_content, 'html.parser')
        
        # Verify key elements are preserved
        assert soup.find('p') is not None
        assert soup.find('strong') is not None
        assert soup.find('em') is not None
        assert soup.find('a') is not None
        assert soup.find('blockquote') is not None
        assert soup.find('code') is not None
        assert soup.find('ul') is not None
        assert soup.find('li') is not None
        assert soup.find('b') is not None
        assert soup.find('i') is not None
        assert soup.find('u') is not None
        assert soup.find('ol') is not None
        assert soup.find('pre') is not None
        assert soup.find('img') is not None
        assert soup.find('hr') is not None
        assert soup.find('s') is not None
        assert soup.find('br') is not None
    
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    @patch('builtins.open', mock_open())
    def test_split_content_handles_standalone_elements(self, mock_exists, mock_telegraph):
        """Test that standalone inline elements are properly handled."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph_instance.create_account.return_value = {
            'access_token': 'test_token',
            'short_name': 'test',
            'author_name': 'Test Author'
        }
        mock_telegraph.return_value = mock_telegraph_instance
        mock_exists.return_value = False
        
        manager = TelegraphManager(access_token='test_token')
        
        # Test content with standalone elements and mixed structure
        mixed_content = '''
        <img src="https://example.com/standalone.jpg" alt="Standalone image">
        <p>Regular paragraph</p>
        <strong>Standalone bold text</strong>
        <hr>
        <em>Standalone italic text</em>
        '''
        
        chunks = manager.split_content(mixed_content)
        
        # Should have at least one chunk
        assert len(chunks) >= 1
        
        # Verify content preservation
        combined_content = ''.join(chunks)
        soup = BeautifulSoup(combined_content, 'html.parser')
        
        # Check that standalone elements are preserved
        assert soup.find('img') is not None
        assert soup.find('p') is not None
        assert 'Standalone bold text' in combined_content
        assert 'Standalone italic text' in combined_content
        assert soup.find('hr') is not None
    
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    @patch('builtins.open', mock_open())
    def test_split_content_with_navigation_reservation(self, mock_exists, mock_telegraph):
        """Test that split_content reserves space for navigation links when requested."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph_instance.create_account.return_value = {
            'access_token': 'test_token',
            'short_name': 'test',
            'author_name': 'Test Author'
        }
        mock_telegraph.return_value = mock_telegraph_instance
        mock_exists.return_value = False
        
        manager = TelegraphManager(access_token='test_token')
        
        # Test with small content - should not change behavior significantly
        small_content = '<p>Small content</p>'
        chunks_without_nav = manager.split_content(small_content, "Test Title", reserve_space_for_nav=False)
        chunks_with_nav = manager.split_content(small_content, "Test Title", reserve_space_for_nav=True)
        
        # Both should have same number of chunks for small content
        assert len(chunks_without_nav) == len(chunks_with_nav) == 1
        
        # Content should be the same
        assert chunks_without_nav[0] == chunks_with_nav[0]
    
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    @patch('builtins.open', mock_open())
    def test_estimate_chunks_count(self, mock_exists, mock_telegraph):
        """Test the _estimate_chunks_count method."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph_instance.create_account.return_value = {
            'access_token': 'test_token',
            'short_name': 'test',
            'author_name': 'Test Author'
        }
        mock_telegraph.return_value = mock_telegraph_instance
        mock_exists.return_value = False
        
        manager = TelegraphManager(access_token='test_token')
        
        # Test with small content
        small_content = '<p>Small content</p>'
        estimate = manager._estimate_chunks_count(small_content, "Test Title")
        assert estimate == 1
        
        # Test with large content
        large_content = '<p>' + 'A' * 70000 + '</p>'
        estimate = manager._estimate_chunks_count(large_content, "Test Title")
        assert estimate > 1
    
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    @patch('builtins.open', mock_open())
    def test_create_navigation_links(self, mock_exists, mock_telegraph):
        """Test the _create_navigation_links method."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph_instance.create_account.return_value = {
            'access_token': 'test_token',
            'short_name': 'test',
            'author_name': 'Test Author'
        }
        mock_telegraph.return_value = mock_telegraph_instance
        mock_exists.return_value = False
        
        manager = TelegraphManager(access_token='test_token')
        
        urls = ['https://telegra.ph/Test-1', 'https://telegra.ph/Test-2', 'https://telegra.ph/Test-3']
        title = "Test Article"
        
        # Test first part (index 0)
        nav = manager._create_navigation_links(0, 3, urls, title)
        assert 'Next:' in nav['top']
        assert 'Previous' not in nav['top']
        assert nav['bottom'] == f"<hr>{nav['top']}"
        
        # Test middle part (index 1)
        nav = manager._create_navigation_links(1, 3, urls, title)
        assert 'Previous:' in nav['top']
        assert 'Next:' in nav['top']
        
        # Test last part (index 2)
        nav = manager._create_navigation_links(2, 3, urls, title)
        assert 'Previous:' in nav['top']
        assert 'Next' not in nav['top']
    
    @patch('src.telegraph_manager.Telegraph')
    @patch('os.path.exists')
    @patch('builtins.open', mock_open())
    def test_add_nav_to_content(self, mock_exists, mock_telegraph):
        """Test the _add_nav_to_content method."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph_instance.create_account.return_value = {
            'access_token': 'test_token',
            'short_name': 'test',
            'author_name': 'Test Author'
        }
        mock_telegraph.return_value = mock_telegraph_instance
        mock_exists.return_value = False
        
        manager = TelegraphManager(access_token='test_token')
        
        content = '''
        <p class="has-text-align-right">Publication info</p>
        <p>Article content</p>
        '''
        
        nav_links = {
            'top': '<p><strong>Navigation:</strong> <a href="test">Next</a></p><hr>',
            'bottom': '<hr><p><strong>Navigation:</strong> <a href="test">Next</a></p><hr>'
        }
        
        # Test first part (should insert after publication info)
        result = manager._add_nav_to_content(content, nav_links, is_first_part=True)
        
        # Navigation should be added at least once
        assert '<strong>Navigation:</strong>' in result
        # Check that content is preserved
        assert 'Article content' in result
        assert 'Publication info' in result
        # Should have navigation elements
        from bs4 import BeautifulSoup
        result_soup = BeautifulSoup(result, 'html.parser')
        nav_elements = result_soup.find_all(string='Navigation:')
        assert len(nav_elements) >= 1  # At least top navigation should be there


class TestTelegraphManagerRepostingDate:
    """Test class specifically for _add_reposting_date functionality."""
    
    @pytest.fixture
    def manager(self):
        """Create a TelegraphManager instance for testing."""
        with patch('src.telegraph_manager.Telegraph') as mock_telegraph_class, \
             patch('os.path.exists') as mock_exists, \
             patch('builtins.open', mock_open()):
            
            # Mock Telegraph class and instance
            mock_telegraph_instance = MagicMock()
            mock_telegraph_class.return_value = mock_telegraph_instance
            
            # Make os.path.exists return False so it doesn't try to read JSON
            mock_exists.return_value = False
            
            # Mock create_account method
            mock_telegraph_instance.create_account.return_value = {
                'access_token': 'test_token',
                'short_name': 'test',
                'author_name': 'Test Author'
            }
            
            return TelegraphManager(access_token='test_token')
    
    @pytest.fixture
    def mock_datetime(self):
        """Mock datetime to have consistent test results."""
        with patch('datetime.datetime') as mock_dt:
            # Mock datetime.now() to return September 15, 2025
            mock_now = MagicMock()
            mock_now.strftime.return_value = "2025-09-15"  # For repost date format
            mock_dt.now.return_value = mock_now
            
            # Also mock for when we need month_year format
            mock_now.strftime.side_effect = lambda fmt: {
                "%Y-%m-%d": "2025-09-15",
                "%B %Y": "September 2025"
            }.get(fmt, fmt)
            
            yield mock_dt
    
    def test_add_reposting_date_with_existing_publication_info(self, manager, mock_datetime):
        """Test adding repost date to existing publication info paragraph."""
        content = '''
        <div>
            <p>Some intro text</p>
            <p class="has-text-align-right">
                <a href="https://platypus1917.org/category/pr/issue-179/">
                    <em>Platypus Review</em> 179
                </a> | September 2025
            </p>
            <p>Article content here</p>
        </div>
        '''
        
        result = manager._add_reposting_date(content)
        soup = BeautifulSoup(result, 'html.parser')
        
        # Check that the publication paragraph exists and contains repost date
        pub_paragraph = soup.find('p', class_='has-text-align-right')
        assert pub_paragraph is not None
        assert 'Platypus Review' in pub_paragraph.get_text()
        assert 'Reposted on: 2025-09-15' in pub_paragraph.get_text()
        assert 'September 2025' in pub_paragraph.get_text()
    
    def test_add_reposting_date_without_existing_publication_info(self, manager, mock_datetime):
        """Test creating new publication info when none exists."""
        content = '''
        <div>
            <p>Some intro text</p>
            <p>Article content here</p>
        </div>
        '''
        
        result = manager._add_reposting_date(content)
        soup = BeautifulSoup(result, 'html.parser')
        
        # Check that a new publication paragraph was created
        pub_paragraph = soup.find('p', class_='has-text-align-right')
        assert pub_paragraph is not None
        assert 'Platypus Review' in pub_paragraph.get_text()
        assert 'Reposted on: 2025-09-15' in pub_paragraph.get_text()
        assert 'September 2025' in pub_paragraph.get_text()
        assert 'issue-179' in str(pub_paragraph)
    
    def test_add_reposting_date_with_wrong_class_paragraph(self, manager, mock_datetime):
        """Test when paragraph exists but without the correct class."""
        content = '''
        <div>
            <p>Some intro text</p>
            <p class="different-class">
                <a href="https://platypus1917.org/category/pr/issue-179/">
                    <em>Platypus Review</em> 179
                </a> | September 2025
            </p>
            <p>Article content here</p>
        </div>
        '''
        
        result = manager._add_reposting_date(content)
        soup = BeautifulSoup(result, 'html.parser')
        
        # Should create a new publication paragraph since the existing one doesn't have the right class
        pub_paragraphs = soup.find_all('p', class_='has-text-align-right')
        assert len(pub_paragraphs) == 1  # Should have created a new one
        
        new_pub_paragraph = pub_paragraphs[0]
        assert 'Platypus Review' in new_pub_paragraph.get_text()
        assert 'Reposted on: 2025-09-15' in new_pub_paragraph.get_text()
    
    def test_add_reposting_date_with_paragraph_without_platypus_review(self, manager, mock_datetime):
        """Test when correct class exists but doesn't contain 'Platypus Review'."""
        content = '''
        <div>
            <p>Some intro text</p>
            <p class="has-text-align-right">
                <a href="https://example.com/">Some Other Publication</a> | September 2025
            </p>
            <p>Article content here</p>
        </div>
        '''
        
        result = manager._add_reposting_date(content)
        soup = BeautifulSoup(result, 'html.parser')
        
        # Should create a new publication paragraph since existing one doesn't contain "Platypus Review"
        pub_paragraphs = soup.find_all('p', class_='has-text-align-right')
        # Should have both the original and the new one
        assert len(pub_paragraphs) >= 1
        
        # Check that at least one paragraph contains Platypus Review and repost date
        platypus_paragraph = None
        for p in pub_paragraphs:
            if 'Platypus Review' in p.get_text():
                platypus_paragraph = p
                break
        
        assert platypus_paragraph is not None
        assert 'Reposted on: 2025-09-15' in platypus_paragraph.get_text()
    
    @pytest.mark.parametrize("test_date,expected_format", [
        (datetime(2025, 9, 15), "2025-09-15"),
        (datetime(2025, 12, 31), "2025-12-31"),
        (datetime(2024, 1, 1), "2024-01-01"),
        (datetime(2025, 7, 4), "2025-07-04"),
    ])
    def test_add_reposting_date_different_dates(self, manager, test_date, expected_format):
        """Test repost date formatting with different dates."""
        content = '''
        <div>
            <p class="has-text-align-right">
                <a href="https://platypus1917.org/category/pr/issue-179/">
                    <em>Platypus Review</em> 179
                </a> | September 2025
            </p>
        </div>
        '''
        
        with patch('datetime.datetime') as mock_dt:
            mock_now = MagicMock()
            mock_now.strftime.return_value = expected_format
            mock_dt.now.return_value = mock_now
            
            result = manager._add_reposting_date(content)
            soup = BeautifulSoup(result, 'html.parser')
            
            pub_paragraph = soup.find('p', class_='has-text-align-right')
            assert f'Reposted on: {expected_format}' in pub_paragraph.get_text()
    
    def test_add_reposting_date_empty_content(self, manager, mock_datetime):
        """Test handling of empty content."""
        content = ''
        
        result = manager._add_reposting_date(content)
        soup = BeautifulSoup(result, 'html.parser')
        
        # Should create a new publication paragraph
        pub_paragraph = soup.find('p', class_='has-text-align-right')
        assert pub_paragraph is not None
        assert 'Platypus Review' in pub_paragraph.get_text()
        assert 'Reposted on: 2025-09-15' in pub_paragraph.get_text()
    
    def test_add_reposting_date_preserves_original_content(self, manager, mock_datetime):
        """Test that original content is preserved when adding repost date."""
        original_content = '''
        <div>
            <h1>Article Title</h1>
            <p>First paragraph</p>
            <p class="has-text-align-right">
                <a href="https://platypus1917.org/category/pr/issue-179/">
                    <em>Platypus Review</em> 179
                </a> | September 2025
            </p>
            <p>Last paragraph</p>
        </div>
        '''
        
        result = manager._add_reposting_date(original_content)
        soup = BeautifulSoup(result, 'html.parser')
        
        # Check that all original content is still there
        assert soup.find('h1', string='Article Title') is not None
        assert soup.find('p', string='First paragraph') is not None
        assert soup.find('p', string='Last paragraph') is not None
        
        # And repost date was added
        pub_paragraph = soup.find('p', class_='has-text-align-right')
        assert 'Reposted on: 2025-09-15' in pub_paragraph.get_text()