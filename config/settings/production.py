import os

from .base import *

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# Render provides DATABASE_URL automatically when PostgreSQL is attached
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Parse DATABASE_URL manually without extra dependencies
    # Format: postgresql://user:password@host:port/dbname
    import re

    match = re.match(
        r"postgresql://(?P<user>[^:]+):(?P<password>[^@]+)@"
        r"(?P<host>[^:]+):(?P<port>\d+)/(?P<dbname>.+)",
        DATABASE_URL,
    )
    if match:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": match.group("dbname"),
                "USER": match.group("user"),
                "PASSWORD": match.group("password"),
                "HOST": match.group("host"),
                "PORT": match.group("port"),
            }
        }
else:
    # Fallback to individual env vars
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "taskmanager"),
            "USER": os.getenv("POSTGRES_USER", "postgres"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
