"""Isolated regression tests. Never connect to a local or production database."""
from .test_base import *

SECRET_KEY = 'sgp-isolated-regression-tests-only'
SITE_ID = 6
COUNTRY = 'pe'
SITE_URL = 'http://testserver/'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_HOST_USER = 'sgp@example.test'
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
CSRF_COOKIE_SECURE = False
