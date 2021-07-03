from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from bot.misc import Router

router = Router()


# -------- /start --------
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.reply("Hello!")


# -------- echo --------
@router.message()
async def echo(message: types.Message):
    await message.reply(message.text)
