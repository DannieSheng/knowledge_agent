import schedule
import time
from fetch_data import *

def job():
    ai_medium = fetch_medium_ai_blogs()
    # 处理数据并发送给你（可以调用发送邮件功能）
    print(ai_medium)
    ai_tds = fetch_tds_ai_blogs()
    # 处理数据并发送给你（可以调用发送邮件功能）
    print(ai_tds)

# 每天8点执行一次
schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)