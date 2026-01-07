"""Logic for creation of menu's inline keyboards and headers."""
from telebot import types

from telegram_bot.settings import MENU_CONFIG


class Menu():
    """Class of inline menu."""

    def __create_menu(self, menu_slug):
        keyboard = types.InlineKeyboardMarkup()

        buttons = MENU_CONFIG[menu_slug].get('buttons')
        header = MENU_CONFIG[menu_slug].get('header')
        state = MENU_CONFIG[menu_slug].get('state')

        for command, text in buttons:
            button = types.InlineKeyboardButton(
                text=text,
                callback_data=command
            )
            keyboard.add(button)

        return keyboard, header, state

    def __init__(self):
        """Initialize an object with all menus."""
        self.menus = {}

        for menu_slug in MENU_CONFIG.keys():
            self.menus[menu_slug] = {}
            (
                self.menus[menu_slug]['keyboard'],
                self.menus[menu_slug]['header'],
                self.menus[menu_slug]['state']
            ) = self.__create_menu(menu_slug)

    def get_menu(self, call=None):
        """Return requested menu."""
        if call is not None:
            menus_slug = call.data
        else:
            menus_slug = 'main'

        return (
            self.menus[menus_slug].get('keyboard'),
            self.menus[menus_slug].get('header')
        )

    def get_state(self, call=None):
        """Return state for call."""
        menus_slug = call.data
        return self.menus[menus_slug].get('state')
