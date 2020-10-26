import os
import socket
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
# noinspection DjangoDebugModeSettings

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
]

# Application definition

INSTALLED_APPS = [
    #  Standard apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party apps
    'debug_toolbar',
    'rest_framework',
    'djoser',
    'drf_yasg2',

    # Project's apps
    'users.apps.UsersConfig',
    'misc.apps.MiscConfig',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'entropy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'entropy.wsgi.application'
ASGI_APPLICATION = 'entropy.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

#  Cache settings.
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

#  INTERNAL_IPS dynamically calculated for docker.
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]

#  User model
AUTH_USER_MODEL = 'users.User'

#  Password hashers for basic auth.
PASSWORD_HASHERS = [
    'entropy.password_hashers.CustomArgon2PasswordHasher',  # new
]

# Simple JWT settings

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
}

# default timeout for 1 DB operation
DEFAULT_DATABASE_STATEMENT_TIMEOUT = 3000

# DJOSER = {
#     'SERIALIZERS': {
#         'user': 'users.serializers.CustomUserSerializer',
#     },
# }

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# HERE STARTS DYNACONF EXTENSION LOAD (Keep at the very bottom of settings.py)
# Read more at https://dynaconf.readthedocs.io/en/latest/guides/django.html
import dynaconf  # noqa

settings = dynaconf.DjangoDynaconf(
    __name__,
    core_loaders=['YAML', 'PY'],
    load_dotenv=True,
    dotenv_verbose=True,
    environments=True,
    merge_enabled=True,
    root_path=Path(r'.'),
    settings_files=[
        Path('settings.yaml'),
        Path('.secrets.yaml'),
        Path('drf_folder/drf_settings.yaml'),
        Path('djoser_folder/djoser_settings.yaml'),
    ],
    validators=[
        # Databases password and user must exists
        *[
            dynaconf.Validator(f'DATABASES.{database}.USER', must_exist=True) &
            dynaconf.Validator(f'DATABASES.{database}.PASSWORD', must_exist=True)
            for database in dynaconf.settings.DATABASES
        ],
        # REDIS password must exists
        *[
            dynaconf.Validator(f'CACHES.{cache}.OPTIONS.PASSWORD', must_exist=True)
            for cache in dynaconf.settings.CACHES
        ],
    ]
)  # noqa
# HERE ENDS DYNACONF EXTENSION LOAD (No more code below this line)
