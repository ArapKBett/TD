import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL_ID")
    
    # Discord
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    DISCORD_CHANNEL = int(os.getenv("DISCORD_CHANNEL_ID"))
    
    # APIs
    API_KEYS = {
        "cve": os.getenv("CVE_API_KEY"),
        "github": os.getenv("GITHUB_TOKEN")
    }
    
    # Security
    ALLOWED_USERS = [int(id) for id in os.getenv("ALLOWED_USERS").split(",")]
    RATE_LIMIT = 5  # Requests per minute
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "security_data.db")
