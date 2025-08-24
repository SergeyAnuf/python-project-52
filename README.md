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
