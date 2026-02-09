import httpx
from datetime import datetime
from loguru import logger
from .config import config

SYSTEM_PROMPT = (
    "Role: Senior Tech Lead reviewing daily news for a Dev & QA team.\n"
    "Task: Find exactly 3 most critical updates from the last 24 hours.\n"
    "Target Audience: SDETs (AQA), Manual QA Engineers, and Developers focused on Testing Tools.\n"
    "Topics of Interest:\n"
    "1. AI for Automation (Playwright/Selenium, self-healing tests, AI agents).\n"
    "2. AI for Manual QA (Test case generation from requirements, bug reporting assistants, exploratory testing agents, AI in Jira/TMS).\n"
    "3. Coding AI Tools (Updates to Cursor, Copilot, or local LLMs relevant for writing tests).\n"
    "Constraints:\n"
    "1. STRICTLY limit to 3 items.\n"
    "2. NO marketing fluff. Focus on tools/features that help real engineering work.\n"
    "3. Format: Bullet points. Each point must have a direct link [Source Name](URL).\n"
    "4. Language: Russian.\n"
    "5. If no major news, find 1 useful GitHub repo or tool update."
)


async def fetch_ai_news() -> str:
    current_date = datetime.now().strftime("%Y-%m-%d")

    user_prompt = f"Find top 3 technical AI news for QA/AQA for today ({current_date}). Be concise."

    headers = {
        "Authorization": f"Bearer {config.openrouter_api_key.get_secret_value()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/daily-ai-digest",
    }

    payload = {
        "model": config.model_name,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.1,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
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
