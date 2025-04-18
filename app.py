import os
from flask import Flask
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from fetch_data import fetch_all_ai_blogs
from db import create_db, insert_news
from blueprints.api import api
from blueprints.views import views
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)  # Load development config
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Use simple in-memory cache

# Ensure the database and tables are created
if not os.path.exists('ai_news.db'): # Only run this in development or if needed
    create_db()  # Create the database if it doesn't already exist
    print("✅ Database created successfully!")

@app.cli.command("init-db")
def init_db():
    """Flask CLI command to initialize the database."""
    create_db()   
    print("✅ Database initialized successfully!") 

# Function to fetch and store news
@cache.cached(timeout=86400)  # Cache for 24 hours
def fetch_and_store_news():
    """Fetch AI news and store in the database."""
    print(f"➡️➡️ Fetching news at {datetime.now()}... 2")
    blogs = fetch_all_ai_blogs()
    # Clear the current database or overwrite if needed
    # For simplicity, assuming each news item is inserted fresh each day
    # for news in news_data:
    #     # insert_news(news["title"], news["link"], news["summary"], news["categories"], news["published"])
    #     insert_news(news)
    for blog in blogs:        
        # insert to database
        insert_news(blog)
    print("✅ News fetched and stored. 2")

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_news, 'interval', hours=24)  # Fetch news every 24 hours

# Start the scheduler
scheduler.start()

# Register the Blueprints
# app.register_blueprint(api)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(views)



if __name__ == '__main__':
    app.run(debug=True)
