"""Main Telegram bot module for FinSight."""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import Conflict
from scraper import ScreenerScraper
from ai_insights import AIInsightsGenerator
import config

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class FinSightBot:
    """Main bot class for FinSight."""
    
    def __init__(self):
        """Initialize the bot with scraper and AI generator."""
        self.scraper = ScreenerScraper()
        self.ai_generator = AIInsightsGenerator()
    
    def format_metrics(self, data: dict) -> str:
        """
        Format scraped metrics into a readable message.
        
        Args:
            data: Dictionary of scraped metrics
            
        Returns:
            Formatted string
        """
        if "error" in data:
            return f"❌ {data['error']}"
        
        lines = ["📊 **Stock Metrics**\n"]
        
        # Get company name if available
        company_name = data.get("Company Name", "Stock")
        lines.append(f"**{company_name}**\n")
        
        # Format metrics
        metric_labels = [
            "Current Price", "Market Cap", "P/E", "ROCE", "ROE",
            "Debt/Equity", "High / Low", "Profit Growth", "Sales Growth", "Cash Flows"
        ]
        
        metrics_found = []
        for label in metric_labels:
            value = data.get(label)
            if value:
                metrics_found.append(f"• **{label}**: {value}")
        
        if metrics_found:
            lines.extend(metrics_found)
        else:
            lines.append("⚠️ Limited data available for this stock.")
        
        return "\n".join(lines)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = """
🤖 **Welcome to FinSight!**

I'm your AI-powered stock analysis assistant for **Nifty 50 stocks**.

**How to use:**
Simply send me a stock name or NSE symbol (e.g., "reliance", "tcs", "hdfcbank", "infosys") and I'll provide:
• Real-time metrics from Screener.in
• AI-generated insights
• Sentiment analysis

**Examples:**
• "tcs" or "TCS" → Tata Consultancy Services
• "reliance" → Reliance Industries
• "hdfcbank" → HDFC Bank
• "infosys" → Infosys

**Note:** I support Nifty 50 stocks only. Use company name or NSE symbol.

Let's get started! 📈
"""
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages with stock queries."""
        query = update.message.text.strip()
        
        if not query:
            await update.message.reply_text("Please send a stock name or symbol.")
            return
        
        # Send "processing" message
        processing_msg = await update.message.reply_text("🔍 Fetching stock data...")
        
        try:
            # Scrape data
            await processing_msg.edit_text("📊 Scraping data from Screener.in...")
            data = self.scraper.get_stock_data(query)
            
            if "error" in data:
                error_msg = f"❌ {data['error']}\n\n"
                error_msg += "💡 **Tip:** Use company name or NSE symbol from Nifty 50.\n"
                error_msg += "Examples: 'tcs', 'reliance', 'hdfcbank', 'infosys'"
                await processing_msg.edit_text(error_msg, parse_mode='Markdown')
                return
            
            # Format metrics
            metrics_text = self.format_metrics(data)
            await processing_msg.edit_text(metrics_text, parse_mode='Markdown')
            
            # Generate AI insights
            await update.message.reply_text("🤖 Generating AI insights...")
            
            stock_name = data.get("Company Name", query.upper())
            
            try:
                insights = self.ai_generator.generate_insights(stock_name, data)
                
                if insights:
                    # Check if it's a quota exhausted message (starts with warning emoji)
                    if "⚠️" in insights or "Free Tier Quota" in insights:
                        await update.message.reply_text(insights, parse_mode='Markdown')
                    else:
                        insights_text = f"💡 **AI Insights & Sentiment Analysis**\n\n{insights}"
                        await update.message.reply_text(insights_text, parse_mode='Markdown')
                else:
                    error_msg = "⚠️ Could not generate AI insights.\n\n"
                    error_msg += "**Free Tier Limits:**\n"
                    error_msg += "• 15 requests per minute\n"
                    error_msg += "• 1,500 requests per day\n\n"
                    error_msg += "**Possible reasons:**\n"
                    error_msg += "• Daily quota exhausted (resets at midnight UTC)\n"
                    error_msg += "• Rate limit reached - wait a few minutes\n"
                    error_msg += "• API key issue - verify your Gemini API key\n\n"
                    error_msg += "💡 **Tip:** Free tier resets daily at midnight UTC.\n"
                    error_msg += "Check usage: https://ai.dev/usage"
                    await update.message.reply_text(error_msg, parse_mode='Markdown')
            except Exception as e:
                logger.error(f"Error in AI insights generation: {e}")
                error_msg = "⚠️ Error generating AI insights.\n\n"
                error_msg += "**Free Tier Info:**\n"
                error_msg += "• 15 requests/minute\n"
                error_msg += "• 1,500 requests/day\n\n"
                error_msg += "Please check:\n"
                error_msg += "• Gemini API key is valid\n"
                error_msg += "• Free tier quota not exhausted\n"
                error_msg += "• Your internet connection is stable\n\n"
                error_msg += "Check usage: https://ai.dev/usage"
                await update.message.reply_text(error_msg, parse_mode='Markdown')
        
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await update.message.reply_text(
                "❌ An error occurred while processing your request. Please try again later."
            )
    
    async def post_init(self, application: Application):
        """Post-initialization callback to delete webhook."""
        try:
            await application.bot.delete_webhook(drop_pending_updates=True)
            logger.info("Webhook deleted successfully")
        except Exception as e:
            logger.warning(f"Could not delete webhook: {e}")
    
    def run(self):
        """Start the bot."""
        application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        
        # Set post_init to delete webhook
        application.post_init = self.post_init
        
        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Start the bot with error handling
        logger.info("FinSight bot is starting...")
        try:
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except Conflict as e:
            logger.error(f"Conflict error: {e}")
            logger.error("Another bot instance is running or webhook is still active.")
            logger.error("Please:")
            logger.error("1. Stop any other running bot instances (check all terminal windows)")
            logger.error("2. Wait a few seconds and try again")
            logger.error("3. If problem persists, delete webhook manually")
            raise
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise


def main():
    """Main entry point."""
    bot = FinSightBot()
    bot.run()


if __name__ == "__main__":
    main()

