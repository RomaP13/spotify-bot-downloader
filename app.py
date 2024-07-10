import logging
import os

import uvicorn
from aiogram import types
from dotenv import load_dotenv
from fastapi import FastAPI, Request

from bot import bot, dp

load_dotenv(override=True)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
NGROK_TUNNEL_URL = os.getenv("NGROK_TUNNEL_URL")

WEBHOOK_PATH = f"/bot/{TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        logger.info(f"Setting webhook URL to {WEBHOOK_URL}")
        await bot.set_webhook(url=WEBHOOK_URL)
    else:
        logger.info(f"Webhook URL is already set to {WEBHOOK_URL}")


async def on_shutdown():
    await bot.session.close()
    logger.info("Bot session closed")


app = FastAPI(on_startup=[on_startup], on_shutdown=[on_shutdown])


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    update = await request.json()
    update = types.Update(**update)
    logger.info("Received update")
    await dp.feed_update(bot, update)
    return {"ok": True}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
