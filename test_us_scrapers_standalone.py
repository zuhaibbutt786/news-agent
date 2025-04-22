import logging
import sys
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('us_scraper_test')

# Base scraper class
class BaseScraper:
    def __init__(self, source_name, base_url):
        self.source_name = source_name
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_page(self, url):
        """Fetch a page and return its HTML content"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

# AP News scraper
class APNewsScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            source_name="AP News",
            base_url="https://apnews.com/"
        )
    
    def get_article_urls(self, category=None, limit=10):
        try:
            article_urls = []
            url = self.base_url
            
            # Fetch the page
            html = self.get_page(url)
            if not html:
                return []
            
            # Parse the page
            soup = BeautifulSoup(html, 'html.parser')
            
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
            logger.error(f"Error fetching articles from AP News: {str(e)}")
            return []
    
    def scrape_article(self, url):
        try:
            # Fetch the article
            html = self.get_page(url)
            if not html:
                return None
            
            # Parse the article
            soup = BeautifulSoup(html, 'html.parser')
            
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
                    logger.error(f"Error parsing date from AP News: {str(e)}")
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
            logger.error(f"Error parsing article from AP News: {str(e)}")
            return None

# NPR scraper
class NPRScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            source_name="NPR",
            base_url="https://www.npr.org/"
        )
    
    def get_article_urls(self, category=None, limit=10):
        try:
            article_urls = []
            url = self.base_url
            
            # Fetch the page
            html = self.get_page(url)
            if not html:
                return []
            
            # Parse the page
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find article links
            articles = soup.find_all('a')
            
            for article in articles:
                article_url = article.get('href')
                
                # Handle relative URLs
                if article_url and article_url.startswith('/'):
                    article_url = self.base_url.rstrip('/') + article_url
                
                # Only include article URLs
                if article_url and article_url.startswith(self.base_url) and ('/story/' in article_url or '/sections/' in article_url) and article_url not in article_urls:
                    article_urls.append(article_url)
                    
                    if len(article_urls) >= limit:
                        break
            
            return article_urls
            
        except Exception as e:
            logger.error(f"Error fetching articles from NPR: {str(e)}")
            return []
    
    def scrape_article(self, url):
        try:
            # Fetch the article
            html = self.get_page(url)
            if not html:
                return None
            
            # Parse the article
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract article data
            title_element = soup.select_one('h1')
            title = title_element.text.strip() if title_element else ""
            
            # Extract content
            content_elements = soup.select('.storytext p')
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
                    logger.error(f"Error parsing date from NPR: {str(e)}")
                    published_date = datetime.now()
            
            if not published_date:
                published_date = datetime.now()
            
            # Extract category
            category_element = soup.select_one('.topic-label')
            category = category_element.text.strip() if category_element else "General"
            
            # Extract image URL
            image_element = soup.select_one('.img img')
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
            logger.error(f"Error parsing article from NPR: {str(e)}")
            return None

# CNN scraper
class CNNScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            source_name="CNN",
            base_url="https://www.cnn.com/"
        )
    
    def get_article_urls(self, category=None, limit=10):
        try:
            article_urls = []
            url = self.base_url
            
            # Fetch the page
            html = self.get_page(url)
            if not html:
                return []
            
            # Parse the page
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find article links
            articles = soup.find_all('a')
            
            for article in articles:
                article_url = article.get('href')
                
                # Handle relative URLs
                if article_url and article_url.startswith('/'):
                    article_url = self.base_url.rstrip('/') + article_url
                
                # Only include article URLs
                if article_url and article_url.startswith(self.base_url) and (('/2025/' in article_url) or ('/2024/' in article_url)) and '/index.html' in article_url and article_url not in article_urls:
                    article_urls.append(article_url)
                    
                    if len(article_urls) >= limit:
                        break
            
            return article_urls
            
        except Exception as e:
            logger.error(f"Error fetching articles from CNN: {str(e)}")
            return []
    
    def scrape_article(self, url):
        try:
            # Fetch the article
            html = self.get_page(url)
            if not html:
                return None
            
            # Parse the article
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract article data
            title_element = soup.select_one('h1.headline__text')
            title = title_element.text.strip() if title_element else ""
            
            # Extract content
            content_elements = soup.select('.article__content p')
            content = '\n\n'.join([p.text.strip() for p in content_elements if p.text.strip()])
            
            # Extract date
            date_element = soup.select_one('.timestamp')
            date_str = date_element.text.strip() if date_element else ""
            
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
                    logger.error(f"Error parsing date from CNN: {str(e)}")
                    published_date = datetime.now()
            
            if not published_date:
                published_date = datetime.now()
            
            # Extract category
            category_element = soup.select_one('.metadata__section-label')
            category = category_element.text.strip() if category_element else "General"
            
            # Extract image URL
            image_element = soup.select_one('.image__picture img')
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
            logger.error(f"Error parsing article from CNN: {str(e)}")
            return None

def test_scraper(scraper, name):
    """Test a scraper by fetching and parsing articles"""
    logger.info(f"Testing {name} scraper...")
    
    # Fetch article URLs
    logger.info(f"Fetching from URL: {scraper.base_url}")
    articles = scraper.get_article_urls(limit=3)
    logger.info(f"Fetched {len(articles)} articles from {name}")
    
    if not articles:
        logger.warning(f"No articles found for {name}")
        return
    
    # Parse the first article
    article_url = articles[0]
    logger.info(f"Parsing article: {article_url}")
    article_data = scraper.scrape_article(article_url)
    
    if article_data:
        logger.info(f"Successfully parsed article: {article_data['title']}")
        logger.info(f"Content length: {len(article_data['content'])} characters")
        logger.info(f"Published date: {article_data['published_date']}")
        logger.info(f"Category: {article_data['category']}")
        logger.info(f"Image URL: {article_data['image_url']}")
    else:
        logger.error(f"Failed to parse article from {article_url}")
    
    logger.info("-" * 50 + "\n")

def main():
    """Run tests for all US scrapers"""
    logger.info("Starting US scraper tests...")
    
    # List of scrapers to test
    scrapers = [
        (APNewsScraper(), "AP News"),
        (NPRScraper(), "NPR"),
        (CNNScraper(), "CNN")
    ]
    
    # Test each scraper
    for scraper, name in scrapers:
        test_scraper(scraper, name)
    
    logger.info("US scraper tests completed")

if __name__ == "__main__":
    main()