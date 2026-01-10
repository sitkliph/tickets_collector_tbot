"""Custom handlers' filters for telegram bot."""
from telebot.custom_filters import SimpleCustomFilter

from telegram_bot.utils import get_admins_ids


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
        self.admin_ids = get_admins_ids()

    def check(self, message):
        return str(message.from_user.id) in self.admin_ids
