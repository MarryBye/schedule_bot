import asyncio

from schedulebot.schedulebot import Bot
from schedulebot.config import BOT_TOKEN

from schedulebot.routers.main_router import router as main_router
from schedulebot.routers.commands_router import router as commands_router

bot = Bot(token=BOT_TOKEN)

asyncio.run(bot.run([main_router, commands_router]))
