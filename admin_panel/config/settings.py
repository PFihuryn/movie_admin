"""
Django's settings for config project.
"""
import os
from pathlib import Path

import environs

env = environs.Env()
env.read_env()
AUTH_API_LOGIN_URL = env.str('AUTH_API_LOGIN_URL')

with env.prefixed('BACKEND_'):
    SECRET_KEY = env.str('SECRET_KEY')
    DEBUG = env.bool('DEBUG', False)
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', ['*'])
    INTERNAL_IPS = env.list("INTERNAL_IPS", '127.0.0.1')

with env.prefixed('NOTIFICATION_'):
    NOTIFICATION_DB_NAME = env.str('DB_NAME')
    NOTIFICATION_DB_USER = env.str('DB_USER')
    NOTIFICATION_DB_PASSWORD = env.str('DB_PASSWORD')
    NOTIFICATION_DB_HOST = env.str('DB_HOST', '127.0.0.1')
    NOTIFICATION_DB_PORT = env.str('DB_PORT', '5432')

with env.prefixed('AUTH_'):
    AUTH_DB_NAME = env.str('DB_NAME')
    AUTH_DB_USER = env.str('DB_USER')
    AUTH_DB_PASSWORD = env.str('DB_PASSWORD')
    AUTH_DB_HOST = env.str('DB_HOST', '127.0.0.1')
    AUTH_DB_PORT = env.str('DB_PORT', '5433')

with env.prefixed('MOVIE_'):
    MOVIE_DB_NAME = env.str('DB_NAME')
    MOVIE_DB_USER = env.str('DB_USER')
    MOVIE_DB_PASSWORD = env.str('DB_PASSWORD')
    MOVIE_DB_HOST = env.str('DB_HOST', '127.0.0.1')
    MOVIE_DB_PORT = env.str('DB_PORT', '5434')

with env.prefixed('MONGO_'):
    MONGO_HOST = env.str('HOST')
    MONGO_PORT = env.str('PORT')
    MONGO_DATABASE = env.str('DATABASE')

BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # install apps
    'django_summernote',
    'debug_toolbar',
    'djongo',
    # user apps
    'administrator.apps.AdministratorConfig',
    'notification',
    'authentication',
    'movie',
    'user_profile',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'auth_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': AUTH_DB_NAME,
        'USER': AUTH_DB_USER,
        'PASSWORD': AUTH_DB_PASSWORD,
        'HOST': AUTH_DB_HOST,
        'PORT': AUTH_DB_PORT,
        'OPTIONS': {
           'options': '-c search_path=public,auth'
        },
    },
    'notification_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': NOTIFICATION_DB_NAME,
        'USER': NOTIFICATION_DB_USER,
        'PASSWORD': NOTIFICATION_DB_PASSWORD,
        'HOST': NOTIFICATION_DB_HOST,
        'PORT': NOTIFICATION_DB_PORT,
        'OPTIONS': {
            'options': '-c search_path=public,notifications'
        },
    },
    'movie_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': MOVIE_DB_NAME,
        'USER': MOVIE_DB_USER,
        'PASSWORD': MOVIE_DB_PASSWORD,
        'HOST': MOVIE_DB_HOST,
        'PORT': MOVIE_DB_PORT,
        'OPTIONS': {
           'options': '-c search_path=public,movie'
        },
    },
    'profile_db': {
        'ENGINE': 'djongo',
        'NAME': MONGO_DATABASE,
        'CLIENT': {
            'host': f'mongodb://{MONGO_HOST}:{MONGO_PORT}',
        },
    },
}

DATABASE_ROUTERS = ['config.routers.CustomRouter']

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
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
}

LANGUAGE_CODE = 'ru-Ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

X_FRAME_OPTIONS = 'SAMEORIGIN'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'administrator.User'

AUTHENTICATION_BACKENDS = [
    'administrator.auth.CustomBackend',
    'django.contrib.auth.backends.ModelBackend',

]

LOCALE_PATHS = ['admin_panel/locale']
