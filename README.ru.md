# Tickets Collector Telegram Bot
[![en](https://img.shields.io/badge/lang-en-white.svg)](README.md)

Телеграм бот для сбора вопросов, жалоб, обращений и запросов от пользоватлей.

## Статус проекта
Проект в разработке.

## Описание проекта
Синхронный телеграмм бот, с помощью которого можно собирать обратную связь от пользователей.  
В `tbot_app/telegram_bot/settings.py` можно настроить название, контактную информацию, inline меню,
включая кнопки, по нажатию которых бот обрабатывает произвольное текстовое сообщение и
добавляет запись в таблицу Google Sheets.

Для тестирования и разработки используется хранилище состояний - `telebot.storage.StateMemoryStorage`.  
При необходимости измените параметр STORAGE в `tbot_app/telegram_bot/settings.py`.

### Структура проекта
```
tickets_collector_tbot/
├── logs/
├── tbot_app/
│   ├── google_sheets/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── settings.py
│   │   └── utils.py
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
│   │   └── utils.py
│   ├── Dockerfile
│   └── start_bot.py
├── tests/
│   └── __init__.py
├── Docker-compose.yml
├── LICENSE
├── README.md
├── README.ru.md
├── requirements.txt
└── setup.cfg
```

### Стек использованных технологий

- Python 3.12.7
- pyTelegramBotAPI 4.22.1
- gspread 6.2.1

## Установка и запуск проекта в ручном режиме

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
- Запустить Redis или перенастроить проект на использование StateMemoryStorage для разработки

### 5. Запустить проект

```bash
cd tbot_app
python start_bot.py
```

## Пример
https://t.me/KhozRevizorBot

## Автор
Sergei Bakin  
sergey.bakin2000@gmail.com

## Лицензия
Проект распространяется под лицензией **MIT**.  
Подробности см. в файле [LICENSE](LICENSE).