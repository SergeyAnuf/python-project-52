from setuptools import setup, find_packages

setup(
    name='task_manager',
    version='0.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src', include=[
        'task_manager',
        'task_manager.*',
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