from aiogram import types

from bot.misc import Router
from bot.services.ad import AdService

router = Router()


@router.message(state="*", commands="unsubscribe")
async def cmd_unsubscribe(message: types.Message, ad_service: AdService):
    chat_id = message.chat.id
    subs = enumerate(await ad_service.get_subscriptions(chat_id))

    text = f"От чего вы хотите отписаться?\n" + "\n".join(
        f"\n{i}. {sub.url}"
        for i, sub in subs
    )
    await message.answer(text)
