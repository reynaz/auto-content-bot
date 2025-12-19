"""
Configuration module for Auto-Content-Bot.
Handles environment variables and demo/production mode switching.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration management."""
    
    # Demo Mode - if True, uses mock data instead of real APIs
    DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # WordPress
    WP_URL = os.getenv("WP_URL", "")
    WP_USER = os.getenv("WP_USER", "")
    WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "")
    
    # Email/SMTP
    SMTP_EMAIL = os.getenv("SMTP_EMAIL", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")
    
    # LinkedIn
    LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    
    # Twitter
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
    
    @classmethod
    def is_openai_configured(cls) -> bool:
        """Check if OpenAI API is properly configured."""
        return bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY.startswith("sk-"))
    
    @classmethod
    def is_wordpress_configured(cls) -> bool:
        """Check if WordPress API is properly configured."""
        return all([cls.WP_URL, cls.WP_USER, cls.WP_APP_PASSWORD])
    
    @classmethod
    def is_smtp_configured(cls) -> bool:
        """Check if SMTP email is properly configured."""
        return all([cls.SMTP_EMAIL, cls.SMTP_PASSWORD])
    
    @classmethod
    def is_linkedin_configured(cls) -> bool:
        """Check if LinkedIn API is properly configured."""
        return bool(cls.LINKEDIN_ACCESS_TOKEN)
    
    @classmethod
    def is_twitter_configured(cls) -> bool:
        """Check if Twitter API is properly configured."""
        return all([
            cls.TWITTER_API_KEY, 
            cls.TWITTER_API_SECRET,
            cls.TWITTER_ACCESS_TOKEN,
            cls.TWITTER_ACCESS_TOKEN_SECRET
        ])
    
    @classmethod
    def get_status(cls) -> dict:
        """Return status of all integrations."""
        return {
            "demo_mode": cls.DEMO_MODE,
            "openai": cls.is_openai_configured(),
            "wordpress": cls.is_wordpress_configured(),
            "smtp": cls.is_smtp_configured(),
            "linkedin": cls.is_linkedin_configured(),
            "twitter": cls.is_twitter_configured()
        }
