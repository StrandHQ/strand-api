"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

if os.environ.get('ENVIRONMENT') == 'PROD':
    from config.settings.production import *
elif os.environ.get('ENVIRONMENT') == 'STAGING':
    from config.settings.staging import *
elif os.environ.get('ENVIRONMENT') == 'DEVELOPMENT':
    from config.settings.development import *
elif os.environ.get('ENVIRONMENT') == 'TEST':
    from config.settings.testing import *
else:
    from config.settings.local import *

# Release version
VERSION = '0.1.1'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+-t%(!_0ue0g5f=&p-2=2me_oktk#l=eaz!t631(j+$nv0fjm)'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'django_celery_results',
    'graphene_django',
    'rest_framework',
    'rest_framework.authtoken',
    'django_fsm',
    'fsm_admin',
    'corsheaders',
    'waffle',
    'storages',
    'app.users',
    'app.groups',
    'app.topics',
    'app.slack_integration',
    'app.dialogues',
    'raven.contrib.django.raven_compat',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Override auth user model
AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Graphene
# https://github.com/graphql-python/graphene-django/blob/master/docs/tutorial-plain.rst
GRAPHENE = {
    'SCHEMA': 'app.api.schema.schema'
}

# Django REST framework
# http://www.django-rest-framework.org/
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# Celery
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Sentry
# https://docs.sentry.io/clients/python/integrations/django/#setup
if os.environ.get('RAVEN_DSN'):
    RAVEN_CONFIG = {
        'dsn': os.environ['RAVEN_DSN'],
        'release': VERSION
    }

# http://waffle.readthedocs.io/en/latest/starting/configuring.html
WAFFLE_SWITCH_DEFAULT = False
