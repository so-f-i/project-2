import aiohttp
import asyncio
import json
import logging
from storage.advice_cache import load_cache, get_cached_advice, update_cache

API_URL = "https://api.adviceslip.com/advice"
cache = load_cache()

logging.basicConfig(
    filename="logs/bot.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def fetch_advice_from_api():
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(API_URL) as response:
                text = await response.text()
                data = json.loads(text)
                advice = data['slip']['advice']
                logging.info("Successfully fetched advice from API")
                return advice
    except asyncio.TimeoutError:
        logging.warning("Timeout while fetching advice from API")
        return 'Sorry, I waited too long for the stars to align 💫'
    except Exception as e:
        logging.exception("API error:")
        return 'Something went wrong while reaching out to the cosmos 😞'

async def get_advice(user_id):
    advice = get_cached_advice(user_id, cache)
    if advice:
        logging.info(f"Advice found in cache for user {user_id}")
        return advice

    advice = await fetch_advice_from_api()
    if advice:
        update_cache(user_id, advice, cache)
        logging.info(f"Advice cached for user {user_id}")
        return advice

    logging.error(f"Failed to get advice for user {user_id}")
    return 'Hmm... I couldn’t understand the stars’ whisper 😕'
