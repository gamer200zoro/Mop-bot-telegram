import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "") # For SQLAlchemy

    # Ensure essential settings are provided
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")
    if not SUPABASE_URL:
        raise ValueError("SUPABASE_URL is not set")
    if not SUPABASE_KEY:
        raise ValueError("SUPABASE_KEY is not set")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set")

settings = Settings()
