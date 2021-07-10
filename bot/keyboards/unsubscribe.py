from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.keyboards.cancel import CANCEL
from bot.models import SubscriptionModel

unsubscribe_cd = CallbackData("unsubscribe", "subscribe_id")


def get_unsubscribe_keyboard(subscriptions: list[tuple[int, SubscriptionModel]]) \
        -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=5)

    buttons = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=unsubscribe_cd.new(
                subscribe_id=str(sub.id)
            )
        )
        for i, sub in subscriptions
    ]
    keyboard.add(*buttons)

    keyboard.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=CANCEL
        )
    )

    return keyboard
