import mongomock
from mongoengine import disconnect, connect

from .base import *  # noqa


# Based on https://www.hacksoft.io/blog/optimize-django-build-to-run-faster-on-github-actions

DEBUG = False
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# MongoDB Test Configuration
MONGO_DB = 'test_hrms'  # Separate test database
MONGO_HOST = 'mongodb://localhost'

# Override MongoDB connection
disconnect()  # Disconnect any existing connections
connect(
    db=MONGO_DB,
    host=MONGO_HOST,
    alias='default',
    mongo_client_class=mongomock.MongoClient
)


# Your tests use mongomock for your MongoEngine models,
# while the SQLite configuration is solely to satisfy
# Django's expectations (e.g., for flush commands and other management operations)
# that require a SQL database backend.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Testing-specific email backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Speed up file storage
DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
