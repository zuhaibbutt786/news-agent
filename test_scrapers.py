#!/usr/bin/env python3
"""
Test script for the news scrapers
"""

import logging
import sys
from app.scrapers.scraper_manager import ScraperManager
from app.scrapers.geo_scraper import GeoNewsScraper
from app.scrapers.ary_scraper import ARYNewsScraper
from app.scrapers.dunya_scraper import DunyaNewsScraper
from app.scrapers.express_scraper import ExpressNewsScraper
from app.scrapers.dawn_scraper import DawnNewsScraper
from app.scrapers.samaa_scraper import SamaaNewsScraper
from app.scrapers.bol_scraper import BolNewsScraper
from app.scrapers.tribune_scraper import TribuneNewsScraper
from app.scrapers.aaj_scraper import AajNewsScraper
from app.scrapers.92news_scraper import News92Scraper
from app.scrapers.thenews_scraper import TheNewsScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('scraper_test')

def test_scraper(scraper, name):
    """Test a single scraper"""
    logger.info(f"Testing {name} scraper...")
    
    # Test fetching articles
    articles = scraper.fetch_articles(limit=3)
    logger.info(f"Fetched {len(articles)} articles from {name}")
    
    if not articles:
        logger.warning(f"No articles found for {name}")
        return
    
    # Test parsing the first article
    article_url = articles[0]
    logger.info(f"Parsing article: {article_url}")
    
    article_data = scraper.parse_article(article_url)
    
    if article_data:
        logger.info(f"Successfully parsed article: {article_data['title']}")
        logger.info(f"Content length: {len(article_data['content'])} characters")
        logger.info(f"Published date: {article_data['published_date']}")
        logger.info(f"Category: {article_data['category']}")
        logger.info(f"Image URL: {article_data['image_url']}")
    else:
        logger.error(f"Failed to parse article from {name}")

def main():
    """Main function to test all scrapers"""
    logger.info("Starting scraper tests...")
    
    # Create instances of all scrapers
    scrapers = {
        'Geo News': GeoNewsScraper(),
        'ARY News': ARYNewsScraper(),
        'Dunya News': DunyaNewsScraper(),
        'Express News': ExpressNewsScraper(),
        'Dawn News': DawnNewsScraper(),
        'Samaa News': SamaaNewsScraper(),
        'BOL News': BolNewsScraper(),
        'Tribune News': TribuneNewsScraper(),
        'Aaj News': AajNewsScraper(),
        '92 News': News92Scraper(),
        'The News': TheNewsScraper()
    }
    
    # Test each scraper
    for name, scraper in scrapers.items():
        try:
            test_scraper(scraper, name)
            print("\n" + "-" * 50 + "\n")
        except Exception as e:
            logger.error(f"Error testing {name} scraper: {str(e)}")
    
    logger.info("Scraper tests completed")

if __name__ == "__main__":
    main()