import os
from flask import Flask#
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from fetch_data import fetch_all_ai_blogs_with_categories
from db import create_db, insert_news
# from email_sender import send_email, generate_email_body
from blueprints.api import api
from blueprints.views import views
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)  # Load development config

# Ensure the database and tables are created
if not os.path.exists('ai_news.db'): # Only run this in development or if needed
    create_db()  # Create the database if it doesn't already exist
    print("✅ Database initialized successfully!")

@app.cli.command("init-db")
def init_db():
    """Flask CLI command to initialize the database."""
    create_db()
    

# Function to fetch and store news
def fetch_and_store_news():
    """Fetch AI news and store in the database."""
    print(f"➡️➡️ Fetching news at {datetime.now()}")
    blogs = fetch_all_ai_blogs_with_categories()
    # Clear the current database or overwrite if needed
    # For simplicity, assuming each news item is inserted fresh each day
    # for news in news_data:
    #     # insert_news(news["title"], news["link"], news["summary"], news["categories"], news["published"])
    #     insert_news(news)
    for blog in blogs:        
        # insert to database
        insert_news(blog)
    print("✅ News fetched and stored.")

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_news, 'interval', hours=12)  # Fetch news every 24 hours

# Start the scheduler
scheduler.start()

# Register the Blueprints
app.register_blueprint(api)
app.register_blueprint(views)


if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/')
# def index():
#     # 获取AI热点新闻
#     blogs = fetch_all_ai_blogs()
#     return render_template('index.html', blogs=blogs)

# @app.route('/api/blogs', methods=['GET'])
# def get_blogs():
#     # 返回AI热点新闻的JSON数据
#     blogs = fetch_all_ai_blogs()
#     return jsonify(blogs)


# @app.route('/archive')
# def archive():
#     all_news = get_all_news()
#     return render_template('archive.html', news=all_news)
