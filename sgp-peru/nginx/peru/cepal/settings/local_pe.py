from .cepal_pe import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
SECURE_HSTS_SECONDS = 0

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
