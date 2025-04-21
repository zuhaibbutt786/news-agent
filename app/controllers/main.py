from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.news import NewsArticle, Category
from app import db
from sqlalchemy import desc

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get latest news articles
    latest_news = NewsArticle.query.filter_by(status='published').order_by(desc(NewsArticle.published_date)).limit(10).all()
    
    # Get categories
    categories = Category.query.all()
    
    return render_template('index.html', latest_news=latest_news, categories=categories)

@main_bp.route('/category/<string:slug>')
def category(slug):
    # Get category by slug
    category = Category.query.filter_by(slug=slug).first_or_404()
    
    # Get news articles for this category
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    news_articles = NewsArticle.query.filter_by(
        category_id=category.id, 
        status='published'
    ).order_by(
        desc(NewsArticle.published_date)
    ).paginate(page=page, per_page=per_page)
    
    return render_template('category.html', category=category, news_articles=news_articles)

@main_bp.route('/article/<string:slug>')
def article(slug):
    # Get article by slug
    article = NewsArticle.query.filter_by(slug=slug, status='published').first_or_404()
    
    # Get related articles
    related_articles = NewsArticle.query.filter_by(
        category_id=article.category_id, 
        status='published'
    ).filter(
        NewsArticle.id != article.id
    ).order_by(
        desc(NewsArticle.published_date)
    ).limit(5).all()
    
    return render_template('article.html', article=article, related_articles=related_articles)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    
    if not query:
        return redirect(url_for('main.index'))
    
    # Search for articles
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    search_results = NewsArticle.query.filter(
        NewsArticle.status == 'published',
        (
            NewsArticle.title.ilike(f'%{query}%') | 
            NewsArticle.content.ilike(f'%{query}%') |
            NewsArticle.title_urdu.ilike(f'%{query}%') |
            NewsArticle.content_urdu.ilike(f'%{query}%')
        )
    ).order_by(
        desc(NewsArticle.published_date)
    ).paginate(page=page, per_page=per_page)
    
    return render_template('search.html', query=query, search_results=search_results)