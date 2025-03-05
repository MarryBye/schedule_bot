import google.generativeai as genai

from schedulebot.singleton import Singleton
from schedulebot.config import GEMINI_API_TOKEN, SQLITE_DBFILE, GROUP_ID
from schedulebot.controllers.database_controller import DatabaseController

genai.configure(api_key=GEMINI_API_TOKEN)

class AIController(genai.GenerativeModel, metaclass=Singleton):
    def __init__(self, model_name: str, *args, **kwargs) -> None:
        super().__init__(model_name, *args, **kwargs)