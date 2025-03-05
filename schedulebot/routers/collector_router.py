import pandas as pd

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from schedulebot.schedulebot import ScheduleBot
from schedulebot.functions import normalize_string

# router: Router = Router(name=__name__)

# @router.message()
# async def collect_data(msg: Message, bot: ScheduleBot) -> None:
#     chat_id = msg.chat.id
#     text = normalize_string(msg.text) if msg.text is not None else None
#     author_id = msg.from_user.id
#     author_name = msg.from_user.full_name
#     author_username = msg.from_user.username
#     is_bot = msg.from_user.is_bot
#     is_answer = msg.reply_to_message is not None
#     answerred_text = normalize_string(msg.reply_to_message.text) if is_answer else None
#     answerred_author_id = msg.reply_to_message.from_user.id if is_answer else None
#     answerred_author_name = msg.reply_to_message.from_user.full_name if is_answer else None
#     creation_date = msg.date.date().strftime("%d-%m-%Y")
#     creation_time = msg.date.time().strftime("%H:%M")
#     chat_type = msg.chat.type
    
#     if is_bot: return
#     if text is None: return
    
#     new_message = pd.DataFrame(
#         {
#             "author_id": [author_id],
#             "author_name": [author_name],
#             "author_username": [author_username],
#             "creation_date": [creation_date],
#             "creation_time": [creation_time],
#             "chat_id": [chat_id],
#             "chat_type": [chat_type],
#             "text": [text],
#             "is_answer": [is_answer],
#             "answerred_text": [answerred_text],
#             "answerred_author_id": [answerred_author_id],
#             "answerred_author_name": [answerred_author_name]
#         }
#     )
    
#     bot.messages_set = bot.messages_set._append(new_message, ignore_index=True)