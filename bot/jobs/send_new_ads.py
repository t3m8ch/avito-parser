import asyncio
from typing import Callable, Coroutine, NewType

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

    for ad in ads:
        text = f"<b>{ad.title}</b>\n" \
               f"Цена: {'{0:f}'.format(ad.price) + ' рублей' or 'не указана'}\n\n" \
               f"{ad.url}"
        await bot.send_message(chat_id, text)
        await asyncio.sleep(1)
