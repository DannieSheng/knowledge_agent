from datetime import datetime
from flask import Blueprint, jsonify, request
from fetch_data import fetch_all_ai_blogs
from db import insert_news, get_paginated_news
# from email_sender.email_scheduler import send_daily_email_task

api = Blueprint('api', __name__)

@api.route('/news', methods=['GET'])
def get_news():
    """API Endpoint to get AI news"""
    print(f"➡️➡️ Fetching news at {datetime.now()}")
    blogs = fetch_all_ai_blogs()
    if not blogs:
        print("Debug: No blogs fetched!")
    # Insert news into the database
    for blog in blogs:
        insert_news(blog)  # Ensure this line is active
    print("✅ News fetched and stored.")
    # send_daily_email_task(blogs)
    return jsonify(blogs)

@api.route('/archive', methods=['GET'])
def get_archived_news():
    """API endpoint to get archived news with pagination."""
    page = request.args.get('page', default=1, type=int)  # Get the current page number from request
    per_page = 10  # Number of items per page
    all_news = get_paginated_news(page, per_page)  # Fetch paginated results from DB
    return jsonify(all_news)  # Return the results as JSON