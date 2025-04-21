from flask import Blueprint, jsonify, request
from app.models.news import NewsArticle, Category, Source
from app import db
from sqlalchemy import desc
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/news', methods=['GET'])
def get_news():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_slug = request.args.get('category', None)
    
    query = NewsArticle.query.filter_by(status='published')
    
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter_by(category_id=category.id)
    
    news_pagination = query.order_by(desc(NewsArticle.published_date)).paginate(page=page, per_page=per_page)
    
    news_list = []
    for article in news_pagination.items:
        news_list.append({
            'id': article.id,
            'title': article.title,
            'title_urdu': article.title_urdu,
            'slug': article.slug,
            'summary': article.summary,
            'image_url': article.image_url,
            'published_date': article.published_date.isoformat(),
            'category': article.category.name,
            'source': article.source.name
        })
    
    return jsonify({
        'news': news_list,
        'total': news_pagination.total,
        'pages': news_pagination.pages,
        'current_page': news_pagination.page
    })

@api_bp.route('/news/<string:slug>', methods=['GET'])
def get_article(slug):
    article = NewsArticle.query.filter_by(slug=slug, status='published').first_or_404()
    
    article_data = {
        'id': article.id,
        'title': article.title,
        'title_urdu': article.title_urdu,
        'slug': article.slug,
        'content': article.content,
        'content_urdu': article.content_urdu,
        'summary': article.summary,
        'image_url': article.image_url,
        'original_url': article.original_url,
        'published_date': article.published_date.isoformat(),
        'category': {
            'id': article.category.id,
            'name': article.category.name,
            'slug': article.category.slug
        },
        'source': {
            'id': article.source.id,
            'name': article.source.name,
            'url': article.source.url
        }
    }
    
    return jsonify(article_data)

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    
    category_list = []
    for category in categories:
        category_list.append({
            'id': category.id,
            'name': category.name,
            'slug': category.slug
        })
    
    return jsonify({'categories': category_list})

@api_bp.route('/sources', methods=['GET'])
def get_sources():
    sources = Source.query.all()
    
    source_list = []
    for source in sources:
        source_list.append({
            'id': source.id,
            'name': source.name,
            'url': source.url,
            'logo': source.logo
        })
    
    return jsonify({'sources': source_list})