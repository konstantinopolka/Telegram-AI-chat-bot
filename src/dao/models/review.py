#default libraries
from typing import Optional, List

#third party libraries
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

#local 
# from src.dao.models import Article

class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    id: Optional[int] = Field(default=None, primary_key=True)
    source_url: str = Field(max_length=500)
    # Relationship: one review -> many articles
    articles: Optional[List["Article"]] = Relationship(back_populates="review")
    
    def __str__(self) -> str:
        """
        Format review as HTML string for Telegram messages.
        
        Returns:
            Formatted HTML message string with articles and Telegraph URLs
        """
        lines = [f"📰 <b>Review #{self.id}</b>\n"]
        
        if not self.articles or len(self.articles) == 0:
            lines.append("⚠️ No articles found in this review.")
        else:
            lines.append(f"📚 <b>{len(self.articles)} article(s):</b>\n")
            
            for idx, article in enumerate(self.articles, 1):
                lines.append(f"{idx}. <b>{article.title}</b>")
                
                # Add Telegraph URLs if available
                if article.telegraph_urls and len(article.telegraph_urls) > 0:
                    # Add all Telegraph URLs
                    lines.extend([f"   📎 <a href='{url}'>Telegraph</a>" for url in article.telegraph_urls])
                else:
                    lines.append("   ⚠️ No Telegraph URLs available")
                
                # Add original URL and spacing
                lines.extend([
                    f"   🔗 <a href='{article.original_url}'>Original article</a>",
                    ""  # Empty line for spacing
                ])
        
        # Add source URL
        lines.append(f"\n📖 <a href='{self.source_url}'>View source review</a>")
        
        return "\n".join(lines)
    

