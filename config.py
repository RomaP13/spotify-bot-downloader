import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Retrieve and assert environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
assert CLIENT_ID is not None, "CLIENT_ID environment variable is not set"

CLIENT_SECRET = os.getenv("CLIENT_SECRET")
assert (
    CLIENT_SECRET is not None
), "CLIENT_SECRET environment variable is not set"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
assert (
    TELEGRAM_BOT_TOKEN is not None
), "TELEGRAM_BOT_TOKEN environment variable is not set"

TELEGRAM_API_BASE_URL = os.getenv("TELEGRAM_API_BASE_URL")

if TELEGRAM_API_BASE_URL is None:
    TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
    assert (
        TELEGRAM_API_ID is not None
    ), "TELEGRAM_API_ID environment variable is not set"

    TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
    assert (
        TELEGRAM_API_HASH is not None
    ), "TELEGRAM_API_HASH environment variable is not set"

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
assert (
    YOUTUBE_API_KEY is not None
), "YOUTUBE_API_KEY environment variable is not set"
