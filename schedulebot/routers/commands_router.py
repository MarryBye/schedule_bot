from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from typing import Any

from json import load as json_load

from schedulebot.functions import form_day_schedule, form_next_lesson
from schedulebot.schedulebot import Bot
from schedulebot.language import lessons_time

router: Router = Router(name=__name__)

@router.message(Command("day_schedule"))
async def day_schedule(msg: Message, bot: Bot) -> None:
    day_schedule = bot.get_day_lessons()
    msg_text = form_day_schedule(day_schedule)
    await msg.reply(msg_text, parse_mode="HTML", disable_web_page_preview=True)
    
@router.message(Command("next_lesson"))
async def next_lesson(msg: Message, bot: Bot) -> None:
    next_lesson = bot.get_next_lesson()
    msg_text = form_next_lesson(next_lesson)
    await msg.reply(msg_text, parse_mode="HTML", disable_web_page_preview=True)

@router.message(Command("load_new_schedule"))
async def load_new_schedule(msg: Message, bot: Bot) -> None:
    bot.clear_lessons()
    
    with open("schedule.json", "r", encoding="UTF-8") as file:
        data: list[list[dict[str, Any] | None]] = json_load(file)
        
        for day in range(len(data)):
            day_lessons = data[day]
            for lesson in range(len(day_lessons)):
                lesson_data = day_lessons[lesson]
                if lesson_data is None: continue
                
                bot.add_new_lesson(
                    day, 
                    lessons_time[lesson], 
                    lesson_data["teacher_id"], 
                    lesson_data["discipline_id"], 
                    lesson_data["zoom_link"], 
                    lesson_data["period"], 
                    lesson_data["info"], 
                    lesson_data["type"]
                )
    
        await msg.reply("Загрузил новое расписание", parse_mode="HTML")
        
