"""Starts telegram bot."""
import sys

from telegram_bot import start_polling

if __name__ == '__main__':
    try:
        start_polling()
    except Exception:
        sys.exit()
