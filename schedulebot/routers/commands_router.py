from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from typing import Any
from json import load as json_load
from datetime import date, timedelta

from schedulebot.schedulebot import ScheduleBot
from schedulebot.apps import Apps
from schedulebot.functions import form_day_schedule, form_next_lesson, get_week
from schedulebot.language import lessons_time, week_days

router: Router = Router(name=__name__)

async def form_schedule(d: date, apps: Apps):
    week_day = d.weekday()
    week_number = get_week(d)
    day_schedule = apps.database_controller.get_day_lessons(week_day)
    text_title = f"📆<b>{week_days[week_day]}, {d}, {week_number} неделя</b>"
    msg_text = text_title + form_day_schedule(day_schedule, d)
    keyboard = apps.keyboards_controller.get_keyboard("show_schedule")
    
    return msg_text, keyboard

@router.message(Command("show_schedule"))
async def show_schedule(msg: Message, bot: ScheduleBot, session: dict, apps: Apps) -> None:
    today_date = date.today()
    session["date"] = today_date
    
    msg_text, keyboard = await form_schedule(today_date, apps)
    await msg.reply(text=msg_text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=keyboard)

@router.callback_query(lambda call: call.data.split("|")[0] == "schedule_selector")
async def shedule_change_day(call: CallbackQuery, bot: ScheduleBot, session: dict, apps: Apps):
    today_date = session.get("date", None)
    if today_date is None:
        today_date = date.today()
        session["date"] = today_date
    
    match call.data.split("|")[1]:
        case "plus_day":
            new_date = session["date"] + timedelta(days=1)
        case "minus_day":
            new_date = session["date"] - timedelta(days=1)
            
    session["date"] = new_date
    
    msg_text, keyboard = await form_schedule(session["date"], apps)
    await call.message.edit_text(text=msg_text, parse_mode="HTML", disable_web_page_preview=True, reply_markup=keyboard)
    
@router.message(Command("next_lesson"))
async def next_lesson(msg: Message, bot: ScheduleBot, session: dict, apps: Apps) -> None:
    next_lesson = apps.database_controller.get_next_lesson()
    msg_text = form_next_lesson(next_lesson)
    await msg.reply(msg_text, parse_mode="HTML", disable_web_page_preview=True)

@router.message(Command("load_new_schedule"))
async def load_new_schedule(msg: Message, bot: ScheduleBot, session: dict, apps: Apps) -> None:
    apps.database_controller.clear_lessons()
    
    with open("schedule.json", "r", encoding="UTF-8") as file:
        data: list[list[dict[str, Any] | None]] = json_load(file)
        
        for day in range(len(data)):
            day_lessons = data[day]
            for lesson in range(len(day_lessons)):
                lesson_data = day_lessons[lesson]
                if lesson_data is None: continue
                
                apps.database_controller.add_new_lesson(
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
        
