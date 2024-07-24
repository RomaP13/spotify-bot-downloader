import logging
import os

from utils.metadata_utils import add_metadata_to_track
from utils.spotify.image_utils import download_cover_image
from utils.youtube_utils import download_track, search_youtube

logger = logging.getLogger(__name__)


def process_track(track_info: dict, track_dir: str) -> str | None:
    """
    Process a track by searching for it on YouTube, downloading the audio,
    downloading the cover image, and adding metadata to the audio file.

    Args:
        track_info (dict): Information about the track, including title,
        artists, and cover URL.
        tracks_dir (str): Directory where the downloaded tracks will be stored.

    Returns:
        str | None: The path to the downloaded track if successful,
        otherwise None.
    """
    track_title = track_info["title"]
    track_artists = track_info["artists"]
    try:
        logger.info(f"Processing: {track_artists} - {track_title}")

        if not track_title or not track_artists:
            logger.warning("Track not found.")
            return None

        # Search the track
        search_query = f"{track_title} {track_artists}"
        youtube_track_url = search_youtube(search_query)
        if not youtube_track_url:
            logger.warning(f"Could not find YouTube URL for: {track_title}")
            return None

        # Download the track
        track_path = os.path.join(track_dir, f"{track_title}.mp3")
        track_path = download_track(youtube_track_url, track_path)
        if not track_path:
            logger.warning(f"Failed to download track: {track_title}")
            return None

        # Download the cover image
        cover_path = f"media/img/{track_title}.jpg"
        cover_url = track_info["cover_url"]
        if cover_url:
            download_cover_image(cover_url, cover_path)
        else:
            logger.warning(f"No cover URL for track: {track_title}")

        # Add metadata to the downloaded track
        add_metadata_to_track(track_path, track_info, cover_path)

        return track_path
    except Exception as e:
        logger.error(f"Failed to download the track: {track_title}")
        logger.error(f"Error handling Spotify URL: {e}")

    return None
