from aiogram import types

from bot.misc.errors import (SubscriptionAlreadyExistsError,
                             LimitSubscriptionsCountError,
                             NotValidUrlError)

from bot.utils import Router

router = Router()


@router.errors(exception=SubscriptionAlreadyExistsError)
async def subscription_already_exists_error(update: types.Update,
                                            exception: SubscriptionAlreadyExistsError):
    await update.message.reply(
        f"Вы уже подписаны на новые объявления по адресу:\n{exception.subscription.url}"
    )
    return True


@router.errors(exception=LimitSubscriptionsCountError)
async def limit_subscriptions_count_error(update: types.Update, _):
    text = f"Вы не можете сделать больше <b>двух</b> подписок.\n" \
           f"Ограничение сделано с целью сохранение работоспособности бота."
    await update.message.reply(text)
    return True


@router.errors(exception=NotValidUrlError)
async def not_valid_url_error(update: types.Update, _):
    await update.message.reply(
        f"Вы кинули невалидный адрес!"
    )
    return True
