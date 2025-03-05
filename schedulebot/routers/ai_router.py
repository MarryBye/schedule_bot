from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject

from schedulebot.schedulebot import ScheduleBot
from schedulebot.apps import Apps
from schedulebot.functions import command_args_to_kvalues, get_rows_from_kvalues

router: Router = Router(name=__name__)
    
@router.message(Command("custom_prompt"))
async def custom_prompt(msg: Message, command: CommandObject, bot: ScheduleBot, session: dict, apps: Apps) -> None:
    
    command_args_string: str = "".join(command.args)
    
    kvalues = command_args_to_kvalues(command_args_string)
    kvalues["chat_id"] = msg.chat.id

    if "prompt" not in kvalues:
        await msg.reply("Необходимо указать параметр prompt")
        return
    
    response = apps.ai_controller.generate_content(f"{kvalues["prompt"]}.")
    
    await msg.reply(response, parse_mode="HTML")