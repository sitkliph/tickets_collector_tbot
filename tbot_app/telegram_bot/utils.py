"""Utils for telegram bot."""
import time
from typing import cast, Set

import redis
from telebot.apihelper import ApiTelegramException

from telegram_bot import settings
from telegram_bot.bot import bot


redis_client = redis.Redis(
    password=settings.DATA_BASE_PASSWORD, decode_responses=True
)
redis_client.sadd('users:admins', *settings.START_ADMIN_IDS)


def get_admins_ids():
    """Get ids of admin users from database."""
    return redis_client.smembers('users:admins')


def register_user(user_id: int) -> None:
    """Register user in database."""
    redis_client.sadd('users:all', str(user_id))


def broadcast(text: str) -> dict:
    """
    Send message to all bot's users.

    Function sends message and returns sending's statistics.
    """
    chat_ids = cast(Set, redis_client.smembers('users:all'))
    stats = {
        'total': len(chat_ids),
        'sent': 0,
        'failed': 0
    }

    for chat_id in chat_ids:
        try:
            bot.send_message(int(chat_id), text)
            stats['sent'] += 1
            time.sleep(0.1)
        except ApiTelegramException:
            stats['failed'] += 1
            time.sleep(0.1)

    return stats
