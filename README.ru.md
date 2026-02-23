# Tickets Collector Telegram Bot
[![en](https://img.shields.io/badge/lang-en-white.svg)](README.md) 
![workflow status badge](https://github.com/sitkliph/tickets_collector_tbot/actions/workflows/main.yml/badge.svg)

Бот для приема обращений, жалоб, вопросов и заявлений от пользователей.

## Описание проекта
Синхронный телеграмм бот, с помощью которого можно собирать обратную связь от пользователей.  
В `tbot_app/telegram_bot/settings.py` можно настроить название, контактную информацию, inline-меню,
включая кнопки, по нажатию которых бот обрабатывает произвольное текстовое сообщение и
добавляет запись в таблицу Google Sheets.

### Структура проекта
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

### Стек использованных технологий

- Python 3.12.7
- pyTelegramBotAPI 4.31.0
- gspread 6.2.1
- Redis 7.1.0
- FastAPI 0.129.0
- Uvicorn 0.41.0
- Docker

## Установка и запуск проекта (без использования Docker)

### 1. Клонировать репозиторий и перейти в него в командной строке

```bash
git clone https://github.com/sitkliph/tickets_collector_tbot
```

```bash
cd tickets_collector_tbot
```

### 2. Cоздать и активировать виртуальное окружение

```bash
python3 -m venv venv  # Linux / macOS
python -m venv venv   # Windows
```

```bash
source venv/bin/activate      # Linux / macOS
source venv/Scripts/activate  # Windows
```

### 3. Установить зависимости из файла requirements.txt

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

### 4. Выполнить настроки проекта

- Создать проект в консоли Google Cloud.
- Создать service user в консоли Google Cloud и получить JSON ключ.
- Подключить service user к онлайн таблице Google Sheets.
- Заполнить константы файлов `tbot_app/google_sheets/settings.py` и `tbot_app/telegram_bot/settings.py`.
- Создать файл `.env` по примеру `.env.example`

### 5. Запустить проект

```bash
cd tbot_app
python start_bot.py
```

## Пример
https://t.me/RevizorDVGUPSBot

## Автор
Sergei Bakin  
sergey.bakin2000@gmail.com

## Лицензия
Проект распространяется под лицензией **MIT**.  
Подробности см. в файле [LICENSE](LICENSE).