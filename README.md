# Tickets Collector Telegram Bot
[![ru](https://img.shields.io/badge/lang-ru-blue.svg)](README.ru.md)

Telegram bot collects questions, complaints, appeals and requests from users.

## Description
Sync Telegram bot that allows you to collect user feedback.  
In `tbot_app/telegram_bot/settings.py`, you can configure the bot name, contact information, and inline menu,
including buttons that trigger the bot to process text messages and
add records to a Google Sheets table.

### Structure
```
tickets_collector_tbot/
├── tbot_app/
│   ├── google_sheets/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── settings.py
│   │   └── utils.py
│   ├── logs/
│   ├── telegram_bot/
│   │   ├── __init__.py
│   │   ├── bot.py
│   │   ├── decorators.py
│   │   ├── exceptions.py
│   │   ├── filters.py
│   │   ├── handlers.py
│   │   ├── menu.py
│   │   ├── settings.py
│   │   ├── states.py
│   │   ├── text_templates.py
│   │   ├── utils.py
│   │   └── webhook.py
│   ├── Dockerfile
│   └── start_bot.py
├── tests/
│   └── __init__.py
├── Docker-compose.production.yml
├── Docker-compose.yml
├── LICENSE
├── README.md
├── README.ru.md
├── requirements.txt
├── requirements.txt.bak
└── setup.cfg
```

### Tech Stack

- Python 3.12.7
- pyTelegramBotAPI 4.31.0
- gspread 6.2.1
- Redis 7.1.0
- FastAPI 0.129.0
- Uvicorn 0.41.0
- Docker

## Project Setup and Run (without Docker)

### 1. Clone the repository and navigate into it using the command line

```bash
git clone https://github.com/sitkliph/tickets_collector_tbot
```

```bash
cd tickets_collector_tbot
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv  # Linux / macOS
python -m venv venv   # Windows
```

```bash
source venv/bin/activate      # Linux / macOS
source venv/Scripts/activate  # Windows
```

### 3. Install dependencies from requirements.txt

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### 4. Configurate the project

- Create a project in Google Cloud Console.
- Create a service user in Google Cloud Console and get a JSON key.
- Add a service user in editors of Google Sheets table.
- Fill constants in `tbot_app/google_sheets/settings.py` and `tbot_app/telegram_bot/settings.py`.
- Create file `.env` like `.env.example`

### 5. Run project

```bash
cd tbot_app
python start_bot.py
```

## Example
https://t.me/RevizorDVGUPSBot

## Author
Sergei Bakin  
sergey.bakin2000@gmail.com

## License
This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) for details.