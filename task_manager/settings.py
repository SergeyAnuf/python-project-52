"""
Django settings for task_manager project.

Generated by 'django-admin startproject' using Django 5.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django.http import Http404
from django.core.exceptions import PermissionDenied

import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(BASE_DIR)

# Загрузка переменных окружения
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-backup-key')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.getenv('DEBUG', 'True') == 'True'
DEBUG = True

import os
import rollbar

# Rollbar Settings
ROLLBAR_ACCESS_TOKEN = os.getenv('ROLLBAR_ACCESS_TOKEN')



    # Rollbar Configuration
ROLLBAR = {
    'access_token': ROLLBAR_ACCESS_TOKEN,
    'environment': 'development' if DEBUG else 'production',
    'scrub_fields': ['password', 'secret', 'token', 'api_key'],
    'branch': 'main',
    'code_version': '1.0',
    'root': BASE_DIR,
    'exception_level_filters': [
        (Http404, 'ignored'),
        (PermissionDenied, 'warning'),
    ],
    'enabled': not DEBUG,  # Отключаем в режиме разработки
}

# Initialize Rollbar
rollbar.init(**ROLLBAR)

ALLOWED_HOSTS = [
    'python-project-52-ru09.onrender.com',
    'webserver',
    'localhost',
    '127.0.0.1',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'task_manager',
    'django_bootstrap5',
    'task_manager.users.apps.UsersConfig',
    'task_manager.statuses',
    'task_manager.tasks',
    'task_manager.labels',
    'django_filters',
]


# Database configuration
# Database configuration
# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'your_db_name'),  # Значение по умолчанию для локальной разработки
        'USER': os.getenv('DB_USER', 'your_db_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'your_db_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'disable',  # Явное отключение SSL
            'ssl': False,           # Дополнительное отключение SSL
        },
    }
}

if os.getenv('DATABASE_URL'):
    # Обновляем конфигурацию для PostgreSQL
    DATABASES['default'] = dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        engine='django.db.backends.postgresql',
        ssl_require=True
    )

    # Для PostgreSQL явно указываем sslmode
    if DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
        # Создаем OPTIONS если его нет
        if 'OPTIONS' not in DATABASES['default']:
            DATABASES['default']['OPTIONS'] = {}
        DATABASES['default']['OPTIONS']['sslmode'] = 'require'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddlewareExcluding404',
]

ROOT_URLCONF = 'task_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'src/task_manager/templates',
            BASE_DIR / 'templates/django_bootstrap5',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_manager.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'rollbar': {
            'access_token': ROLLBAR_ACCESS_TOKEN,
            'class': 'rollbar.logger.RollbarHandler',
            'level': 'ERROR',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['rollbar'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/
AUTH_USER_MODEL = 'auth.User'

LANGUAGE_CODE = 'ru-ru'

LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Используйте BASE_DIR вместо абсолютного пути
]
STATIC_ROOT = BASE_DIR /'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
