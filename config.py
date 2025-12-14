"""Configuration management for FinSight bot."""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate required environment variables
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is required")

