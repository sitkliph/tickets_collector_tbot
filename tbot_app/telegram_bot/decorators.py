"""Decorators for telegram bot."""
from functools import wraps

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot.bot import bot


def confirm_command(func):
    """Send message with inline menu to confirm admin command."""
    @wraps(func)
    def wrapper(message):
        command, param = func()

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
            (
                f'Подтвердите команду <b>{command}</b> '
                'с параметром <b>{param}</b>'
            ),
            reply_markup=markup
        )
    return wrapper
