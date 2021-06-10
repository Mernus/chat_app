import os
import dj_database_url

from re import search
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = os.getenv('DJANGO_SECRET', "django-insecure-xv99l00gmzi%bgm+%6w_i$jga*3gt-@1f=5o0#e#u^3vwkibr3")
DEBUG = bool(int(os.getenv('DJANGO_DEBUG', 0)))
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat.apps.ChatConfig',

    # Third party apps
    'rest_framework',
    # 'corsheaders',
    'channels',
    'channels_redis',

    # Our apps
    'notifications'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'chat_app/templates'],
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

X_FRAME_OPTIONS = 'SAMEORIGIN'
ROOT_URLCONF = 'emanager_chat.urls'
WSGI_APPLICATION = 'emanager_chat.wsgi.application'
ASGI_APPLICATION = 'emanager_chat.asgi.application'

DATABASE_URL = os.getenv('DATABASE_URL')
CONFIG = dj_database_url.config(ssl_require=True, conn_max_age=600, engine="mongodb")

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': CONFIG.get('NAME'),
        'CLIENT': {
            'host': DATABASE_URL,
            'username': CONFIG.get('USER'),
            'password': CONFIG.get('PASSWORD')
        }
    }
}

LANGUAGE_CODE = 'en-us'

# Datetime
USE_TZ = True
USE_L10N = False
TIME_ZONE = 'Europe/Moscow'
DATETIME_FORMAT = "d.m.Y H:i"

# Static
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "emanager_chat/staticfiles")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "chat_app/static"),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (),
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PAGINATION_CLASS': 'main.pagination.BasePagination',
    'DATETIME_FORMAT': "%d.%m.%Y %H:%M",
}

# CORS_ORIGIN_ALLOW_ALL = True

NOTIFICATIONS_CHANNELS = {
    'websocket': 'notifications.channels.WebSocketChannel'
}

# Redis
REDIS_URL = os.getenv('STACKHERO_REDIS_URL_TLS', 'redis://localhost:6379')
REDIS_REGEX = search(r'(.+):(\d+)$', REDIS_URL)
REDIS_HOST, REDIS_PORT = REDIS_REGEX[1], REDIS_REGEX[2]

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

# Cache and sessions
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            'MAX_ENTRIES': 10000
        },
        "KEY_PREFIX": "emanager",
        "TIMEOUT": 432000,
    }
}

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://f3df07cb547f4f0eb1e265691773069e@o787779.ingest.sentry.io/5810465",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
