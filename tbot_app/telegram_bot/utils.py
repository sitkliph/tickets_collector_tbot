"""Utils for telegram bot."""
import time
from typing import cast, Set

import redis
from telebot.types import Message
from telebot.apihelper import ApiTelegramException

from telegram_bot import settings
from telegram_bot.bot import bot
from telegram_bot.exceptions import InvalidAdminCommandError


USERS_DATABASE_KEY = 'users:all'
ADMINS_DATABASE_KEY = 'users:admins'

redis_client = redis.Redis(
    password=settings.DATA_BASE_PASSWORD, decode_responses=True
)
redis_client.sadd(ADMINS_DATABASE_KEY, *settings.START_ADMIN_IDS)


def get_admins_ids() -> Set:
    """Get ids of admin users from database."""
    return cast(Set, redis_client.smembers(ADMINS_DATABASE_KEY))


def add_admin(user_id: int) -> None:
    """Add admin in database."""
    redis_client.sadd(ADMINS_DATABASE_KEY, str(user_id))


def del_admin(user_id: int) -> None:
    """Delete admin from database."""
    redis_client.srem(ADMINS_DATABASE_KEY, str(user_id))


def register_user(user_id: int) -> None:
    """Register user in database."""
    redis_client.sadd(USERS_DATABASE_KEY, str(user_id))


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


def get_command_param(message: Message) -> str:
    """Check admin command and get parametr from the message."""
    parts = message.text.split(maxsplit=1)
    command = parts[0].lstrip('/')
    try:
        param = parts[1].strip()
    except IndexError:
        raise InvalidAdminCommandError(message, command)
    if command != 'broadcast' and not param.isdigit():
        raise InvalidAdminCommandError(message, command)
    return command, param
