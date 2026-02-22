"""Starts telegram bot."""
import sys

from telegram_bot import WEBHOOK_MODE, start_polling

if __name__ == '__main__' and not WEBHOOK_MODE:
    try:
        start_polling()
    except Exception:
        sys.exit()
