#!/bin/bash

# Скрипт для запуска всех компонентов проекта Habit Tracker

echo "🚀 Запуск Habit Tracker..."

# Проверка виртуального окружения
if [ ! -d "venv" ]; then
    echo "❌ Виртуальное окружение не найдено. Создайте его командой: python -m venv venv"
    exit 1
fi

# Активация виртуального окружения
source venv/bin/activate

# Проверка зависимостей
echo "📦 Проверка зависимостей..."
pip install -r requirements.txt --quiet

# Применение миграций
echo "🗃️  Применение миграций..."
python manage.py migrate

# Запуск сервисов в фоне
echo "🔧 Запуск Redis..."
redis-server &
REDIS_PID=$!

echo "⚙️  Запуск Django сервера..."
python manage.py runserver &
DJANGO_PID=$!

echo "📨 Запуск Celery Worker..."
celery -A config worker -l info &
CELERY_WORKER_PID=$!

echo "⏰ Запуск Celery Beat..."
celery -A config beat -l info &
CELERY_BEAT_PID=$!

echo ""
echo "✅ Все сервисы запущены!"
echo ""
echo "📍 Django сервер: http://localhost:8000"
echo "📍 Админка: http://localhost:8000/admin"
echo "📍 Swagger: http://localhost:8000/swagger"
echo "📍 ReDoc: http://localhost:8000/redoc"
echo ""
echo "Для остановки нажмите Ctrl+C"

# Функция для остановки всех процессов
cleanup() {
    echo ""
    echo "🛑 Остановка сервисов..."
    kill $REDIS_PID $DJANGO_PID $CELERY_WORKER_PID $CELERY_BEAT_PID 2>/dev/null
    echo "✅ Все сервисы остановлены"
    exit 0
}

# Обработка сигнала остановки
trap cleanup SIGINT SIGTERM

# Ожидание
wait
