import time
import logging

import requests

logger = logging.getLogger(__name__)


def get_ngrok_url(timeout=30):
    """
    Retrieve the public URL of the ngrok tunnel.

    This function attempts to fetch the public URL from the ngrok API
    by polling the local ngrok instance running at
    `http://localhost:4040/api/tunnels`.
    If the URL is not available within the specified timeout period,
    an exception is raised.

    Args:
        timeout (int): The maximum time (in seconds) to wait for ngrok to
        start and provide a public URL.
        Defaults to 30 seconds.

    Returns:
        str: The public URL of the ngrok tunnel.

    Raises:
        Exception: If ngrok does not start or provide a public URL
        within the specified timeout.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            if response.status_code == 200:
                data = response.json()
                public_url = data.get("tunnels", [{}])[0].get("public_url")
                if public_url:
                    return public_url
        except requests.exceptions.ConnectionError:
            logger.info("Waiting for ngrok to start...")
        time.sleep(2)
    raise Exception("Ngrok did not start in time.")
