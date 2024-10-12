import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from .jazzmin_settings import JAZZMIN_SETTINGS, JAZZMIN_UI_TWEAKS

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS = [
    # 'jazzmin',
    'adminsortable2',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tours',
    'flights',
    'hotels',
    'transfer',
    'about',
    'blog',
    'main',
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'ckeditor',
    'common',
    'contacts',
    'corsheaders',
    'django_admin_listfilter_dropdown',
    'rangefilter',
    'services',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'atlas_travel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Format', 'Font', 'FontSize', 'Bold', 'Italic', 'Underline', '-',
             'NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock', 'Image', 'Link', 'Unlink', 'Table',
             'Source', 'Maximize'],
        ],
        'width': 'auto',
        'height': '200px',
        'toolbarCanCollapse': True,
        'uiColor': '#f0f0f0',
        'removePlugins': 'elementspath',
        'extraPlugins': 'font,maximize',
        'fontSize_sizes': (
            '8/8px;9/9px;10/10px;11/11px;12/12px;14/14px;16/16px;18/18px;'
            '20/20px;22/22px;24/24px;26/26px;28/28px;36/36px;48/48px;72/72px'
        ),
        'font_names': (
            'Arial/Arial, Helvetica, sans-serif;'
            'Times New Roman/Times New Roman, Times, serif;'
            'Verdana'
        ),
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"

WSGI_APPLICATION = 'atlas_travel.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'AtlasTravel'),
        'USER': os.environ.get('POSTGRES_USER', 'admin'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'AtlasTravel'),
        'HOST': os.environ.get('POSTGRES_HOST', 'db'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]

LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('ky', _('Кыргызча')),
    ('ru', _('Русский')),
    ('en', _('English')),
]

MODELTRANSLATION_LANGUAGES = ('ky', 'ru', 'en')

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

BASE_URL = "http://185.245.182.159"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = [
    'cookie', 'x-csrftoken', 'content-type', 'accept', 'origin',
    'authorization', 'x-requested-with', 'access-control-request-headers',
    'access-control-request-method',
]

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
CSRF_COOKIE_HTTPONLY = False


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
MODELTRANSLATION_CACHE_BACKEND = 'default'
