"""Starts telegram bot."""
import sys

from telegram_bot import start_polling, WEBHOOK_MODE

if __name__ == '__main__' and not WEBHOOK_MODE:
    try:
        start_polling()
    except Exception:
        sys.exit()
