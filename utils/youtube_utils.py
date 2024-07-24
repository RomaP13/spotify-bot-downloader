import logging
import os
from typing import Union

import requests
import yt_dlp

from config import YOUTUBE_API_KEY

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # noqa: E501


def search_youtube(query: str) -> Union[str, None]:
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
