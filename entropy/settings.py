import os
import socket
from pathlib import Path

from configurations import Configuration, values
from dotenv import load_dotenv

load_dotenv()

# MARKERS
# env 'I_AM_IN_DOCKER' defined in DOCKERFILE.
I_AM_IN_DOCKER = bool(int(os.getenv('I_AM_IN_DOCKER', default=0)))


class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.Value(os.getenv('SECRET_KEY'))

    # SECURITY WARNING: don't run with debug turned on in production!
    # noinspection DjangoDebugModeSettings
    DEBUG = values.BooleanValue(int(os.getenv('DEBUG', default=1)))

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
    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'django.middleware.security.SecurityMiddleware',
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

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DATABASE_NAME'),
            'USER': values.Value(os.getenv('DATABASE_USER')),
            'PASSWORD': values.Value(os.getenv('DATABASE_PASSWORD')),
            'HOST': values.Value(os.getenv('DATABASE_HOST')),
            'PORT': values.Value(os.getenv('DATABASE_PORT')),
            'CONN_MAX_AGE': None,
            'TEST': {
                'NAME': 'entropy_db_tests',
                'SERIALIZE': False,
            },
        }
    }

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

    INTERNAL_IPS = ['127.0.0.1', 'localhost', '0.0.0.0', ]


class Docker(Configuration):
    @property
    def INTERNAL_IPS(self):
        hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())

        return [ip[:-1] + "1" for ip in ips]