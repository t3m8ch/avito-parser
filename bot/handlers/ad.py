from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot.misc import Router
from bot.models import SubscriptionModel
from bot.services.ad import AdService

router = Router()


class SubscribeToNewAds(StatesGroup):
    waiting_for_url = State()
    waiting_for_tag = State()


@router.message(state="*", commands="subscribe")
async def cmd_subscribe_to_new_ads(message: types.Message):
    await message.answer("Отправьте ссылку со списком объявлений")
    await SubscribeToNewAds.waiting_for_url.set()


@router.message(state=SubscribeToNewAds.waiting_for_url)
async def process_url(message: types.Message, state: FSMContext, ad_service: AdService):
    async with state.proxy() as data:
        data["chat_id"] = message.chat.id
        data["url"] = message.text

    await message.reply(
        f"Введите метку, которая поможет вам различать объявления"
    )
    await SubscribeToNewAds.next()


@router.message(state=SubscribeToNewAds.waiting_for_tag)
async def process_tag(message: types.Message, state: FSMContext, ad_service: AdService):
    async with state.proxy() as data:
        chat_id = data["chat_id"]
        url = data["url"]

    tag = message.text

    # TODO: Add validation URL
    await ad_service.subscribe_to_new_ads(SubscriptionModel(
        chat_id=chat_id,
        url=url,
        tag=tag
    ))

    await message.reply(
        f"Вы подписаны на получение новых объявлений по этому адресу:\n{url}"
    )