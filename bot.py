import logging
import os
import zipfile

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command

from config import TELEGRAM_BOT_TOKEN
from utils.spotify_utils import (
    download_cover_image,
    get_auth_header,
    get_playlist_id_by_url,
    get_playlist_title,
    get_playlist_tracks,
    get_token,
    get_track,
    get_track_id_by_url,
    get_track_info,
)
from utils.youtube_utils import (
    add_metadata_to_track,
    download_track,
    get_track_from_youtube,
)

bot = Bot(token=TELEGRAM_BOT_TOKEN)  # type: ignore
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
            f"Received track Spotify URL from {message.from_user.id}: {message.text}"
        )

    track_url = message.text.strip()  # type: ignore
    token = get_token()
    headers = get_auth_header(token)
    track_id = get_track_id_by_url(track_url)
    json_result = get_track(headers, track_id)
    track_info = get_track_info(headers, json_result)
    track_title = track_info["title"]
    track_artists = track_info["artists"]
    logger.info(f"Processing track: {track_title}")

    try:
        search_query = f"{track_title} {track_artists}"
        youtube_track = get_track_from_youtube(search_query)
        output_path = f"media/tracks/{track_title}.mp3"
        file_path = await download_track(youtube_track, output_path)

        # Download the cover image
        cover_path = f"media/img/{track_title}.jpg"
        cover_path = download_cover_image(track_info["cover_url"], cover_path)
        if cover_path is None:
            logger.warning(
                f"Failed to download the track cover for {track_title}"
            )

        # Add metadata to the downloaded track
        add_metadata_to_track(file_path, track_info, cover_path)

        await message.answer("Downloading track from YouTube...")
        file = types.FSInputFile(file_path)
        await message.answer_audio(file)
        logger.info("Track was processed.")
    except Exception as e:
        logger.error(f"Error handling Spotify URL: {e}")
        await message.answer(
            "An error occurred while processing your request. Please try again later."  # noqa: E501
        )


@dp.message(F.text.startswith("https://open.spotify.com/playlist/"))
async def handle_spotify_playlist_url(message: types.Message) -> None:
    if message.from_user:
        message_id = message.message_id
        logger.info(f"Handling message with id: {message_id}")

        logger.info(
            f"Received playlist Spotify URL from {message.from_user.id}: {message.text}"
        )

    playlist_url = message.text.strip()  # type: ignore
    token = get_token()
    headers = get_auth_header(token)
    playlist_id = get_playlist_id_by_url(playlist_url)
    playlist_title = get_playlist_title(headers, playlist_id)
    tracks_info = get_playlist_tracks(headers, playlist_id)
    if len(tracks_info) == 0:
        logger.warning("Tracks info is empty")
        await message.answer("No tracks found in the playlist.")
        return

    # Directory to store downloaded tracks
    tracks_dir = f"media/playlists/{playlist_title}"
    os.makedirs(tracks_dir, exist_ok=True)

    track_files = []
    for track_info in tracks_info:
        try:
            track_title = track_info["title"]
            track_artists = track_info["artists"]
            logger.info(f"Processing track: {track_title}")

            search_query = f"{track_title} {track_artists}"
            youtube_track = get_track_from_youtube(search_query)

            # Download the track
            track_path = os.path.join(tracks_dir, f"{track_title}.mp3")
            track_path = await download_track(youtube_track, track_path)
            track_files.append(track_path)

            # Download the cover image
            cover_path = f"media/img/{track_title}.jpg"
            cover_path = download_cover_image(
                track_info["cover_url"], cover_path
            )
            if cover_path is None:
                logger.warning(
                    f"Failed to download the track cover for {track_title}"
                )

            # Add metadata to the downloaded track
            add_metadata_to_track(track_path, track_info, cover_path)

        except Exception as e:
            logger.error(f"Failed to download the track: {track_title}")
            logger.error(f"Error handling Spotify URL: {e}")

    # Create ZIP file
    zip_path = f"media/playlists/{playlist_title}.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in os.listdir(tracks_dir):
            if file.endswith(".mp3"):
                zipf.write(
                    os.path.join(tracks_dir, file),
                    os.path.join(os.path.basename(tracks_dir), file),
                )

    # Send ZIP file
    file = types.FSInputFile(zip_path)
    await message.answer_document(file)

    logger.info("All tracks from playlist was processed.")


@dp.message()
async def handle_invalid_message(message: types.Message) -> None:
    await message.answer("Please send a valid Spotify track URL.")
