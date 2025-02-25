import datetime

from typing import Any
from core.classes.database.database_controller import DatabaseController
from language import *

db_controller = DatabaseController("suitt_schedule.db")

def get_today_week() -> int:
    date_now = datetime.date.today()
    if 1 <= date_now.month <= 8:
        first_week = datetime.date(year=date_now.year - 1, month=8, day=1)
    else:
        first_week = datetime.date(year=date_now.year - 1, month=8, day=1)
    today_week = round((date_now - first_week).days / 7)
    
    return today_week

def form_lesson(lesson):
    start_time = datetime.datetime.strptime(lesson["time"], "%H:%M:%S")
    delta_time = datetime.timedelta(hours=1, minutes=30)
    end_time = start_time + delta_time

    end_time = end_time.strftime("%H:%M")
    start_time = start_time.strftime("%H:%M")
    
    lesson_text = lesson_text_template % (start_time, end_time, discipline_types[lesson["is_exam_discipline"]], lesson["discipline_name"], lesson["teacher"], lesson_types[lesson["type"]], lesson["info"], lesson["zoom_link"])
    
    return lesson_text
    
def get_day_schedule(day: int) -> str:
    day_schedule: list[Any] | None = db_controller.execute("get_day_lessons.sql", day)
    msg_text = ""
    
    today_week = get_today_week()
    
    if day_schedule is not None:
        s = f"**{week_days[day]}**\n"
        for lesson in day_schedule:
            lesson_period = list(map(int, lesson["period"].split("-")))
            if lesson_period[0] <= today_week <= lesson_period[1]:
                s += form_lesson(lesson)
        msg_text = s
    else:
        msg_text = "Сегодня выходной"
        
    return msg_text

def get_next_lesson(day: int) -> str:
    next_lesson: list[Any] | None = db_controller.execute("get_next_lesson.sql", day, fetch_count=1)
    msg_text = ""
    
    today_week = get_today_week()
    
    if next_lesson is not None:
        s = f"**{week_days[day]}**\n"
        lesson_period = list(map(int, next_lesson["period"].split("-")))
        if lesson_period[0] <= today_week <= lesson_period[1]:
            s += form_lesson(next_lesson)
        msg_text = s
    else:
        msg_text = "На сегодня пар хватит"
    return msg_text