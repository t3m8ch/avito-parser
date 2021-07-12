from aiogram import types

bot_commands = [
    types.BotCommand("subscribe", "подписаться на получения объявлений"),
    types.BotCommand("unsubscribe", "отписаться от получения объявлений"),
    types.BotCommand("getSpreadSheet", "получить таблицу с объявлениями"),
    types.BotCommand("cancel", "отменить действие"),
    types.BotCommand("help", "подробнее о командах"),
]
