import asyncio
from loguru import logger
from src.client_ai import fetch_ai_news
from src.publisher import send_to_google_chat


async def main():
    logger.info("Starting news fetching process...")

    try:
        raw_news = await fetch_ai_news()
        logger.info("News fetched successfully.")

        await send_to_google_chat(raw_news)

    except Exception as e:
        logger.critical(f"Script execution failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
