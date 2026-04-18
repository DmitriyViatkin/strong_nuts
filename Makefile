.PHONY: run migrate makemigrations createsuperuser run_celery run_npm start_dev

# Переменные
PYTHON=python3
MANAGE=manage.py
PORT=8000

# Запуск Django
run:
	$(PYTHON) $(MANAGE) runserver 127.0.0.1:$(PORT)

# Миграции
migrate:
	$(PYTHON) $(MANAGE) migrate

makemigrations:
	$(PYTHON) $(MANAGE) makemigrations


run_celery:
	celery -A config worker -B -l info

# Запуск Vite (предполагаем, что папка называется frontend)
run_npm:
	cd frontend && npm run dev

m-migrate:
	 make makemigrations migrate

start_dev:
	make -j3 run run_npm run_celery

stop_all:
	pkill -f "runserver" || true
	pkill -f "celery" || true
	pkill -f "vite" || true

initial_data:
	$(PYTHON) $(MANAGE) start_page
start_prod:
	$(PYTHON) $(MANAGE) migrate wagtailcore && \
	$(PYTHON) $(MANAGE) migrate cities_light && \
	$(PYTHON) $(MANAGE) migrate && \
	$(PYTHON) $(MANAGE) collectstatic --noinput && \
	gunicorn config.wsgi:application --bind 0.0.0.0:8000