import sqlite3
import datetime


def create_db():
    """ 创建数据库和新闻表 """
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        summary_en TEXT,
        summary_zh TEXT,
        categories TEXT,
        published TEXT,
        likes INTEGER DEFAULT 0,  -- Add a likes column
        dislikes INTEGER DEFAULT 0  -- Add a dislikes column
    )
    ''')
    conn.commit()
    conn.close()

def insert_news(blog):
    """ 插入新闻到数据库 """
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    # print(f"Debug: Inserting blog into DB: {blog}")  # Debugging line

    c.execute('''
        INSERT INTO news (title, link, summary_en, summary_zh, categories, published)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (blog['title'], blog['link'], blog['summary_en'],  blog['summary_zh'], ",".join(blog['categories']), blog['published'])) # 
    conn.commit()
    conn.close()
    print("Debug: Insert completed.")  # Debugging line


def get_all_news():
    """Get all news in history (archived)"""
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    
    print("Debug: Querying all news...")  # Debugging line for querying
    c.execute('SELECT * FROM news ORDER BY published DESC')
    all_news = c.fetchall()
    conn.close()
    # Check if any news articles were found
    if not all_news:
        print("Debug: No news articles found in DB.")
    else:
        print(f"Debug: Total number of archived news articles in DB: {len(all_news)}")
    return all_news

# def get_all_news():
#     """ get all news in history (archived) """
#     conn = sqlite3.connect('ai_news.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM news ORDER BY published DESC')
#     all_news = c.fetchall()
#     conn.close()

#     print(f"Debug: Total number of archived news articles in DB: {len(all_news)}")  # Debugging line
#     return all_news

def update_news_feedback(news_id, feedback_type):
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    column = 'likes' if feedback_type == 'like' else 'dislikes'
    c.execute(f"UPDATE news SET {column} = {column} + 1 WHERE id = ?", (news_id,))
    conn.commit()
    conn.close()

def get_paginated_news(page, per_page):
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    offset = (page - 1) * per_page
    c.execute('SELECT * FROM news ORDER BY published DESC LIMIT ? OFFSET ?', (per_page, offset))
    all_news = c.fetchall()
    conn.close()
    return all_news