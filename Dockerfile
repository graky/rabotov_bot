FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install pyTelegramBotAPI sqlalchemy
RUN python models.py
