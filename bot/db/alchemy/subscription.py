from typing import Optional

from sqlalchemy import select, delete, func
from sqlalchemy.dialects.postgresql import insert as psql_insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from bot.db.alchemy.tables import SubscriptionTable
from bot.db.subscription import BaseSubscriptionRepository
from bot.misc.errors import SubscriptionAlreadyExistsError
from bot.misc.models import SubscriptionModel


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
                    id=sub.id,
                    chat_id=sub.chat_id,
                    url=sub.url
                )
                for sub in subscriptions.scalars().all()
            )

    async def get_subscriptions_count(self, chat_id: int) -> int:
        async with AsyncSession(self._engine) as session:
            count = (await session.execute(
                select(func.count())
                    .where(SubscriptionTable.chat_id == chat_id)
            )).one()[0]

        return count

    async def remove_subscription(self, sub_id: int) -> SubscriptionModel:
        async with AsyncSession(self._engine) as session:
            sub = await session.execute(
                delete(SubscriptionTable)
                    .where(SubscriptionTable.id == sub_id)
                    .returning(SubscriptionTable)
            )
            await session.commit()

        sub = sub.fetchall()[0]
        return SubscriptionModel(
            id=sub.id,
            chat_id=sub.chat_id,
            url=sub.url
        )
