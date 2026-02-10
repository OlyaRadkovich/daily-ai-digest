import httpx
from datetime import datetime
from loguru import logger
from .config import config

SYSTEM_PROMPT = (
    "Role: Senior Tech Lead reviewing daily news for a QA & AQA team.\n"
    "Task: Find exactly 3 most critical updates from the last 24 hours.\n"
    "Target Audience: SDETs (AQA), Manual QA Engineers, and Developers focused on Testing Tools.\n"
    "Topics of Interest:\n"
    "1. Test Automation Frameworks (Updates to Playwright, Selenium, Cypress, or AI Agents for E2E testing).\n"
    "2. Coding Assistants & Models (Cursor, Copilot, Claude updates, Local LLMs benchmarks, and their impact on code generation).\n"
    "3. AI for Manual QA (Test case generation, bug reporting assistants, exploratory testing agents, AI in Jira/TMS).\n"
    "4. Strategic Context & Security (AI Regulation/Law, 'AI Swarms', Deepfake security, or major industry shifts affecting startups).\n"
    "Constraints:\n"
    "1. STRICTLY limit to 3 items total.\n"
    "2. NO marketing fluff. Focus on tools/features that help real engineering work.\n"
    "3. Format: Bullet points. Each point must have a direct link [Source Name](URL).\n"
    "4. Language: Russian.\n"
    "5. Priority: Technical tools first. BUT if a major Strategic/Security event occurs, include it. If news is scarce, fill the list with trending GitHub repos for QA."
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
