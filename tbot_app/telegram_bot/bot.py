"""Initialize the telegram bot."""
import logging

from telebot import custom_filters, logger, TeleBot
from telebot.states.sync.middleware import StateMiddleware

from telegram_bot import settings
# from telegram_bot.filters import IsBotAdminFilter


LOG_FILE = settings.BASE_DIR / 'logs' / 'bot.log'

bot_logger = logger
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s - %(name)s: %(message)s'
)
file_output_handler = logging.FileHandler(LOG_FILE)
file_output_handler.setFormatter(formatter)
bot_logger.addHandler(file_output_handler)

bot = TeleBot(
    settings.TELEGRAM_BOT_TOKEN,
    state_storage=settings.STORAGE,
    use_class_middlewares=True,
    parse_mode='HTML'
)
bot.setup_middleware(StateMiddleware(bot))
bot.add_custom_filter(custom_filters.StateFilter(bot))
# bot.add_custom_filter(IsBotAdminFilter())
