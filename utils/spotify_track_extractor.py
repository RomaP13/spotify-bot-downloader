def get_title(json_result: dict) -> str:
    """
    Extracts the title from the JSON result.

    Args:
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        str: The title of the track, or "Unknown" if not found.
    """
    return json_result.get("name", "Unknown")


def get_artists(json_result: dict) -> str:
    """
    Extracts the artists' names from the JSON result.

    Args:
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        str: A comma-separated string of artists' names,
        or "Unknown" if not found.
    """
    artists = json_result.get("artists", [])
    if len(artists) == 0:
        return "Unknown"
    return ", ".join(artist["name"] for artist in artists)


def get_album(json_result: dict) -> str:
    """
    Extracts the album name from the JSON result.

    Args:
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        str: The album name, or "Unknown" if not found.
    """
    return json_result.get("album", {}).get("name", "Unknown")


def get_release_date(json_result: dict) -> str:
    """
    Extracts the release date from the JSON result.

    Args:
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        str: The release date, or "Unknown" if not found.
    """
    return json_result.get("album", {}).get("release_date", "Unknown")


def get_genres(json_result: dict) -> str:
    """
    Extracts the genres from the JSON result.

    Args:
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        str: A comma-separated string of genres,
        or an empty string if not found.
    """
    genres = json_result.get("artists", [{}])[0].get("genres", [])
    return ", ".join(genre for genre in genres)


def get_cover_url(json_result: dict) -> str:
    """
    Extracts the cover URL from the JSON result.

    Args:
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        str: The cover URL, or an empty string if not found.
    """
    return json_result.get("album", {}).get("images", [{}])[0].get("url", "")


def get_track_number(json_result: dict) -> str:
    """
    Extracts the track number from the JSON result.

    Args:
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        str: The track number, or "Unknown" if not found.
    """
    return json_result.get("track_number", "Unknown")


def get_total_tracks(json_result: dict) -> str:
    """
    Extracts the total number of tracks in the album from the JSON result.

    Args:
        json_result (dict): The JSON result from the Spotify API.

    Returns:
        str: The total number of tracks, or "Unknown" if not found.
    """
    return json_result.get("album", {}).get("total_tracks", "Unknown")
