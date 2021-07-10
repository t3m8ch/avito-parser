from aiogram import Bot
from apscheduler.schedulers.base import BaseScheduler
from sqlalchemy.ext.asyncio import AsyncEngine

from bot.misc.config import config
from bot.db.ad import BaseAdRepository
from bot.db.alchemy.ad import AlchemyAdRepository
from bot.db.alchemy.subscription import AlchemySubscriptionRepository
from bot.db.subscription import BaseSubscriptionRepository
from bot.errors import NotValidUrlError
from bot.jobs import send_new_ads_job
from bot.models import SubscriptionModel
from bot.services.parsers.base import BaseParser


class AdService:
    def __init__(self,
                 ad_repo: BaseAdRepository,
                 subscription_repo: BaseSubscriptionRepository,
                 parser: BaseParser,  # TODO: Delegate the definition of the needed parser
                 scheduler: BaseScheduler,
                 bot: Bot):
        self._ad_repo = ad_repo
        self._subscription_repo = subscription_repo
        self._parser = parser
        self._scheduler = scheduler
        self._bot = bot

    async def subscribe_to_new_ads(self, subscription: SubscriptionModel):
        is_valid = self._parser.validate_url(subscription.url)
        if not is_valid:
            raise NotValidUrlError(subscription.url)

        await self._subscription_repo.add_subscription(subscription)
        self._add_job(subscription)

    async def get_subscriptions(self, chat_id: int) -> list[SubscriptionModel]:
        return await self._subscription_repo.get_subscriptions(chat_id)

    async def remove_subscription(self, sub_id: int):
        sub = await self._subscription_repo.remove_subscription(sub_id)
        self._remove_job(sub)

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
                      scheduler: BaseScheduler,
                      bot: Bot):
    ad_repo = AlchemyAdRepository(engine)
    subscription_repo = AlchemySubscriptionRepository(engine)

    return AdService(
        ad_repo, subscription_repo, parser, scheduler, bot
    )
