"""Exceptions for telegram bot."""
from telegram_bot.bot import bot


class InvalidAdminCommandError(Exception):
    """Exception for invalid admin commands."""

    def __init__(self, message, command: str):
        """
        Initialize an exception.

        :param message: telebot.types.Message object.
        """
        self.error = "Введена неверная админ-команда."
        if command == 'broadcast':
            param_pattern = 'сообщение'
        else:
            param_pattern = 'ID пользователя'
        bot.reply_to(
            message,
            (
                'Команда введена неверно!\n'
                'Правильное использование: '
                f'<code>/{command} &lt{param_pattern}></code>'
            )
        )

    def __str__(self):
        return self.error
