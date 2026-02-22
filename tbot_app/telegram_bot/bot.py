"""Initialize the telegram bot."""
import logging
from typing import List

from redis.exceptions import ConnectionError
from telebot import TeleBot, logger
from telebot.custom_filters import StateFilter
from telebot.states.sync.middleware import StateMiddleware
from telebot.types import Update

from telegram_bot import settings
from telegram_bot.decorators import handle_exceptions
from telegram_bot.exceptions import EmptyEnvVarsError, RedisUnavailableError
from telegram_bot.filters import IsBotAdminFilter
from telegram_bot.utils import add_admins_from_settings

LOG_FILE = settings.BASE_DIR / 'logs' / 'bot.log'

logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s - %(name)s: %(message)s'
)
file_output_handler = logging.FileHandler(LOG_FILE)
file_output_handler.setFormatter(formatter)
logger.addHandler(file_output_handler)


def check_env_vars():
    """Check environment variables for empty values."""
    env_vars = {
        'TELEGRAM_TOKEN': settings.TELEGRAM_BOT_TOKEN,
        'NOTIFICATION_CHAT_ID': settings.NOTIFICATION_CHAT_ID
    }
    empty_env_vars = [
        token_key
        for token_key, token_value in env_vars.items() if (
            token_value is None or token_value == ''
        )
    ]

    if empty_env_vars:
        empty_env_vars_msg = ', '.join(empty_env_vars)
        message = (
            f'Отсутствуют обязательные переменные окружения: '
            f'{empty_env_vars_msg}\n'
            'Программа принудительно остановлена.'
        )
        logger.critical(message)
        raise EmptyEnvVarsError(message)


def initial_check_redis():
    """Check Redis available."""
    try:
        settings.STORAGE.redis.ping()
    except ConnectionError as error:
        message = (
            'Redis is not available at start! '
            f'{error}'
        )
        logger.critical(message)
        raise RedisUnavailableError(message)
    except AttributeError:
        logger.warning('Using StateMemoryStorage. Do not use it in prod!')


check_env_vars()
bot = TeleBot(
    settings.TELEGRAM_BOT_TOKEN,
    state_storage=settings.STORAGE,
    use_class_middlewares=True,
    parse_mode='HTML'
)
initial_check_redis()
bot.setup_middleware(StateMiddleware(bot))
bot.add_custom_filter(StateFilter(bot))
bot.add_custom_filter(IsBotAdminFilter())
add_admins_from_settings()
bot.remove_webhook()

if settings.WEBHOOK_MODE:
    url = f'{settings.WEBHOOK_DOMAIN}/webhook/{settings.WEBHOOK_SECRET}'
    bot.set_webhook(url, secret_token=settings.WEBHOOK_TOKEN)


@handle_exceptions(bot)
def start_polling() -> None:
    """Start polling of telegram server."""
    bot.polling()


@handle_exceptions(bot)
def process_updates_from_webhook(updates: List[Update]) -> None:
    """Process new updates from telgram webhook to bot."""
    bot.process_new_updates(updates)
