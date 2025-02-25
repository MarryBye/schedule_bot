from typing import Any
from config import GROUP_ID, ROUTERS
from core.classes.singleton import Singleton
from core.classes.database.database_controller import DatabaseController

import aiogram
import datetime
import asyncio

from core.functions import get_day_schedule, get_next_lesson

class Bot(aiogram.Bot, metaclass=Singleton):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
        self.dispatcher = aiogram.Dispatcher()
        self.db_controller = DatabaseController("suitt_schedule.db")

    async def heart_beat(self):
        last_day = None
        while True:
            time_now = datetime.datetime.now()
            day_of_week = datetime.date.today().weekday()
            
            next_lesson = self.db_controller.execute("get_next_lesson.sql", day_of_week, fetch_count=1)

            if next_lesson is not None:
                next_lesson_time = datetime.datetime.strptime(next_lesson["time"], "%H:%M:%S").replace(
                    year=time_now.year, month=time_now.month, day=time_now.day
                )

                if 0 <= (next_lesson_time - time_now).total_seconds() <= 60:
                    await self.send_message(GROUP_ID, get_next_lesson(day_of_week), parse_mode="MarkdownV2", disable_web_page_preview=True)
                
                if day_of_week != last_day and time_now.hour == 6 and time_now.minute == 0:
                    last_day = day_of_week
                    await self.send_message(GROUP_ID, get_day_schedule(day_of_week), parse_mode="MarkdownV2", disable_web_page_preview=True)
                
            sleep_time = 60 - (datetime.datetime.now().second)
            await asyncio.sleep(sleep_time)
    
    async def run(self) -> None:
        self.dispatcher.include_routers(*ROUTERS)
        asyncio.create_task(self.heart_beat()) 
        await self.dispatcher.start_polling(self)