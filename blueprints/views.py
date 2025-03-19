from flask import Blueprint, render_template
from db import get_all_news

views = Blueprint('views', __name__)

# @views.route('/')
# def index():
#     """Render home page with AI news"""
#     blogs = get_all_news()
#     return render_template('index.html', blogs=blogs)

@views.route('/')
def home():
    """Render home page with latest AI news"""
    news = get_all_news()
    return render_template('index.html', news=news)

@views.route('/archive')
def archive():
    """Render archive page"""
    all_news = get_all_news()
    return render_template('archive.html', news=all_news)