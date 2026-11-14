import os

from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = [h.strip() for h in os.environ["ALLOWED_HOSTS"].split(",") if h.strip()]

# Runflare disk mounts (ADR-0003): one disk at /app/database keeps the
# sqlite file across redeploys, and one at /app/public/media keeps uploads.
# Not at /app/public: a disk there would hide the committed public/static/.
# Static and media paths themselves live in base.py.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DATABASE_PATH", "/app/database/db.sqlite3"),
    }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email provider not picked yet (must be reachable from Iran — see
# docs/plan.md open items). Until EMAIL_HOST is set, notifications are
# silently skipped; inquiries are still saved and readable in the admin.
# Dummy, not console, backend: console would write patient details to logs.
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_BACKEND = (
    "django.core.mail.backends.smtp.EmailBackend"
    if EMAIL_HOST
    else "django.core.mail.backends.dummy.EmailBackend"
)
EMAIL_PORT = int(os.environ.get("EMAIL_PORT") or 587)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True
INQUIRY_NOTIFICATION_EMAIL = os.environ.get("INQUIRY_NOTIFICATION_EMAIL", "")
