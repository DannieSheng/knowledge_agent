from flask import Blueprint, render_template, request
from db import get_all_news, update_news_feedback, get_paginated_news
import datetime  

views = Blueprint('views', __name__)

# @views.route('/')
# def index():
#     """Render home page with AI news"""
#     blogs = get_all_news()
#     return render_template('index.html', blogs=blogs)

@views.route('/')
def home():
    """Render home page with latest AI news"""
    today = datetime.datetime.now().strftime("%Y-%m-%d %A")  # Format: YYYY-MM-DD Day
    news = get_all_news()
    return render_template('index.html', news=news, today=today)

@views.route('/archive', methods=['GET'])
def archive():
    """Render archive page"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    all_news = get_all_news()
    all_news = get_paginated_news(page, per_page)
    return render_template('archive.html', news=all_news)

@views.route('/like/<int:news_id>', methods=['POST'])
def like_news(news_id):
    update_news_feedback(news_id, 'like')
    return '', 204

@views.route('/dislike/<int:news_id>', methods=['POST'])
def dislike_news(news_id):
    update_news_feedback(news_id, 'dislike')
    return '', 204



