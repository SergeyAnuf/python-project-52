#!/usr/bin/env bash
set -e  # Прерывать скрипт при ошибках

# Установка uv (если нужно)
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.cargo/env"
fi

# Установка зависимостей
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Применение миграций
echo "Applying database migrations..."
python manage.py migrate --noinput

# Сбор статических файлов
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Опционально: создание суперпользователя (только для первого запуска)
# if [ -z "$(python manage.py shell -c 'from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(username="admin").exists()')" ]; then
#     echo "Creating superuser..."
#     echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', '$ADMIN_PASSWORD')" | python manage.py shell
# fi

echo "Build completed successfully!"