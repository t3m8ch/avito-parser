import asyncio
import logging as log
import ssl

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import create_async_engine

from bot.db.alchemy.ad import AlchemyAdRepository
from bot.db.alchemy.subscription import AlchemySubscriptionRepository
from bot.jobs import send_new_ads_job
from bot.middlewares import setup_middlewares
from bot.services.ad import create_ad_service
from bot.services.parsers.avito import AvitoParser
from config import config, UpdateMethod
from handlers import register_handlers


async def on_startup(dp: Dispatcher):
    if config.tg_update_method == UpdateMethod.WEBHOOKS:

        with open(config.ssl_certificate_path, 'rb') as file:
            ssl_certificate = file.read()

        await dp.bot.set_webhook(
            url=config.tg_webhook_url,
            certificate=ssl_certificate
        )

    log.warning("START BOT!")


async def on_shutdown(dp: Dispatcher):
    await dp.bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    log.warning("BOT STOPPED!")


def run():
    # Logging configuration
    log.basicConfig(
        level=config.log_level,
        format=config.log_format
    )

    # Base
    event_loop = asyncio.get_event_loop()
    storage = MemoryStorage()  # TODO: Redis
    bot = Bot(
        token=config.tg_token,
        parse_mode=config.tg_parse_mode
    )
    dp = Dispatcher(bot, storage=storage)

    # DB
    engine = create_async_engine(config.db_url)

    # Scheduler
    scheduler = AsyncIOScheduler(
        jobstores={
            "default": MemoryJobStore()
        }
    )
    scheduler.start()

    # Subscriptions
    ad_service = create_ad_service(
        parser=AvitoParser(),
        engine=engine,
        scheduler=scheduler,
        bot=bot
    )
    event_loop.run_until_complete(ad_service.init_jobs())

    # Register
    register_handlers(dp)
    setup_middlewares(dp, engine, scheduler, bot)

    # Start bot!
    if config.tg_update_method == UpdateMethod.LONG_POLLING:
        executor.start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            loop=event_loop,
            skip_updates=True
        )

    elif config.tg_update_method == UpdateMethod.WEBHOOKS:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(
            config.ssl_certificate_path,
            config.ssl_private_key_path
        )

        executor.start_webhook(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            loop=event_loop,
            webhook_path=config.tg_webhook_path,
            host=config.webapp_host,
            port=config.webapp_port,
            skip_updates=True,
            ssl_context=ssl_context
        )


if __name__ == "__main__":
    run()
