import json

import requests

from utils.spotify.track_utils import get_track_info


def get_playlist_id_by_url(playlist_url: str) -> str:
    """
    Extract the playlist ID from a Spotify playlist URL.

    Args:
        playlist_url (str): Spotify playlist URL.

    Returns:
        str: Playlist ID.
    """
    return playlist_url.split("/")[-1].split("?")[0]


def get_playlist_title(headers: dict, playlist_id: str) -> str:
    """
    Extract the playlist title from a Spotify playlist.

    Args:
        headers (dict): Authorization header.
        playlist_id (str): Spotify playlist ID.

    Returns:
        str: Playlist title.
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result["name"]


def get_playlist_tracks(headers: dict, playlist_id: str) -> list:
    """
    Retrieve tracks information from a Spotify playlist.

    Args:
        headers (dict): Authorization header.
        playlist_id (str): Spotify playlist ID.

    Returns:
        list: List of dictionaries containing track information.
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    tracks = []

    while url:
        result = requests.get(url, headers=headers)
        json_result = result.json()

        if "items" not in json_result:
            break

        for item in json_result["items"]:
            track = item["track"]
            track_info = get_track_info(headers, track)
            tracks.append(track_info)

        url = json_result.get("next")  # Get the next URL to fetch more tracks

    return tracks


def is_playlist_accessible(headers: dict, playlist_id: str) -> bool:
    """
    Check if a Spotify playlist is accessible.

    This function sends a GET request to the Spotify API to check
    if the playlist with the given playlist_id is accessible.
    If the response status code is 200, the playlist is accessible;
    otherwise, it is not.

    Args:
        headers (dict): Authorization headers.
        playlist_id (str): The Spotify ID of the playlist to check.

    Returns:
        bool: True if the playlist is accessible, False otherwise.
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    response = requests.get(url, headers=headers)
    return response.status_code == 200
