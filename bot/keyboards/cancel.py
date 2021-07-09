from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

CANCEL = "cancel"


def get_cancel_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=CANCEL
        )
    )
    return keyboard
