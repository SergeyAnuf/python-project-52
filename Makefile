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
		uv run gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi:application

install:
    uv pip install -r requirements.txt

collectstatic:
    python manage.py collectstatic --noinput

migrate:
    python manage.py migrate