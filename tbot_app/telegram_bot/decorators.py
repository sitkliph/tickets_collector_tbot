"""Decorators for telegram bot."""
from functools import wraps

from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.settings import STORAGE


def check_redis(func):
    """
    Call function if redis is active.

    If StateMemoryStorage is installed, function, which uses Redis, will not
    be called.
    """
    @wraps(func)
    def wrapper(*args):
        try:
            STORAGE.redis.ping()
        except AttributeError:
            return
        else:
            return func(*args)
    return wrapper


def confirm_command(bot: TeleBot):
    """Send message with inline menu to confirm admin command."""
    def decorator(func):
        @wraps(func)
        def wrapper(message):
            command, param = func(message)

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    'Подтвердить',
                    # TODO сделать поддержку длинных параметров
                    callback_data=f'confirm:{command}:{param}'
                ),
                InlineKeyboardButton(
                    'Отмена',
                    callback_data='cancel'
                )
            )

            bot.reply_to(
                message,
                (
                    f'Подтвердите команду <b>{command}</b> '
                    f'с параметром <b>{param}</b>'
                ),
                reply_markup=markup
            )
        return wrapper
    return decorator
