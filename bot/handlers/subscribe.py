from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.errors import SubscriptionAlreadyExistsError, NotValidUrlError
from bot.keyboards.cancel import get_cancel_inline_keyboard
from bot.keyboards.unsubscribe import get_unsubscribe_keyboard
from bot.misc import Router
from bot.models import SubscriptionModel
from bot.services.ad import AdService

router = Router()


class SubscribeToNewAds(StatesGroup):
    waiting_for_url = State()


@router.message(state="*", commands="subscribe")
async def cmd_subscribe_to_new_ads(message: types.Message):
    instruction_file_url = "https://telegra.ph/file/583815bcebb623c47b8f1.png"
    text = "<b>Для того, чтобы подписаться на определённые объявления, вы должны:</b>\n\n" \
           "1. Зайти на сайт avito.ru;\n\n" \
           "2. Ввести в поиск нужный вам запрос, задать фильтры и нажать на <i>Найти</i>;\n\n" \
           "3. Скопировать URL из адресной строки вашего браузера и отправить его сюда."

    await message.answer_photo(
        photo=instruction_file_url,
        caption=text,
        reply_markup=get_cancel_inline_keyboard()
    )

    await SubscribeToNewAds.waiting_for_url.set()


@router.message(state=SubscribeToNewAds.waiting_for_url)
async def process_url(message: types.Message, state: FSMContext, ad_service: AdService):
    chat_id = message.chat.id
    url = message.text

    try:
        await ad_service.subscribe_to_new_ads(SubscriptionModel(
            chat_id=chat_id,
            url=url
        ))
    except SubscriptionAlreadyExistsError:
        await message.reply(
            f"Вы уже подписаны на новые объявления по адресу:\n{url}"
        )
    except NotValidUrlError:
        await message.reply(
            f"Вы кинули невалидный адрес!"
        )
    else:
        await message.reply(
            f"Вы подписаны на получение новых объявлений по этому адресу:\n{url}"
        )
        await state.finish()
