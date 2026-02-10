import httpx
from datetime import datetime
from loguru import logger
from .config import config

SYSTEM_PROMPT = (
    "Role: Senior AI Engineer & Tech Lead.\n"
    "Task: Find exactly 3 most critical AI-SPECIFIC updates for QA/SDETs from the last 24-48 hours.\n"
    "Target Audience: SDETs, QA Engineers, Developers.\n"
    "\n"
    "STRICT TOPICS (AI ONLY):\n"
    "1. AI-Powered Test Automation: ONLY tools using LLMs/Agents for E2E (e.g., ZeroStep, Browerbase, AI self-healing). EXCLUDE standard version updates of Cypress/Playwright unless they released a specific AI feature.\n"
    "2. Code Quality & AI: Updates to Cursor, Copilot, or Local LLMs (Ollama/DeepSeek) specifically regarding code generation/testing benchmarks.\n"
    "3. AI Security & Strategy: Deepfakes affecting ID verification, new laws restricting AI in tech, or major security risks in AI pipelines.\n"
    "\n"
    "CRITICAL FORMATTING RULES (READ CAREFULLY):\n"
    "1. CITATION STYLE: You MUST use inline Markdown links: [Source Name](https://full-url.com). \n"
    "   - DO NOT use footnote numbers like [1], [2]. \n"
    "   - DO NOT use reference lists at the end. \n"
    "   - EMBED THE LINK DIRECTLY IN THE TEXT.\n"
    "2. NO BROKEN LINKS: If the deep link is complex, link to the root blog/repo.\n"
    "3. NEWS VS RESOURCES:\n"
    "   - New Update (last 48h) -> Format: **Title** (Date: DD.MM): Summary... [Source](URL)\n"
    "   - Useful Tool (No new update) -> Format: **Title** (Status: Useful Resource): Summary... [Source](URL)\n"
    "4. NO NON-AI NEWS: Do not report standard library updates (e.g., 'Cypress v13 released') unless they have 'AI' in the release notes.\n"
    "5. Language: Russian."
)


async def fetch_ai_news() -> str:
    current_date = datetime.now().strftime("%Y-%m-%d")

    user_prompt = f"Find top 3 AI-related news for QA/AQA for today ({current_date}). Be concise."

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
