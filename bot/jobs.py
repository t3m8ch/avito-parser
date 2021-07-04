from typing import Callable, Coroutine

import aiohttp
from aiogram import Bot

from bot.db.ad import BaseAdRepository
from bot.services.parsers.base import BaseParser

SendNewAdsJobCallback = Callable[[Bot, str, int], Coroutine]


async def send_new_ads_job(bot: Bot,
                           url: str,
                           chat_id: int,
                           ad_repo: BaseAdRepository,
                           parser: BaseParser):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    ads = parser.parse(html)
    ads = await ad_repo.add_ads(ads)

    if ads:
        for ad in ads:
            await bot.send_message(chat_id, str(ad))
