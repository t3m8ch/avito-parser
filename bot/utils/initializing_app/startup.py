from aiogram import Dispatcher

import logging as log

from .config import config, UpdateMethod
from .ssl import get_ssl_certificate_bytes


async def on_startup(dp: Dispatcher):
    if config.tg_update_method == UpdateMethod.WEBHOOKS:
        await dp.bot.set_webhook(
            url=config.tg_webhook_url,
            certificate=get_ssl_certificate_bytes()
        )

    log.warning("START BOT!")
