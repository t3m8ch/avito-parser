from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from bot.misc import Router

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    text = "Приветствую! Это бот для получения уведомлений о новых объявлениях на Avito.\n\n" \
           "Чтобы им воспользоваться, введите в поиск на Авито ваш запрос, после чего " \
           "скопируй адрес, отправьте команду /subscribe, отправьте скопированный адрес и готово!\n\n" \
           "Если вы хотите отписаться от получения уведомлений, отправьте команду /unsubscribe и выберите, " \
           "от чего отписаться.\n\n" \
           "Все доступные команды - /help"
    await message.answer(text)


@router.message(CommandHelp())
async def cmd_help(message: types.Message):
    text = "Доступные команды:\n\n" \
           "/subscribe - <b>подписаться на уведомления о объявлениях</b>\n" \
           "После ввода команды необходимо отправить адрес, где нужно смотреть объявления.\n" \
           "Чтобы получить адрес, зайдите на Авито, введите в поиск нужный запрос и скопируйте " \
           "адрес из адресной строки браузера.\n\n" \
           "/unsubscribe - <b>отписаться от уведомлений о новых объявлениях</b>\n" \
           "После ввода команды будет предложено выбрать, от каких объявлений нужно отписаться.\n\n" \
           "/help - <b>получить справку о командах</b>"
    await message.answer(text)


@router.message()
async def cmd_not_found(message: types.Message):
    await message.answer("Такой команды не существует :(")


# -------- echo --------
@router.message()
async def echo(message: types.Message):
    await message.reply(message.text)
