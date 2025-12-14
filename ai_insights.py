"""Google Gemini integration for generating stock insights and sentiment analysis."""
import google.generativeai as genai
from typing import Dict, Optional
import config


class AIInsightsGenerator:
    """Generate AI-powered insights using Google Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client."""
        # Configure Gemini API
        genai.configure(api_key=config.GEMINI_API_KEY)
        
        # Initialize the model (using free tier: gemini-2.0-flash-lite)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
    
    def format_data_for_prompt(self, data: Dict[str, Optional[str]]) -> str:
        """
        Format scraped data into a readable string for the prompt.
        
        Args:
            data: Dictionary of scraped stock metrics
            
        Returns:
            Formatted string representation of the data
        """
        formatted_lines = []
        for key, value in data.items():
            if key not in ["error", "slug"] and value:
                formatted_lines.append(f"{key}: {value}")
        return "\n".join(formatted_lines)
    
    def generate_insights(self, stock_name: str, data: Dict[str, Optional[str]]) -> Optional[str]:
        """
        Generate AI insights and sentiment analysis for stock data.
        
        Args:
            stock_name: Name of the stock
            data: Scraped stock metrics
            
        Returns:
            Formatted insights string or None on error
        """
        if "error" in data:
            return None
        
        formatted_data = self.format_data_for_prompt(data)
        
        prompt = f"""You are a financial analyst. Analyze the following scraped data for {stock_name}.
Provide:

1. Bullish insights (2-3 key positive points)
2. Bearish risks (2-3 key concerns)
3. Overall sentiment (Positive/Neutral/Negative)
4. Actionable summary in 4 lines

Data:
{formatted_data}

Format your response clearly with headings for each section."""

        import time
        
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                # Create the full prompt with system instructions
                full_prompt = f"""You are an expert financial analyst specializing in Indian stock market analysis. Provide clear, concise, and actionable insights.

{prompt}"""

                # Generate content using Gemini
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=800,
                    )
                )
                
                return response.text.strip()
                
            except Exception as e:
                error_msg = str(e)
                print(f"Error generating AI insights (attempt {attempt + 1}/{max_retries}): {error_msg}")
                
                # Check for rate limit errors (429) - retry with delay
                if "429" in error_msg or "quota" in error_msg.lower() or "rate_limit" in error_msg.lower():
                    # Check if it's free tier quota exhausted
                    if "free_tier" in error_msg.lower() or ("limit: 0" in error_msg.lower() and "429" in error_msg):
                        print("Free tier daily quota exhausted.")
                        print("Free tier limits: 15 requests/minute, 1,500 requests/day.")
                        print("Quota resets at midnight UTC. Check usage: https://ai.dev/usage")
                        # Return a helpful message instead of None so bot can show it
                        return "⚠️ **Free Tier Quota Exhausted**\n\n" \
                               "Your daily free tier quota (1,500 requests/day) has been exhausted.\n\n" \
                               "**What to do:**\n" \
                               "• Wait until midnight UTC for quota reset\n" \
                               "• Check your usage: https://ai.dev/usage\n" \
                               "• Consider upgrading to a paid plan for higher limits\n\n" \
                               "The stock metrics above are still available!"
                    
                    if attempt < max_retries - 1:
                        # Extract retry delay from error if available
                        if "retry in" in error_msg.lower():
                            try:
                                import re
                                delay_match = re.search(r'retry in ([\d.]+)s', error_msg.lower())
                                if delay_match:
                                    retry_delay = int(float(delay_match.group(1))) + 1
                            except:
                                pass
                        
                        print(f"Rate limit hit. Retrying in {retry_delay} seconds...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        print("Gemini API rate limit exceeded after retries. Please wait and try again later.")
                        return None
                elif "invalid" in error_msg.lower() or "401" in error_msg or "403" in error_msg:
                    print("Gemini API key is invalid. Please check your API key in .env file.")
                    return None
                elif "safety" in error_msg.lower():
                    print("Content was blocked by safety filters. Try rephrasing the query.")
                    return None
                else:
                    # For other errors, don't retry
                    print(f"Unexpected error: {error_msg}")
                    return None
        
        return None

