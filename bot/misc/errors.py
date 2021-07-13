from bot.misc.models import SubscriptionModel


class SubscriptionAlreadyExistsError(Exception):
    def __init__(self, subscription: SubscriptionModel):
        self.subscription = subscription


class NotValidUrlError(Exception):
    def __init__(self, url: str):
        self.url = url


class LimitSubscriptionsCountError(Exception):
    def __init__(self, max_count: int):
        self.max_count = max_count


class UserHasNoAdsError(Exception):
    pass
