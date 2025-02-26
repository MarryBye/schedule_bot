import asyncio

from schedulebot.schedulebot import Bot
from schedulebot.config import BOT_TOKEN

from schedulebot.routers.main_router import router as main_router
from schedulebot.routers.commands_router import router as commands_router
from schedulebot.routers.ai_router import router as ai_router
from schedulebot.routers.collector_router import router as collector_router

bot = Bot(token=BOT_TOKEN)

asyncio.run(bot.run([main_router, commands_router, ai_router, collector_router]))
