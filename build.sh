#!/usr/bin/env bash
# Скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Установка зависимостей
uv pip install -r requirements.txt

# Миграции и сборка статики
python manage.py migrate
python manage.py collectstatic --noinput
