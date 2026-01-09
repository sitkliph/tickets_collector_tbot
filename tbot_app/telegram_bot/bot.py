"""Initialize the telegram bot."""
# import logging

from telebot import custom_filters, TeleBot
from telebot.states.sync.middleware import StateMiddleware

from telegram_bot import settings
# from telegram_bot.filters import IsBotAdminFilter


bot = TeleBot(
    settings.TELEGRAM_BOT_TOKEN,
    state_storage=settings.STORAGE,
    use_class_middlewares=True,
    parse_mode='HTML'
)
bot.setup_middleware(StateMiddleware(bot))
bot.add_custom_filter(custom_filters.StateFilter(bot))
# bot.add_custom_filter(IsBotAdminFilter())
