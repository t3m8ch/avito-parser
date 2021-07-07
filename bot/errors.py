class SubscriptionAlreadyExistsError(Exception):
    pass


class NotValidUrlError(Exception):
    def __init__(self, url: str):
        self.url = url
