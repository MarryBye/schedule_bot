from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

from schedulebot.apps import Apps

class AppsMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        pass

    async def __call__(
        self, 
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], 
        event: TelegramObject, 
        data: Dict[str, Any]
    ) -> Any:
        data["apps"] = Apps()
        return await handler(event, data)