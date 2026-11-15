"""
Reads `.env` into the environment. The entry points (manage.py, wsgi.py,
asgi.py) call `load_env()` before Django picks a settings module, so
`DJANGO_SETTINGS_MODULE` can come from `.env`. Variables already set in the
real environment (e.g. the Runflare panel) always win over `.env`.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# config/env.py -> config -> repo root
BASE_DIR = Path(__file__).resolve().parent.parent


def load_env():
    load_dotenv(BASE_DIR / ".env")


def env_bool(name, default):
    """`true/1/yes/on` are True, `false/0/no/off` False; unset or empty gives `default`."""
    value = os.environ.get(name, "").strip().lower()
    if not value:
        return default
    if value in ("1", "true", "yes", "on"):
        return True
    if value in ("0", "false", "no", "off"):
        return False
    raise ValueError(f"{name}={value!r} is not a boolean (use true or false)")
