import aiogram
import asyncio

from typing import Any
from datetime import datetime

from schedulebot.singleton import Singleton
from schedulebot.middlewares.bot_middleware import BotMiddleware
from schedulebot.middlewares.session_middleware import SessionMiddleware
from schedulebot.middlewares.apps_container_middleware import AppsMiddleware

class ScheduleBot(aiogram.Bot, metaclass=Singleton):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
        self.dispatcher = aiogram.Dispatcher()
    
    async def run(self, routers=[]) -> None:
        self.dispatcher.include_routers(*routers)
        
        self.dispatcher.update.middleware(BotMiddleware(self))
        self.dispatcher.update.middleware(SessionMiddleware(self))
        self.dispatcher.update.middleware(AppsMiddleware(self))
        
        asyncio.create_task(self.heart_beat()) 
        await self.dispatcher.start_polling(self)
    
    async def heart_beat(self):
        while True:
            print("Bot Heart Beat")
            sleep_time = 60 - (datetime.now().second)
            await asyncio.sleep(sleep_time)