from app import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    
    news_articles = db.relationship('NewsArticle', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=True)
    
    news_articles = db.relationship('NewsArticle', backref='source', lazy=True)
    
    def __repr__(self):
        return f'<Source {self.name}>'

class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    title_urdu = db.Column(db.Text, nullable=True)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_urdu = db.Column(db.Text, nullable=True)
    summary = db.Column(db.Text, nullable=True)
    original_url = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    published_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # SEO fields
    meta_title = db.Column(db.String(255), nullable=True)
    meta_description = db.Column(db.Text, nullable=True)
    keywords = db.Column(db.String(255), nullable=True)
    
    # Foreign keys
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'), nullable=False)
    
    # Status (draft, published, etc.)
    status = db.Column(db.String(20), nullable=False, default='draft')
    
    def __repr__(self):
        return f'<NewsArticle {self.title}>'