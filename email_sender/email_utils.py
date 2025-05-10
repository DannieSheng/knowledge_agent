import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import smtplib
from email.mime.text import MIMEText
import pickle as pkl
from config import EmailConfig


#### Gmail API method ####
# SCOPES define the access we need to Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail(dir_credentials="../credentials"):
    """Authenticate with Gmail API using environment variables for OAuth credentials."""
    creds = None

    # Check if token.pickle exists and contains valid credentials
    path_credentials = os.path.join(dir_credentials, 'gm_token.pkl')
    if os.path.exists(path_credentials):
        with open(path_credentials, 'rb') as token:
            creds = pkl.load(token)
    # If there are no valid credentials, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh expired credentials
        else:
            # Use environment variables for client ID and secret
            client_id = EmailConfig.CLIENT_ID
            client_secret = EmailConfig.CLIENT_SECRET
            project_id = EmailConfig.PROJECT_ID

            if not client_id or not client_secret:
                raise ValueError("Client ID and Client Secret must be set in environment variables.")

            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "project_id": project_id,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["http://localhost"]  # Set the redirect URI as required
                }
            }

            # Create the flow using the environment credentials
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=8080)  # This will open the browser for authentication

        # Save credentials for the next run
        print(f"save to {path_credentials}")
        with open(path_credentials, 'wb') as token:
            pkl.dump(creds, token)

    return creds

def send_email(subject, body, to_email):
    """Send email using Gmail API"""
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    message = create_message('me', to_email, subject, body)
    send_message(service, 'me', message)

def create_message(sender, to, subject, body):
    """Create message for email"""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(body, 'plain')
    message.attach(msg)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def send_message(service, sender, message):
    """Send email using the Gmail API"""
    service.users().messages().send(userId=sender, body=message).execute()


#### SMTP method ####
def generate_email_content(news):
    """Generate dynamic email content with news summaries."""
    content = "Here are today's AI news updates:\n\n"
    
    # Iterate through the fetched news articles and create a summary for the email
    for article in news:
        content += f"Title: {article['title']}\n"
        content += f"Summary: {article['summary_en']}\n"
        content += f"摘要: {article['summary_zh']}\n"
        content += f"Link: {article['link']}\n\n"
    
    return content

def send_email_smtp(sender, recipient, subject, body):
    mail_host = "smtp.gmail.com"
    sender = EmailConfig.MAIL_USER
    mail_pwd = EmailConfig.MAIL_PWD
    smtpObj = smtplib.SMTP_SSL(host=mail_host, port=smtplib.SMTP_SSL_PORT)
    smtpObj.login(sender, mail_pwd)

    _subtype="plain"
    msg = MIMEText(body, _subtype, 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        smtpObj.sendmail(sender, recipient, msg.as_string())
        print("✅ Email sent successfully via SMTP!")
    except Exception as e:
        print(f"Failed to send email: {e}")
