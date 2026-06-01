"""Groq integration for generating stock insights and sentiment analysis."""
from groq import Groq
from typing import Dict, Optional
import config


class AIInsightsGenerator:
    """Generate AI-powered insights using Groq API."""

    def __init__(self):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = "llama-3.1-8b-instant"  # Free, fast model on Groq

    def format_data_for_prompt(self, data: Dict[str, Optional[str]]) -> str:
        formatted_lines = []
        for key, value in data.items():
            if key not in ["error", "slug"] and value:
                formatted_lines.append(f"{key}: {value}")
        return "\n".join(formatted_lines)

    def generate_insights(self, stock_name: str, data: Dict[str, Optional[str]]) -> Optional[str]:
        if "error" in data:
            return None

        formatted_data = self.format_data_for_prompt(data)

        prompt = f"""You are an expert financial analyst specializing in Indian stock market analysis.
Analyze the following data for {stock_name} and provide:

1. Bullish insights (2-3 key positive points)
2. Bearish risks (2-3 key concerns)
3. Overall sentiment (Positive/Neutral/Negative)
4. Actionable summary in 4 lines

Data:
{formatted_data}

Format your response clearly with headings for each section."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            error_msg = str(e)
            print(f"Error generating insights: {error_msg}")

            if "429" in error_msg or "rate_limit" in error_msg.lower():
                return (
                    "⚠️ *Rate limit reached.*\n\n"
                    "Groq free tier: 30 requests/minute, 14,400 requests/day.\n"
                    "Please wait a moment and try again."
                )
            elif "401" in error_msg or "invalid" in error_msg.lower():
                return "⚠️ *Invalid Groq API key.* Please check your `.env` file."
            else:
                return None
