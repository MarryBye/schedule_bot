from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from schedulebot.controllers.session_controller import SessionController

class SessionMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        if data["event_from_user"]:
            data["session"] = SessionController().get_session(data["event_from_user"].id)
        return await handler(event, data)