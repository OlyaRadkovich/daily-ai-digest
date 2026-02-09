import httpx
from loguru import logger
from .config import config

SYSTEM_PROMPT = (
    "You are a professional Technical Digest Assistant. "
    "Topic: Applied AI in Software Development and Quality Assurance. "
    "Language: Russian. "
    "Instructions: Provide a concise daily digest. Avoid marketing hype. "
    "Focus on practical applications (Tools for Dev/QA, LLM updates, Playwright/Selenium, GitHub repos). "
    "Format: Clean bulleted list, one-sentence summary per item, direct links included."
)

USER_PROMPT = "Provide a daily digest on Applied AI in Software Development and QA for today."


async def fetch_ai_news() -> str:
    headers = {
        "Authorization": f"Bearer {config.openrouter_api_key.get_secret_value()}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": config.model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ],
        "temperature": 0.2
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error requesting OpenRouter: {e}")
            raise