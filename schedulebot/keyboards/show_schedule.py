from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from schedulebot.controllers.keyboards_controller import KeyboardsController

KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️", callback_data="schedule_selector|minus_day"), InlineKeyboardButton(text="День", callback_data="decoration", ), InlineKeyboardButton(text="➡️", callback_data="schedule_selector|plus_day")]
    ]
)

KeyboardsController().add_keyboard("show_schedule", KEYBOARD)