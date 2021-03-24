FROM python:3.8-slim
WORKDIR /app
COPY . .
RUN pip install pyTelegramBotAPI sqlalchemy
RUN mkdir -p db
RUN python models.py
