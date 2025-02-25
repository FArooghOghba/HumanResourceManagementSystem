import os

from src.config.env import BASE_DIR, env


env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition
LOCAL_APPS = [
    'src.hr_management_system.core.apps.CoreConfig',
    'src.hr_management_system.common.apps.CommonConfig',
    'src.hr_management_system.users.apps.UsersConfig',
    'src.hr_management_system.departments.apps.DepartmentsConfig',
    'src.hr_management_system.employees.apps.EmployeesConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_mongoengine',
    'django_mongoengine.mongo_auth',
    'django_extensions',
    'corsheaders',
    'drf_spectacular',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.config.urls'

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

WSGI_APPLICATION = 'src.config.wsgi.application'


# Database

# MongoDB Configuration
# MongoDB Configuration for django-mongoengine:

MONGODB_DATABASES = {
    'default': {
        'ENGINE': 'django_mongoengine.mongoengine',  # Official MongoEngine Django integration
        'NAME': env('MONGO_DB', default='hrms'),
        'CLIENT': {
            'host': env('MONGO_URI', default='mongodb://localhost:27017/'),
            'authSource': env('MONGO_AUTH_SOURCE', default='admin'),
        }
    }
}

from mongoengine import connect
connect(
    db=env('MONGO_DB', default='hrms'),
    host=env('MONGO_URI', default='mongodb://localhost:27017/'),
    authentication_source=env('MONGO_AUTH_SOURCE', default='admin')
)

# File Storage Configuration
DEFAULT_FILE_STORAGE = 'django_mongoengine.storage.GridFSStorage'
GRIDFS_DATABASE = 'hrms_files'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'src.hr_management_system.users.models.BaseUser'
AUTHENTICATION_BACKENDS = [
    'django_mongoengine.mongo_auth.backends.MongoEngineBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = '/vol/web/static/'
STATIC_URL = '/static/'

MEDIA_ROOT = '/vol/web/media/'
MEDIA_URL = '/media/'

APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

# Security Headers
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

from src.config.settings.rest_framework import *  # noqa
from src.config.settings.cors import *  # noqa
from src.config.settings.jwt import *  # noqa
# from src.config.settings.sessions import *  # noqa
from src.config.settings.swagger import *  # noqa
from src.config.settings.logger import *  # noqa
