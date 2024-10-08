from contextlib import asynccontextmanager
import logging

from aiogram import types
from fastapi import FastAPI, Request
import uvicorn

from bot import bot, dp
from config import TELEGRAM_BOT_TOKEN
from utils.ngrok import get_ngrok_url


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


NGROK_TUNNEL_URL = get_ngrok_url()
WEBHOOK_PATH = f"/bot/{TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"
# Set to store processed update_ids
processed_update_ids = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    # Remove webhook if it exists
    delete_webhook_result = await bot.delete_webhook(drop_pending_updates=True)
    if delete_webhook_result:
        logger.info("Webhook integration was removed.")
    else:
        logger.info("Webhook integration wasn't removed.")

    # Set new webhook
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        logger.info(f"Setting webhook URL to {WEBHOOK_URL}")
        await bot.set_webhook(url=WEBHOOK_URL)
    else:
        logger.info(f"Webhook URL is already set to {WEBHOOK_URL}")

    yield

    # Shutdown logic
    await bot.session.close()
    logger.info("Bot session closed")


# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    update = await request.json()
    update_id = update["update_id"]

    # Check if update_id is already processed
    if update_id in processed_update_ids:
        logger.info(f"Ignoring already processed update: {update_id}")
        return {"ok": True}

    logger.info(f"Received update: {update_id}")
    processed_update_ids.add(update_id)

    # Remove old update_ids to prevent memory leaks
    if len(processed_update_ids) > 20:
        processed_update_ids.clear()

    update = types.Update(**update)
    await dp.feed_update(bot, update)
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
