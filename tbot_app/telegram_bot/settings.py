"""Project's settings."""
import os
from pathlib import Path

from dotenv import load_dotenv
from telebot.storage import StateMemoryStorage, StateRedisStorage

from telegram_bot.states import SupportedStates as states

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
WEBHOOK_MODE = (
    os.getenv('WEBHOOK_MODE', 'false').lower() == 'true'
)
WEBHOOK_DOMAIN = os.getenv('WEBHOOK_DOMAIN')
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
NOTIFICATION_CHAT_ID = os.getenv('NOTIFICATION_CHAT_ID')
IS_PROD_STORAGE = (
    os.getenv('IS_PROD_STORAGE', 'false').lower() == 'true'
)
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'strong_password')

BOT_NAME = 'Ревизор ДВГУПС'
CONTACTS = [
    {
        'unit': 'Жилищно-бытовая комиссия Профкома студентов ДВГУПС',
        'name': 'Никита Ставров',
        'tg_username': 'NikStv',
        'vk_username': 'nista9'
    },
    {
        'unit': 'Центр социальной поддержки Профкома студентов ДВГУПС',
        'name': 'Юлия Гришина',
        'tg_username': 'itz_gregory',
        'vk_username': 'id398583299'
    }
]

START_ADMIN_IDS = (
    '290277110',
    '327070804'
)

if IS_PROD_STORAGE:
    STORAGE = StateRedisStorage(
        host=DB_HOST, password=DB_PASSWORD
    )
else:
    STORAGE = StateMemoryStorage()  # type: ignore[assignment]

MENU_CONFIG = {
    'main': {
        'header': 'Выберите интересующий Вас раздел:',
        'state': states.in_menu,
        'buttons': (
            ('problem', 'Отправить обращение'),
            ('question', 'Задать вопрос'),
            ('repair', 'Подать заявку на ремонт'),
            ('pool', 'Подать заявку на абонемент в бассейн'),
        ),
    },
    'problem': {
        'header': 'Выберите тип обращения:',
        'state': states.in_menu,
        'buttons': (
            ('campus_problem', 'Проблема с общежитием'),
            ('financial_problem', 'Проблема с материальной помощью'),
            ('issue', 'Конфликт с сотрудником администрации'),
            ('other_problem', 'Другое'),
            ('main', 'Назад'),
        )
    },
    'campus_problem': {
        'header': 'Напишите Ваше обращение в свободной форме:',
        'state': states.waiting_reply,
        'buttons': (
            ('problem', 'Назад'),
        )
    },
    'financial_problem': {
        'header': 'Напишите Ваше обращение в свободной форме:',
        'state': states.waiting_reply,
        'buttons': (
            ('problem', 'Назад'),
        )
    },
    'issue': {
        'header': 'Напишите Ваше обращение в свободной форме:',
        'state': states.waiting_reply,
        'buttons': (
            ('problem', 'Назад'),
        )
    },
    'other_problem': {
        'header': 'Напишите Ваше обращение в свободной форме:',
        'state': states.waiting_reply,
        'buttons': (
            ('problem', 'Назад'),
        )
    },
    'question': {
        'header': 'Задайте Ваш вопрос в свободной форме:',
        'state': states.waiting_reply,
        'buttons': (
            ('main', 'Назад'),
        )
    },
    'repair': {
        'header': 'Опишите Вашу заявку на ремонт:',
        'state': states.waiting_reply,
        'buttons': (
            ('main', 'Назад'),
        )
    },
    'pool': {
        'header': (
            'Укажите ФИО, номер группы и дни посещения бассейна (Пн, Ср, Пт):'
        ),
        'state': states.waiting_reply,
        'buttons': (
            ('main', 'Назад'),
        )
    }
}
