from .base import *  # noqa: F401,F403

DEBUG = True

# Serve static through WhiteNoise in dev too, uncached, so an edited CSS or JS
# file shows on a plain reload (owner decision: never a hard refresh).
INSTALLED_APPS = ["whitenoise.runserver_nostatic", *INSTALLED_APPS]  # noqa: F405
WHITENOISE_MAX_AGE = 0
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
