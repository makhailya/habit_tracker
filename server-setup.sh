#!/bin/bash

# Скрипт для первоначальной настройки Ubuntu сервера для Habit Tracker
# Запускать с sudo правами

set -e  # Остановка при ошибке

echo "🚀 Начало настройки сервера для Habit Tracker"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Проверка прав root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ Этот скрипт должен быть запущен с правами root (sudo)${NC}"
   exit 1
fi

# 1. Обновление системы
echo -e "\n${YELLOW}📦 Обновление системы...${NC}"
apt-get update
apt-get upgrade -y

# 2. Установка необходимых пакетов
echo -e "\n${YELLOW}📦 Установка базовых пакетов...${NC}"
apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    redis-server \
    nginx \
    git \
    curl \
    supervisor \
    ufw \
    fail2ban

# 3. Настройка PostgreSQL
echo -e "\n${YELLOW}🗄️  Настройка PostgreSQL...${NC}"
sudo -u postgres psql -c "CREATE DATABASE habit_tracker_db;" 2>/dev/null || echo "База данных уже существует"
sudo -u postgres psql -c "CREATE USER habit_user WITH PASSWORD 'secure_password_here';" 2>/dev/null || echo "Пользователь уже существует"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE habit_tracker_db TO habit_user;" 2>/dev/null

# 4. Настройка Redis
echo -e "\n${YELLOW}🔴 Настройка Redis...${NC}"
systemctl enable redis-server
systemctl start redis-server

# 5. Создание пользователя для приложения
echo -e "\n${YELLOW}👤 Создание пользователя для приложения...${NC}"
useradd -m -s /bin/bash habituser 2>/dev/null || echo "Пользователь habituser уже существует"

# 6. Настройка директории проекта
echo -e "\n${YELLOW}📁 Настройка директории проекта...${NC}"
PROJECT_DIR="/home/habituser/habit_tracker"
mkdir -p $PROJECT_DIR
chown -R habituser:habituser /home/habituser

# 7. Клонирование репозитория (если указан)
if [ ! -z "$1" ]; then
    echo -e "\n${YELLOW}📥 Клонирование репозитория...${NC}"
    sudo -u habituser git clone $1 $PROJECT_DIR
fi

# 8. Создание виртуального окружения
if [ -d "$PROJECT_DIR" ] && [ ! -d "$PROJECT_DIR/venv" ]; then
    echo -e "\n${YELLOW}🐍 Создание виртуального окружения...${NC}"
    sudo -u habituser python3.11 -m venv $PROJECT_DIR/venv
fi

# 9. Настройка UFW (Firewall)
echo -e "\n${YELLOW}🔥 Настройка Firewall...${NC}"
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8000/tcp

# 10. Настройка Fail2Ban
echo -e "\n${YELLOW}🛡️  Настройка Fail2Ban...${NC}"
systemctl enable fail2ban
systemctl start fail2ban

# 11. Создание systemd сервисов
echo -e "\n${YELLOW}⚙️  Создание systemd сервисов...${NC}"

# Gunicorn сервис
cat > /etc/systemd/system/habit_tracker.service << EOF
[Unit]
Description=Habit Tracker Django Application
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=habituser
Group=habituser
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
    --workers 3 \\
    --bind unix:$PROJECT_DIR/habit_tracker.sock \\
    config.wsgi:application
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Celery Worker сервис
cat > /etc/systemd/system/celery-habit-tracker.service << EOF
[Unit]
Description=Celery Worker for Habit Tracker
After=network.target redis.service

[Service]
Type=forking
User=habituser
Group=habituser
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/celery -A config worker -l info --detach
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Celery Beat сервис
cat > /etc/systemd/system/celery-beat-habit-tracker.service << EOF
[Unit]
Description=Celery Beat for Habit Tracker
After=network.target redis.service

[Service]
Type=forking
User=habituser
Group=habituser
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/celery -A config beat -l info --detach
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 12. Настройка Nginx
echo -e "\n${YELLOW}🌐 Настройка Nginx...${NC}"
cat > /etc/nginx/sites-available/habit_tracker << 'EOF'
server {
    listen 80;
    server_name _;

    client_max_body_size 20M;

    location /static/ {
        alias /home/habituser/habit_tracker/staticfiles/;
    }

    location /media/ {
        alias /home/habituser/habit_tracker/media/;
    }

    location / {
        proxy_pass http://unix:/home/habituser/habit_tracker/habit_tracker.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/habit_tracker /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t

# 13. Перезагрузка сервисов
echo -e "\n${YELLOW}🔄 Перезагрузка сервисов...${NC}"
systemctl daemon-reload

# Не запускаем сервисы автоматически, т.к. нужно сначала настроить приложение
# systemctl enable habit_tracker celery-habit-tracker celery-beat-habit-tracker nginx
# systemctl start habit_tracker celery-habit-tracker celery-beat-habit-tracker
systemctl enable nginx
systemctl restart nginx

# 14. Установка Docker (опционально, для дополнительного задания)
echo -e "\n${YELLOW}🐳 Установка Docker...${NC}"
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
usermod -aG docker habituser
rm get-docker.sh

# Установка Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 15. Финальные инструкции
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Сервер успешно настроен!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"

echo -e "${YELLOW}📝 Следующие шаги:${NC}"
echo -e "1. Переключитесь на пользователя habituser:"
echo -e "   ${GREEN}sudo -u habituser -i${NC}"
echo -e ""
echo -e "2. Перейдите в директорию проекта:"
echo -e "   ${GREEN}cd ~/habit_tracker${NC}"
echo -e ""
echo -e "3. Создайте файл .env с настройками"
echo -e ""
echo -e "4. Установите зависимости:"
echo -e "   ${GREEN}source venv/bin/activate${NC}"
echo -e "   ${GREEN}pip install -r requirements.txt${NC}"
echo -e ""
echo -e "5. Примените миграции:"
echo -e "   ${GREEN}python manage.py migrate${NC}"
echo -e ""
echo -e "6. Соберите статику:"
echo -e "   ${GREEN}python manage.py collectstatic --noinput${NC}"
echo -e ""
echo -e "7. Создайте суперпользователя:"
echo -e "   ${GREEN}python manage.py createsuperuser${NC}"
echo -e ""
echo -e "8. Запустите сервисы:"
echo -e "   ${GREEN}sudo systemctl start habit_tracker${NC}"
echo -e "   ${GREEN}sudo systemctl start celery-habit-tracker${NC}"
echo -e "   ${GREEN}sudo systemctl start celery-beat-habit-tracker${NC}"
echo -e ""
echo -e "9. Включите автозапуск:"
echo -e "   ${GREEN}sudo systemctl enable habit_tracker${NC}"
echo -e "   ${GREEN}sudo systemctl enable celery-habit-tracker${NC}"
echo -e "   ${GREEN}sudo systemctl enable celery-beat-habit-tracker${NC}"

echo -e "\n${YELLOW}🔒 Настройки безопасности:${NC}"
echo -e "- UFW Firewall настроен"
echo -e "- Fail2Ban активирован"
echo -e "- Используйте SSH-ключи для доступа"
echo -e "- Измените пароль PostgreSQL в production"

echo -e "\n${YELLOW}📍 Полезные команды:${NC}"
echo -e "- Статус сервисов: ${GREEN}systemctl status habit_tracker${NC}"
echo -e "- Логи: ${GREEN}journalctl -u habit_tracker -f${NC}"
echo -e "- Перезапуск Nginx: ${GREEN}sudo systemctl restart nginx${NC}"
