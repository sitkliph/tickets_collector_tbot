""""""
from telebot.handler_backends import State, StatesGroup


class SupportedStates(StatesGroup):
    in_menu = State()
    waiting_reply = State()
