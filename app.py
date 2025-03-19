from flask import Flask, render_template, jsonify, Blueprint, render_template
from fetch_data import fetch_all_ai_blogs
from db import create_db
# from email_sender import send_email, generate_email_body
from blueprints.api import api
from blueprints.views import views
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)  # Load development config

# Register the Blueprints
app.register_blueprint(api)
app.register_blueprint(views)

@app.cli.command("init-db")
def init_db():
    """Flask CLI command to initialize the database."""
    create_db()
    print("✅ Database initialized successfully!")

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


if __name__ == '__main__':
    app.run(debug=True)