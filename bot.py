import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.filters import Command

from config import TELEGRAM_BOT_TOKEN
from utils.file_utils import create_zip_file, send_file_to_user
from utils.message_utils import update_progress
from utils.spotify.album_utils import (
    get_album_id_by_url,
    get_album_title,
    get_album_tracks,
)
from utils.spotify.auth import get_auth_header, get_token
from utils.spotify.playlist_utils import (
    get_playlist_id_by_url,
    get_playlist_title,
    get_playlist_tracks,
    is_playlist_accessible,
)
from utils.spotify.track_utils import (
    get_track,
    get_track_id_by_url,
    get_track_info,
)
from utils.track_processor import process_track

# Initialize bot with custom session pointing
# to the local telegram-bot-api server
session = AiohttpSession(
    api=TelegramAPIServer.from_base("http://localhost:8081")
)
bot = Bot(token=TELEGRAM_BOT_TOKEN, session=session)  # type: ignore
dp = Dispatcher()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(Command("start"))
async def start(message: types.Message) -> None:
    if message.from_user:
        logger.info(f"Received /start command from {message.from_user.id}")
    await message.answer(
        "Hello, send me a Spotify track URL, and I'll provide track info."
    )


@dp.message(F.text.startswith("https://open.spotify.com/track/"))
async def handle_spotify_track_url(message: types.Message) -> None:
    if message.from_user:
        logger.info(
            f"Received track Spotify URL from {message.from_user.id}: {message.text}"  # noqa: E501
        )

    track_url = message.text.strip()  # type: ignore
    token = get_token()
    headers = get_auth_header(token)
    track_id = get_track_id_by_url(track_url)
    json_result = get_track(headers, track_id)
    track_info = get_track_info(headers, json_result)
    track_dir = "media/tracks"

    bot_message = await message.answer("Starting to process track...")
    bot_message_id = bot_message.message_id
    chat_id = bot_message.chat.id

    track_path = process_track(track_info, track_dir)
    if track_path:
        # Indicate that the bot is sending a document
        await bot.send_chat_action(chat_id, "upload_document")

        await send_file_to_user(message, track_path, "audio")
        progress_text = "Track was sent."
    else:
        progress_text = "Track wasn't found."
    logger.info(progress_text)
    await update_progress(bot, progress_text, chat_id, bot_message_id)


@dp.message(F.text.startswith("https://open.spotify.com/playlist/"))
async def handle_spotify_playlist_url(message: types.Message) -> None:
    if message.from_user:
        message_id = message.message_id
        logger.info(f"Handling message with id: {message_id}")

        logger.info(
            f"Received playlist Spotify URL from {message.from_user.id}: {message.text}"  # noqa: E501
        )

    playlist_url = message.text.strip()  # type: ignore
    token = get_token()
    headers = get_auth_header(token)
    playlist_id = get_playlist_id_by_url(playlist_url)

    # Check if the playlist is not private
    if not is_playlist_accessible(headers, playlist_id):
        logger.info(f"Received private playlist with id: {playlist_id}")
        await message.answer("The playlist is private or inaccessible.")
        return

    playlist_title = get_playlist_title(headers, playlist_id)
    tracks_info = get_playlist_tracks(headers, playlist_id)
    if len(tracks_info) == 0:
        logger.warning("Tracks info is empty")
        await message.answer("No tracks found in the playlist.")
        return

    # Directory to store downloaded tracks
    tracks_dir = f"media/playlists/{playlist_title}"
    os.makedirs(tracks_dir, exist_ok=True)

    bot_message = await message.answer("Starting to process tracks...")
    bot_message_id = bot_message.message_id
    chat_id = bot_message.chat.id
    total_tracks = len(tracks_info)

    for current, track_info in enumerate(tracks_info):
        progress_text = f"Processing track {current + 1}/{total_tracks}: {track_info['artists']} - {track_info['title']}"  # noqa: E501
        await update_progress(
            bot,
            progress_text,
            chat_id,
            bot_message_id,
        )
        process_track(track_info, tracks_dir)

    await update_progress(
        bot,
        "Playlist was downloaded. Sending...",
        chat_id,
        bot_message_id,
    )

    # Indicate that the bot is sending a document
    await bot.send_chat_action(chat_id, "upload_document")

    # Create ZIP file
    zip_path = f"media/playlists/{playlist_title}.zip"
    create_zip_file(tracks_dir, zip_path)

    # Send ZIP file to the user
    await send_file_to_user(message, zip_path, "document")

    progress_text = "Playlist was sent."
    logger.info(progress_text)
    await update_progress(
        bot,
        progress_text,
        chat_id,
        bot_message_id,
    )


@dp.message(F.text.startswith("https://open.spotify.com/album/"))
async def handle_spotify_album_url(message: types.Message) -> None:
    if message.from_user:
        message_id = message.message_id
        logger.info(f"Handling message with id: {message_id}")

        logger.info(
            f"Received album Spotify URL from {message.from_user.id}: {message.text}"  # noqa: E501
        )

    album_url = message.text.strip()  # type: ignore
    token = get_token()
    headers = get_auth_header(token)
    album_id = get_album_id_by_url(album_url)
    album_title = get_album_title(headers, album_id)
    tracks_info = get_album_tracks(headers, album_id)
    if len(tracks_info) == 0:
        logger.warning("Tracks info is empty")
        await message.answer("No tracks found in the album.")
        return

    # Directory to store downloaded tracks
    tracks_dir = f"media/albums/{album_title}"
    os.makedirs(tracks_dir, exist_ok=True)

    bot_message = await message.answer("Starting to process tracks...")
    bot_message_id = bot_message.message_id
    chat_id = bot_message.chat.id
    total_tracks = len(tracks_info)

    for current, track_info in enumerate(tracks_info):
        progress_text = f"Processing track {current + 1}/{total_tracks}: {track_info['artists']} - {track_info['title']}"  # noqa: E501
        await update_progress(
            bot,
            progress_text,
            chat_id,
            bot_message_id,
        )
        process_track(track_info, tracks_dir)

    await update_progress(
        bot,
        "Album was downloaded. Sending...",
        chat_id,
        bot_message_id,
    )

    # Indicate that the bot is sending a document
    await bot.send_chat_action(chat_id, "upload_document")

    # Create ZIP file
    zip_path = f"media/albums/{album_title}.zip"
    create_zip_file(tracks_dir, zip_path)

    # Send ZIP file to the user
    await send_file_to_user(message, zip_path, "document")

    progress_text = "Album was sent."
    logger.info(progress_text)
    await update_progress(
        bot,
        progress_text,
        chat_id,
        bot_message_id,
    )


@dp.message()
async def handle_invalid_message(message: types.Message) -> None:
    await message.answer("Please send a valid Spotify track URL.")
