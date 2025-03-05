import os
import sqlite3 as sql

from typing import Any, Union
from schedulebot.singleton import Singleton
from datetime import datetime

class DatabaseController(metaclass=Singleton):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        
        self.scripts: dict[str, str] = {}
        self.load_scripts()
        
    def load_scripts(self) -> None:
        scripts_folder = "./schedulebot/database/"
        for script in os.listdir(scripts_folder):
            script_path = os.path.join(scripts_folder, script)
            with open(script_path, "r", encoding="UTF-8") as file:
                self.scripts[script] = file.read()
    
    def get_script(self, script_name: str) -> str:
        return self.scripts.get(script_name, "None")
    
    def connect(self) -> None:
        self.connection: sql.Connection = sql.connect(self.db_name)
        self.connection.row_factory = sql.Row
        self.cursor: sql.Cursor = self.connection.cursor()
        
    def disconnect(self) -> None:
        self.cursor.close()
        self.connection.close()
        
    def execute(self, script_name: str, *args: Any, fetch_count: int=-1) -> Union[Any, None]:
        result = None
        try:
            self.cursor.execute(self.get_script(script_name), args)
            self.connection.commit()
            match fetch_count:
                case -1: result = self.cursor.fetchall()
                case 1: result = self.cursor.fetchone()
                case _: result = self.cursor.fetchmany(fetch_count)
            print(f"Successfully completed script: {script_name}!")
        except Exception as e:
            print(f"Error with script {script_name}: {e}")
            self.connection.rollback()
        finally:
            return result
        
    def add_new_lesson(self, day_of_week: int, time: str, teacher_id: int, discipline_id: int, zoom_link: str, period: str, additional_info: str, type: int):
        self.execute("add_new_lesson.sql", day_of_week, time, teacher_id, discipline_id, zoom_link, period, additional_info, type)
        
    def clear_lessons(self):
        self.execute("clear_schedule.sql")
        
    def recreate_tables(self):
        self.execute("create_tables.sql")
        
    def get_day_lessons(self, week_day: int=-1):
        if week_day == -1: week_day = datetime.now().weekday()
        result = self.execute("get_day_lessons.sql", week_day)
        return result
    
    def get_next_lesson(self, week_day: int=-1, after_time: str="now"):
        if week_day == -1: week_day = datetime.now().weekday()
        if after_time == "now": after_time = datetime.now().strftime("%H:%M")
        result = self.execute("get_next_lesson.sql", week_day, after_time, fetch_count=1)
        return result