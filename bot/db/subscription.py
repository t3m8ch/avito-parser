from abc import ABC, abstractmethod

from bot.models import SubscriptionModel


class BaseSubscriptionRepository(ABC):
    @abstractmethod
    async def add_subscription(self, subscription: SubscriptionModel):
        pass

    @abstractmethod
    async def get_subscriptions(self) -> list[SubscriptionModel]:
        pass
