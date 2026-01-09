# flake8: noqa: D103, D107
"""Custom handlers' filters for telegram bot."""
from telebot.custom_filters import SimpleCustomFilter

from telegram_bot.settings import BOT_ADMINS


class IsBotAdminFilter(SimpleCustomFilter):
    """
    Filter to check user in admin list.

    .. code-block:: python3
        :caption: Example on using this filter:

        @bot.message_handler(is_bot_admin=True)
        # your function
    """

    key = 'is_bot_admin'

    def __init__(self):
        self.admin_ids = BOT_ADMINS

    def check(self, message):
        return message.from_user.id in self.admin_ids
