from abc import abstractmethod, ABC
from collections import Iterable

from bot.misc.models import AdModel


class BaseAdRepository(ABC):
    @abstractmethod
    async def add_ads(self, ads: Iterable[AdModel]) -> Iterable[AdModel]:
        """Adds nonexistent ads and returns only those ads that were added"""
        pass

    @abstractmethod
    async def get_ads(self, chat_id: int) -> Iterable[AdModel]:
        pass
