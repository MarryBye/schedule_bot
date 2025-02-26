from typing import Any
from datetime import date, datetime, timedelta

from schedulebot.language import *

def get_today_week() -> int:
    date_now = date.today()
    if 1 <= date_now.month <= 8:
        first_week = date(year=date_now.year - 1, month=8, day=1)
    else:
        first_week = date(year=date_now.year, month=8, day=1)
    today_week = round((date_now - first_week).days / 7)
    
    return today_week

def form_lesson(lesson):
    start_time = datetime.strptime(lesson["time"], "%H:%M:%S")
    delta_time = timedelta(hours=1, minutes=30)
    end_time = start_time + delta_time

    end_time = end_time.strftime("%H:%M")
    start_time = start_time.strftime("%H:%M")
    
    lesson_text = lesson_text_template % (lesson["discipline_name"], start_time, end_time, lesson["teacher"], lesson_types[lesson["type"]], discipline_types[lesson["is_exam_discipline"]], lesson["info"], lesson["zoom_link"])
    
    return lesson_text

def is_actual_lesson(lesson):
    lesson_period = list(map(int, lesson["period"].split("-")))
    today_week = get_today_week()
    return lesson_period[0] <= today_week <= lesson_period[1]

def form_day_schedule(day_schedule: list[Any]) -> str:
    msg_text = "Сегодня выходной"
    
    if day_schedule is None or len(day_schedule) == 0: return msg_text
    
    msg_text = ""
    for lesson in day_schedule:
        if is_actual_lesson(lesson):
            msg_text += form_lesson(lesson)
        
    return msg_text

def form_next_lesson(lesson: list[Any]) -> str:
    msg_text = "Сегодня больше нет пар!"
    
    if lesson is None: return msg_text

    if is_actual_lesson(lesson):
        return form_lesson(lesson)
    
    return msg_text