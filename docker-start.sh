#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐳 Запуск Habit Tracker через Docker${NC}\n"

# Проверка установки Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker не установлен!${NC}"
    echo "Установите Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Проверка установки Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose не установлен!${NC}"
    echo "Установите Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker и Docker Compose установлены${NC}\n"

# Проверка файла .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  Файл .env не найден${NC}"
    echo "Создание .env из .env.docker..."
    cp .env.docker .env
    echo -e "${GREEN}✅ Файл .env создан${NC}\n"
else
    echo -e "${GREEN}✅ Файл .env найден${NC}\n"
fi

# Остановка существующих контейнеров
echo -e "${YELLOW}🛑 Остановка существующих контейнеров...${NC}"
docker-compose down

# Сборка образов
echo -e "\n${YELLOW}🔨 Сборка Docker образов...${NC}"
docker-compose build

# Запуск контейнеров
echo -e "\n${YELLOW}🚀 Запуск контейнеров...${NC}"
docker-compose up -d

# Ожидание запуска БД
echo -e "\n${YELLOW}⏳ Ожидание запуска базы данных...${NC}"
sleep 5

# Проверка статуса
echo -e "\n${YELLOW}📊 Проверка статуса контейнеров...${NC}"
docker-compose ps

# Применение миграций
echo -e "\n${YELLOW}🔄 Применение миграций...${NC}"
docker-compose exec -T web python manage.py migrate

# Сбор статики
echo -e "\n${YELLOW}📦 Сбор статических файлов...${NC}"
docker-compose exec -T web python manage.py collectstatic --noinput

# Проверка здоровья сервисов
echo -e "\n${YELLOW}🏥 Проверка здоровья сервисов...${NC}"

# Проверка PostgreSQL
if docker-compose exec -T db pg_isready -U postgres > /dev/null 2>&1; then
    echo -e "${GREEN}✅ PostgreSQL работает${NC}"
else
    echo -e "${RED}❌ PostgreSQL недоступен${NC}"
fi

# Проверка Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Redis работает${NC}"
else
    echo -e "${RED}❌ Redis недоступен${NC}"
fi

# Проверка Django
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Django работает${NC}"
else
    echo -e "${YELLOW}⚠️  Django еще запускается (подождите 10-15 секунд)${NC}"
fi

# Итоговая информация
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Habit Tracker успешно запущен!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "📍 Доступные URL:"
echo -e "   ${GREEN}API:${NC}        http://localhost:8000"
echo -e "   ${GREEN}Админка:${NC}    http://localhost:8000/admin"
echo -e "   ${GREEN}Swagger:${NC}    http://localhost:8000/swagger"
echo -e "   ${GREEN}ReDoc:${NC}      http://localhost:8000/redoc"

echo -e "\n📊 Полезные команды:"
echo -e "   ${YELLOW}Логи:${NC}              docker-compose logs -f"
echo -e "   ${YELLOW}Остановка:${NC}         docker-compose down"
echo -e "   ${YELLOW}Суперпользователь:${NC} docker-compose exec web python manage.py createsuperuser"
echo -e "   ${YELLOW}Тесты:${NC}             docker-compose exec web python manage.py test"

echo -e "\n${GREEN}Подробная документация в DOCKER_SETUP.md${NC}\n"
