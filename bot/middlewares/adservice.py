from aiogram import types, Bot
from aiogram.dispatcher.middlewares import BaseMiddleware
from apscheduler.schedulers.base import BaseScheduler
from sqlalchemy.ext.asyncio import AsyncEngine

from bot.db.alchemy.ad import AlchemyAdRepository
from bot.db.alchemy.subscription import AlchemySubscriptionRepository
from bot.services.ad import create_ad_service
from bot.services.parsers.avito import AvitoParser


class AdServiceMiddleware(BaseMiddleware):
    def __init__(self,
                 alchemy_async_engine: AsyncEngine,
                 scheduler: BaseScheduler,
                 bot: Bot):
        self._alchemy_async_engine = alchemy_async_engine
        self._scheduler = scheduler
        self._bot = bot
        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        # TODO: Create an AdService instance only if required
        parser = AvitoParser()  # TODO: Add a check that the url links to Avito

        data["ad_service"] = create_ad_service(
            engine=self._alchemy_async_engine,
            parser=parser,
            scheduler=self._scheduler,
            bot=self._bot
        )
