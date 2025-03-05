import asyncio

from schedulebot.schedulebot import ScheduleBot
from schedulebot.config import BOT_TOKEN

from schedulebot.routers.main_router import router as main_router
from schedulebot.routers.commands_router import router as commands_router
from schedulebot.routers.ai_router import router as ai_router

from schedulebot.keyboards.show_schedule import KEYBOARD

if __name__ == "__main__":
    bot = ScheduleBot(token=BOT_TOKEN)
    asyncio.run(bot.run([main_router, commands_router, ai_router]))
