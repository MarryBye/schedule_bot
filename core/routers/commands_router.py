from typing import Any
import aiogram
import datetime
import json

import aiogram.filters
from core.classes.database.database_controller import DatabaseController
from core.functions import get_day_schedule, get_next_lesson
from language import *

router: aiogram.Router = aiogram.Router(name=__name__)
db_controller = DatabaseController("suitt_schedule.db")

@router.message()
async def aaa(msg: aiogram.types.Message) -> None:
    print(msg.chat.id)

@router.message(aiogram.filters.Command("day_schedule"))
async def day_schedule(msg: aiogram.types.Message) -> None:
    day_of_week: int = datetime.date.today().weekday()
    msg_text = get_day_schedule(day_of_week)
    await msg.reply(msg_text, parse_mode="MarkdownV2", disable_web_page_preview=True)
    
@router.message(aiogram.filters.Command("next_lesson"))
async def next_lesson(msg: aiogram.types.Message) -> None:
    day_of_week: int = datetime.date.today().weekday()
    msg_text = get_next_lesson(day_of_week)
    await msg.reply(msg_text, parse_mode="MarkdownV2", disable_web_page_preview=True)

@router.message(aiogram.filters.Command("load_new_schedule"))
async def load_new_schedule(msg: aiogram.types.Message) -> None:
    db_controller.execute("clear_schedule.sql")
    
    with open("schedule.json", "r", encoding="UTF-8") as file:
        data: list[list[dict[str, Any] | None]] = json.load(file)
        
    for day in range(len(data)):
        day_lessons = data[day]
        for lesson in range(len(day_lessons)):
            lesson_data = day_lessons[lesson]
            if lesson_data is None: continue
            
            db_controller.execute(
                "add_new_lesson.sql", 
                day, 
                lessons_time[lesson], 
                lesson_data["teacher_id"], 
                lesson_data["discipline_id"], 
                lesson_data["zoom_link"], 
                lesson_data["period"], 
                lesson_data["info"], 
                lesson_data["type"]
            )
    
    await msg.reply("Загрузил новое расписание", parse_mode="MarkdownV2")
        
