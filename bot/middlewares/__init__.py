from aiogram import Dispatcher, Bot
from apscheduler.schedulers.base import BaseScheduler
from gspread_asyncio import AsyncioGspreadClientManager
from sqlalchemy.ext.asyncio import AsyncEngine

from bot.middlewares.adservice import AdServiceMiddleware


def setup_middlewares(dp: Dispatcher,
                      alchemy_async_engine: AsyncEngine,
                      scheduler: BaseScheduler,
                      gspread_client_manager: AsyncioGspreadClientManager,
                      bot: Bot):
    dp.setup_middleware(AdServiceMiddleware(
        alchemy_async_engine,
        scheduler,
        gspread_client_manager,
        bot
    ))
