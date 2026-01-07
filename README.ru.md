# Tickets Collector Telegram Bot
[![en](https://img.shields.io/badge/lang-en-white.svg)](README.md)

Телеграм бот для сбора вопросов, жалоб, обращений и запросов от пользоватлей.

## Статус проекта
Проект в разработке.

## Описание проекта
Телеграмм бот, с помощью которого можно собирать обратную связь от пользователей.  
В `tbot_app/telegram_bot/settings.py` можно настроить название, контактную информацию, inline меню,
включая кнопки, по нажатию которых бот обрабатывает произвольное текстовое сообщение и
добавляет запись в таблицу Google Sheets.

Для тестирования и разработки используется хранилище состояний - `telebot.storage.StateMemoryStorage`.  
При необходимости измените параметр STORAGE в `tbot_app/telegram_bot/settings.py`.

### Структура проекта
```
tickets_collector_tbot/
├── LICENSE
├── README.md
├── README.ru.md
├── requirements.txt
├── setup.cfg
├── tbot_app/
│   ├── google_sheets/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── settings.py
│   │   └── utils.py
│   ├── start_bot.py
│   └── telegram_bot/
│       ├── __init__.py
│       ├── bot.py
│       ├── handlers.py
│       ├── menu.py
│       ├── settings.py
│       └── states.py
└── tests/
    └── __init__.py
```

### Стек использованных технологий

- Python 3.12.7
- pyTelegramBotAPI 4.22.1
- gspread 6.2.1

## Установка и запуск проекта

### 1. Клонировать репозиторий и перейти в него в командной строке

```bash
git clone https://github.com/sitkliph/tickets_collector_tbot
```

```bash
cd tickets_collector_tbot
```

### 2. Cоздать и активировать виртуальное окружение

```bash
python3 -m venv venv
```

```
source venv/bin/activate       # Linux / macOS
       venv/Scripts/activate   # Windows
```

### 3. Установить зависимости из файла requirements.txt

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### 4. Выполнить настроки проекта

- Создать проект в консоли Google Cloud.
- Создать service user в консоли Google Cloud и получить JSON ключ.
- Подключить service user к онлайн таблице Google Sheets.
- Заполнить константы файлов `tbot_app/google_sheets/settings.py` и `tbot_app/telegram_bot/settings.py`.
- Создать файл `.env` по примеру:

```
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
GOOGLE_API_JSON_KEY_PATH = path_to_service_user_json_key
```

### 5. Запустить проект

```bash
cd tbot_app
python3 start_bot.py
```

## Пример
https://t.me/KhozRevizorBot

## Автор
Sergei Bakin  
sergey.bakin2000@gmail.com

## Лицензия
Проект распространяется под лицензией **MIT**.  
Подробности см. в файле [LICENSE](LICENSE).