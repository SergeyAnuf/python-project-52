### Project Task manager
__________________________________________________________________________________________________________________
### Hexlet tests and linter status:
[![Actions Status](https://github.com/SergeyAnuf/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)]
[![Actions Status](https://github.com/SergeyAnuf/python-project-52/actions/workflows/my_workflow.yml/badge.svg)]


[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=SergeyAnuf_python-project-52)](https://sonarcloud.io/summary/new_code?id=SergeyAnuf_python-project-52)
__________________________________________________________________________
Ссылка на проект на Render:

https://python-project-52-ru09.onrender.com
__________________________________________________________________________
***
## Requiremtnts:
    python>=3.12
    uv>=0.7.3
    django>=5.2.3
    gunicorn>=23.0.0
    python-dotenv>=1.1.1
    dj-database-url>=3.0.0
    psycopg2-binary>=2.9.10
    ruff>=0.11.9
    django-bootstrap5>=25.1
    whitenoise>=6.9.0
    django-filter>=24.2
    rollbar>=1.3.0
## Installation:

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

Local start:
````
python manage.py runserver
````
***
Command on render.com:

build:
````
uv sync --frozen && uv cache prune --ci && python manage.py collectstatic --noinput
````
start:
````
gunicorn --bind 0.0.0.0:$(PORT) task_manager.wsgi:application
````
***
