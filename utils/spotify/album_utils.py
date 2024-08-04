import json

import requests

from utils.spotify.track_utils import (
    get_track,
    get_track_id_by_url,
    get_track_info,
)


def get_album_id_by_url(album_url: str) -> str:
    """
    Extract the album ID from a Spotify album URL.

    Args:
        album_url (str): Spotify album URL.

    Returns:
        str: album ID.
    """
    return album_url.split("/")[-1].split("?")[0]


def get_album_title(headers: dict, album_id: str) -> str:
    """
    Extract the album title from a Spotify album.

    Args:
        headers (dict): Authorization header.
        album_id (str): Spotify album ID.

    Returns:
        str: album title.
    """
    url = f"https://api.spotify.com/v1/albums/{album_id}"
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result["name"]


def get_album_tracks(headers: dict, album_id: str) -> list:
    """
    Retrieve tracks information from a Spotify album.

    Args:
        headers (dict): Authorization header.
        album_id (str): Spotify album ID.

    Returns:
        list: List of dictionaries containing track information.
    """
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    tracks = []

    while url:
        result = requests.get(url, headers=headers)
        json_result = result.json()
        with open("result.json", "w") as json_file:
            json.dump(json_result, json_file, indent=4, ensure_ascii=False)

        if "items" not in json_result:
            break

        for item in json_result["items"]:
            track_url = item["external_urls"]["spotify"]
            track_id = get_track_id_by_url(track_url)
            track_json_result = get_track(headers, track_id)
            track_info = get_track_info(headers, track_json_result)
            tracks.append(track_info)

        url = json_result.get("next")  # Get the next URL to fetch more tracks

    return tracks
