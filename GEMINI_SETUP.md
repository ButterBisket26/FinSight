# Gemini API Setup Guide

## Getting Your Gemini API Key

1. **Go to Google AI Studio**
   - Visit: https://aistudio.google.com/apikey

2. **Sign in with your Google account**

3. **Create API Key**
   - Click "Create API Key"
   - Select "Create API key in new project" or choose an existing project
   - Copy the API key (starts with `AIza...`)

4. **Update your .env file**
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Free Tier Limits

- **Free tier**: 15 requests per minute (RPM)
- **Free tier**: 1,500 requests per day (RPD)
- No credit card required for free tier!

## Model Options

The bot uses `gemini-1.5-flash` by default (fast and free). You can change it in `ai_insights.py`:

```python
self.model = genai.GenerativeModel('gemini-1.5-flash')  # Fast, free
# or
self.model = genai.GenerativeModel('gemini-1.5-pro')    # Better quality, may have costs
```

## Testing Your API Key

```powershell
python -c "import google.generativeai as genai; import os; from dotenv import load_dotenv; load_dotenv(); genai.configure(api_key=os.getenv('GEMINI_API_KEY')); model = genai.GenerativeModel('gemini-1.5-flash'); response = model.generate_content('Hello'); print('API Key works!' if response.text else 'Failed')"
```

## Troubleshooting

**Error: "API key not found"**
- Make sure `.env` file has `GEMINI_API_KEY=your_key`
- Restart the bot after updating `.env`

**Error: "Quota exceeded"**
- Free tier: 15 requests/minute, 1,500/day
- Wait a few minutes and try again
- Consider upgrading if you need more

**Error: "Invalid API key"**
- Verify your key at https://aistudio.google.com/apikey
- Make sure there are no extra spaces in `.env` file

