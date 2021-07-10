from abc import ABC, abstractmethod
from typing import Optional

from bot.misc.models import SubscriptionModel


class BaseSubscriptionRepository(ABC):
    @abstractmethod
    async def add_subscription(self, subscription: SubscriptionModel):
        pass

    @abstractmethod
    async def get_subscriptions(self, chat_id: Optional[int] = None) \
            -> list[SubscriptionModel]:
        pass

    @abstractmethod
    async def remove_subscription(self, sub_id: int) -> SubscriptionModel:
        pass
