from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.keyboards.cancel import CANCEL
from bot.misc import Router

router = Router()


@router.callback_query(state="*", text=CANCEL)
async def cq_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.answer()


@router.message(state="*", commands="cancel")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено!")
