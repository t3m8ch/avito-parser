from aiogram import types

from bot.keyboards.unsubscribe import get_unsubscribe_keyboard, unsubscribe_cd
from bot.misc import Router
from bot.models import SubscriptionModel
from bot.services.ad import AdService

router = Router()


@router.message(state="*", commands="unsubscribe")
async def cmd_unsubscribe(message: types.Message, ad_service: AdService):
    chat_id = message.chat.id

    subs = list(
        enumerate(
            await ad_service.get_subscriptions(chat_id),
            start=1
        )
    )

    await message.answer(
        _get_message_text(subs),
        reply_markup=get_unsubscribe_keyboard(subs)
    )


@router.callback_query(unsubscribe_cd.filter())
async def cq_unsubscribe(call: types.CallbackQuery,
                         callback_data: dict,
                         ad_service: AdService):
    sub_id = int(callback_data["subscribe_id"])
    await ad_service.remove_subscription(sub_id)  # TODO: Add processing of a non-existent subscription

    await call.answer(
        text="Вы успешно отписались от этих объявлений",
        show_alert=True
    )


def _get_message_text(subscriptions: list[tuple[int, SubscriptionModel]]):
    if not subscriptions:
        return "Вам не от чего отписываться"

    return f"От чего вы хотите отписаться?\n" + "\n".join(
        f"\n{i}. {sub.url}"
        for i, sub in subscriptions
    )
