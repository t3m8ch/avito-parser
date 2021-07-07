from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as psql_insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from bot.db.alchemy.tables import SubscriptionTable
from bot.db.subscription import BaseSubscriptionRepository
from bot.errors import SubscriptionAlreadyExistsError
from bot.models import SubscriptionModel


class AlchemySubscriptionRepository(BaseSubscriptionRepository):
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    async def add_subscription(self, subscription: SubscriptionModel):
        async with AsyncSession(self._engine) as session:
            subs = (await session.execute(
                psql_insert(SubscriptionTable).values(
                    chat_id=subscription.chat_id,
                    url=subscription.url
                ).on_conflict_do_nothing()
                .returning(SubscriptionTable.id)
            )).fetchall()

            if not subs:
                raise SubscriptionAlreadyExistsError()

            await session.commit()

    async def get_subscriptions(self, chat_id: Optional[int] = None) \
            -> list[SubscriptionModel]:
        query = select(SubscriptionTable)
        if chat_id:
            query = query.where(SubscriptionTable.chat_id == chat_id)

        async with AsyncSession(self._engine) as session:
            subscriptions = await session.execute(query)

            return list(
                SubscriptionModel(
                    chat_id=sub.chat_id,
                    url=sub.url
                )
                for sub in subscriptions.scalars().all()
            )
