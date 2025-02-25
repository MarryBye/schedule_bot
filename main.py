from core.classes.schedulebot import Bot
from config import BOT_TOKEN
import asyncio

bot = Bot(token=BOT_TOKEN)

asyncio.run(bot.run())
