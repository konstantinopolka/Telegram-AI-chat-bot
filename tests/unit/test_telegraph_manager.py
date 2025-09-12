"""
Unit tests for TelegraphManager with environment variable configuration.
"""
import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
from src.telegraph_manager import TelegraphManager


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
    def test_split_content(self, mock_telegraph):
        """Test content splitting functionality."""
        mock_telegraph_instance = MagicMock()
        mock_telegraph.return_value = mock_telegraph_instance
        
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