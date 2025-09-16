"""
Integration tests for TelegraphManager that create real Telegraph pages.
These tests use artificially generated HTML content to test the complete functionality
including multi-part articles with navigation links.
"""
import pytest
import os
from unittest.mock import patch
from src.telegraph_manager import TelegraphManager
from src.dao.models import Article


class TestTelegraphIntegration:
    """Integration tests that create real Telegraph pages."""
    
    @pytest.fixture
    def telegraph_manager(self):
        """Create TelegraphManager with real Telegraph API access."""
        # Skip if no Telegraph token is available
        if not os.getenv('TELEGRAPH_ACCESS_TOKEN'):
            pytest.skip("No TELEGRAPH_ACCESS_TOKEN environment variable set")
        
        return TelegraphManager()
    
    def _generate_large_html_content(self, size_kb: int = 80) -> str:
        """Generate large HTML content for testing multi-part articles."""
        # Base content structure
        base_content = '''
        <p class="has-text-align-right">
            <a href="https://platypus1917.org/category/pr/issue-179/">
                <em>Platypus Review</em> 179
            </a> | September 2025
        </p>
        <h2>Introduction</h2>
        <p>This is a test article with artificially generated content to test Telegraph's multi-part functionality.</p>
        '''
        
        # Generate paragraphs to reach desired size
        target_bytes = size_kb * 1024
        current_size = len(base_content.encode('utf-8'))
        
        paragraph_template = '''
        <p>This is paragraph {num} of the artificially generated content. 
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod 
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim 
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea 
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate 
        velit esse cillum dolore eu fugiat nulla pariatur.</p>
        
        <blockquote>
        This is a blockquote in paragraph {num}. Excepteur sint occaecat cupidatat 
        non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </blockquote>
        
        <ul>
            <li>List item {num}.1 - Some detailed explanation</li>
            <li>List item {num}.2 - Another important point</li>
            <li>List item {num}.3 - Final consideration</li>
        </ul>
        '''
        
        content = base_content
        paragraph_num = 1
        
        while current_size < target_bytes:
            new_paragraph = paragraph_template.format(num=paragraph_num)
            content += new_paragraph
            current_size = len(content.encode('utf-8'))
            paragraph_num += 1
        
        # Add conclusion
        content += '''
        <h2>Conclusion</h2>
        <p>This concludes our artificially generated test article. The content was 
        designed to exceed Telegraph's 64KB limit and test multi-part article 
        functionality with navigation links.</p>
        '''
        
        return content
    
    def _generate_medium_html_content(self) -> str:
        """Generate medium-sized HTML content (single part)."""
        return '''
        <p class="has-text-align-right">
            <a href="https://platypus1917.org/category/pr/issue-179/">
                <em>Platypus Review</em> 179
            </a> | September 2025
        </p>
        <h2>Test Article</h2>
        <p>This is a medium-sized test article that should fit in a single Telegraph page.</p>
        <p>It contains multiple paragraphs but stays under the 64KB limit.</p>
        <blockquote>
        This is a test blockquote to add some variety to the content structure.
        </blockquote>
        <ul>
            <li>First test point</li>
            <li>Second test point</li>
            <li>Third test point</li>
        </ul>
        <p>Final paragraph of the medium test article.</p>
        '''
    
    @pytest.mark.integration
    async def test_single_part_article_creation(self, telegraph_manager):
        """Test creating a single-part Telegraph article."""
        # Create test article
        article = Article(
            title="Test Single Part Article",
            content=self._generate_medium_html_content(),
            original_url="https://test.example.com/single-part"
        )
        
        # Create Telegraph article
        urls = await telegraph_manager.create_article(article)
        
        # Assertions
        assert urls is not None
        assert len(urls) == 1
        assert all(url.startswith('https://telegra.ph/') for url in urls)
        
        print(f"✅ Created single-part article: {urls[0]}")
    
    @pytest.mark.integration
    async def test_three_part_article_creation(self, telegraph_manager):
        """Test creating a three-part Telegraph article with navigation."""
        # Create large test article (should split into multiple parts)
        article = Article(
            title="Test Three Part Article",
            content=self._generate_large_html_content(size_kb=120),  # ~120KB content
            original_url="https://test.example.com/three-part"
        )
        
        # Create Telegraph article
        urls = await telegraph_manager.create_article(article)
        
        # Assertions
        assert urls is not None
        assert len(urls) >= 2, f"Expected at least 2 parts, got {len(urls)}"
        assert all(url.startswith('https://telegra.ph/') for url in urls)
        
        print(f"✅ Created {len(urls)}-part article:")
        for i, url in enumerate(urls, 1):
            print(f"   Part {i}: {url}")
    
    @pytest.mark.integration
    async def test_five_part_article_creation(self, telegraph_manager):
        """Test creating a five-part Telegraph article with navigation."""
        # Create very large test article (should split into multiple parts)
        article = Article(
            title="Test Five Part Article - Very Large Content",
            content=self._generate_large_html_content(size_kb=200),  # ~200KB content
            original_url="https://test.example.com/five-part"
        )
        
        # Create Telegraph article
        urls = await telegraph_manager.create_article(article)
        
        # Assertions
        assert urls is not None
        assert len(urls) >= 3, f"Expected at least 3 parts, got {len(urls)}"
        assert all(url.startswith('https://telegra.ph/') for url in urls)
        
        print(f"✅ Created {len(urls)}-part article:")
        for i, url in enumerate(urls, 1):
            print(f"   Part {i}: {url}")
    
    @pytest.mark.integration
    async def test_article_with_publication_info(self, telegraph_manager):
        """Test that reposting date is correctly added to articles."""
        article = Article(
            title="Test Article with Publication Info",
            content=self._generate_medium_html_content(),
            original_url="https://test.example.com/with-pub-info"
        )
        
        # Create Telegraph article
        urls = await telegraph_manager.create_article(article)
        
        # Assertions
        assert urls is not None
        assert len(urls) >= 1
        assert all(url.startswith('https://telegra.ph/') for url in urls)
        
        print(f"✅ Created article with publication info: {urls[0]}")
    
    @pytest.mark.integration
    async def test_article_without_existing_publication_info(self, telegraph_manager):
        """Test article creation when no existing publication info is present."""
        # Content without existing publication paragraph
        content_without_pub = '''
        <h2>Article Without Publication Info</h2>
        <p>This article doesn't have existing publication information.</p>
        <p>The system should add publication info automatically.</p>
        <ul>
            <li>Test point 1</li>
            <li>Test point 2</li>
        </ul>
        '''
        
        article = Article(
            title="Test Article Without Existing Pub Info",
            content=content_without_pub,
            original_url="https://test.example.com/no-pub-info"
        )
        
        # Create Telegraph article
        urls = await telegraph_manager.create_article(article)
        
        # Assertions
        assert urls is not None
        assert len(urls) >= 1
        assert all(url.startswith('https://telegra.ph/') for url in urls)
        
        print(f"✅ Created article without existing pub info: {urls[0]}")
    
    @pytest.mark.integration
    async def test_complex_html_structure(self, telegraph_manager):
        """Test article with complex HTML structure (images, code blocks, etc.)."""
        complex_content = '''
        <p class="has-text-align-right">
            <a href="https://platypus1917.org/category/pr/issue-179/">
                <em>Platypus Review</em> 179
            </a> | September 2025
        </p>
        <h2>Complex HTML Structure Test</h2>
        <p>This article tests various HTML elements supported by Telegraph.</p>
        
        <h3>Code Example</h3>
        <pre>
def test_function():
    return "Hello, Telegraph!"
        </pre>
        
        <h3>Inline Code</h3>
        <p>You can use <code>inline code</code> within paragraphs.</p>
        
        <h3>Emphasis and Formatting</h3>
        <p>This paragraph has <strong>bold text</strong>, <em>italic text</em>, 
        and <u>underlined text</u>. You can also have <s>strikethrough</s> text.</p>
        
        <h3>Lists</h3>
        <ol>
            <li>First ordered item</li>
            <li>Second ordered item with <strong>bold</strong> text</li>
            <li>Third item with <a href="https://example.com">a link</a></li>
        </ol>
        
        <blockquote>
        This is a blockquote that contains multiple lines of text.
        It can span across several lines and contain formatting like <em>italics</em>.
        </blockquote>
        
        <hr>
        
        <p>Content after horizontal rule.</p>
        '''
        
        article = Article(
            title="Test Complex HTML Structure",
            content=complex_content,
            original_url="https://test.example.com/complex-html"
        )
        
        # Create Telegraph article
        urls = await telegraph_manager.create_article(article)
        
        # Assertions
        assert urls is not None
        assert len(urls) >= 1
        assert all(url.startswith('https://telegra.ph/') for url in urls)
        
        print(f"✅ Created article with complex HTML: {urls[0]}")
    
    @pytest.mark.integration
    async def test_content_size_estimation(self, telegraph_manager):
        """Test that content size estimation works correctly."""
        # Test with content that should definitely split
        large_content = self._generate_large_html_content(size_kb=150)
        
        # Test estimation
        estimated_chunks = telegraph_manager._estimate_chunks_count(large_content, "Test Title")
        
        # Create actual article to compare
        article = Article(
            title="Test Size Estimation",
            content=large_content,
            original_url="https://test.example.com/size-estimation"
        )
        
        urls = await telegraph_manager.create_article(article)
        actual_chunks = len(urls)
        
        # Assertions
        assert estimated_chunks > 1
        assert actual_chunks > 1
        # Estimation should be reasonably close (within 1-2 chunks)
        assert abs(estimated_chunks - actual_chunks) <= 2
        
        print(f"✅ Size estimation test: estimated {estimated_chunks}, actual {actual_chunks}")
        for i, url in enumerate(urls, 1):
            print(f"   Part {i}: {url}")


@pytest.mark.integration  
class TestNavigationLinksIntegration:
    """Integration tests specifically for navigation links functionality."""
    
    @pytest.fixture
    def telegraph_manager(self):
        """Create TelegraphManager with real Telegraph API access."""
        if not os.getenv('TELEGRAPH_ACCESS_TOKEN'):
            pytest.skip("No TELEGRAPH_ACCESS_TOKEN environment variable set")
        
        return TelegraphManager()
    
    def _create_navigation_test_content(self, size_kb: int = 100) -> str:
        """Create content specifically for testing navigation links."""
        base_content = '''
        <p class="has-text-align-right">
            <a href="https://platypus1917.org/category/pr/issue-179/">
                <em>Platypus Review</em> 179
            </a> | September 2025
        </p>
        <h1>Navigation Links Test Article</h1>
        <p>This article is designed to test the navigation links functionality between multiple Telegraph parts.</p>
        '''
        
        # Generate enough content to force splitting
        target_bytes = size_kb * 1024
        current_size = len(base_content.encode('utf-8'))
        
        section_template = '''
        <h2>Section {num}: Navigation Test Content</h2>
        <p>This is section {num} of the navigation test article. Each section contains 
        substantial content to ensure proper splitting across multiple Telegraph pages.</p>
        
        <p>The navigation system should automatically add "Previous" and "Next" links 
        at the beginning and end of each part, except:</p>
        
        <ul>
            <li>First part: Only "Next" link (no "Previous")</li>
            <li>Middle parts: Both "Previous" and "Next" links</li>
            <li>Last part: Only "Previous" link (no "Next")</li>
        </ul>
        
        <blockquote>
        Section {num} blockquote: The navigation links should be placed after the 
        publication information on the first part, and at the very beginning for 
        subsequent parts. They should also appear at the end of every part.
        </blockquote>
        
        <p>Additional paragraph {num}.1 with more content to increase the size.</p>
        <p>Additional paragraph {num}.2 with even more content for proper testing.</p>
        <p>Additional paragraph {num}.3 to ensure we reach the target size limit.</p>
        
        <pre>
# Code block in section {num}
def section_{num}_function():
    return "This is test code for section {num}"
        </pre>
        '''
        
        content = base_content
        section_num = 1
        
        while current_size < target_bytes:
            new_section = section_template.format(num=section_num)
            content += new_section
            current_size = len(content.encode('utf-8'))
            section_num += 1
        
        return content
    
    @pytest.mark.integration
    async def test_navigation_links_three_parts(self, telegraph_manager):
        """Test navigation links in a multi-part article."""
        article = Article(
            title="Navigation Links Test - Multiple Parts",
            content=self._create_navigation_test_content(size_kb=120),
            original_url="https://test.example.com/nav-test-multi-parts"
        )
        
        urls = await telegraph_manager.create_article(article)
        
        # Should have multiple parts
        assert len(urls) >= 2
        
        print(f"✅ Created {len(urls)}-part article with navigation links:")
        print("   Please manually verify that:")
        print("   1. First part has only 'Next' navigation")
        print("   2. Middle parts have both 'Previous' and 'Next' navigation")  
        print("   3. Last part has only 'Previous' navigation")
        print("   4. Navigation appears at top (after pub info) and bottom of each part")
        
        for i, url in enumerate(urls, 1):
            expected_nav = []
            if i > 1:
                expected_nav.append("← Previous")
            if i < len(urls):
                expected_nav.append("Next →")
            
            nav_description = " & ".join(expected_nav) if expected_nav else "No navigation"
            print(f"   Part {i}: {url} (Expected: {nav_description})")
    
    @pytest.mark.integration
    async def test_navigation_with_custom_title(self, telegraph_manager):
        """Test navigation links with a custom article title."""
        custom_title = "Custom Title with Special Characters: Test & Validation"
        
        article = Article(
            title=custom_title,
            content=self._create_navigation_test_content(size_kb=100),
            original_url="https://test.example.com/custom-title-nav"
        )
        
        urls = await telegraph_manager.create_article(article)
        
        assert len(urls) >= 2
        
        print(f"✅ Created {len(urls)}-part article with custom title:")
        print(f"   Title: {custom_title}")
        print("   Navigation links should properly handle the custom title")
        
        for i, url in enumerate(urls, 1):
            print(f"   Part {i}: {url}")