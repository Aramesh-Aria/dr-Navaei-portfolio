import os

from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = [h.strip() for h in os.environ["ALLOWED_HOSTS"].split(",") if h.strip()]

# Paths below match Runflare's documented disk-mount setup (ADR-0003):
# a disk mounted at DATABASE_DISK_PATH keeps the sqlite file across
# redeploys, and a disk mounted at /app/public covers both static and
# media so neither is lost when the container restarts.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DATABASE_PATH", "/app/database/db.sqlite3"),
    }
}

STATIC_URL = "/public/static/"
STATIC_ROOT = "/app/public/static"
MEDIA_URL = "/public/media/"
MEDIA_ROOT = "/app/public/media"

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_USE_TLS = True
INQUIRY_NOTIFICATION_EMAIL = os.environ["INQUIRY_NOTIFICATION_EMAIL"]
