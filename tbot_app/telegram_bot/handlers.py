"""Handlers for telegram bot."""
from datetime import datetime

from telebot import logger, types

from google_sheets import insert_ticket_info
from telegram_bot import settings, text_templates, utils
from telegram_bot.bot import bot
from telegram_bot.decorators import confirm_command
from telegram_bot.exceptions import InvalidAdminCommandError
from telegram_bot.menu import Menu
from telegram_bot.states import SupportedStates as states

menu = Menu()


# Default commands.
@bot.message_handler(commands=['start', 'restart'])
def handle_command_start(message):
    """Handle commands /start & /restart."""
    chat = message.chat
    user_id = message.from_user.id
    text = (
        '<tg-emoji emoji-id="5397939353156609692">💬</tg-emoji> '
        f'<b>{chat.first_name}, добро пожаловать в {settings.BOT_NAME}!</b>'
        '\n\n'
        'Выберите интересующий Вас раздел с помощью кнопок клавиатуры '
        '<tg-emoji emoji-id="5397810121885639797">⌨️</tg-emoji>'
    )
    text_additional = utils.append_admin_start_message(user_id)
    if text_additional is not None:
        text += text_additional

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_tickets = types.KeyboardButton(
        'Создать запрос', icon_custom_emoji_id='5400151776710126080'
    )
    button_contacts = types.KeyboardButton(
        'Контакты', icon_custom_emoji_id='5397829049806513915'
    )
    keyboard.add(button_tickets, button_contacts)

    bot.set_state(user_id, states.in_menu, chat.id)
    with bot.retrieve_data(user_id, chat.id) as data:
        if not data.get('tickets'):
            data['tickets'] = []
        if not data.get('tickets_counter'):
            data['tickets_counter'] = 0

    utils.register_user(user_id)

    bot.send_message(
        chat.id,
        text,
        reply_markup=keyboard
    )


@bot.message_handler(commands=['stop',])
def handle_command_stop(message):
    """Handle command /stop."""
    user_id = message.from_user.id
    chat_id = message.chat.id
    bot.delete_state(user_id, chat_id)
    bot.reset_data(user_id, chat_id)
    bot.reply_to(
        message,
        text_templates.COMMAND_STOP_MSG
    )


# Admin commands (Redis is required).
@bot.message_handler(
    commands=['add_admin', 'del_admin', 'broadcast'], is_bot_admin=True
)
@confirm_command(bot)
def handle_admin_commands(message):
    """Handle inputed admin commands."""
    logger.info(
        f'Пользователем @{message.from_user.username} введена команда '
        'администратора.'
    )
    try:
        return utils.get_command_param(message)
    except InvalidAdminCommandError as error:
        if error.command == 'broadcast':
            param_pattern = 'сообщение'
        else:
            param_pattern = 'ID пользователя'
        bot.reply_to(
            error.message,
            (
                'Команда введена неверно!\n'
                'Правильное использование: '
                f'<pre>/{error.command} &lt;{param_pattern}></pre>'
            )
        )
        raise InvalidAdminCommandError(error.message, error.command)


@bot.message_handler(
    commands=['ls_admin',], is_bot_admin=True
)
def handle_safe_admin_commands(message):
    """Handle admin commands without writing or changing data."""
    text = (
        'Список администраторов бота: \n'
    )
    for number, admin_id in enumerate(utils.get_admins_ids(), 1):
        text += (
            f'{number}. '
            f'<a href="tg://user?id={admin_id}">id - {admin_id}</a>\n'
        )
    bot.reply_to(
        message,
        text
    )


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('confirm'), is_bot_admin=True
)
def handle_confirmed_admin_commands(call):
    """Handle confirmation of admin commands."""
    _, command, param = call.data.split(':')

    if command == 'add_admin':
        utils.add_admin(int(param))
        text = (
            f'<a href="tg://user?id={int(param)}">Пользователь </a>'
            'добавлен в список администраторов.'
        )
    elif command == 'del_admin':
        utils.del_admin(int(param))
        text = (
            f'<a href="tg://user?id={int(param)}">Пользователь </a>'
            'удален из списка администраторов.'
        )
    elif command == 'broadcast':
        text = utils.broadcast(bot)

    notification_text = (
        f'Подтверждена и выполнена команда /{command} с параметром "{param}".'
    )
    logger.info(notification_text)
    bot.send_message(
        settings.NOTIFICATION_CHAT_ID,
        notification_text
    )

    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id
    )


@bot.callback_query_handler(
    func=lambda call: call.data == 'cancel', is_bot_admin=True
)
def handle_canceled_admin_commands(call):
    """Handle cancelation of admin commands."""
    bot.edit_message_text(
        'Команда отменена.',
        call.message.chat.id,
        call.message.message_id
    )


# Contact block.
@bot.message_handler(func=lambda message: message.text == 'Контакты')
def handle_contact_block(message):
    """Send message with contact information."""
    text = ''
    for contact in settings.CONTACTS:
        text += text_templates.CONTACT.format(**contact)
    text += (
        '<tg-emoji emoji-id="5397639147827521319">🏛️</tg-emoji> '
        '<b>Профком студентов ДВГУПС:</b>\n'
        '<a href="https://t.me/profkom_festu">Телеграм-канал</a>\n'
        '<a href="https://vk.com/profkomkhv">Группа Вконтакте</a>\n'
    )
    bot.send_message(
        message.chat.id,
        text,
        link_preview_options=types.LinkPreviewOptions(True)
    )


# Tickets block.
@bot.message_handler(
    func=lambda message: message.text == 'Создать запрос'
)
def handle_tickets_block(message):
    """Send message with inline menu to choose type of ticket."""
    keyboard, text = menu.get_menu()

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_menu(call):
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
            'user': f'https://t.me/{user.username}',
            'status': 'created'
        }
        data['tickets'] = data.get('tickets') + [ticket]

    current_ticket = data.get('tickets')[-1]
    notification_text = (
        '<b>Пришел тикет от пользователя '
        f'<a href="https://t.me/{user.username}">{user.first_name}</a></b>'
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
            '<tg-emoji emoji-id="5397936320909699087">✅</tg-emoji> '
            f'<b>Тикет №{current_ticket.get('id')}</b> принят к рассмотрению '
            'администраторами.\n'
            'Ожидайте ответ '
            '<tg-emoji emoji-id="5397939353156609692">💬</tg-emoji>'
        ),
        chat_id,
        data.get('current_message_id')
    )
