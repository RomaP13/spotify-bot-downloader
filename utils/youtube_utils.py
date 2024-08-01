import logging
import os
from typing import Union

import requests
import yt_dlp

from config import YOUTUBE_API_KEY

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # noqa: E501


def search_youtube(query: str) -> Union[str, None]:
    """
    Searches YouTube for a video based on a query string.

    Args:
        query (str): The search query string.

    Returns:
        Union[str, None]: The URL of the first video found,
        or None if no video found or an error occurs.
    """
    SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
    VIDEO_URL = "https://www.youtube.com/watch?v="

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        results = response.json()
        if "items" in results and len(results["items"]) > 0:
            video_id = results["items"][0]["id"]["videoId"]
            return VIDEO_URL + video_id
    else:
        print(f"Error: {response.status_code}, {response.text}")

    return None


def download_track(
    youtube_track_url: str, output_path: str, max_retries: int = 3
) -> str | None:
    """
    Downloads the audio track of a YouTube video and saves it as an MP3 file.

    Args:
        youtube_track_url (str): The URL of the YouTube video to download.
        output_path (str): The file path to save the downloaded audio track.
        max_retries (int): The maximum number of retries if
        the download fails. Defaults to 3.

    Returns:
        Union[str, None]: The file path of the downloaded MP3 file,
        or None if the download fails.
    """
    base, _ = os.path.splitext(output_path)  # Remove any existing extension
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{base}.%(ext)s",
        "quiet": True,
        "user_agent": USER_AGENT,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    for attempt in range(max_retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(youtube_track_url)
            logger.info(f"Download successful on attempt {attempt + 1}")
            return f"{base}.mp3"
        except yt_dlp.utils.DownloadError as e:
            logger.error(f"Error downloading the track: {e}")
            if attempt >= max_retries - 1:
                logger.error(
                    f"Failed to download the track after {max_retries} attempts."  # noqa: E501
                )
                raise

    return None
