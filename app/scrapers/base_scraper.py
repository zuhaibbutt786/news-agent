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
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    def get_soup(self, url):
        """Get BeautifulSoup object from URL"""
        html = self.get_page(url)
        if html:
            return BeautifulSoup(html, 'html.parser')
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
        article_urls = self.get_article_urls(category, limit)
        articles = []
        
        for url in article_urls:
            self.random_delay()
            article_data = self.scrape_article(url)
            if article_data:
                articles.append(article_data)
        
        return articles