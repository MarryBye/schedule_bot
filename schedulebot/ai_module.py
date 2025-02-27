import google.generativeai as genai

from schedulebot.config import GEMINI_API_TOKEN

genai.configure(api_key=GEMINI_API_TOKEN)

class BotAIModule(genai.GenerativeModel):
    def __init__(self, model_name: str, *args, **kwargs) -> None:
        super().__init__(model_name, *args, **kwargs)