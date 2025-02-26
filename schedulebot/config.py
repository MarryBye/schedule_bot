import os

from schedulebot.routers.main_router import router as main_router
from schedulebot.routers.commands_router import router as commands_router

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
SQLITE_DBFILE = "suitt_schedule.db"
ROUTERS = [main_router, commands_router]