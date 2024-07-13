import base64
import json

import requests

from config import CLIENT_ID, CLIENT_SECRET
from utils.spotify_track_extractor import (
    get_album,
    get_artists,
    get_cover_url,
    get_genres,
    get_release_date,
    get_title,
    get_total_tracks,
    get_track_number,
)


def get_token() -> str:
    """
    Obtain an access token from the Spotify API using client credentials.

    Returns:
        str: Access token.
    """
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token


def get_auth_header(token: str) -> dict:
    """
    Create an authorization header using the given token.

    Args:
        token (str): Access token.

    Returns:
        dict: Authorization header.
    """
    return {"Authorization": "Bearer " + token}


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


def download_cover_image(url: str, output_path: str) -> str | None:
    """
    Download the cover image from a given URL and
    save it to the specified output path.

    Args:
        url (str): URL of the cover image.
        output_path (str): Path where the image will be saved.

    Returns:
        str | None: Path to the saved image or None if an error occurred.
    """
    try:
        response = requests.get(url)
        with open(output_path, "wb") as file:
            file.write(response.content)
        return output_path
    except requests.RequestException as e:
        print(f"ERROR: {e}")

    return None
