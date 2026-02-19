FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY ./tbot_app .

CMD [ "python", "start_bot.py" ]