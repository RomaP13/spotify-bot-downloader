import json

import requests

from utils.spotify.track_extractor import (
    get_album,
    get_artists,
    get_cover_url,
    get_genres,
    get_release_date,
    get_title,
    get_total_tracks,
    get_track_number,
)


def get_track(headers: dict, track_id: str) -> dict:
    """
    Retrieve raw track information from the Spotify API.

    Args:
        headers (dict): Authorization header.
        track_id (str): Spotify track ID.

    Returns:
        dict: Raw JSON result from the Spotify API.
    """
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_track_id_by_url(track_url: str) -> str:
    """
    Extract the track ID from a Spotify track URL.

    Args:
        track_url (str): Spotify track URL.

    Returns:
        str: Track ID.
    """
    return track_url.split("/")[-1].split("?")[0]


def get_track_info(headers: dict, json_result: dict) -> dict:
    """
    Retrieve track information from the json_result.

    Args:
        headers (dict): Authorization header.
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        dict: Dictionary containing track information.
    """
    title = get_title(json_result)
    album = get_album(json_result)
    artists = get_artists(json_result)
    release_date = get_release_date(json_result)
    genres = get_genres(json_result, headers)
    cover_url = get_cover_url(json_result)
    track_number = get_track_number(json_result)
    total_tracks = get_total_tracks(json_result)

    track_info = {
        "title": title,
        "album": album,
        "artists": artists,
        "release_date": release_date,
        "genres": genres,
        "cover_url": cover_url,
        "track_number": track_number,
        "total_tracks": total_tracks,
    }

    return track_info
