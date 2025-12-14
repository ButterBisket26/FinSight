"""Helper script to delete Telegram bot webhook."""
import asyncio
import sys
from telegram import Bot
import config

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

async def delete_webhook():
    """Delete webhook for the bot."""
    try:
        bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        result = await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook deleted successfully!")
        await bot.close()
    except Exception as e:
        print(f"Error deleting webhook: {e}")

if __name__ == "__main__":
    asyncio.run(delete_webhook())

