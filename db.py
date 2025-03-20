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
        published TEXT  
    )
    ''')
    conn.commit()
    conn.close()

def insert_news(blog):
    """ 插入新闻到数据库 """
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()

    # c.execute('''INSERT INTO news (title, link, summary_en, summary_zh, published) 
    #              VALUES (?, ?, ?, ?, ?)''', 
    #           (blog['title'], 
    #            blog['link'], 
    #            blog['summary_en'], 
    #            blog['summary_zh'], #', '.join(blog['categories']), 
    #            blog['published']))
    c.execute('''
        INSERT INTO news (title, link, summary_en, summary_zh, categories, published)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (blog['title'], blog['link'], blog['summary_en'],  blog['summary_zh'], ",".join(blog['categories']), blog['published'])) # 
    conn.commit()
    conn.close()

def get_all_news():
    """ get all news in history (archived) """
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news ORDER BY published DESC')
    all_news = c.fetchall()
    conn.close()

    print(f"Debug: Total number of archived news articles in DB: {len(all_news)}")  # Debugging line
    return all_news