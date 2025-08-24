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
###МЕНЕДЖЕР ЗАДАЧ 
___________________________________________________________________________
Это веб-приложение, разработанное на Python, для управления задачами.С его помощью можно создавать задачи, назначать исполнителей, устанавливать статусы и добавлять метки. Также можно производить изменения во всех данных задач.
__________________________________________________________________________

###🛠️ Инструменты и зависимости

Проект использует следующие ключевые зависимости:

Django (django>=5.2.3) — высокоуровневый Python веб-фреймворк для быстрой разработки с чистой архитектурой.

Gunicorn (gunicorn>=23.0.0) — WSGI-сервер для развертывания Django-приложений в production-среде.

Python-dotenv (python-dotenv>=1.1.1) — загрузка переменных окружения из файла .env для конфигурации приложения.

Dj-database-url (dj-database-url>=3.0.0) — парсинг строк подключения к БД из переменной окружения DATABASE_URL.

Psycopg2-binary (psycopg2-binary>=2.9.10) — адаптер PostgreSQL для Django, необходим для работы с PostgreSQL.

Ruff (ruff>=0.11.9) — сверхбыстрый линтер и форматтер для Python, заменяет flake8, isort и другие.

Django-bootstrap5 (django-bootstrap5>=25.1) — интеграция Bootstrap 5 с Django для стилизации и компонентов.

Whitenoise (whitenoise>=6.9.0) — обслуживание статических файлов (CSS, JS, изображения) в production без反向代理.

Django-filter (django-filter>=24.2) — простой и мощный фильтр для наборов данных Django QuerySet.

Rollbar (rollbar>=1.3.0) — отслеживание ошибок и мониторинг производительности приложения в реальном времени.



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
