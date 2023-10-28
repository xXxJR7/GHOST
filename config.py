from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

SESSION = getenv("SESSION")

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_USER = getenv("BOT_USER")

REDIS_URL = getenv("REDIS_URL")
REDIS_PASSWORD = getenv("REDIS_PASSWORD")

LOGS = getenv("LOGS")

TZ = getenv("TZ")

LANGUAGE = getenv("LANGUAGE")

START_IMG = getenv("START_IMG") or None
