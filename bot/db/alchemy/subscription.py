from typing import AsyncIterable

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from bot.db.alchemy.tables import SubscriptionTable
from bot.db.subscription import BaseSubscriptionRepository
from bot.models import SubscriptionModel


class AlchemySubscriptionRepository(BaseSubscriptionRepository):
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    async def add_subscription(self, subscription: SubscriptionModel):
        # TODO: Add existing URL error handling
        async with AsyncSession(self._engine) as session:
            await session.execute(
                insert(SubscriptionTable).values(
                    chat_id=subscription.chat_id,
                    url=subscription.url
                )
            )
            await session.commit()

    async def get_subscriptions(self) -> list[SubscriptionModel]:
        async with AsyncSession(self._engine) as session:
            subscriptions = await session.execute(
                select(SubscriptionTable)
            )

            return list(
                SubscriptionModel(
                    chat_id=sub.chat_id,
                    url=sub.url
                )
                for sub in subscriptions.scalars().all()
            )
