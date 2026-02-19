"""Utils for telegram bot."""
from typing import Set, cast

from telegram_bot import settings
from telegram_bot.decorators import check_redis
from telegram_bot.exceptions import InvalidAdminCommandError
from telegram_bot.settings import STORAGE
from telegram_bot.text_templates import ADMIN_COMANDS

USERS_DATABASE_KEY = 'users:all'
ADMINS_DATABASE_KEY = 'users:admins'


@check_redis
def add_admins_from_settings():
    """Add admins from settings.py in database."""
    STORAGE.redis.sadd(ADMINS_DATABASE_KEY, *settings.START_ADMIN_IDS)


@check_redis
def get_admins_ids() -> list:
    """Get ids of admin users from database."""
    return [
        admin_id.decode() for admin_id in (
            cast(Set, STORAGE.redis.smembers(ADMINS_DATABASE_KEY))
        )
    ]


@check_redis
def append_admin_start_message(user_id: int) -> str:
    """Return adiitinal text for start message if user is admin."""
    if str(user_id) in get_admins_ids():
        return ADMIN_COMANDS
    return ''


@check_redis
def add_admin(user_id: int) -> None:
    """Add admin in database."""
    STORAGE.redis.sadd(ADMINS_DATABASE_KEY, str(user_id))


@check_redis
def del_admin(user_id: int) -> None:
    """Delete admin from database."""
    STORAGE.redis.srem(ADMINS_DATABASE_KEY, str(user_id))


@check_redis
def register_user(user_id: int) -> None:
    """Register user in database."""
    STORAGE.redis.sadd(USERS_DATABASE_KEY, str(user_id))


@check_redis
def get_command_param(message) -> tuple:
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
