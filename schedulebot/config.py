import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
GEMINI_API_TOKEN = os.getenv("GEMINI_API_TOKEN")
SQLITE_DBFILE = "suitt_schedule.db"