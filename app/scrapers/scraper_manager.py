import logging
from app.scrapers.bbc_scraper import BBCScraper
from app.scrapers.geo_scraper import GeoNewsScraper
from app.scrapers.ary_scraper import ARYNewsScraper
from app.scrapers.dunya_scraper import DunyaNewsScraper
from app.scrapers.express_scraper import ExpressNewsScraper
from app.scrapers.dawn_scraper import DawnNewsScraper
from app.scrapers.samaa_scraper import SamaaNewsScraper
from app.scrapers.bol_scraper import BolNewsScraper
from app.scrapers.tribune_scraper import TribuneNewsScraper
from app.scrapers.aaj_scraper import AajNewsScraper
from app.scrapers.news92_scraper import News92Scraper
from app.scrapers.thenews_scraper import TheNewsScraper
# International news sources
from app.scrapers.aljazeera_scraper import AlJazeeraScraper
from app.scrapers.arabnews_scraper import ArabNewsScraper
from app.scrapers.tehrantimes_scraper import TehranTimesScraper
from app.scrapers.jpost_scraper import JerusalemPostScraper
from app.scrapers.ansa_scraper import AnsaNewsScraper
from app.scrapers.reuters_scraper import ReutersScraper
from app.scrapers.france24_scraper import France24Scraper
from app.scrapers.apnews_scraper import APNewsScraper
from app.scrapers.npr_scraper import NPRScraper
from app.scrapers.cnn_scraper import CNNScraper
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
            # Pakistani news sources
            'bbc': BBCScraper(),
            'geo': GeoNewsScraper(),
            'ary': ARYNewsScraper(),
            'dunya': DunyaNewsScraper(),
            'express': ExpressNewsScraper(),
            'dawn': DawnNewsScraper(),
            'samaa': SamaaNewsScraper(),
            'bol': BolNewsScraper(),
            'tribune': TribuneNewsScraper(),
            'aaj': AajNewsScraper(),
            '92news': News92Scraper(),
            'thenews': TheNewsScraper(),
            
            # International news sources
            'aljazeera': AlJazeeraScraper(),
            'arabnews': ArabNewsScraper(),
            'tehrantimes': TehranTimesScraper(),
            'jpost': JerusalemPostScraper(),
            'ansa': AnsaNewsScraper(),
            'reuters': ReutersScraper(),
            'france24': France24Scraper(),
            'apnews': APNewsScraper(),
            'npr': NPRScraper(),
            'cnn': CNNScraper()
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
        failed_scrapers = []
        
        for name, scraper in self.scrapers.items():
            self.logger.info(f"Running scraper: {name}")
            try:
                articles = scraper.scrape_articles(limit=limit_per_source)
                if articles:
                    all_articles.extend(articles)
                    self.logger.info(f"Scraped {len(articles)} articles from {name}")
                else:
                    self.logger.warning(f"No articles scraped from {name}")
                    failed_scrapers.append(name)
            except Exception as e:
                self.logger.error(f"Error running scraper {name}: {e}")
                failed_scrapers.append(name)
                # Continue with the next scraper
                continue
        
        if failed_scrapers:
            self.logger.warning(f"The following scrapers failed: {', '.join(failed_scrapers)}")
        
        self.logger.info(f"Successfully scraped {len(all_articles)} articles from {len(self.scrapers) - len(failed_scrapers)} sources")
        return all_articles
    
    def process_and_save_articles(self, articles):
        """Process and save articles to the database"""
        saved_count = 0
        error_count = 0
        skipped_count = 0
        
        for article_data in articles:
            try:
                # Validate required fields
                required_fields = ['title', 'content', 'original_url', 'source', 'category']
                missing_fields = [field for field in required_fields if field not in article_data or not article_data[field]]
                
                if missing_fields:
                    self.logger.warning(f"Skipping article due to missing fields: {', '.join(missing_fields)}")
                    skipped_count += 1
                    continue
                
                # Check if article already exists
                existing_article = NewsArticle.query.filter_by(
                    original_url=article_data['original_url']
                ).first()
                
                if existing_article:
                    self.logger.info(f"Article already exists: {article_data['title']}")
                    skipped_count += 1
                    continue
                
                # Get or create source
                try:
                    source = Source.query.filter_by(name=article_data['source']).first()
                    if not source:
                        source = Source(
                            name=article_data['source'],
                            url=article_data.get('source_url', '')
                        )
                        db.session.add(source)
                        db.session.commit()
                except Exception as e:
                    self.logger.error(f"Error creating source {article_data['source']}: {e}")
                    db.session.rollback()
                    # Create a default source if needed
                    source = Source.query.filter_by(name='Unknown').first()
                    if not source:
                        source = Source(name='Unknown', url='')
                        db.session.add(source)
                        db.session.commit()
                
                # Get or create category
                try:
                    category = Category.query.filter_by(name=article_data['category']).first()
                    if not category:
                        category_slug = generate_slug(article_data['category'])
                        category = Category(
                            name=article_data['category'],
                            slug=category_slug
                        )
                        db.session.add(category)
                        db.session.commit()
                except Exception as e:
                    self.logger.error(f"Error creating category {article_data['category']}: {e}")
                    db.session.rollback()
                    # Create a default category if needed
                    category = Category.query.filter_by(name='General').first()
                    if not category:
                        category = Category(name='General', slug='general')
                        db.session.add(category)
                        db.session.commit()
                
                # Process text with error handling
                try:
                    processed_content = self.text_processor.process(article_data['content'])
                except Exception as e:
                    self.logger.error(f"Error processing content: {e}")
                    processed_content = article_data['content']  # Use original content if processing fails
                
                # Translate to Urdu with error handling
                try:
                    title_urdu = self.translator.translate_to_urdu(article_data['title'])
                    content_urdu = self.translator.translate_to_urdu(processed_content)
                except Exception as e:
                    self.logger.error(f"Error translating content: {e}")
                    title_urdu = article_data['title']  # Use original title if translation fails
                    content_urdu = processed_content  # Use processed content if translation fails
                
                # Generate SEO metadata with error handling
                try:
                    seo_data = self.seo_optimizer.optimize(
                        title=article_data['title'],
                        content=processed_content,
                        category=article_data['category']
                    )
                except Exception as e:
                    self.logger.error(f"Error generating SEO data: {e}")
                    # Create default SEO data
                    seo_data = {
                        'meta_title': article_data['title'],
                        'meta_description': article_data['content'][:160] if len(article_data['content']) > 160 else article_data['content'],
                        'keywords': article_data['category']
                    }
                
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
                saved_count += 1
                
                # Add a small delay to avoid overloading the database
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error processing article {article_data.get('title', 'Unknown')}: {e}")
                error_count += 1
                db.session.rollback()
                continue  # Continue with the next article
        
        self.logger.info(f"Article processing summary: {saved_count} saved, {skipped_count} skipped, {error_count} errors")
    
    def run_scraping_job(self):
        """Run a complete scraping job"""
        self.logger.info("Starting scraping job")
        start_time = time.time()
        
        try:
            # Run all scrapers with error handling
            articles = self.run_all_scrapers()
            
            if not articles:
                self.logger.warning("No articles were scraped from any source")
                return
                
            # Process and save articles with error handling
            self.process_and_save_articles(articles)
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self.logger.info(f"Scraping job completed successfully in {duration} seconds")
            
        except Exception as e:
            self.logger.error(f"Critical error in scraping job: {e}")
            # Continue execution even if there's an error
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            self.logger.info(f"Scraping job completed with errors in {duration} seconds")