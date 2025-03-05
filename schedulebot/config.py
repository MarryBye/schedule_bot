import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
GEMINI_API_TOKEN = os.getenv("GEMINI_API_TOKEN")
GEMINI_USED_MODEL = os.getenv("GEMINI_USED_MODEL")
SQLITE_DBFILE = os.getenv("SQLITE_DBFILE")
