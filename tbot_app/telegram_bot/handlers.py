"""Handlers for telegram bot."""
from datetime import datetime

from telebot import types

from google_sheets import insert_ticket_info
from telegram_bot import settings
from telegram_bot.bot import bot
from telegram_bot.menu import Menu
from telegram_bot.states import SupportedStates as states
# from telegram_bot.utils import broadcast, get_admins_ids, register_user


menu = Menu()


@bot.message_handler(commands=['start',])
def command_start(message):
    """Handle command /start."""
    chat = message.chat
    text = (
        f'<b>{chat.first_name}, добро пожаловать в {settings.BOT_NAME}!</b>'
        '\n\n'
        'Выберите интересующий Вас раздел с помощью кнопок клавиатуры.'
    )
    # if str(message.from_user.id) in get_admins_ids():
    #     text += (
    #         '\n\n<b>Также Вам доступны команды администратора бота:</b>\n'
    #         '<pre>/add_admin &ltID пользователя></pre>'
    #         'добавление пользователя в список администраторов.'
    #         '<pre>/del_admin &ltID пользователя></pre>'
    #         'удаление пользователя из списка администраторов.'
    #         '<pre>/broadcast &ltтекст для рассылки></pre>'
    #         'рассылка сообщения всем пользователям, активировавшим бот <i>(во '
    #         'время выполнения команды бот перестает исполнять любые другие '
    #         'запросы от всех пользователей).</i>'
    #     )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_tickets = types.KeyboardButton('Жилищно-бытовая проблема')
    button_contacts = types.KeyboardButton('Контакты')
    keyboard.add(button_tickets, button_contacts)

    user_id = message.from_user.id
    bot.set_state(user_id, states.in_menu, chat.id)
    with bot.retrieve_data(user_id, chat.id) as data:
        if not data.get('tickets'):
            data['tickets'] = []
        if not data.get('tickets_counter'):
            data['tickets_counter'] = 0

    # register_user(user_id)

    bot.send_message(
        chat.id,
        text,
        reply_markup=keyboard
    )


# @bot.message_handler(commands=['broadcast'], is_bot_admin=True)
# def command_broadcast(message):
#     """Handle admin command /broadcast."""
#     parts = message.text.split(maxsplit=1)
#     if len(parts) < 2 or not parts[1].strip():
#         return bot.reply_to(
#             message,
#             (
#                 'Команда введена неверно!\n'
#                 'Правильное использование: '
#                 '<code>/broadcast &lтекст для рассылки></code>'
#             )
#         )

#     stats = broadcast(parts[1].strip())
#     bot.reply_to(
#         message,
#         (
#             'Рассылка завершена.\n'
#             'Всего попыток: {total}, из них: '
#             'успешно отправлено - {sent}, ошибок - {failed}.'
#         ).format(**stats)
#     )


@bot.message_handler(
    func=lambda message: message.text == 'Жилищно-бытовая проблема'
)
def tickets_block(message):
    """Send message with inline menu to choose type of ticket."""
    keyboard, text = menu.get_menu()

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def menu_handler(call):
    """Handle inline menu buttons."""
    bot.answer_callback_query(call.id, 'Обрабатываю запрос...')
    chat_id = call.message.chat.id
    keyboard, text = menu.get_menu(call)
    state = menu.get_state(call)

    bot.set_state(call.from_user.id, state, chat_id)
    if state == states.waiting_reply:
        bot.add_data(
            call.from_user.id,
            chat_id,
            current_ticket_type=call.data,
            current_message_id=call.message.message_id
        )

    bot.edit_message_text(
        text,
        chat_id,
        call.message.message_id,
        reply_markup=keyboard
    )


@bot.message_handler(state=states.in_menu)
def in_menu_state_handler(message):
    """Handle text messages from users with 'in_menu' state."""
    bot.send_message(
        message.chat.id,
        'Воспользуйтесь меню и выберите тип обращения.'
    )


@bot.message_handler(state=states.waiting_reply)
def reply_state_handler(message):
    """Handle ticket from user."""
    user = message.from_user
    chat_id = message.chat.id

    with bot.retrieve_data(user.id, chat_id) as data:
        data['tickets_counter'] = data.get('tickets_counter') + 1
        data['current_ticket_id'] = (
            f'{str(user.id)}.{str(data.get('tickets_counter'))}'
        )
        ticket = {
            'date': str(datetime.now()),
            'id': data.get('current_ticket_id'),
            'type': data.get('current_ticket_type'),
            'text': message.text.strip(),
            'status': 'created'
        }
        data['tickets'] = data.get('tickets') + [ticket]

    current_ticket = data.get('tickets')[-1]
    notification_text = (
        '<b>Пришел тикет от пользователя '
        f'<a href="tg://user?id={user.id}">{user.first_name}</a></b>'
        '\n\n'
        'Номер: {id}\n'
        'Тип: {type}, статус {status}'
        '<blockquote>{text}</blockquote>'
    ).format(**current_ticket)

    bot.send_message(
        settings.NOTIFICATION_CHAT_ID,
        notification_text,
    )

    insert_ticket_info(current_ticket)

    bot.set_state(user.id, states.in_menu, message.chat.id)
    bot.edit_message_text(
        (
            f'<b>Тикет №{current_ticket.get('id')}</b> принят к рассмотрению '
            'администраторами.\n'
            'Ожидайте ответ.'
        ),
        chat_id,
        data.get('current_message_id')
    )


@bot.message_handler(func=lambda message: message.text == 'Контакты')
def contact_block(message):
    """Send message with contact information."""
    text = (
        '<b>Жилищно-бытовая комиссия Профкома студентов ДВГУПС</b>\n'
        'Председатель комиссии: '
        '<a href="https://t.me/{tg_username}">{name}</a>\n'
        '(также можете написать во '
        '<a href="https://vk.com/{vk_username}">Вконтакте</a>)\n\n'
        'Профком студентов ДВГУПС:\n'
        '<a href="https://t.me/profkom_festu">Телеграм-канал</a>\n'
        '<a href="https://vk.com/profkomkhv">Группа Вконтакте</a>\n'
    ).format(**settings.CONTACT)
    bot.send_message(
        message.chat.id,
        text,
        disable_web_page_preview=True
    )


def start_polling():
    """Start polling of telegram server."""
    bot.polling()
