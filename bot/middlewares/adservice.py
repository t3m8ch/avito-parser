from aiogram import types, Bot
from aiogram.dispatcher.middlewares import BaseMiddleware
from apscheduler.schedulers.base import BaseScheduler
from gspread_asyncio import AsyncioGspreadClientManager
from sqlalchemy.ext.asyncio import AsyncEngine

from bot.services.ad import create_ad_service, AdService
from bot.services.parsers.avito import AvitoParser


class AdServiceMiddleware(BaseMiddleware):
    def __init__(self,
                 alchemy_async_engine: AsyncEngine,
                 scheduler: BaseScheduler,
                 gspread_client_manager: AsyncioGspreadClientManager,
                 bot: Bot):
        self._gspread_client_manager = gspread_client_manager
        self._alchemy_async_engine = alchemy_async_engine
        self._scheduler = scheduler
        self._bot = bot
        super().__init__()

    def _get_service(self) -> AdService:
        # TODO: Create an AdService instance only if required
        parser = AvitoParser()  # TODO: Add a check that the url links to Avito

        return create_ad_service(
            engine=self._alchemy_async_engine,
            parser=parser,
            scheduler=self._scheduler,
            spreadsheet_client_manager=self._gspread_client_manager,
            bot=self._bot
        )

    async def on_process_message(self, message: types.Message, data: dict):
        data["ad_service"] = self._get_service()

    async def on_process_callback_query(self, message: types.Message, data: dict):
        data["ad_service"] = self._get_service()
