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

NGROK_TUNNEL_URL = os.getenv("NGROK_TUNNEL_URL")
assert (
    NGROK_TUNNEL_URL is not None
), "NGROK_TUNNEL_URL environment variable is not set"

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
assert (
    YOUTUBE_API_KEY is not None
), "YOUTUBE_API_KEY environment variable is not set"
