import asyncio
import logging
import os
from typing import Union

import eyed3
import yt_dlp

logger = logging.getLogger(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"  # noqa: E501


def get_track_from_youtube(search_query: str) -> Union[dict, None]:
    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "default_search": "ytsearch",
        "max_downloads": 1,
        "user_agent": USER_AGENT,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        results = ydl.extract_info(search_query, download=False)
        if results is not None and isinstance(results, dict):
            if "entries" in results and isinstance(results["entries"], list):
                return results["entries"][0]

        return results


def download_track(youtube_track: dict, output_path: str) -> str:
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

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_track["webpage_url"]])
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Error downloading the track: {e}")
        raise

    return f"{base}.mp3"


def add_metadata_to_track(
    file_path: str, track_info: dict, cover_path: str
):
    audiofile = eyed3.load(file_path)
    assert audiofile is not None
    assert audiofile.tag is not None

    audiofile.tag.title = track_info["title"]
    audiofile.tag.artist = track_info["artists"]
    audiofile.tag.album = track_info["album"]
    audiofile.tag.release_date = track_info["release_date"]
    audiofile.tag.genre = track_info["genres"]
    audiofile.tag.track_num = (
        track_info["track_number"],
        track_info["total_tracks"],
    )

    with open(cover_path, "rb") as image_file:
        imagedata = image_file.read()
    audiofile.tag.images.set(3, imagedata, "image/jpeg", "cover")

    audiofile.tag.save()
