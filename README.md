# Tickets Collector Telegram Bot
[![ru](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md)

Telegram bot collects questions, complaints, appeals and requests from users.

## Status
In development.

## Description
A Telegram bot that allows you to collect user feedback.  
In `tbot_app/telegram_bot/settings.py`, you can configure the bot name, contact information, and inline menu,
including buttons that trigger the bot to process text messages and
add records to a Google Sheets table.

For testing and development, the state storage `telebot.storage.StateMemoryStorage` is used.  
If necessary, change the STORAGE parameter in `tbot_app/telegram_bot/settings.py`.

### Structure
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

### Tech Stack

- Python 3.12.7
- pyTelegramBotAPI 4.22.1
- gspread 6.2.1

## Project Setup and Run

### 1. Clone the repository and navigate into it using the command line

```bash
git clone https://github.com/sitkliph/tickets_collector_tbot
```

```bash
cd tickets_collector_tbot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
```

```
source venv/bin/activate       # Linux / macOS
       venv/Scripts/activate   # Windows
```

### 3. Install dependencies from requirements.txt

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### 4. Configurate the project

- Create a project in Google Cloud Console.
- Create a service user in Google Cloud Console and get a JSON key.
- Add a service user in editors of Google Sheets table.
- Fill constants in `tbot_app/google_sheets/settings.py` and `tbot_app/telegram_bot/settings.py`.
- Create file `.env` like this:

```
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
GOOGLE_API_JSON_KEY_PATH = path_to_service_user_json_key
```

### 5. Run project

```bash
cd tbot_app
python3 start_bot.py
```

## Example
https://t.me/KhozRevizorBot

## Author
Sergei Bakin  
sergey.bakin2000@gmail.com

## License
This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) for details.