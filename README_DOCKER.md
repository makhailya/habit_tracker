# 🎯 Habit Tracker

**Веб-приложение для отслеживания полезных привычек** на Django REST Framework с полной контейнеризацией через Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Tests](https://img.shields.io/badge/tests-24%20passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-97%25-brightgreen)

---

## 📋 Оглавление

- [Особенности](#-особенности)
- [Технологии](#-технологии)
- [Архитектура](#-архитектура)
- [Быстрый старт](#-быстрый-старт-локально)
- [Деплой на сервер](#-деплой-на-production-сервер)
- [CI/CD](#-cicd-pipeline)
- [API Документация](#-api-документация)
- [Тестирование](#-тестирование)

---

## ✨ Особенности

- ✅ Аутентификация пользователей (JWT токены)
- ✅ CRUD операции с привычками
- ✅ Telegram уведомления через бота
- ✅ Автоматические напоминания (Celery + Beat)
- ✅ Публичные и приватные привычки
- ✅ API документация (Swagger/ReDoc)
- ✅ Покрытие тестами 97%
- 🐳 **Полная контейнеризация всех сервисов**
- 🚀 **Автоматический деплой через GitHub Actions**

---

## 🛠 Технологии

### Backend
```
Django 4.2, Django REST Framework 3.14, Python 3.11
PostgreSQL 15, Redis 7, Celery 5.3
```

### DevOps & Контейнеризация
```
Docker, Docker Compose
Nginx (reverse proxy)
Gunicorn (WSGI server)
GitHub Actions (CI/CD)
```

### Интеграции
```
Telegram Bot API
Swagger/ReDoc (API docs)
```

---

## 🏗 Архитектура

Проект состоит из **6 контейнеров**, управляемых через Docker Compose:

```
┌─────────────────────────────────────────────────┐
│                    Nginx :80                     │
│              (Reverse Proxy)                     │
└──────────────────┬──────────────────────────────┘
                   │
           ┌───────┴────────┐
           │                │
┌──────────▼──────┐  ┌─────▼──────────┐
│   Django :8000  │  │  Static/Media  │
│   (Gunicorn)    │  │    (Volumes)   │
└────┬────────────┘  └────────────────┘
     │
     ├──────────────┬──────────────┬──────────────┐
     │              │              │              │
┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐  ┌─────▼──────┐
│PostgreSQL│  │  Redis   │  │  Celery  │  │Celery Beat │
│   :5432  │  │  :6379   │  │  Worker  │  │ (Scheduler)│
└──────────┘  └──────────┘  └──────────┘  └────────────┘
```

### Сервисы

| Контейнер | Описание | Порт |
|-----------|----------|------|
| **nginx** | Reverse proxy, отдача статики | 80 |
| **web** | Django + Gunicorn | 8000 (internal) |
| **db** | PostgreSQL база данных | 5432 (internal) |
| **redis** | Кэш и брокер для Celery | 6379 (internal) |
| **celery** | Асинхронный worker | - |
| **celery-beat** | Планировщик задач | - |

---

## 🚀 Быстрый старт (локально)

### Требования

- Docker 20.10+
- Docker Compose 2.0+

### Установка и запуск

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/makhailya/habit_tracker.git
cd habit_tracker

# 2. Создайте .env файл
cp .env.docker .env

# 3. Запустите все сервисы одной командой
docker-compose up -d

# 4. Создайте суперпользователя
docker-compose exec web python manage.py createsuperuser

# 5. Откройте приложение
open http://localhost
```

✅ **Готово!** Приложение запущено на http://localhost

### Полезные команды

```bash
# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Выполнение команд Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py test
docker-compose exec web python manage.py shell

# Проверка статуса
docker-compose ps
```

---

## 🌐 Деплой на production сервер

### Требования к серверу

- Ubuntu 20.04 / 22.04 LTS
- Минимум 2GB RAM
- Docker и Docker Compose установлены
- SSH доступ

### Шаг 1: Подготовка сервера

```bash
# Подключитесь к серверу
ssh user@your-server-ip

# Обновите систему
sudo apt-get update && sudo apt-get upgrade -y

# Установите Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Установите Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Проверьте установку
docker --version
docker-compose --version
```

### Шаг 2: Клонирование проекта

```bash
# На сервере
git clone https://github.com/makhailya/habit_tracker.git
cd habit_tracker

# Создайте .env файл
cp .env.docker .env
nano .env  # Отредактируйте переменные
```

### Шаг 3: Настройка .env для production

```env
# Django
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-server-ip,your-domain.com

# Database
DB_NAME=habit_tracker_db
DB_USER=postgres
DB_PASSWORD=strong-password-here
DB_HOST=db
DB_PORT=5432

# Celery & Redis
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Telegram (опционально)
TELEGRAM_BOT_TOKEN=your-bot-token
```

### Шаг 4: Запуск

```bash
# Запустите все контейнеры
docker-compose up -d

# Примените миграции (автоматически при старте)
# Но можно выполнить вручную:
docker-compose exec web python manage.py migrate

# Создайте суперпользователя
docker-compose exec web python manage.py createsuperuser

# Проверьте статус
docker-compose ps
```

### Шаг 5: Настройка firewall

```bash
# Откройте необходимые порты
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS (если используется)
sudo ufw enable
```

### Проверка работы

```
http://your-server-ip/           - Главная (404 - норма)
http://your-server-ip/admin      - Админка ✅
http://your-server-ip/swagger    - API документация ✅
```

---

## 🚀 CI/CD Pipeline

### Настройка автоматического деплоя

Проект использует **GitHub Actions** для автоматического тестирования и деплоя.

#### Workflow состоит из 3 jobs:

```
1. test           - Запуск тестов, coverage, flake8
2. docker-build   - Проверка сборки Docker образа
3. deploy         - Деплой на сервер через Docker Compose
```

### Настройка GitHub Secrets

Добавьте в Settings → Secrets and variables → Actions:

| Secret | Описание | Пример |
|--------|----------|--------|
| `SECRET_KEY` | Django SECRET_KEY | `django-insecure-abc123...` |
| `SERVER_HOST` | IP адрес сервера | `192.168.3.179` |
| `SERVER_USER` | SSH пользователь | `your-username` |
| `SERVER_PORT` | SSH порт | `22` |
| `SSH_PRIVATE_KEY` | SSH приватный ключ | `-----BEGIN OPENSSH...` |
| `PROJECT_PATH` | Путь к проекту на сервере | `/home/user/habit_tracker` |

### Генерация SSH ключа

```bash
# На вашем компьютере
ssh-keygen -t ed25519 -C "github-actions"

# Публичный ключ добавьте на сервер
cat ~/.ssh/id_ed25519.pub | ssh user@server-ip "cat >> ~/.ssh/authorized_keys"

# Приватный ключ добавьте в GitHub Secrets
cat ~/.ssh/id_ed25519
# Скопируйте весь вывод в SSH_PRIVATE_KEY
```

### Использование

После настройки:

```bash
# Просто делайте push в main или develop
git push origin main

# GitHub Actions автоматически:
# ✅ Запустит тесты
# ✅ Проверит Docker сборку
# ✅ Задеплоит на сервер
```

Следите за процессом: GitHub → Actions → Latest workflow

---

## 📖 API Документация

### Endpoints

#### Аутентификация
```
POST   /api/users/register/    - Регистрация
POST   /api/users/login/       - Получение токена
GET    /api/users/profile/     - Профиль пользователя
PATCH  /api/users/profile/     - Обновление профиля
```

#### Привычки
```
GET    /api/habits/my-habits/      - Список личных привычек
POST   /api/habits/my-habits/      - Создание привычки
GET    /api/habits/my-habits/{id}/ - Детали привычки
PUT    /api/habits/my-habits/{id}/ - Полное обновление
PATCH  /api/habits/my-habits/{id}/ - Частичное обновление
DELETE /api/habits/my-habits/{id}/ - Удаление
GET    /api/habits/public/         - Публичные привычки
```

#### Документация
```
/swagger/   - Swagger UI (интерактивная документация)
/redoc/     - ReDoc (альтернативная документация)
/api/schema/ - OpenAPI схема
```

### Пример запроса

```bash
# Регистрация
curl -X POST http://localhost/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'

# Создание привычки
curl -X POST http://localhost/api/habits/my-habits/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "place": "Дом",
    "time": "08:00:00",
    "action": "Выпить воду",
    "execution_time": 60,
    "periodicity": 1
  }'
```

---

## 🧪 Тестирование

### Локально

```bash
# В контейнере
docker-compose exec web python manage.py test

# С coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report

# Flake8
docker-compose exec web flake8
```

### Результаты

```
Tests: 24 passing ✅
Coverage: 97% ✅
PEP8: 100% ✅
```

---

## 📁 Структура проекта

```
habit_tracker/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow
├── config/                     # Django настройки
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── users/                      # Приложение пользователей
│   ├── models.py
│   ├── views.py
│   └── serializers.py
├── habits/                     # Приложение привычек
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── tasks.py              # Celery задачи
│   └── telegram_bot.py       # Telegram интеграция
├── nginx/                      # Nginx конфигурация
│   ├── nginx.conf
│   └── conf.d/
│       └── habit_tracker.conf
├── docker-compose.yml          # Оркестрация контейнеров
├── Dockerfile                  # Docker образ приложения
├── .dockerignore              # Исключения для Docker
├── .env.docker                # Шаблон переменных
├── requirements.txt           # Python зависимости
└── README.md                  # Этот файл
```

---

## 🌍 Демо

**Production сервер:**
```
http://192.168.3.179
```

**Публичный URL (ngrok):**
```
https://noncohesively-noncompromised-rosenda.ngrok-free.dev
```

---

## 🤝 Контрибьюция

1. Fork проекта
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменений (`git commit -m 'Add AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

---

## 📄 Лицензия

MIT License

---

## 👤 Автор

**Илья Маханек**

[![GitHub](https://img.shields.io/badge/GitHub-makhailya-181717?style=flat-square&logo=github)](https://github.com/makhailya)
[![Email](https://img.shields.io/badge/Email-makhailya@gmail.com-D14836?style=flat-square&logo=gmail)](mailto:makhailya@gmail.com)

**Python Backend Developer | Django Specialist | DevOps Enthusiast**

---

<div align="center">

**Сделано с ❤️ в рамках курса Django REST Framework**

⭐ Если проект был полезен, поставьте звезду!

</div>
