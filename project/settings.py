"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import firebase_admin
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-b&spl-j@t=97q@a!3rr=ss#z4&+b(y^1ofw53uy_3mx!4+9how"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True").lower() not in ["false", "no", "0"]

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = ["core"]

MIDDLEWARE = ["requestlogs.middleware.RequestLogsMiddleware"]

ROOT_URLCONF = "project.urls"


WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "requestlogs": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

REQUESTLOGS = {
    "STORAGE_CLASS": "project.logging.CustomRequestLogStorage",
    "ENTRY_CLASS": "project.logging.CustomRequestLogEntry",
    "SERIALIZER_CLASS": "project.logging.CustomRequestLogEntrySerializer",
    "SECRETS": ["password", "token"],
    "METHODS": ("GET", "PUT", "PATCH", "POST", "DELETE"),
    "SHRINK_JSON_GREATER_THAN": 256,
}


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": ["project.authentication.FirebaseAuthentication"],
    "UNAUTHENTICATED_USER": None,
    "DEFAULT_THROTTLE_CLASSES": ["project.throttling.DebounceThrottle"],
    "EXCEPTION_HANDLER": "requestlogs.views.exception_handler",
}


# Firebase configuration
# https://firebase.google.com/docs/admin/setup#initialize-sdk
os.environ.setdefault(
    "GOOGLE_APPLICATION_CREDENTIALS", str(BASE_DIR / "service-account-file.json")
)
FIREBASE_AUTH_HEADER_PREFIX = "Bearer"
FIREBASE_PROJECT_ID = "my-firebase-project-id"
FIREBASE_APP = firebase_admin.initialize_app()
