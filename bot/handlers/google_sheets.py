from aiogram import types

from bot.keyboards.spreadsheets import (
    get_spreadsheets_processor_choice_keyboard,
    spreadsheets_processor_cq,
    SpreadsheetsProcessor
)
from bot.services.ad import AdService
from bot.utils import Router

router = Router()


@router.message(commands="getSpreadSheet")
async def cmd_get_spreadsheet(message: types.Message):
    await message.answer(
        "Где вы хотите создать таблицу?",
        reply_markup=get_spreadsheets_processor_choice_keyboard()
    )


@router.callback_query(spreadsheets_processor_cq.filter(
    name=SpreadsheetsProcessor.GOOGLE_SPREADSHEETS))
async def cq_choose_google_spreadsheets(call: types.CallbackQuery,
                                        ad_service: AdService):
    chat_id = call.message.chat.id

    await call.message.edit_text(
        "Пожалуйста, подождите, ваша таблица скоро будет готова ⏱"
    )

    url = await ad_service.get_url_to_ads_google_spreadsheets(chat_id)

    await call.message.edit_text(
        f"Ваша таблица готова ✅\n{url}"
    )
