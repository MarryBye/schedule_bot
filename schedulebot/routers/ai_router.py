from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from schedulebot.functions import command_args_to_kvalues, get_rows_from_kvalues

from schedulebot.schedulebot import Bot

router: Router = Router(name=__name__)
    
@router.message(Command("custom_prompt"))
async def custom_prompt(msg: Message, command: CommandObject, bot: Bot) -> None:
    
    command_args_string: str = "".join(command.args)
    
    kvalues = command_args_to_kvalues(command_args_string)
    kvalues["chat_id"] = msg.chat.id

    if "prompt" not in kvalues:
        await msg.reply("Необходимо указать параметр prompt")
        return
    
    filtered_records = get_rows_from_kvalues(bot.messages_set, kvalues)
    response = bot.generate_content([f"{kvalues["prompt"]}. Чтобы ответить на вопрос, ты можешь использовать данные: {filtered_records.to_string()}, можешь также писать что-то от себя, если это уместно для указанного вопроса."])
    print(f"{kvalues["prompt"]}. Используй для этого следующие данные: {filtered_records.to_string()}")
    
    await msg.reply(response, parse_mode="HTML")