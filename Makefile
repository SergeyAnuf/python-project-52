PORT ?= 8000

build:
		./build.sh

install:
		uv sync

lint:
		uv run ruff check

lint-fix:
		uv run ruff check --fix

dev:
		python manage.py runserver

render-start:
		gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi:application