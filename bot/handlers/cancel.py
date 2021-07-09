from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.misc import Router

router = Router()


@router.message(commands="cancel", state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено!")
