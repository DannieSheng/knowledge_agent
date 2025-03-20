import os
from dotenv import load_dotenv
import feedparser
from openai import OpenAI
from db import insert_news, create_db
# from email_sender import send_email, generate_email_body
from config import DevelopmentConfig  # Import config directly

# Load API key and base URL from config
API_KEY = DevelopmentConfig.API_KEY
BASE_URL = DevelopmentConfig.BASE_URL

# load_dotenv()
# api_key = os.getenv('API_KEY')  # Get the value of API_KEY
# base_url = os.getenv('BASE_URL')  # Get the value of BASE_URL
# print(api_key, base_url)
# # Create database
# create_db()


def summarize_text_multiple_languages(text):
    """ 使用OpenAI GPT生成文本摘要 """
    client = OpenAI(api_key=API_KEY, 
                base_url=BASE_URL)
    response_en = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please summarize the following text in English:\n{text}"}
        ]
    )
    response_zh = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"请用中文总结以下文本：\n{text}"}
        ]
    )
    summary_en, summary_zh = response_en.choices[0].message.content, response_zh.choices[0].message.content
    return summary_en, summary_zh


def filter_relevant_news(entries):
    """ 过滤掉无关的新闻 """
    relevant_news = []
    for entry in entries:
        # 以关键词过滤新闻，可以根据AI领域或关键字调整
        if "AI" in entry.title or "Artificial Intelligence" in entry.title:
            relevant_news.append(entry)
    return relevant_news


def categorize_blog(blog):
    """ 基于简单的关键词来分类新闻 """
    categories = []
    
    if "machine learning" in blog['title'].lower() or "deep learning" in blog['summary_en'].lower():
        categories.append("Machine Learning")
    if "computer vision" in blog['title'].lower() or "vision" in blog['summary_en'].lower():
        categories.append("Computer Vision")
    if "ethics" in blog['title'].lower() or "AI ethics" in blog['summary_en'].lower():
        categories.append("AI Ethics")
    if not categories:
        categories.append("General AI")
    
    return categories


def fetch_blogs(rss_url):
    feed = feedparser.parse(rss_url)
    # filter
    relevant_entries = filter_relevant_news(feed.entries)
    blogs = []
    for entry in relevant_entries:
        summary_en, summary_zh = summarize_text_multiple_languages(entry.summary)  # summarize
        
        blog = {
            "title": entry.title,
            "link": entry.link,
            "summary_en": summary_en,
            "summary_zh": summary_zh,
            # "categories": categories,
            "published": entry.published
            
        }
        blog['categories'] = categorize_blog(blog) # categorize
        blogs.append(blog)
    return blogs

# def fetch_medium_ai_blogs():
#     rss_url = "https://medium.com/feed/tag/artificial-intelligence"
#     feed = feedparser.parse(rss_url)
    
#     # 过滤新闻
#     relevant_entries = filter_relevant_news(feed.entries)
    
#     blogs = []
#     for entry in relevant_entries:
#         summary_en, summary_zh = summarize_text_multiple_languages(entry.summary)  # 对新闻进行摘要
#         blog = {
#             "title": entry.title,
#             "link": entry.link,
#             "summary_en": summary_en,
#             "summary_zh": summary_zh,
#             "published": entry.published
#         }
#         blogs.append(blog)
    
#     return blogs


# def fetch_tds_ai_blogs():
#     rss_url = "https://towardsdatascience.com/feed"
#     feed = feedparser.parse(rss_url)
    
#     # 过滤新闻
#     relevant_entries = filter_relevant_news(feed.entries)
    
#     blogs = []
#     for entry in relevant_entries:
#         summary_en, summary_zh = summarize_text_multiple_languages(entry.summary)  # 对新闻进行摘要
#         blog = {
#             "title": entry.title,
#             "link": entry.link,
#             "summary_en": summary_en,
#             "summary_zh": summary_zh,
#             "published": entry.published
#         }
#         blogs.append(blog)
    
#     return blogs


def fetch_all_ai_blogs(
        urls=[
            "https://medium.com/feed/tag/artificial-intelligence",
            "https://towardsdatascience.com/feed",
        ]
):
    # medium_blogs = fetch_medium_ai_blogs()
    # tds_blogs = fetch_tds_ai_blogs()
    
    # # 合并两个来源的文章
    # all_blogs = medium_blogs + tds_blogs
    all_blogs = []
    for url in urls:
        blogs = fetch_blogs(url)
        all_blogs += blogs
        
    return all_blogs


def fetch_all_ai_blogs_with_categories():
    all_blogs = fetch_all_ai_blogs()
    print(f"Total number of fetched blogs: {len(all_blogs)}")  # Debugging line    
    return all_blogs


# def send_daily_email():
#     blogs = fetch_all_ai_blogs_with_categories()
#     email_body = generate_email_body(blogs)
#     send_email("Daily AI News Digest", email_body, "hudanyun.sheng@outlook.com")

# send_daily_email()