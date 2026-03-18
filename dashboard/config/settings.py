from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production-xyz123'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
            ],
        },
    },
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
WSGI_APPLICATION = 'config.wsgi.application'

STATIC_URL  = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ── Project-specific paths ───────────────────────────────────────────────────
# Adjust if your data/ and models/ folders are elsewhere
DATA_DIR   = BASE_DIR.parent / 'data'
MODELS_DIR = BASE_DIR.parent / 'models'
MAPS_DIR   = BASE_DIR.parent / 'maps'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
