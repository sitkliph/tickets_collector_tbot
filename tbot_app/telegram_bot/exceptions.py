"""Exceptions for telegram bot."""


class EmptyEnvVarsError(SystemExit):
    """Exception for empty env values."""


class InvalidAdminCommandError(Exception):
    """Exception for invalid admin commands."""

    def __init__(self, message, command: str):
        """
        Initialize an exception.

        :param message: telebot.types.Message object.
        """
        self.message = message
        self.command = command

    def __str__(self):
        return 'Введена неверная админ-команда.'


class RedisUnavailableError(Exception):
    """Exception for unavilable Redis."""
