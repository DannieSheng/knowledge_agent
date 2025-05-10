from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .email_utils import send_email_smtp, generate_email_content # send_email, authenticate_gmail, 
from fetch_data import fetch_all_ai_blogs 



## Gmail API
# def send_daily_email_task():
#     creds = authenticate_gmail()
#     subject = "AI News Summary for Today"
#     body = "Here is your daily AI news summary..."  # You can dynamically generate this content
#     recipient_email = "recipient_email@gmail.com"
#     send_email(subject, body, recipient_email, creds)

# # Setup scheduler to send daily email at 8 AM
# scheduler = BackgroundScheduler()
# scheduler.add_job(send_daily_email_task, 'cron', hour=8, minute=0)
# scheduler.start()


## SMTP
def send_daily_email_task():
    """Task to send a daily email with the latest AI news."""

    # Fetch the latest AI news
    news = fetch_all_ai_blogs()  # You can replace this with your news-fetching function

    # Generate the email body from the fetched news
    email_body = generate_email_content(news)
    
    # Set the email subject
    subject = "AI News Summary for Today"
    
    # Recipient email address
    recipients = ["hudanyun.sheng@outlook.com", "dsheng3@its.jnj.com"] 

    # Send the email using the send_email function
    for recipient in recipients:
        send_email_smtp(sender="hudanyun.sheng@gmail.com", recipient=recipient, subject=subject, body=email_body)
    
    print("✅ Email sent successfully.")
# Set up the scheduler to send the email every day at 8 AM
# scheduler = BackgroundScheduler()
# scheduler.add_job(send_daily_email_task, 'cron', hour=8, minute=0)
# scheduler.start()

# Run the email-sending task immediately for testing
send_daily_email_task()

# Set up the scheduler to send the email every day at 8 AM
scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_email_task, 'cron', hour=8, minute=0)
scheduler.start()

# Keep the script running so the scheduler continues to function
try:
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()