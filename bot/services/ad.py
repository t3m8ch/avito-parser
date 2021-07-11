from aiogram import Bot
from apscheduler.schedulers.base import BaseScheduler
from gspread_asyncio import AsyncioGspreadClientManager
from sqlalchemy.ext.asyncio import AsyncEngine

from bot.services.google_sheets import GoogleSheetsService
from bot.utils.config import config
from bot.db.ad import BaseAdRepository
from bot.db.alchemy.ad import AlchemyAdRepository
from bot.db.alchemy.subscription import AlchemySubscriptionRepository
from bot.db.subscription import BaseSubscriptionRepository
from bot.misc.errors import NotValidUrlError, LimitSubscriptionsCountError
from bot.jobs import send_new_ads_job
from bot.misc.models import SubscriptionModel
from bot.services.parsers.base import BaseParser


class AdService:
    def __init__(self,
                 ad_repo: BaseAdRepository,
                 subscription_repo: BaseSubscriptionRepository,
                 parser: BaseParser,  # TODO: Delegate the definition of the needed parser
                 google_sheets_service: GoogleSheetsService,
                 scheduler: BaseScheduler,
                 bot: Bot):
        self._ad_repo = ad_repo
        self._subscription_repo = subscription_repo
        self._parser = parser
        self._google_sheets_service = google_sheets_service
        self._scheduler = scheduler
        self._bot = bot

    async def subscribe_to_new_ads(self, subscription: SubscriptionModel):
        is_valid = self._parser.validate_url(subscription.url)
        if not is_valid:
            raise NotValidUrlError(subscription.url)

        corrected_url = self._parser.correct_url(subscription.url)

        subscriptions_count = await self._subscription_repo \
            .get_subscriptions_count(subscription.chat_id)

        if subscriptions_count >= 2:
            raise LimitSubscriptionsCountError(2)

        corrected_subscription = SubscriptionModel(
            id=subscription.id,
            chat_id=subscription.chat_id,
            url=corrected_url
        )

        await self._subscription_repo.add_subscription(corrected_subscription)
        self._add_job(corrected_subscription)

    async def get_subscriptions(self, chat_id: int) -> list[SubscriptionModel]:
        return await self._subscription_repo.get_subscriptions(chat_id)

    async def remove_subscription(self, sub_id: int):
        sub = await self._subscription_repo.remove_subscription(sub_id)
        self._remove_job(sub)

    async def get_url_to_ads_google_spreadsheets(self, chat_id: int) -> str:
        ads = await self._ad_repo.get_ads(chat_id)
        return await self._google_sheets_service \
            .get_url_to_ads_spreadsheet(ads)

    async def init_jobs(self):
        subscriptions = await self._subscription_repo.get_subscriptions()
        for sub in subscriptions:
            self._add_job(sub)

    def _add_job(self, subscription: SubscriptionModel):
        self._scheduler.add_job(
            send_new_ads_job,
            "interval",
            seconds=config.check_interval_seconds,  # TODO: Change this value
            kwargs={
                "bot": self._bot,
                "url": subscription.url,
                "chat_id": subscription.chat_id,
                "ad_repo": self._ad_repo,
                "parser": self._parser
            },
        )

    def _remove_job(self, subscription: SubscriptionModel):
        job = filter(
            lambda j: j.kwargs["chat_id"] == subscription.chat_id and j.kwargs["url"] == subscription.url,
            self._scheduler.get_jobs()
        ).__next__()
        self._scheduler.remove_job(job.id)


def create_ad_service(*,
                      parser: BaseParser,
                      engine: AsyncEngine,
                      google_sheets_client_manager: AsyncioGspreadClientManager,
                      scheduler: BaseScheduler,
                      bot: Bot):
    ad_repo = AlchemyAdRepository(engine)
    subscription_repo = AlchemySubscriptionRepository(engine)
    google_sheets_service = GoogleSheetsService(google_sheets_client_manager)

    return AdService(
        ad_repo, subscription_repo, parser, google_sheets_service, scheduler, bot
    )
