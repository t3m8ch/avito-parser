import asyncio

import aiohttp
from aiogram import Bot

from bot.db.ad import BaseAdRepository
from bot.misc.models import SubscriptionModel
from bot.services.parsers.base import BaseParser


async def send_new_ads_job(bot: Bot,
                           url: str,
                           chat_id: int,
                           ad_repo: BaseAdRepository,
                           parser: BaseParser):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    ads = parser.parse(html, SubscriptionModel(
        chat_id=chat_id,
        url=url
    ))
    ads = await ad_repo.add_ads(ads)

    disable_notification = False
    if len(ads) > 1:
        await bot.send_message(chat_id, "Новые объявления!")
        disable_notification = True

    for ad in ads:
        price_text = f"{ad.price:f} рублей" if ad.price else "не указана"
        text = f"<b>{ad.title}</b>\n" \
               f"Цена: {price_text}\n\n" \
               f"{ad.url}"
        await bot.send_message(chat_id, text, disable_notification=disable_notification)
        await asyncio.sleep(1)
