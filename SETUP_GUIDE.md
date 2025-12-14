# FinSight - Step-by-Step Setup Guide

Follow these steps to get your FinSight bot up and running.

## Step 1: Prerequisites Check

Make sure you have Python 3.8 or higher installed:

```bash
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

## Step 2: Get Your API Keys

### Step 2.1: Get Telegram Bot Token

1. Open Telegram app (mobile or web)
2. Search for **@BotFather** (official Telegram bot creator)
3. Start a chat with BotFather
4. Send the command: `/newbot`
5. Follow the prompts:
   - Choose a name for your bot (e.g., "FinSight Bot")
   - Choose a username (must end with 'bot', e.g., "finsight_stock_bot")
6. BotFather will give you a token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
7. **Copy and save this token** - you'll need it in Step 4

### Step 2.2: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up for an account (or log in if you already have one)
3. Click on your profile icon (top right) → **View API keys**
4. Click **Create new secret key**
5. Give it a name (e.g., "FinSight Bot")
6. **Copy the key immediately** (it starts with `sk-`) - you won't be able to see it again!
7. Make sure you have credits in your OpenAI account (add payment method if needed)

## Step 3: Install Dependencies

1. Open your terminal/command prompt
2. Navigate to the FinSight project folder:
   ```bash
   cd D:\FinSight
   ```

3. Install all required packages:
   ```bash
   pip install -r requirements.txt
   ```

   If you get permission errors, try:
   ```bash
   pip install --user -r requirements.txt
   ```

## Step 4: Create Environment File

1. In the FinSight folder, create a new file named `.env`
   - On Windows: You can create it in Notepad or any text editor
   - Make sure the file is named exactly `.env` (not `.env.txt`)

2. Open the `.env` file and add your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Replace the placeholders:
   - Replace `your_telegram_bot_token_here` with the token from Step 2.1
   - Replace `your_openai_api_key_here` with the key from Step 2.2

   Example:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   OPENAI_API_KEY=sk-proj-abcdefghijklmnopqrstuvwxyz123456789
   ```

4. **Save the file**

## Step 5: Test Your Setup (Optional but Recommended)

Run the test script to verify everything is configured correctly:

```bash
python test_setup.py
```

This will check:
- ✅ Environment variables are set
- ✅ All packages are installed
- ✅ Scraper can connect to Screener.in
- ✅ OpenAI connection works

If all tests pass, you're ready to run the bot!

## Step 6: Run the Bot

1. In your terminal, make sure you're in the FinSight folder:
   ```bash
   cd D:\FinSight
   ```

2. Start the bot:
   ```bash
   python bot.py
   ```

3. You should see:
   ```
   2024-XX-XX XX:XX:XX,XXX - __main__ - INFO - FinSight bot is starting...
   ```

4. **Keep this terminal window open** - the bot needs to keep running

## Step 7: Use Your Bot

1. Open Telegram app
2. Search for your bot using the username you created (e.g., "finsight_stock_bot")
3. Click **Start** or send `/start`
4. Send a stock name or symbol, for example:
   - `reliance`
   - `tcs`
   - `hdfcbank`
   - `infosys`

5. Wait for the bot to respond with:
   - Stock metrics from Screener.in
   - AI-generated insights
   - Sentiment analysis

## Troubleshooting

### Bot not starting?

**Error: "TELEGRAM_BOT_TOKEN environment variable is required"**
- Make sure `.env` file exists in the project folder
- Check that the file is named `.env` (not `.env.txt`)
- Verify the token is correct (no extra spaces)

**Error: "OPENAI_API_KEY environment variable is required"**
- Check your `.env` file has the OpenAI key
- Make sure there are no quotes around the values in `.env`

**Error: "ModuleNotFoundError"**
- Run: `pip install -r requirements.txt` again
- Make sure you're using the correct Python version

### Bot not responding in Telegram?

- Make sure the bot is running (check terminal window)
- Verify you're messaging the correct bot (check username)
- Make sure you clicked "Start" first

### Stock not found?

- Try using the full company name
- Use the exact symbol as listed on Screener.in
- Check spelling

### Scraping errors?

- Check your internet connection
- Screener.in may have rate limits - wait a few seconds and try again
- Some stocks may not have complete data available

## Stopping the Bot

To stop the bot:
1. Go to the terminal where the bot is running
2. Press `Ctrl + C`
3. The bot will stop

## Running in Background (Advanced)

If you want to run the bot in the background on Windows:

1. Use PowerShell:
   ```powershell
   Start-Process python -ArgumentList "bot.py" -WindowStyle Hidden
   ```

2. Or use a process manager like PM2 for Node.js (with python wrapper)

## Next Steps

- Customize the AI model in `ai_insights.py` (change `gpt-4o-mini` to `gpt-4o` for better quality)
- Add more metrics to scrape in `scraper.py`
- Deploy to a cloud server for 24/7 operation

## Need Help?

Check the main `README.md` file for more details about the project structure and features.

