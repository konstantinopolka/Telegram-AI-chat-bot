from typing import Dict, List, Optional, Any, Set
from bs4 import BeautifulSoup

class ArchiveParser():
    """
    Parses archive page to extract review URLs.
    
    HTML structure to parse:
    <div class="archive">
        <a href="/category/pr/issue-179/">Issue 179</a>
        <a href="/category/pr/issue-178/">Issue 178</a>
        ...
    </div>
    """
    
    def parse_archive_page(self, html: str) -> List[str]:
        """
        Extract review urls from archive.
        
        Returns:
           {url1, url2, .....}
           
        """
        soup: BeautifulSoup = BeautifulSoup(html, 'html.parser')
        
        selectors = [ 
            'dc-four dc-columns h2 > a[href^=https://platypus1917.org/category/pr/issue-]',
                
        ]
        
        
        # TO-DO: parse the archive website
        pass