"""Initialize the telegram bot."""
# import logging
import os

from dotenv import load_dotenv
from telebot import custom_filters, TeleBot
from telebot.states.sync.middleware import StateMiddleware

from telegram_bot import settings


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = TeleBot(
    TELEGRAM_BOT_TOKEN,
    state_storage=settings.STORAGE,
    use_class_middlewares=True,
    parse_mode='HTML'
)
bot.setup_middleware(StateMiddleware(bot))
bot.add_custom_filter(custom_filters.StateFilter(bot))
