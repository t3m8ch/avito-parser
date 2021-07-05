from typing import Optional

from aiogram import Bot
from apscheduler.schedulers.base import BaseScheduler

from bot.db.ad import BaseAdRepository
from bot.db.subscription import BaseSubscriptionRepository
from bot.jobs import send_new_ads_job, SendNewAdsJobCallback
from bot.models import SubscriptionModel
from bot.services.parsers.base import BaseParser


class AdService:
    def __init__(self,
                 ad_repo: BaseAdRepository,
                 subscription_repo: BaseSubscriptionRepository,
                 parser: BaseParser,
                 scheduler: BaseScheduler,
                 bot: Bot):
        self._ad_repo = ad_repo
        self._subscription_repo = subscription_repo
        self._parser = parser
        self._scheduler = scheduler
        self._bot = bot

    async def subscribe_to_new_ads(self, subscription: SubscriptionModel):
        await self._subscription_repo.add_subscription(subscription)
        self._add_job(subscription)

    def _add_job(self, subscription: SubscriptionModel):
        self._scheduler.add_job(
            send_new_ads_job,
            "interval",
            seconds=30,  # TODO: Change this value
            kwargs={
                "bot": self._bot,
                "url": subscription.url,
                "chat_id": subscription.chat_id,
                "ad_repo": self._ad_repo,
                "parser": self._parser
            },
        )


# TODO: Remove this
async def create_ad_service(*,
                            ad_repo: BaseAdRepository,
                            subscription_repo: BaseSubscriptionRepository,
                            parser: BaseParser,
                            scheduler: BaseScheduler,
                            bot: Bot):
    service = AdService(
        ad_repo, subscription_repo, parser, scheduler, bot
    )

    return service
