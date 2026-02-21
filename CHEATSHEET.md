# Шпаргалка по командам

## Быстрый старт

### 1. Первоначальная настройка
```bash
# Создать виртуальное окружение
python -m venv venv

# Активировать
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Создать .env из примера
cp .env.example .env
# Отредактировать .env своими значениями

# Создать БД
createdb habit_tracker_db

# Миграции
python manage.py makemigrations
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser
```

### 2. Ежедневный запуск

#### Вариант 1: Скрипт (Linux/Mac)
```bash
chmod +x start.sh
./start.sh
```

#### Вариант 2: Makefile
```bash
# Запустить Django
make run

# В других терминалах
make celery-worker
make celery-beat
```

#### Вариант 3: Вручную
```bash
# Терминал 1: Redis
redis-server

# Терминал 2: Django
python manage.py runserver

# Терминал 3: Celery Worker
celery -A config worker -l info

# Терминал 4: Celery Beat
celery -A config beat -l info
```

#### Вариант 4: Docker
```bash
docker-compose up
```

## Django команды

```bash
# Создать миграции
python manage.py makemigrations

# Применить миграции
python manage.py migrate

# Запустить сервер
python manage.py runserver

# Создать суперпользователя
python manage.py createsuperuser

# Django shell
python manage.py shell

# Собрать статику
python manage.py collectstatic

# Проверить проект
python manage.py check
```

## Тестирование

```bash
# Все тесты
python manage.py test

# Конкретное приложение
python manage.py test habits
python manage.py test users

# Конкретный тест
python manage.py test habits.tests.HabitModelTest

# С покрытием
coverage run --source='.' manage.py test
coverage report
coverage html  # -> htmlcov/index.html
```

## Проверка кода

```bash
# Flake8
flake8

# Только конкретная папка
flake8 habits/
flake8 users/

# Игнорировать миграции
flake8 --exclude=*/migrations/*
```

## Celery

```bash
# Worker
celery -A config worker -l info

# Beat scheduler
celery -A config beat -l info

# Вместе
celery -A config worker -B -l info

# Flower (мониторинг)
celery -A config flower
# Открыть http://localhost:5555
```

## Git команды

```bash
# Инициализация
git init
git add .
git commit -m "Initial commit"

# Добавить remote
git remote add origin <URL>
git push -u origin main

# Обновление
git add .
git commit -m "Описание изменений"
git push

# Статус
git status
git log --oneline
```

## PostgreSQL команды

```bash
# Создать БД
createdb habit_tracker_db

# Удалить БД
dropdb habit_tracker_db

# Подключиться к БД
psql habit_tracker_db

# Внутри psql
\dt                # Список таблиц
\d <table_name>    # Структура таблицы
\q                 # Выход
```

## Docker команды

```bash
# Запустить
docker-compose up

# Запустить в фоне
docker-compose up -d

# Остановить
docker-compose down

# Пересобрать
docker-compose build

# Логи
docker-compose logs -f

# Выполнить команду
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Полезные URL

```
Django Admin:    http://localhost:8000/admin
Swagger UI:      http://localhost:8000/swagger
ReDoc:           http://localhost:8000/redoc
API Root:        http://localhost:8000/api
Flower:          http://localhost:5555
```

## Переменные окружения (.env)

```env
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=habit_tracker_db
DB_USER=postgres
DB_PASSWORD=пароль
DB_HOST=localhost
DB_PORT=5432

TELEGRAM_BOT_TOKEN=ваш-токен
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Решение проблем

### Проблема: Port already in use
```bash
# Найти процесс на порту 8000
lsof -i :8000

# Убить процесс
kill -9 <PID>
```

### Проблема: Redis connection refused
```bash
# Проверить статус Redis
redis-cli ping
# Должно вернуть PONG

# Запустить Redis
redis-server
```

### Проблема: Database does not exist
```bash
# Создать БД
createdb habit_tracker_db

# Или в psql
CREATE DATABASE habit_tracker_db;
```

### Проблема: Migration conflicts
```bash
# Сбросить все миграции (ОСТОРОЖНО!)
python manage.py migrate --fake
python manage.py migrate --fake-initial
```

### Проблема: Static files not found
```bash
python manage.py collectstatic --noinput
```

## Telegram Bot

### Получение Chat ID

1. Найти бота @userinfobot в Telegram
2. Отправить /start
3. Скопировать Id из ответа

### Или через API
```bash
# Отправить сообщение боту
# Затем открыть:
curl https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates

# Найти chat.id в JSON
```

## Создание дампа БД

```bash
# Экспорт
python manage.py dumpdata > db.json

# Импорт
python manage.py loaddata db.json

# Только конкретное приложение
python manage.py dumpdata habits > habits.json
```

## Очистка

```bash
# Удалить __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +

# Удалить .pyc файлы
find . -type f -name "*.pyc" -delete

# Или использовать make
make clean
```

## Горячие клавиши PyCharm

```
Ctrl + Shift + F10  - Запустить файл
Ctrl + Shift + F9   - Отладка
Ctrl + /            - Комментарий
Ctrl + D            - Дублировать строку
Ctrl + Y            - Удалить строку
Ctrl + Alt + L      - Форматировать код
Shift + F6          - Переименовать
```

## Чеклист перед сдачей

- [ ] Все тесты проходят
- [ ] Покрытие тестами ≥ 80%
- [ ] Flake8 = 100%
- [ ] README.md заполнен
- [ ] .env.example обновлен
- [ ] Документация API работает
- [ ] CORS настроен
- [ ] Telegram интеграция работает
- [ ] Celery задачи работают
- [ ] Код на GitHub
- [ ] requirements.txt актуален
- 