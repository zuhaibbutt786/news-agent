import requests
from bs4 import BeautifulSoup
import logging
from abc import ABC, abstractmethod
from datetime import datetime
import re
import time
import random
from urllib.parse import urlparse

class BaseScraper(ABC):
    def __init__(self, source_name, base_url):
        self.source_name = source_name
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.logger = logging.getLogger(f'scraper.{source_name}')
    
    def get_page(self, url):
        """Fetch the HTML content of a page"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.HTTPError as e:
                status_code = e.response.status_code
                if status_code in [403, 429]:  # Forbidden or Too Many Requests
                    self.logger.warning(f"Access denied (status {status_code}) for {url}. Changing user agent and retrying...")
                    # Rotate user agents
                    user_agents = [
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
                    ]
                    self.headers['User-Agent'] = user_agents[attempt % len(user_agents)]
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    self.logger.error(f"HTTP error fetching {url}: {e}")
                    return None
            except requests.RequestException as e:
                self.logger.error(f"Error fetching {url}: {e}")
                if attempt < max_retries - 1:
                    self.logger.info(f"Retrying {url} (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                return None
            except Exception as e:
                self.logger.error(f"Unexpected error fetching {url}: {e}")
                return None
        
        self.logger.error(f"Failed to fetch {url} after {max_retries} attempts")
        return None
    
    def get_soup(self, url):
        """Get BeautifulSoup object from URL"""
        try:
            html = self.get_page(url)
            if html:
                try:
                    return BeautifulSoup(html, 'html.parser')
                except Exception as e:
                    self.logger.error(f"Error parsing HTML from {url}: {e}")
                    # Try with a more lenient parser
                    try:
                        return BeautifulSoup(html, 'lxml')
                    except Exception as e2:
                        self.logger.error(f"Error parsing HTML with lxml from {url}: {e2}")
                        # Last resort: use html5lib
                        try:
                            return BeautifulSoup(html, 'html5lib')
                        except Exception as e3:
                            self.logger.error(f"All HTML parsers failed for {url}: {e3}")
                            return None
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error in get_soup for {url}: {e}")
            return None
    
    def clean_text(self, text):
        """Clean text by removing extra whitespace"""
        if not text:
            return ""
        # Replace multiple spaces, newlines, and tabs with a single space
        text = re.sub(r'\s+', ' ', text)
        # Remove leading and trailing whitespace
        return text.strip()
    
    def get_absolute_url(self, url):
        """Convert relative URL to absolute URL"""
        if not url:
            return None
        
        if url.startswith('http'):
            return url
        
        # Handle relative URLs
        parsed_base = urlparse(self.base_url)
        base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
        
        if url.startswith('/'):
            return f"{base_domain}{url}"
        else:
            path = '/'.join(parsed_base.path.split('/')[:-1]) if parsed_base.path else ''
            return f"{base_domain}{path}/{url}"
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Add a random delay to avoid being blocked"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    @abstractmethod
    def get_article_urls(self, category=None, limit=10):
        """Get a list of article URLs to scrape"""
        pass
    
    @abstractmethod
    def scrape_article(self, url):
        """Scrape a single article and return its data"""
        pass
    
    def scrape_articles(self, category=None, limit=10):
        """Scrape multiple articles"""
        try:
            article_urls = self.get_article_urls(category, limit)
            articles = []
            
            for url in article_urls:
                try:
                    self.random_delay()
                    article_data = self.scrape_article(url)
                    if article_data:
                        articles.append(article_data)
                except Exception as e:
                    self.logger.error(f"Error scraping article {url}: {e}")
                    # Continue with the next article even if this one fails
                    continue
            
            return articles
        except Exception as e:
            self.logger.error(f"Error in scrape_articles for {self.source_name}: {e}")
            # Return empty list instead of failing completely
            return []