from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import logging
from app.scrapers.scraper_manager import ScraperManager
import atexit

class Scheduler:
    def __init__(self, app=None):
        self.logger = logging.getLogger('scheduler')
        self.scheduler = BackgroundScheduler()
        self.scraper_manager = ScraperManager()
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize the scheduler with the Flask app"""
        # Register shutdown function
        atexit.register(self.shutdown)
        
        # Add jobs based on app configuration
        self.add_jobs(app)
        
        # Start the scheduler
        self.start()
    
    def add_jobs(self, app):
        """Add jobs to the scheduler based on app configuration"""
        # Add scraping job
        scraping_interval = app.config.get('SCRAPING_INTERVAL_MINUTES', 60)
        self.add_scraping_job(minutes=scraping_interval)
        
        # Add other jobs as needed
    
    def add_scraping_job(self, minutes=60):
        """Add a job to scrape news at regular intervals"""
        self.scheduler.add_job(
            func=self.scraper_manager.run_scraping_job,
            trigger=IntervalTrigger(minutes=minutes),
            id='scraping_job',
            name='Scrape news articles',
            replace_existing=True
        )
        self.logger.info(f"Added scraping job to run every {minutes} minutes")
    
    def add_daily_job(self, func, hour=0, minute=0, id=None, name=None):
        """Add a job to run daily at a specific time"""
        self.scheduler.add_job(
            func=func,
            trigger=CronTrigger(hour=hour, minute=minute),
            id=id,
            name=name,
            replace_existing=True
        )
        self.logger.info(f"Added daily job {name} to run at {hour:02d}:{minute:02d}")
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            self.logger.info("Scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.logger.info("Scheduler shut down")