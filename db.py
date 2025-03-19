import sqlite3

def create_db():
    """ 创建数据库和新闻表 """
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (id INTEGER PRIMARY KEY,
                  title TEXT,
                  link TEXT,
                  summary_en TEXT,
                  summary_zh TEXT,
                  published TEXT)''')
    conn.commit()
    conn.close()

def insert_news(blog):
    """ 插入新闻到数据库 """
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    c.execute('''INSERT INTO news (title, link, summary_en, summary_zh, published) 
                 VALUES (?, ?, ?, ?, ?)''', 
              (blog['title'], blog['link'], blog['summary_en'], 
               blog['summary_zh'], #', '.join(blog['categories']), 
               blog['published']))
    conn.commit()
    conn.close()

def get_all_news():
    """ 获取所有历史新闻 """
    conn = sqlite3.connect('ai_news.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news ORDER BY published DESC')
    all_news = c.fetchall()
    conn.close()
    return all_news