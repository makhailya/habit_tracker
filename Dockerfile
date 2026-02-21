FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание необходимых директорий
RUN mkdir -p staticfiles media

# Переменная окружения для Python
ENV PYTHONUNBUFFERED=1

# Порт приложения
EXPOSE 8000

# Команда запуска (переопределяется в docker-compose.yml)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
