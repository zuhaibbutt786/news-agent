from app.scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
import logging
from datetime import datetime
import re

class GeoNewsScraper(BaseScraper):
    """
    Scraper for Geo News (https://www.geo.tv/)
    """
    
    def __init__(self):
        super().__init__(
            source_name="Geo News",
            source_url="https://www.geo.tv/",
            base_url="https://www.geo.tv/"
        )
        self.categories = {
            "pakistan": "pakistan",
            "world": "world",
            "business": "business",
            "sports": "sports",
            "entertainment": "entertainment",
            "health": "health",
            "sci-tech": "technology"
        }
    
    def fetch_articles(self, category=None, limit=10):
        """
        Fetch articles from Geo News
        
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
                url = f"{self.base_url}/category/{category}"
            else:
                url = self.base_url
            
            # Fetch the page
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find article links
            articles = soup.select('.story__link, .top-stories__item a, .more-stories__item a')
            
            for article in articles:
                article_url = article.get('href')
                
                # Handle relative URLs
                if article_url and not article_url.startswith('http'):
                    article_url = self.base_url.rstrip('/') + article_url
                
                if article_url and article_url not in article_urls:
                    article_urls.append(article_url)
                    
                    if len(article_urls) >= limit:
                        break
            
            return article_urls
            
        except Exception as e:
            logging.error(f"Error fetching articles from Geo News: {str(e)}")
            return []
    
    def parse_article(self, url):
        """
        Parse a single article from Geo News
        
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
            title = soup.select_one('h1.story__title').text.strip() if soup.select_one('h1.story__title') else ""
            
            # Extract content
            content_elements = soup.select('.story__content p')
            content = '\n\n'.join([p.text.strip() for p in content_elements if p.text.strip()])
            
            # Extract date
            date_element = soup.select_one('.story__time, .story__date')
            date_str = date_element.text.strip() if date_element else ""
            
            # Parse date
            published_date = None
            if date_str:
                try:
                    # Try to parse the date in various formats
                    date_patterns = [
                        r'(\w+ \d+, \d{4})',  # e.g., "April 21, 2025"
                        r'(\d{2}-\d{2}-\d{4})',  # e.g., "21-04-2025"
                        r'(\d{2}/\d{2}/\d{4})'   # e.g., "21/04/2025"
                    ]
                    
                    for pattern in date_patterns:
                        match = re.search(pattern, date_str)
                        if match:
                            date_str = match.group(1)
                            break
                    
                    # Try different date formats
                    for fmt in ["%B %d, %Y", "%d-%m-%Y", "%d/%m/%Y"]:
                        try:
                            published_date = datetime.strptime(date_str, fmt)
                            break
                        except ValueError:
                            continue
                            
                except Exception as e:
                    logging.error(f"Error parsing date from Geo News: {str(e)}")
                    published_date = datetime.now()
            
            if not published_date:
                published_date = datetime.now()
            
            # Extract category
            category_element = soup.select_one('.story__category a')
            category = category_element.text.strip() if category_element else "General"
            
            # Extract image URL
            image_element = soup.select_one('.story__image img, .story__featured-image img')
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
            logging.error(f"Error parsing article from Geo News: {str(e)}")
            return None