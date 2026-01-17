FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание директорий для медиа и статики
RUN mkdir -p /app/staticfiles /app/media

# Команда по умолчанию (может быть переопределена в docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "foodgram.wsgi:application"]
