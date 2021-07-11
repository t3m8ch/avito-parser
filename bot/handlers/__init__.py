from bot.handlers import google_sheets

from . import (
    general,
    subscribe,
    unsubscribe,
    cancel
)


def register_handlers(dp):
    """A function that registers all handlers.
    Example of registration of several handlers:

       from . import module1
       from . import module2

       module1.router.register_handlers(dp)
       module2.router.register_handlers(dp)

    Each handler module must contain a router object.
    Remember that the order of handlers is important!
    """
    cancel.router.register_handlers(dp)
    google_sheets.router.register_handlers(dp)
    subscribe.router.register_handlers(dp)
    unsubscribe.router.register_handlers(dp)
    general.router.register_handlers(dp)
