"""Handlers for telegram bot."""
from datetime import datetime

from telebot import types

from google_sheets import insert_ticket_info
from telegram_bot import settings
# from telegram_bot import text_templates
# from telegram_bot import utils
from telegram_bot.bot import bot, bot_logger
# from telegram_bot.decorators import confirm_command
from telegram_bot.menu import Menu
from telegram_bot.states import SupportedStates as states


menu = Menu()
logger = bot_logger


# Default commands.
@bot.message_handler(commands=['start',])
def command_start(message):
    """Handle command /start."""
    chat = message.chat
    text = (
        f'<b>{chat.first_name}, добро пожаловать в {settings.BOT_NAME}!</b>'
        '\n\n'
        'Выберите интересующий Вас раздел с помощью кнопок клавиатуры.'
    )
    # if str(message.from_user.id) in utils.get_admins_ids():
    #     text += text_templates.ADMIN_COMANDS
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

    # utils.register_user(user_id)

    bot.send_message(
        chat.id,
        text,
        reply_markup=keyboard
    )


# # Admin commands (Redis is required).
# @bot.message_handler(
#     commands=['add_admin', 'del_admin', 'broadcast'], is_bot_admin=True
# )
# @confirm_command
# def admin_commands(message):
#     """Handle admin commands."""
#     logger.info(
#         f'Пользователем @{message.from_user.username} введена команда '
#         'администратора.'
#     )
#     return utils.get_command_param(message)


# @bot.callback_query_handler(
#     func=lambda call: call.data.startswith('confirm'), is_bot_admin=True
# )
# def confirm_admin_commands(call):
#     """Handle confirmation of admin commands."""
#     _, command, param = call.data.split(':')

#     if command == 'add_admin':
#         utils.add_admin(int(param))
#         text = (
#             f'<a href="tg://user?id={int(param)}">Пользователь</a>'
#             'добавлен в список администраторов.'
#         )
#     elif command == 'del_admin':
#         utils.del_admin(int(param))
#         text = (
#             f'<a href="tg://user?id={int(param)}">Пользователь</a>'
#             'удален из списка администраторов.'
#         )
#     elif command == 'broadcast':
#         stats = utils.broadcast(param)
#         text = (
#             'Рассылка завершена.\n'
#             'Всего попыток: {total}, из них: '
#             'успешно отправлено - {sent}, ошибок - {failed}.'
#         ).format(**stats)

#     logger.info(
#         f'Подтверждена и выполнена команда /{command} с параметром {param}.'
#     )

#     bot.edit_message_text(
#         text,
#         call.message.chat.id,
#         call.message.message_id
#     )


# @bot.callback_query_handler(
#     func=lambda call: call.data == 'cancel', is_bot_admin=True
# )
# def cancel_admin_commands(call):
#     """Handle cancelation of admin commands."""
#     bot.edit_message_text(
#         'Команда отменена.',
#         call.message.chat.id,
#         call.message.message_id
#     )


# Tickets block.
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


# Contact block.
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
    last_notification_message = ''
    try:
        bot.polling()
    except Exception as error:
        notification_message = f'Сбой в работе программы: {error}'
        if last_notification_message != notification_message:
            bot.send_message(
                settings.NOTIFICATION_CHAT_ID,
                notification_message,
            )
