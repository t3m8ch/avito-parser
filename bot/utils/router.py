from collections import Callable

from aiogram import Dispatcher


class Router:
    """It is for registering handlers using decorators,
    but without the global dispatcher variable"""

    def __init__(self):
        self._handlers = []

    def add_handler(self,
                    handler: Callable,
                    handler_registrar: Callable,
                    *args, **kwargs):
        """Handlers added by this method will be registered when
        the register_handlers method is called"""
        self._handlers.append((
            handler,
            handler_registrar,
            args,
            kwargs
        ))

    def handler(self, handler_registrar, *args, **kwargs):
        """Handlers with this decorator will be registered when
        the register_handlers method is called

        Example:
        >>> from aiogram import types, Dispatcher
        >>> from aiogram.dispatcher.filters import CommandStart
        >>>
        >>> from bot.misc.router import Router
        >>>
        >>> router = Router()
        >>>
        >>>
        >>> @router.handler(Dispatcher.register_message_handler, CommandStart())
        ... async def cmd_start(message: types.Message):
        ...     await message.reply("I'm bot!")
        """

        def decorator(handler):
            self.add_handler(handler, handler_registrar, *args, **kwargs)
            return handler

        return decorator

    def message(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_message_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def edited_message(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_edited_message_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def channel_post(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_channel_post_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def edited_channel_post(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_edited_channel_post_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def inline(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_inline_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def chosen_inline(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_chosen_inline_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def callback_query(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_callback_query_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def shipping_query(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_shipping_query_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def pre_checkout_query(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_pre_checkout_query_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def poll(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_poll_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def poll_answer(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_poll_answer_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def my_chat_member(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_my_chat_member_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def chat_member(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_chat_member_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def errors(self, *args, **kwargs):
        def decorator(handler):
            self.add_handler(handler,
                             Dispatcher.register_errors_handler,
                             *args, **kwargs)
            return handler

        return decorator

    def register_handlers(self, dp: Dispatcher):
        """Registers all headers added by the add_handler
        method or with the handler decorator"""
        for handler, registrar, args, kwargs in self._handlers:
            registrar(dp, handler, *args, **kwargs)
