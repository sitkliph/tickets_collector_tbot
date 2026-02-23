"""Decorators for telegram bot."""
from functools import wraps

from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_bot.settings import NOTIFICATION_CHAT_ID, STORAGE


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


@check_redis
def confirm_command(bot: TeleBot):
    """Send message with inline menu to confirm admin command."""
    def decorator(func):
        @wraps(func)
        def wrapper(message):
            command, param = func(message)

            message_text = (
                f'Подтвердите команду <b>{command}</b> '
                f'с параметром <b>{param}</b>'
            )

            if command == 'broadcast':
                STORAGE.redis.set('global:broadcast_param', param)
                param = ''

            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    'Подтвердить',
                    callback_data=f'confirm:{command}:{param}'
                ),
                InlineKeyboardButton(
                    'Отмена',
                    callback_data='cancel'
                )
            )

            bot.reply_to(
                message,
                message_text,
                reply_markup=markup
            )
        return wrapper
    return decorator


def handle_exceptions(bot: TeleBot):
    """Handle exceptions when starting polling or setup webhook."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            last_notification_message = ''
            try:
                func(*args)
            except Exception as error:
                notification_message = f'Сбой в работе программы: {error}'
                if last_notification_message != notification_message:
                    bot.send_message(
                        NOTIFICATION_CHAT_ID,
                        notification_message,
                    )
        return wrapper
    return decorator
