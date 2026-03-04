# Трекер полезных привычек

Веб-приложение для отслеживания и формирования полезных привычек на основе книги "Атомные привычки" Джеймса Клира.

## Особенности проекта

- 🔐 Аутентификация и регистрация пользователей
- ✅ CRUD операции с привычками
- 📱 Интеграция с Telegram для напоминаний
- ⏰ Автоматические напоминания через Celery
- 📊 Пагинация списка привычек (5 на страницу)
- 🔒 Разделение на личные и публичные привычки
- ✨ Валидация бизнес-правил
- 📖 Автоматическая документация API (Swagger/ReDoc)
- 🧪 Покрытие тестами >80%

## Технологический стек

- Python 3.10+
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Telegram Bot API
- Docker (опционально)

## Установка и запуск

### Вариант 1: Docker (рекомендуется) 🐳

**Самый простой способ запустить проект:**

```bash
# 1. Клонируйте репозиторий
git clone <URL>
cd habit_tracker

# 2. Создайте .env файл
cp .env.docker .env

# 3. Запустите все сервисы
docker-compose up -d

# 4. Создайте суперпользователя
docker-compose exec web python manage.py createsuperuser

# 5. Откройте в браузере
# http://localhost:8000
```

**Подробная документация:** см. [DOCKER_SETUP.md](DOCKER_SETUP.md)

### Вариант 2: Локальная установка

### 1. Клонирование репозитория

```bash
git clone <URL репозитория>
cd habit_tracker
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
venv\Scripts\activate  # для Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` и укажите свои значения:

```env
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=habit_tracker_db
DB_USER=postgres
DB_PASSWORD=ваш-пароль
DB_HOST=localhost
DB_PORT=5432

TELEGRAM_BOT_TOKEN=ваш-токен-бота

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 5. Создание базы данных PostgreSQL

```bash
createdb habit_tracker_db
```

### 6. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Запуск сервера разработки

```bash
python manage.py runserver
```

### 9. Запуск Redis (в отдельном терминале)

```bash
redis-server
```

### 10. Запуск Celery Worker (в отдельном терминале)

```bash
celery -A config worker -l info
```

### 11. Запуск Celery Beat (в отдельном терминале)

```bash
celery -A config beat -l info
```

## Настройка Telegram бота

### 1. Создание бота

1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте токен бота
5. Добавьте токен в файл `.env` как `TELEGRAM_BOT_TOKEN`

### 2. Получение Chat ID

1. Начните диалог с вашим ботом
2. Отправьте любое сообщение
3. Откройте в браузере: `https://api.telegram.org/bot<ВАШ_ТОКЕН>/getUpdates`
4. Найдите `chat.id` в JSON ответе
5. Укажите этот ID в профиле пользователя через API или админку

## API Endpoints

### Пользователи

- `POST /api/users/register/` - Регистрация нового пользователя
- `POST /api/users/login/` - Авторизация пользователя
- `GET /api/users/profile/` - Получение профиля
- `PATCH /api/users/profile/` - Обновление профиля

### Привычки

- `GET /api/habits/my-habits/` - Список привычек пользователя
- `POST /api/habits/my-habits/` - Создание новой привычки
- `GET /api/habits/my-habits/{id}/` - Детали привычки
- `PUT /api/habits/my-habits/{id}/` - Обновление привычки
- `PATCH /api/habits/my-habits/{id}/` - Частичное обновление
- `DELETE /api/habits/my-habits/{id}/` - Удаление привычки
- `GET /api/habits/public/` - Список публичных привычек

### Документация

- `/swagger/` - Swagger UI
- `/redoc/` - ReDoc

## Модель данных

### Habit (Привычка)

| Поле | Тип | Описание |
|------|-----|----------|
| user | ForeignKey | Владелец привычки |
| place | CharField | Место выполнения |
| time | TimeField | Время выполнения |
| action | CharField | Описание действия |
| is_pleasant | Boolean | Признак приятной привычки |
| related_habit | ForeignKey | Связанная приятная привычка |
| periodicity | Integer | Периодичность (1-7 дней) |
| reward | CharField | Вознаграждение |
| execution_time | Integer | Время на выполнение (≤120 сек) |
| is_public | Boolean | Публичная привычка |

## Правила валидации

1. ⏱️ Время выполнения не больше 120 секунд
2. 📅 Периодичность от 1 до 7 дней
3. 🎁 Либо вознаграждение, либо связанная привычка (не оба)
4. 😊 Связанная привычка должна быть приятной
5. ⛔ У приятной привычки нет вознаграждения и связанных привычек

## Запуск тестов

### Запуск всех тестов

```bash
python manage.py test
```

### Запуск тестов с покрытием

```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # для HTML отчета
```

### Проверка стиля кода (Flake8)

```bash
flake8
```

## Деплой на production сервер 🚀

### Автоматический деплой через GitHub Actions

Проект настроен для автоматического деплоя при каждом push в main/develop ветки.

**GitHub Actions автоматически:**
1. ✅ Запускает все тесты
2. ✅ Проверяет code style (flake8)
3. ✅ Измеряет покрытие тестами
4. ✅ Деплоит на сервер (после успешных тестов)

### Быстрый старт деплоя

```bash
# 1. Настройте сервер (один раз)
ssh root@your_server_ip
curl -O https://raw.githubusercontent.com/your-username/habit_tracker/main/server-setup.sh
chmod +x server-setup.sh
sudo ./server-setup.sh https://github.com/your-username/habit_tracker.git

# 2. Настройте GitHub Secrets (один раз)
# См. DEPLOYMENT.md

# 3. Push в main - всё остальное автоматически!
git push origin main
```

**Подробная документация:** см. [DEPLOYMENT.md](DEPLOYMENT.md)

### Docker деплой (альтернатива)

```bash
# На сервере
cd /path/to/project
cp .env.docker .env
docker-compose up -d
```

**Подробная документация:** см. [DOCKER_SETUP.md](DOCKER_SETUP.md)

## Структура проекта

```
habit_tracker/
├── config/              # Настройки проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── celery.py
├── users/               # Приложение пользователей
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── habits/              # Приложение привычек
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── validators.py
│   ├── permissions.py
│   ├── telegram_bot.py
│   ├── tasks.py
│   └── tests.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── .flake8
└── README.md
```

## Примеры использования API

### Регистрация пользователя

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Создание привычки

```bash
curl -X POST http://localhost:8000/api/habits/my-habits/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "place": "Дом",
    "time": "08:00:00",
    "action": "Выпить стакан воды",
    "execution_time": 60,
    "periodicity": 1,
    "is_pleasant": false,
    "is_public": false
  }'
```

## Лицензия

MIT License

## Автор

Маханек Илья

## Контакты

- Email: makhailya@gmail.com
- GitHub: https://github.com/makhailya# Submission for homework
