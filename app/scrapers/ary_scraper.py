from app.scrapers.base_scraper import BaseScraper
from bs4 import BeautifulSoup
import requests
import logging
from datetime import datetime
import re

class ARYNewsScraper(BaseScraper):
    """
    Scraper for ARY News (https://arynews.tv/)
    """
    
    def __init__(self):
        super().__init__(
            source_name="ARY News",
            source_url="https://arynews.tv/",
            base_url="https://arynews.tv/"
        )
        self.categories = {
            "pakistan": "pakistan",
            "world": "world",
            "business": "business",
            "sports": "sports",
            "entertainment": "entertainment",
            "health": "health",
            "technology": "technology"
        }
    
    def fetch_articles(self, category=None, limit=10):
        """
        Fetch articles from ARY News
        
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
                url = f"{self.base_url}/category/{self.categories[category]}"
            else:
                url = self.base_url
            
            # Fetch the page
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find article links
            articles = soup.select('.post-title a, .featured-post a, .post-box a')
            
            for article in articles:
                article_url = article.get('href')
                
                if article_url and article_url not in article_urls:
                    article_urls.append(article_url)
                    
                    if len(article_urls) >= limit:
                        break
            
            return article_urls
            
        except Exception as e:
            logging.error(f"Error fetching articles from ARY News: {str(e)}")
            return []
    
    def parse_article(self, url):
        """
        Parse a single article from ARY News
        
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
            title_element = soup.select_one('.post-title, .entry-title')
            title = title_element.text.strip() if title_element else ""
            
            # Extract content
            content_elements = soup.select('.entry-content p, .post-content p')
            content = '\n\n'.join([p.text.strip() for p in content_elements if p.text.strip()])
            
            # Extract date
            date_element = soup.select_one('.post-date, .entry-date, time')
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
                    logging.error(f"Error parsing date from ARY News: {str(e)}")
                    published_date = datetime.now()
            
            if not published_date:
                published_date = datetime.now()
            
            # Extract category
            category_element = soup.select_one('.post-category a, .category a')
            category = category_element.text.strip() if category_element else "General"
            
            # Extract image URL
            image_element = soup.select_one('.post-thumbnail img, .featured-image img')
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
            logging.error(f"Error parsing article from ARY News: {str(e)}")
            return None