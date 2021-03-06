import asyncio
import logging as log

import gspread_asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.utils import executor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.utils.initializing_app.google_api import get_google_api_credentials

from bot.utils.initializing_app.shutdown import on_shutdown
from bot.utils.initializing_app.ssl import get_ssl_context
from bot.utils.initializing_app.startup import on_startup
from sqlalchemy.ext.asyncio import create_async_engine

from bot.middlewares import setup_middlewares
from bot.services.ad import create_ad_service
from bot.services.parsers.avito import AvitoParser
from bot.utils.initializing_app.config import config, UpdateMethod
from handlers import register_handlers


def run():
    # Logging configuration
    log.basicConfig(
        level=log.getLevelName(config.log_level),
        format=config.log_format
    )

    # Event loop
    event_loop = asyncio.get_event_loop()

    # Storage
    if config.is_redis:
        storage = RedisStorage(
            config.redis_host,
            config.redis_port,
            config.redis_db,
            config.redis_password,
            loop=event_loop
        )
    else:
        storage = MemoryStorage()

    # Base
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

    # Google Sheets
    google_sheets_client_manager = gspread_asyncio \
        .AsyncioGspreadClientManager(get_google_api_credentials)

    # Subscriptions
    ad_service = create_ad_service(
        parser=AvitoParser(),
        engine=engine,
        scheduler=scheduler,
        google_sheets_client_manager=google_sheets_client_manager,
        bot=bot
    )
    event_loop.run_until_complete(ad_service.init_jobs())

    # Register
    register_handlers(dp)
    setup_middlewares(dp, engine, scheduler, google_sheets_client_manager, bot)

    # Start bot!
    if config.tg_update_method == UpdateMethod.LONG_POLLING:
        executor.start_polling(
            dispatcher=dp,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            loop=event_loop,
            skip_updates=config.tg_skip_updates
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
            skip_updates=config.tg_skip_updates,
            ssl_context=get_ssl_context()
        )


if __name__ == "__main__":
    run()
