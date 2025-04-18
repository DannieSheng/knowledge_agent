import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# api_key = os.getenv('API_KEY')  # Get the value of API_KEY
# base_url = os.getenv('BASE_URL')  # Get the value of BASE_URL
# print(api_key, base_url)


class Config:
    """Base configuration."""
    API_KEY = os.getenv('API_KEY') 
    DEBUG = os.getenv("DEBUG", "True") == "True"  # Convert string to bool
    BASE_URL = os.getenv('BASE_URL')  # Get the value of BASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuration for development."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"

class ProductionConfig(Config):
    """Configuration for production."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # Use database from .env

class EmailConfig:
    CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    PROJECT_ID = "ai-news-agent-456908"
    MAIL_USER = os.getenv("GOOGLE_MAIL_USER")
    MAIL_PWD = os.getenv("GOOGLE_MAIL_PWD")