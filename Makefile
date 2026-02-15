.PHONY: help install migrate test coverage flake8 run celery-worker celery-beat superuser clean

help:
	@echo "Доступные команды:"
	@echo "  make install       - Установить зависимости"
	@echo "  make migrate       - Применить миграции"
	@echo "  make test          - Запустить тесты"
	@echo "  make coverage      - Проверить покрытие тестами"
	@echo "  make flake8        - Проверить код с Flake8"
	@echo "  make run           - Запустить Django сервер"
	@echo "  make celery-worker - Запустить Celery worker"
	@echo "  make celery-beat   - Запустить Celery beat"
	@echo "  make superuser     - Создать суперпользователя"
	@echo "  make clean         - Очистить временные файлы"

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

test:
	python manage.py test

coverage:
	coverage run --source='.' manage.py test
	coverage report
	coverage html
	@echo "HTML отчет создан в htmlcov/index.html"

flake8:
	flake8

run:
	python manage.py runserver

celery-worker:
	celery -A config worker -l info

celery-beat:
	celery -A config beat -l info

superuser:
	python manage.py createsuperuser

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf htmlcov/
	rm -f .coverage
	rm -rf .pytest_cache/
