from typing import Iterable

from sqlalchemy.dialects.postgresql import insert as psql_insert
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from bot.db.ad import BaseAdRepository
from bot.db.alchemy.tables import AdTable
from bot.models import AdModel


class AlchemyAdRepository(BaseAdRepository):
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    async def add_ads(self, ads: Iterable[AdModel]) -> Iterable[AdModel]:
        async with AsyncSession(self._engine, future=True) as session:
            rows = await session.execute(
                psql_insert(AdTable)
                .values([ad.dict() for ad in ads])
                .on_conflict_do_nothing(
                    index_elements=['url']
                )
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
