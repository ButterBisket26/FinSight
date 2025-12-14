# FinSight - AI-Powered Stock Analysis Telegram Bot

FinSight is a production-ready Telegram bot that provides AI-generated insights and sentiment analysis on Indian stocks by scraping real-time data from Screener.in.

## Features

- 📊 **Real-time Stock Metrics**: Scrapes comprehensive financial data from Screener.in
- 🤖 **AI-Powered Insights**: Uses OpenAI GPT-4o-mini to generate bullish/bearish insights
- 📈 **Sentiment Analysis**: Provides overall sentiment (Positive/Neutral/Negative)
- 💡 **Actionable Summaries**: 4-line actionable investment summaries
- 🔍 **Easy to Use**: Simply send a stock name or symbol to get instant analysis

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key (from [OpenAI Platform](https://platform.openai.com))

## Installation

1. **Clone or download this repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Getting API Keys

### Telegram Bot Token
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided

### OpenAI API Key
1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

## Usage

1. **Run the bot**
   ```bash
   python bot.py
   ```

2. **Start using the bot**
   - Open Telegram and search for your bot
   - Send `/start` to see the welcome message
   - Send any stock name or symbol (e.g., "reliance", "tcs", "hdfcbank")
   - Receive instant analysis with metrics, insights, and sentiment

## Example Usage

```
User: reliance

Bot Response:
📊 Stock Metrics
Reliance Industries Ltd
• Current Price: ₹2,450.50
• Market Cap: ₹16,50,000 Cr
• P/E: 28.5
• ROCE: 12.5%
• ROE: 10.2%
...

💡 AI Insights & Sentiment Analysis
Bullish insights:
- Strong revenue growth in retail and digital segments
- Diversified business portfolio reducing risk

Bearish risks:
- High debt levels
- Regulatory concerns in telecom sector

Overall sentiment: Positive

Actionable summary:
[4-line investment summary]
```

## Project Structure

```
FinSight/
├── bot.py              # Main Telegram bot module
├── scraper.py          # Screener.in scraping module
├── ai_insights.py      # OpenAI integration for insights
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (create this)
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Scraped Metrics

The bot extracts the following metrics from Screener.in:
- Market Cap
- P/E (Price-to-Earnings)
- ROCE (Return on Capital Employed)
- ROE (Return on Equity)
- Debt
- Current Price
- High / Low
- Profit Growth
- Sales Growth
- Cash Flows

## AI Analysis

The AI analysis includes:
1. **Bullish Insights**: 2-3 key positive points
2. **Bearish Risks**: 2-3 key concerns
3. **Overall Sentiment**: Positive/Neutral/Negative
4. **Actionable Summary**: 4-line investment summary

## Configuration

You can modify the AI model in `ai_insights.py`:
- Default: `gpt-4o-mini` (cost-effective)
- Alternative: `gpt-4o` (better quality, higher cost)

## Error Handling

The bot includes comprehensive error handling for:
- Invalid stock names
- Network errors
- API failures
- Scraping issues

## Notes

- The bot uses proper headers to avoid scraping blocks
- All API calls include timeout handling
- The bot is designed to be production-ready with proper logging

## Troubleshooting

**Bot not responding:**
- Check if `.env` file exists and contains valid tokens
- Verify bot token is correct
- Ensure OpenAI API key is valid and has credits

**Stock not found:**
- Try using the full company name
- Use the exact symbol as listed on Screener.in
- Check spelling

**Scraping errors:**
- Screener.in may have rate limits
- Try again after a few seconds
- Check your internet connection

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This bot is for informational purposes only. It does not provide financial advice. Always consult with a qualified financial advisor before making investment decisions.

