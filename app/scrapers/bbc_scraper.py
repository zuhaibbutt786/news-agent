from app.scrapers.base_scraper import BaseScraper
from datetime import datetime
import re
from bs4 import BeautifulSoup
import logging

class BBCScraper(BaseScraper):
    def __init__(self):
        super().__init__('BBC News', 'https://www.bbc.com/news')
        self.category_urls = {
            'world': 'https://www.bbc.com/news/world',
            'business': 'https://www.bbc.com/news/business',
            'technology': 'https://www.bbc.com/news/technology',
            'science': 'https://www.bbc.com/news/science_and_environment',
            'health': 'https://www.bbc.com/news/health',
            'entertainment': 'https://www.bbc.com/news/entertainment_and_arts'
        }
    
    def get_article_urls(self, category=None, limit=10):
        """Get a list of article URLs from BBC News"""
        url = self.category_urls.get(category, self.base_url)
        soup = self.get_soup(url)
        
        if not soup:
            return []
        
        article_urls = []
        
        # Find all article links
        for link in soup.select('a.gs-c-promo-heading'):
            href = link.get('href')
            if href and '/news/' in href and not href.endswith('/news/'):
                full_url = self.get_absolute_url(href)
                if full_url and full_url not in article_urls:
                    article_urls.append(full_url)
                    if len(article_urls) >= limit:
                        break
        
        return article_urls
    
    def scrape_article(self, url):
        """Scrape a single BBC News article"""
        soup = self.get_soup(url)
        
        if not soup:
            return None
        
        try:
            # Extract title
            title_element = soup.select_one('h1')
            title = self.clean_text(title_element.text) if title_element else None
            
            if not title:
                return None
            
            # Extract content
            content_elements = soup.select('article p, article h2, article ul li')
            content = '\n\n'.join([self.clean_text(p.text) for p in content_elements if p.text.strip()])
            
            # Extract publication date
            date_element = soup.select_one('time')
            published_date = None
            if date_element and date_element.get('datetime'):
                try:
                    published_date = datetime.fromisoformat(date_element['datetime'].replace('Z', '+00:00'))
                except ValueError:
                    published_date = datetime.now()
            else:
                published_date = datetime.now()
            
            # Extract image
            image_element = soup.select_one('article img')
            image_url = None
            if image_element and image_element.get('src'):
                image_url = image_element['src']
            
            # Extract summary
            summary_element = soup.select_one('article p')
            summary = self.clean_text(summary_element.text) if summary_element else None
            
            # Create article data
            article_data = {
                'title': title,
                'content': content,
                'summary': summary,
                'published_date': published_date,
                'image_url': image_url,
                'original_url': url,
                'source': 'BBC News',
                'category': self._determine_category(url)
            }
            
            return article_data
            
        except Exception as e:
            self.logger.error(f"Error scraping BBC article {url}: {e}")
            return None
    
    def _determine_category(self, url):
        """Determine the category of an article based on its URL"""
        for category, category_url in self.category_urls.items():
            if category in url:
                return category
        
        # Default category if none is found
        return 'world'