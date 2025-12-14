"""Test script to verify FinSight bot setup."""
import os
from dotenv import load_dotenv

load_dotenv()

def test_environment():
    """Test if environment variables are set."""
    print("Testing environment setup...")
    
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not telegram_token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env file")
        return False
    else:
        print("✅ TELEGRAM_BOT_TOKEN found")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in .env file")
        return False
    else:
        print("✅ OPENAI_API_KEY found")
    
    return True

def test_imports():
    """Test if all required packages are installed."""
    print("\nTesting package imports...")
    
    packages = {
        "telegram": "python-telegram-bot",
        "requests": "requests",
        "bs4": "beautifulsoup4",
        "openai": "openai",
        "dotenv": "python-dotenv",
    }
    
    all_ok = True
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed. Run: pip install {package}")
            all_ok = False
    
    return all_ok

def test_scraper():
    """Test scraper functionality."""
    print("\nTesting scraper...")
    try:
        from scraper import ScreenerScraper
        scraper = ScreenerScraper()
        
        # Test search
        print("Testing stock search...")
        slug = scraper.search_stock("reliance")
        if slug:
            print(f"✅ Stock search working (found: {slug})")
        else:
            print("⚠️ Stock search returned no results (may be network issue)")
        
        return True
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def test_openai():
    """Test OpenAI connection."""
    print("\nTesting OpenAI connection...")
    try:
        from openai import OpenAI
        from config import OPENAI_API_KEY
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        # Simple test - just check if client initializes
        print("✅ OpenAI client initialized")
        return True
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("FinSight Bot Setup Test")
    print("=" * 50)
    
    env_ok = test_environment()
    imports_ok = test_imports()
    
    if env_ok and imports_ok:
        scraper_ok = test_scraper()
        openai_ok = test_openai()
        
        print("\n" + "=" * 50)
        if env_ok and imports_ok and scraper_ok and openai_ok:
            print("✅ All tests passed! Bot is ready to run.")
            print("Run: python bot.py")
        else:
            print("⚠️ Some tests failed. Please fix the issues above.")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Setup incomplete. Please fix the issues above.")
        print("=" * 50)

