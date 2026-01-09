"""Project's settings."""
import os

from dotenv import load_dotenv
from telebot.storage import StateMemoryStorage

from telegram_bot.states import SupportedStates as states


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATA_BASE_PASSWORD = os.getenv('DATA_BASE_PASSWORD')

BOT_NAME = 'ХозРевизор ДВГУПС'
CONTACT = {
    'name': 'Никита Ставров',
    'tg_username': 'NikStv',
    'vk_username': 'nista9'
}

NOTIFICATION_CHAT_ID = -1003679635348
START_ADMIN_IDS = (
    290277110,
    327070804,
    830659667
)

# STORAGE = StateRedisStorage(password=DATA_BASE_PASSWORD)
STORAGE = StateMemoryStorage()

MENU_CONFIG = {
    'main': {
        'header': 'Выберите интересующий Вас раздел:',
        'state': states.in_menu,
        'buttons': (
            ('problem', 'Отправить обращение'),
            ('question', 'Задать вопрос'),
            ('request', 'Подать заявку на ремонт')
        ),
    },
    'problem': {
        'header': 'Выберите тип обращения:',
        'state': states.in_menu,
        'buttons': (
            ('campus_problem', 'Хозяйственные проблемы'),
            ('check_in_problem', 'Проблема с заселением'),
            ('administration_issue', 'Конфликт с администрацией'),
            ('neighbor_issue', 'Конфликт с соседями'),
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
    'check_in_problem': {
        'header': 'Напишите Ваше обращение в свободной форме:',
        'state': states.waiting_reply,
        'buttons': (
            ('problem', 'Назад'),
        )
    },
    'administration_issue': {
        'header': 'Напишите Ваше обращение в свободной форме:',
        'state': states.waiting_reply,
        'buttons': (
            ('problem', 'Назад'),
        )
    },
    'neighbor_issue': {
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
    'request': {
        'header': 'Опишите Вашу заявку на ремонт:',
        'state': states.waiting_reply,
        'buttons': (
            ('main', 'Назад'),
        )
    }
}
