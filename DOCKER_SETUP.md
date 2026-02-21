# 🐳 Запуск проекта через Docker

Этот файл содержит инструкции по запуску проекта **Habit Tracker** с использованием Docker и Docker Compose.

## 📋 Предварительные требования

Убедитесь, что у вас установлены:

- **Docker** (версия 20.10+)
- **Docker Compose** (версия 2.0+)

### Проверка установки:

```bash
docker --version
docker-compose --version
```

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <URL вашего репозитория>
cd habit_tracker
```

### 2. Настройка переменных окружения

```bash
# Создайте файл .env из примера
cp .env.docker .env

# Или скопируйте .env.example и измените DB_HOST и CELERY URLs
cp .env.example .env
```

**Важно!** Для Docker в файле `.env` должны быть следующие настройки:

```env
DB_HOST=db                              # не localhost!
CELERY_BROKER_URL=redis://redis:6379/0  # не localhost!
```

### 3. Запуск всех сервисов

```bash
# Запуск в фоновом режиме
docker-compose up -d

# Или запуск с выводом логов
docker-compose up
```

### 4. Создание суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Проверка работы

Откройте в браузере:
- **API**: http://localhost:8000
- **Админка**: http://localhost:8000/admin
- **Swagger**: http://localhost:8000/swagger
- **ReDoc**: http://localhost:8000/redoc

## 📦 Сервисы в Docker Compose

| Сервис | Описание | Порт | Контейнер |
|--------|----------|------|-----------|
| **db** | PostgreSQL база данных | 5432 | habit_tracker_db |
| **redis** | Redis для Celery | 6379 | habit_tracker_redis |
| **web** | Django backend | 8000 | habit_tracker_web |
| **celery** | Celery worker | - | habit_tracker_celery |
| **celery-beat** | Celery beat scheduler | - | habit_tracker_celery_beat |

## 🔍 Проверка работоспособности сервисов

### Проверка всех контейнеров

```bash
# Статус всех контейнеров
docker-compose ps

# Должны быть все в статусе "Up"
```

### Проверка Django (web)

```bash
# Проверка логов
docker-compose logs web

# Проверка миграций
docker-compose exec web python manage.py showmigrations

# Доступ к shell Django
docker-compose exec web python manage.py shell
```

### Проверка PostgreSQL (db)

```bash
# Подключение к базе данных
docker-compose exec db psql -U postgres -d habit_tracker_db

# Список таблиц
\dt

# Выход
\q
```

### Проверка Redis

```bash
# Подключение к Redis
docker-compose exec redis redis-cli

# Проверка
ping
# Должно вернуть: PONG

# Выход
exit
```

### Проверка Celery Worker

```bash
# Логи worker
docker-compose logs celery

# Должны видеть: "[tasks]" и "celery@... ready"
```

### Проверка Celery Beat

```bash
# Логи beat
docker-compose logs celery-beat

# Должны видеть: "Scheduler: Sending due task"
```

## 🛠️ Полезные команды

### Управление контейнерами

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Остановка с удалением volumes (БД будет очищена!)
docker-compose down -v

# Перезапуск
docker-compose restart

# Перезапуск конкретного сервиса
docker-compose restart web
```

### Просмотр логов

```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs web
docker-compose logs celery

# Логи в реальном времени
docker-compose logs -f web
```

### Выполнение команд Django

```bash
# Миграции
docker-compose exec web python manage.py migrate

# Создание миграций
docker-compose exec web python manage.py makemigrations

# Создание суперпользователя
docker-compose exec web python manage.py createsuperuser

# Сбор статики
docker-compose exec web python manage.py collectstatic --noinput

# Запуск тестов
docker-compose exec web python manage.py test

# Django shell
docker-compose exec web python manage.py shell
```

### Работа с базой данных

```bash
# Подключение к PostgreSQL
docker-compose exec db psql -U postgres -d habit_tracker_db

# Создание дампа БД
docker-compose exec db pg_dump -U postgres habit_tracker_db > backup.sql

# Восстановление из дампа
docker-compose exec -T db psql -U postgres habit_tracker_db < backup.sql
```

### Пересборка образов

```bash
# Пересборка всех образов
docker-compose build

# Пересборка конкретного сервиса
docker-compose build web

# Пересборка без кеша
docker-compose build --no-cache
```

### Очистка

```bash
# Остановка и удаление контейнеров
docker-compose down

# Удаление volumes (БД будет удалена!)
docker-compose down -v

# Удаление образов
docker-compose down --rmi all

# Полная очистка Docker
docker system prune -a --volumes
```

## 🔧 Разработка с Docker

### Hot reload (автоматическая перезагрузка)

Django автоматически перезагружается при изменении кода благодаря volume монтированию:

```yaml
volumes:
  - .:/app  # Локальная директория монтируется в контейнер
```

### Установка новых зависимостей

```bash
# 1. Добавьте пакет в requirements.txt
echo "новый-пакет==версия" >> requirements.txt

# 2. Пересоберите образ
docker-compose build web

# 3. Перезапустите контейнеры
docker-compose up -d
```

### Debugging

```bash
# Подключение к контейнеру
docker-compose exec web bash

# Внутри контейнера можете запускать команды
python manage.py shell
```

## 📊 Мониторинг

### Celery Flower (опционально)

Добавьте в `docker-compose.yml`:

```yaml
flower:
  build: .
  command: celery -A config flower
  ports:
    - "5555:5555"
  env_file:
    - .env
  depends_on:
    - redis
    - celery
```

Затем:
```bash
docker-compose up -d flower
```

Откройте: http://localhost:5555

## 🐛 Решение проблем

### Контейнер постоянно перезапускается

```bash
# Проверьте логи
docker-compose logs web

# Часто проблема в миграциях или настройках БД
```

### База данных недоступна

```bash
# Проверьте что PostgreSQL запущен
docker-compose ps db

# Проверьте логи
docker-compose logs db

# Проверьте health check
docker inspect habit_tracker_db | grep Health
```

### Celery не выполняет задачи

```bash
# Проверьте что Redis доступен
docker-compose exec redis redis-cli ping

# Проверьте логи worker
docker-compose logs celery

# Перезапустите worker
docker-compose restart celery
```

### Порты заняты

```bash
# Найдите процесс на порту 8000
lsof -i :8000

# Или измените порт в docker-compose.yml
ports:
  - "8001:8000"  # внешний:внутренний
```

### "Permission denied" ошибки

```bash
# В Dockerfile используется непривилегированный пользователь
# Убедитесь, что директории доступны:
docker-compose exec web ls -la /app
```

## 🔒 Production настройки

Для production окружения:

1. **Измените SECRET_KEY** в `.env`
2. **Установите DEBUG=False**
3. **Настройте ALLOWED_HOSTS**
4. **Используйте HTTPS**
5. **Настройте nginx** как reverse proxy
6. **Используйте gunicorn** вместо runserver:

```yaml
web:
  command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

7. **Настройте резервное копирование БД**
8. **Используйте Docker Secrets** для паролей

## 📚 Дополнительные ресурсы

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Django Docker Best Practices](https://docs.docker.com/samples/django/)
- [PostgreSQL Docker Hub](https://hub.docker.com/_/postgres)

## ✅ Чеклист перед деплоем

- [ ] SECRET_KEY изменен
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS настроен
- [ ] База данных защищена паролем
- [ ] .env не в репозитории
- [ ] Telegram токен актуален
- [ ] Тесты проходят
- [ ] Миграции применены
- [ ] Статика собрана
- [ ] Резервное копирование настроено

---

**Готово! Проект запущен в Docker! 🎉**

Если возникнут вопросы - смотрите README.md или CHEATSHEET.md
