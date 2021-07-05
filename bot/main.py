import asyncio
import logging as log

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
from bot.services.parsers.avito import AvitoParser
from config import config, UpdateMethod
from handlers import register_handlers


async def on_startup(dp: Dispatcher):
    if config.tg_update_method == UpdateMethod.WEBHOOKS:
        await dp.bot.set_webhook(config.tg_webhook_url)

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

    # TODO: Refactor this
    subscriptions = event_loop.run_until_complete(AlchemySubscriptionRepository(engine).get_subscriptions())
    ad_repo = AlchemyAdRepository(engine)
    parser = AvitoParser()
    for sub in subscriptions:
        scheduler.add_job(
            send_new_ads_job,
            "interval",
            seconds=30,  # TODO: Change this value
            kwargs={
                "bot": bot,
                "url": sub.url,
                "chat_id": sub.chat_id,
                "ad_repo": ad_repo,
                "parser": parser
            },
        )

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
        executor.start_webhook(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            loop=event_loop,
            webhook_path=config.tg_webhook_path,
            host=config.webapp_host,
            port=config.webapp_port,
            skip_updates=True
        )


if __name__ == "__main__":
    run()
