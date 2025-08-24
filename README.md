### Project Task manager
__________________________________________________________________________________________________________________
### Hexlet tests and linter status:
[![Actions Status](https://github.com/SergeyAnuf/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SergeyAnuf/python-project-52/actions/workflows/hexlet-check.yml)
[![Actions Status](https://github.com/SergeyAnuf/python-project-52/actions/workflows/my_workflow.yml/badge.svg)](https://github.com/SergeyAnuf/python-project-52/actions/workflows/my_workflow.yml)


[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=SergeyAnuf_python-project-52)](https://sonarcloud.io/summary/new_code?id=SergeyAnuf_python-project-52)
__________________________________________________________________________
Ссылка на проект на Render:

https://python-project-52-ru09.onrender.com
__________________________________________________________________________
***
### МЕНЕДЖЕР ЗАДАЧ 
___________________________________________________________________________
Это веб-приложение, разработанное на Python, для управления задачами.С его помощью можно создавать задачи, назначать исполнителей, устанавливать статусы и добавлять метки. Также можно производить изменения во всех данных задач.
__________________________________________________________________________

### 🛠️ Инструменты и зависимости

Проект использует следующие ключевые зависимости:

Django — высокоуровневый Python веб-фреймворк для быстрой разработки с чистой архитектурой.

Gunicorn — WSGI-сервер для развертывания Django-приложений в production-среде.

Python-dotenv — загрузка переменных окружения из файла .env для конфигурации приложения.

Dj-database-url — парсинг строк подключения к БД из переменной окружения DATABASE_URL.

Psycopg2-binary — адаптер PostgreSQL для Django, необходим для работы с PostgreSQL.

Ruff — сверхбыстрый линтер и форматтер для Python, заменяет flake8, isort и другие.

Django-bootstrap5 — интеграция Bootstrap 5 с Django для стилизации и компонентов.

Whitenoise — обслуживание статических файлов (CSS, JS, изображения).

Django-filter — простой и мощный фильтр для наборов данных Django QuerySet.

Rollbar — отслеживание ошибок и мониторинг производительности приложения в реальном времени.



## Установка:

````
git clone git@github.com:SergeyAnuf/python-project-52.git
````

````
cd python-project-52
````

`````
uv build
``````

````````
uv tool install dist/*.whl
````````

***

Локальный запуск:
````
python manage.py runserver
````
***
Команды на render.com:

build:
````
uv sync --frozen && uv cache prune --ci && python manage.py collectstatic --noinput
````
start:
````
gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi:application
````
***
