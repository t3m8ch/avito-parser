from typing import Iterable

from sqlalchemy import select, join
from sqlalchemy.dialects.postgresql import insert as psql_insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from bot.db.ad import BaseAdRepository
from bot.db.alchemy.tables import AdTable, SubscriptionTable
from bot.misc.models import AdModel


class AlchemyAdRepository(BaseAdRepository):
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    async def add_ads(self, ads: Iterable[AdModel]) -> Iterable[AdModel]:
        ads = [
            {
                "title": ad.title,
                "price": ad.price,
                "url": ad.url,
                "subscription_id": select(SubscriptionTable.id)
                    .where(SubscriptionTable.chat_id == ad.subscription.chat_id)
                    .where(SubscriptionTable.url == ad.subscription.url)
            }
            for ad in ads
        ]
        if not ads:
            return []

        async with AsyncSession(self._engine, future=True) as session:
            rows = await session.execute(
                psql_insert(AdTable)
                    .values(ads)
                    .on_conflict_do_nothing()
                    .returning(AdTable)
            )
            await session.commit()

            return [
                AdModel(
                    title=row.title,
                    price=row.price,
                    url=row.url
                )
                for row in rows
            ]

    async def get_ads(self, chat_id: int) -> Iterable[AdModel]:
        joined = join(AdTable, SubscriptionTable,
                      AdTable.subscription_id == SubscriptionTable.id)

        query = select(AdTable, SubscriptionTable.chat_id) \
                .select_from(joined) \
                .where(SubscriptionTable.chat_id == chat_id)

        async with AsyncSession(self._engine, future=True) as session:
            rows = (await session.execute(query)).scalars().all()

        return [
            AdModel(
                title=row.title,
                price=row.price,
                url=row.url
            )
            for row in rows
        ]
