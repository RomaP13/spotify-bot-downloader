import logging
import time

import requests

logger = logging.getLogger(__name__)


def check_telegram_bot_api_server(url: str, token: str, timeout=30) -> bool:
    """
    Check if the Telegram Bot API server is running and accessible.

    Args:
        url (str): The base URL of the Telegram Bot API server.
        token (str): The bot token required to authenticate the request.
        timeout (int): The maximum time (in seconds) to wait for the
        server to start. Defaults to 30 seconds.

    Returns:
        bool: True if the server is up and running;
        otherwise, it raises an exception.

    Raises:
        Exception: If the Telegram Bot API server does not start within
        the specified timeout.
    """
    start_time = time.time()
    api_url = f"{url}/bot{token}/getMe"
    while time.time() - start_time < timeout:
        try:
            response = requests.get(api_url)
            if response.status_code == 200 and response.json().get("ok"):
                logger.info("Telegram Bot API server is up and running.")
                return True
        except requests.exceptions.RequestException:
            logger.warning("Waiting for Telegram Bot API server to start...")
        time.sleep(2)
    logger.error("Telegram Bot API server did not start in time.")
    raise Exception("Telegram Bot API server did not start in time.")
