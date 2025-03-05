import pandas as pd
import re

from typing import Any
from datetime import date, datetime, timedelta

from schedulebot.language import *

def normalize_string(s: str) -> str:
    return " ".join(s.split())

def get_week(d: date=None) -> int:
    if d is None:
        d = date.today()
    first_week = date(year=d.year, month=8, day=5)
    today_week = (d - first_week).days // 7
    return today_week % 52 + 1

def form_lesson(lesson):
    start_time = datetime.strptime(lesson["time"], "%H:%M:%S")
    delta_time = timedelta(hours=1, minutes=20)
    end_time = start_time + delta_time

    end_time = end_time.strftime("%H:%M")
    start_time = start_time.strftime("%H:%M")
    
    lesson_text = lesson_text_template % (lesson["discipline_name"], start_time, end_time, lesson["teacher"], lesson_types[lesson["type"]], discipline_types[lesson["is_exam_discipline"]], lesson["period"], lesson["info"], lesson["zoom_link"])
    
    return lesson_text

def is_actual_lesson(lesson, d: date=None):
    if d is None:
        d = date.today()
    lesson_period = list(map(int, lesson["period"].split("-")))
    today_week = get_week(d)
    return lesson_period[0] <= today_week <= lesson_period[1]

def form_day_schedule(day_schedule: list[Any], d: date=None) -> str:
    if d is None:
        d = date.today()
    msg_text = "\nСегодня выходной"
    if day_schedule is None or len(day_schedule) == 0: return msg_text
    
    msg_text = ""
    for lesson in day_schedule:
        if is_actual_lesson(lesson, d):
            msg_text += form_lesson(lesson)
        
    return msg_text

def form_next_lesson(lesson: list[Any]) -> str:
    msg_text = "\nСегодня больше нет пар!"
    
    if lesson is None: return msg_text

    if is_actual_lesson(lesson):
        return form_lesson(lesson)
    
    return msg_text

def command_args_to_kvalues(msg: str) -> dict:
    kvalue_template = r'(\w+)="([\w\s\-:?!,\.@#$%^&*\(\)\"\'\`\;\<\>\\/|]+)"'
    return dict(re.findall(kvalue_template, msg))

def get_rows_from_kvalues(d: pd.DataFrame, kvalues: dict) -> pd.DataFrame:
    creation_date_filter = d['creation_date'] == kvalues.get('creation_date', None) if kvalues.get('creation_date', None) is not None else None
    creation_time_filter = d['creation_time'] >= kvalues.get('creation_time', None) if kvalues.get('creation_time', None) is not None else None
    author_username_filter = d['author_username'] == kvalues.get('author_username', None) if kvalues.get('author_username', None) is not None else None
    chat_id = d['chat_id'] == kvalues.get('chat_id', None) if kvalues.get('chat_id', None) is not None else None

    filters = []
    if creation_date_filter is not None:
        filters.append(creation_date_filter)
    if creation_time_filter is not None:
        filters.append(creation_time_filter)
    if author_username_filter is not None:
        filters.append(author_username_filter)
    if chat_id is not None:
        filters.append(chat_id)

    if filters:
        return d.loc[pd.concat(filters, axis=1).all(axis=1)]
    else:
        return d