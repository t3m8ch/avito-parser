from abc import ABC, abstractmethod
from collections import Iterable
from typing import Optional

from bot.misc.models import AdModel, SubscriptionModel


class BaseParser(ABC):
    @abstractmethod
    def validate_url(self, url: str) -> bool:
        pass

    @abstractmethod
    def correct_url(self, url: str) -> str:
        pass

    @abstractmethod
    def parse(self, html: str, subscription: Optional[SubscriptionModel] = None) \
            -> Iterable[AdModel]:
        pass
