from setuptools import setup, find_packages

setup(
    name='task_manager',
    version='0.1.0',
    packages=find_packages(include=[
        'task_manager',
        'task_manager.*',
        'users',
        'statuses',
        'labels',
        'tasks',
        'locale',
        'staticfiles'
    ]),
    include_package_data=True,
    install_requires=[
        'Django>=5.0',
        'gunicorn',
        'whitenoise',
        'psycopg2-binary',
        'dj-database-url'
    ],
)