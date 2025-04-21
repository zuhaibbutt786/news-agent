import logging
from app.scrapers.bbc_scraper import BBCScraper
from app.models.news import Source, Category, NewsArticle
from app import db
from app.utils.text_utils import generate_slug
from app.nlp.text_processor import TextProcessor
from app.translations.translator import Translator
from app.seo.seo_optimizer import SEOOptimizer
import time
from datetime import datetime

class ScraperManager:
    def __init__(self):
        self.scrapers = {
            'bbc': BBCScraper()
        }
        self.logger = logging.getLogger('scraper.manager')
        self.text_processor = TextProcessor()
        self.translator = Translator()
        self.seo_optimizer = SEOOptimizer()
    
    def register_scraper(self, name, scraper):
        """Register a new scraper"""
        self.scrapers[name] = scraper
    
    def get_scraper(self, name):
        """Get a scraper by name"""
        return self.scrapers.get(name)
    
    def run_all_scrapers(self, limit_per_source=5):
        """Run all registered scrapers"""
        all_articles = []
        
        for name, scraper in self.scrapers.items():
            self.logger.info(f"Running scraper: {name}")
            try:
                articles = scraper.scrape_articles(limit=limit_per_source)
                all_articles.extend(articles)
                self.logger.info(f"Scraped {len(articles)} articles from {name}")
            except Exception as e:
                self.logger.error(f"Error running scraper {name}: {e}")
        
        return all_articles
    
    def process_and_save_articles(self, articles):
        """Process and save articles to the database"""
        for article_data in articles:
            try:
                # Check if article already exists
                existing_article = NewsArticle.query.filter_by(
                    original_url=article_data['original_url']
                ).first()
                
                if existing_article:
                    self.logger.info(f"Article already exists: {article_data['title']}")
                    continue
                
                # Get or create source
                source = Source.query.filter_by(name=article_data['source']).first()
                if not source:
                    source = Source(
                        name=article_data['source'],
                        url=article_data.get('source_url', '')
                    )
                    db.session.add(source)
                    db.session.commit()
                
                # Get or create category
                category = Category.query.filter_by(name=article_data['category']).first()
                if not category:
                    category_slug = generate_slug(article_data['category'])
                    category = Category(
                        name=article_data['category'],
                        slug=category_slug
                    )
                    db.session.add(category)
                    db.session.commit()
                
                # Process text
                processed_content = self.text_processor.process(article_data['content'])
                
                # Translate to Urdu
                title_urdu = self.translator.translate_to_urdu(article_data['title'])
                content_urdu = self.translator.translate_to_urdu(processed_content)
                
                # Generate SEO metadata
                seo_data = self.seo_optimizer.optimize(
                    title=article_data['title'],
                    content=processed_content,
                    category=article_data['category']
                )
                
                # Create slug
                slug = generate_slug(article_data['title'])
                
                # Create new article
                new_article = NewsArticle(
                    title=article_data['title'],
                    title_urdu=title_urdu,
                    slug=slug,
                    content=processed_content,
                    content_urdu=content_urdu,
                    summary=article_data.get('summary'),
                    original_url=article_data['original_url'],
                    image_url=article_data.get('image_url'),
                    published_date=article_data.get('published_date', datetime.now()),
                    category_id=category.id,
                    source_id=source.id,
                    meta_title=seo_data.get('meta_title'),
                    meta_description=seo_data.get('meta_description'),
                    keywords=seo_data.get('keywords'),
                    status='published'
                )
                
                db.session.add(new_article)
                db.session.commit()
                
                self.logger.info(f"Saved article: {new_article.title}")
                
                # Add a small delay to avoid overloading the database
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error processing article {article_data.get('title', 'Unknown')}: {e}")
                db.session.rollback()
    
    def run_scraping_job(self):
        """Run a complete scraping job"""
        self.logger.info("Starting scraping job")
        
        articles = self.run_all_scrapers()
        self.process_and_save_articles(articles)
        
        self.logger.info("Scraping job completed")