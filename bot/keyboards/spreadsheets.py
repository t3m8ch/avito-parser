from enum import Enum

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

spreadsheets_processor_cq = CallbackData("spreadsheets_processor", "name")


class SpreadsheetsProcessor(str, Enum):
    GOOGLE_SPREADSHEETS = "gspread"


def get_spreadsheets_processor_choice_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    buttons = [
        InlineKeyboardButton(
            "Google Таблицы",
            callback_data=spreadsheets_processor_cq.new(
                name=SpreadsheetsProcessor.GOOGLE_SPREADSHEETS
            )
        )
    ]

    keyboard.add(*buttons)
    return keyboard
