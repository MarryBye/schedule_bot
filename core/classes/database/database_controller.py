import os
import sqlite3 as sql

from typing import Any, Union
from core.classes.singleton import Singleton

class DatabaseController(metaclass=Singleton):
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        
        self.scripts: dict[str, str] = {}
        self.load_scripts()
        
    def load_scripts(self) -> None:
        scripts_folder = "./database/"
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