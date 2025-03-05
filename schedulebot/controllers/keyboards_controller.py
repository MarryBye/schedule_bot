from schedulebot.singleton import Singleton
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

class KeyboardsController(metaclass=Singleton):
    def __init__(self):
        self.keyboards = {}
        
    def add_keyboard(self, name: str, keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup) -> None:
        self.keyboards[name] = keyboard
        
    def get_keyboard(self, name: str) -> InlineKeyboardMarkup | ReplyKeyboardMarkup:
        return self.keyboards[name]