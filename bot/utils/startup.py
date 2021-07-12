from aiogram import Dispatcher

import logging as log

from .config import config, UpdateMethod


async def on_startup(dp: Dispatcher):
    if config.tg_update_method == UpdateMethod.WEBHOOKS:
        if config.ssl_is_set:
            with open(config.ssl_certificate_path, 'rb') as file:
                ssl_certificate = file.read()
        else:
            ssl_certificate = None

        await dp.bot.set_webhook(
            url=config.tg_webhook_url,
            certificate=ssl_certificate
        )

    log.warning("START BOT!")
