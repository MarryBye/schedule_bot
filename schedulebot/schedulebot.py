import aiogram
import asyncio

from typing import Any, Union
from datetime import datetime, date

from schedulebot.singleton import Singleton
from schedulebot.database_controller import DatabaseController
from schedulebot.botmiddleware import BotMiddleware
from schedulebot.config import SQLITE_DBFILE, GROUP_ID
from schedulebot.functions import form_next_lesson, form_day_schedule
from schedulebot.message_history import MessageHistory
from schedulebot.ai_module import BotAIModule

class Bot(aiogram.Bot, metaclass=Singleton):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
        self.dispatcher = aiogram.Dispatcher()
        self.db_controller = DatabaseController(SQLITE_DBFILE)
        
        self.ai_module = BotAIModule('gemini-2.0-flash')
        self.messages_set = MessageHistory("messages.csv")

    def database_execute(self, script_name: str, *args: Any, fetch_count: int=-1) -> Union[Any, None]:
        return self.db_controller.execute(script_name, *args, fetch_count=fetch_count)

    def generate_content(self, content: list):
        return self.ai_module.generate_content(
            ["При формировании ответа не используй никакую разметку, кроме тегов <a>, <b>, <i>, остальные никакие нельзя, текст отделяй просто отступами. Выполни следующую задачу:", *content]
        ).text.strip()

    async def heart_beat(self):
        last_day = None
        while True:
            time_now = datetime.now()
            day_of_week = date.today().weekday()
            
            next_lesson = self.get_next_lesson(day_of_week)

            if next_lesson is not None:
                next_lesson_time = datetime.strptime(next_lesson["time"], "%H:%M:%S").replace(
                    year=time_now.year, month=time_now.month, day=time_now.day
                )

                if 0 <= (next_lesson_time - time_now).total_seconds() <= 60:
                    await self.send_message(GROUP_ID, form_next_lesson(next_lesson), parse_mode="MarkdownV2", disable_web_page_preview=True)
                
                if day_of_week != last_day and time_now.hour == 6 and time_now.minute == 0:
                    last_day = day_of_week
                    day_schedule = self.get_day_lessons(day_of_week)
                    await self.send_message(GROUP_ID, form_day_schedule(day_schedule), parse_mode="MarkdownV2", disable_web_page_preview=True)
            
            self.messages_set.to_csv("messages.csv", index=False)
            
            sleep_time = 60 - (datetime.now().second)
            await asyncio.sleep(sleep_time)
    
    async def run(self, routers=[]) -> None:
        self.dispatcher.include_routers(*routers)
        self.dispatcher.update.middleware(BotMiddleware(self))
        asyncio.create_task(self.heart_beat()) 
        await self.dispatcher.start_polling(self)
        
    def add_new_lesson(self, day_of_week: int, time: str, teacher_id: int, discipline_id: int, zoom_link: str, period: str, additional_info: str, type: int):
        self.database_execute("add_new_lesson.sql", day_of_week, time, teacher_id, discipline_id, zoom_link, period, additional_info, type)
        
    def clear_lessons(self):
        self.database_execute("clear_schedule.sql")
        
    def recreate_tables(self):
        self.database_execute("create_tables.sql")
        
    def get_day_lessons(self, week_day: int=-1):
        if week_day == -1: week_day = datetime.now().weekday()
        result = self.database_execute("get_day_lessons.sql", week_day)
        return result
    
    def get_next_lesson(self, week_day: int=-1, after_time: str="now"):
        if week_day == -1: week_day = datetime.now().weekday()
        if after_time == "now": after_time = datetime.now().strftime("%H:%M")
        result = self.database_execute("get_next_lesson.sql", week_day, after_time, fetch_count=1)
        return result
    
    def save_message(self, author_id, author_name, author_username, creation_date, creation_time, chat_id, chat_type, text, is_answer, answerred_text, answerred_author_id, answerred_author_name):
        self.database_execute("new_message.sql", author_id, author_name, author_username, creation_date, creation_time, chat_id, chat_type, text, is_answer, answerred_text, answerred_author_id, answerred_author_name)
        
    def get_messages(self, chat_id: int, username: str=None, date: str=None, time: str=None):
        result = self.database_execute("get_messages.sql", chat_id, username, date, time)
        return result
    
    def save_ai_note(self, chat_id: int, note_text: str, note_date: str):
        self.database_execute("new_ai_note.sql", chat_id, note_text, note_date)
        
    def get_ai_notes(self, chat_id: int):
        result = self.database_execute("get_ai_notes.sql", chat_id, date)
        return result