import asyncio

from schedulebot.schedulebot import Bot
from schedulebot.config import BOT_TOKEN
from schedulebot.config import ROUTERS

bot = Bot(token=BOT_TOKEN)

asyncio.run(bot.run(ROUTERS))
