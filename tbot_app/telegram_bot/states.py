"""Telegram bot states."""
from telebot.handler_backends import State, StatesGroup


class SupportedStates(StatesGroup):
    """Class of supported custom bot states."""

    in_menu = State()
    waiting_reply = State()
