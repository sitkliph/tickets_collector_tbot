"""Webhook setup."""

import asyncio

from fastapi import FastAPI, HTTPException, Request
from telebot.types import Update

from telegram_bot.bot import bot
from telegram_bot.settings import WEBHOOK_SECRET

api = FastAPI()


@api.get('/health')
def health():
    """Check API available."""
    return {'status': 'ok'}


@api.post(f'/{WEBHOOK_SECRET}')
async def telegram_webhook(request: Request):
    """Configure webhook endponit."""
    try:
        raw_body = await request.body()
        update = Update.de_json(raw_body.decode())
    except Exception:
        raise HTTPException(status_code=400)

    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, bot.process_new_updates, [update])

    return {'ok': True}
