from abc import ABC, abstractmethod
from collections import Iterable
from typing import Optional

from bot.models import AdModel, SubscriptionModel


class BaseParser(ABC):
    @abstractmethod
    def parse(self, html: str, subscription: Optional[SubscriptionModel] = None) \
            -> Iterable[AdModel]:
        pass
