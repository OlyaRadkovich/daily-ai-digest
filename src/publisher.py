import httpx
import re
from loguru import logger
from .config import config
from datetime import datetime


def format_for_google_chat(text: str) -> str:
    """
    Converts standard Markdown to a Google Chat compatible format.
    """

    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<\2|\1>', text)
    text = text.replace("**", "*")
    header = f"🚀 *Daily AI Digest – {datetime.now().strftime('%d.%m.%Y')}*\n\n"

    return header + text


async def send_to_google_chat(text: str):
    """
    Sends formatted text to Google Chat via Webhook.
    """
    formatted_text = format_for_google_chat(text)

    payload = {"text": formatted_text}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                config.google_chat_webhook_url.get_secret_value(),
                json=payload
            )
            response.raise_for_status()
            logger.info("Digest successfully sent to Google Chat.")
        except Exception as e:
            logger.error(f"Error sending to Google Chat: {e}")
            raise
