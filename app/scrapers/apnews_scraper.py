from app.scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
import logging
from datetime import datetime
import re

class APNewsScraper(BaseScraper):
    """
    Scraper for Associated Press News (https://apnews.com/)
    """
    
    def __init__(self):
        super().__init__(
            source_name="AP News",
            base_url="https://apnews.com/"
        )
        self.categories = {
            "world": "hub/world-news",
            "us": "hub/us-news",
            "politics": "hub/politics",
            "sports": "hub/sports",
            "entertainment": "hub/entertainment",
            "business": "hub/business",
            "technology": "hub/technology",
            "health": "hub/health",
            "science": "hub/science"
        }
    
    def get_article_urls(self, category=None, limit=10):
        """
        Fetch articles from AP News
        
        Args:
            category (str, optional): Category to fetch articles from. Defaults to None.
            limit (int, optional): Maximum number of articles to fetch. Defaults to 10.
            
        Returns:
            list: List of article URLs
        """
        try:
            article_urls = []
            
            # Determine URL based on category
            if category and category in self.categories:
                url = f"{self.base_url}{self.categories[category]}"
            else:
                url = self.base_url
            
            # Fetch the page
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find article links
            articles = soup.find_all('a')
            
            for article in articles:
                article_url = article.get('href')
                
                # Handle relative URLs
                if article_url and article_url.startswith('/'):
                    article_url = self.base_url.rstrip('/') + article_url
                
                # Only include article URLs
                if article_url and article_url.startswith(self.base_url) and '/article/' in article_url and article_url not in article_urls:
                    article_urls.append(article_url)
                    
                    if len(article_urls) >= limit:
                        break
            
            return article_urls
            
        except Exception as e:
            logging.error(f"Error fetching articles from AP News: {str(e)}")
            return []
    
    def scrape_article(self, url):
        """
        Parse a single article from AP News
        
        Args:
            url (str): URL of the article to parse
            
        Returns:
            dict: Article data
        """
        try:
            # Fetch the article
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse the article
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract article data
            title_element = soup.select_one('h1')
            title = title_element.text.strip() if title_element else ""
            
            # Extract content
            content_elements = soup.select('.RichTextStoryBody p, .Article p, .article-body p')
            content = '\n\n'.join([p.text.strip() for p in content_elements if p.text.strip()])
            
            # Extract date
            date_element = soup.select_one('time')
            date_str = date_element.get('datetime') if date_element and date_element.get('datetime') else date_element.text.strip() if date_element else ""
            
            # Parse date
            published_date = None
            if date_str:
                try:
                    # Try to parse the date in various formats
                    date_patterns = [
                        r'(\d{4}-\d{2}-\d{2})',  # e.g., "2025-04-21"
                        r'(\w+ \d+, \d{4})',  # e.g., "April 21, 2025"
                        r'(\d{2} \w+ \d{4})'   # e.g., "21 April 2025"
                    ]
                    
                    for pattern in date_patterns:
                        match = re.search(pattern, date_str)
                        if match:
                            date_str = match.group(1)
                            break
                    
                    # Try different date formats
                    for fmt in ["%Y-%m-%d", "%B %d, %Y", "%d %B %Y"]:
                        try:
                            published_date = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                            
                except Exception as e:
                    logging.error(f"Error parsing date from AP News: {str(e)}")
                    published_date = datetime.now()
            
            if not published_date:
                published_date = datetime.now()
            
            # Extract category
            category_element = soup.select_one('.Page-header-category')
            category = category_element.text.strip() if category_element else "General"
            
            # Extract image URL
            image_element = soup.select_one('.LeadFeature-image img')
            image_url = image_element.get('src') if image_element else None
            
            # Create article data
            article_data = {
                'title': title,
                'content': content,
                'url': url,
                'published_date': published_date,
                'source_name': self.source_name,
                'category': category,
                'image_url': image_url
            }
            
            return article_data
            
        except Exception as e:
            logging.error(f"Error parsing article from AP News: {str(e)}")
            return None