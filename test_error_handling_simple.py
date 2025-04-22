#!/usr/bin/env python3
"""
Simplified test script to verify error handling in the news scraper system.
"""

import logging
import sys
import os
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('error_handling_test')

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the necessary modules
from app.scrapers.base_scraper import BaseScraper

# Create a test scraper that will intentionally fail
class FailingScraper(BaseScraper):
    def __init__(self, fail_mode='get_article_urls'):
        super().__init__('Failing Scraper', 'https://example.com')
        self.fail_mode = fail_mode
    
    def get_article_urls(self, category=None, limit=10):
        """Intentionally fail based on fail_mode"""
        if self.fail_mode == 'get_article_urls':
            raise Exception("Intentional failure in get_article_urls")
        
        # Return some dummy URLs
        return ['https://example.com/article1', 'https://example.com/article2']
    
    def scrape_article(self, url):
        """Intentionally fail based on fail_mode"""
        if self.fail_mode == 'scrape_article':
            raise Exception("Intentional failure in scrape_article")
        
        # Return a dummy article
        return {
            'title': 'Test Article',
            'content': 'This is a test article content.',
            'original_url': url,
            'source': 'Failing Scraper',
            'category': 'Test'
        }

def test_get_page_error_handling():
    """Test error handling in the get_page method"""
    logger.info("Testing get_page error handling...")
    
    # Create a test scraper
    scraper = FailingScraper()
    
    # Test with a valid URL
    logger.info("Testing with a valid URL")
    html = scraper.get_page("https://www.example.com")
    logger.info(f"Result: {'Success' if html else 'Failed'}")
    
    # Test with an invalid URL
    logger.info("Testing with an invalid URL")
    html = scraper.get_page("https://invalid-domain-that-does-not-exist.com")
    logger.info(f"Result: {'Success' if html else 'Failed'}")
    
    # Test with a URL that returns a 404
    logger.info("Testing with a URL that returns a 404")
    html = scraper.get_page("https://www.example.com/not-found")
    logger.info(f"Result: {'Success' if html else 'Failed'}")
    
    # Test with a URL that returns a 403
    logger.info("Testing with a URL that returns a 403")
    html = scraper.get_page("https://httpbin.org/status/403")
    logger.info(f"Result: {'Success' if html else 'Failed'}")

def test_scrape_articles_error_handling():
    """Test error handling in the scrape_articles method"""
    logger.info("Testing scrape_articles error handling...")
    
    # Test 1: Scraper that fails in get_article_urls
    logger.info("Test 1: Scraper that fails in get_article_urls")
    failing_scraper1 = FailingScraper(fail_mode='get_article_urls')
    articles1 = failing_scraper1.scrape_articles()
    logger.info(f"Result: {len(articles1)} articles returned (should be 0)")
    
    # Test 2: Scraper that fails in scrape_article
    logger.info("Test 2: Scraper that fails in scrape_article")
    failing_scraper2 = FailingScraper(fail_mode='scrape_article')
    articles2 = failing_scraper2.scrape_articles()
    logger.info(f"Result: {len(articles2)} articles returned (should be 0)")

if __name__ == "__main__":
    test_get_page_error_handling()
    test_scrape_articles_error_handling()