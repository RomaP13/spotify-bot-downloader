import base64
import json

import requests

from config import CLIENT_ID, CLIENT_SECRET


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
