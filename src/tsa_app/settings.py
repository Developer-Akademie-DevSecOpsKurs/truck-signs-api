"""
Django settings for tsa_app project.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

MODE = os.getenv("MODE", "dev")

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(ROOT_BASE_DIR, "templates")

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-change-me-in-production")

DEBUG = os.getenv("DEBUG", "True") == "False"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "cloudinary",
    "tsa_products",
    "django.contrib.admin",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tsa_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
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

WSGI_APPLICATION = "tsa_app.wsgi.application"

db_engine = "django.db.backends.sqlite3" if MODE != "prod" else "django.db.backends.postgresql"

pg_config = {
        "ENGINE": db_engine,
        "NAME": os.getenv("DB_NAME", "trucksigns_db"),
        "USER": os.getenv("DB_USER", "trucksigns_user"),
        "PASSWORD": os.getenv("DB_PASSWORD", "supertrucksignsuser!"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
}
sqlite_config = {
        "ENGINE": db_engine,
        "NAME": BASE_DIR / "db.sqlite3",
    }

db_config = sqlite_config if MODE != "prod" else pg_config

DATABASES = {
    
    "default": db_config
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(ROOT_BASE_DIR, "static/")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(ROOT_BASE_DIR, "media")

CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000,https://www.signsfortrucks.com,https://signsfortrucks.com"
).split(",")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUD_NAME", ""),
    "API_KEY": os.getenv("CLOUD_API_KEY", ""),
    "API_SECRET": os.getenv("CLOUD_API_SECRET", ""),
}

# Only use Cloudinary in production if configured
if os.getenv("CLOUD_NAME", ""):
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
