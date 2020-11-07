"""
Django settings for datatitan_site project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from google.cloud import secretmanager
import google.auth
import google.auth.transport.requests
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "(^i4r9k3ncsb7p1^z6o2(&n1-11uk_iy06qud6zb-@ho_^*$q5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "data-titans.uc.r.appspot.com"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "data.apps.DataConfig",
    "blog.apps.BlogConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "datatitan_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "datatitan_site.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

POSTGRES_USER = os.getenv("POSTGRES_USER", "DataTitans")
POSTGRES_PASSWORD_FILE = os.getenv("POSTGRES_PASSWORD_FILE", BASE_DIR.parent / "cred" / "postgres_password.txt")
APP_ENV = os.getenv("APP_ENV")

if APP_ENV == "docker-compose":
    # Only attempt to access the postgres daemon if you think you're running in a docker container
    with Path(POSTGRES_PASSWORD_FILE).open("r") as file:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "DataTitans",
                "HOST": "db",
                "USER": POSTGRES_USER if POSTGRES_USER else "DataTitans",
                "PASSWORD": file.read(),
                "PORT": "5432",
            }
        }
elif APP_ENV == "google-app-engine":
    creds, project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    client = secretmanager.SecretManagerServiceClient()
    db_user = client.access_secret_version(
        name="projects/984278497023/secrets/DataTitans-Postgres-Account/versions/latest"
    )
    account = json.loads(db_user.payload.data)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "DataTitans",
            "HOST": "/cloudsql/data-titans:us-central1:datatitan-db"
            if os.getenv("SERVER_SOFTWARE")
            else "localhost",
            "PORT": "5432",
            **account,
        }
    }
else:
    with Path(POSTGRES_PASSWORD_FILE).open("r") as file:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "DataTitans",
                "HOST": "db",
                "USER": POSTGRES_USER if POSTGRES_USER else "DataTitans",
                "PASSWORD": file.read(),
                "PORT": "5432",
            }
        }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
        "LOCATION": "memcached:11211"
    } if not APP_ENV != "docker-compose" else {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
