import logging
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv

from utils.spotify_utils import get_track_id_by_url, get_token, get_track_info

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
assert TELEGRAM_BOT_TOKEN is not None

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(Command("start"))
async def start(message: types.Message) -> None:
    logger.info(f"Received /start command from {message.from_user.id}")
    await message.answer("Hello, send me a Spotify track URL, and I'll provide track info.")


@dp.message(F.text.startswith("https://open.spotify.com/track/"))
async def handle_spotify_url(message: types.Message) -> None:
    logger.info(f"Received Spotify URL from {message.from_user.id}: {message.text}")
    track_url = message.text.strip()
    token = get_token()
    track_id = get_track_id_by_url(track_url)
    track_info = get_track_info(token, track_id)
    response = f"Track Name: {track_info['name']}\n" \
               f"Artist: {track_info['artists'][0]['name']}\n" \
               f"Album: {track_info['album']['name']}"
    await message.answer(response)


@dp.message()
async def handle_invalid_message(message: types.Message) -> None:
    await message.answer("Please send a valid Spotify track URL.")
