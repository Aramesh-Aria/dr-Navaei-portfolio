"""
Settings shared by every environment. Never import this directly —
use `dev.py` or `prod.py`, which both start with `from .base import *`.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# config/settings/base.py -> config/settings -> config -> repo root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = False
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "jazzmin",  # must come before django.contrib.admin
    "apps.core.admin_config.SiteAdminConfig",  # replaces django.contrib.admin (unread Inquiry count)
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.core",
    "apps.doctor",
    "apps.conditions",
    "apps.locations",
    "apps.inquiries",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "apps.core.middleware.RevalidateHtmlMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
# The contact form left open too long gets a Persian page back to the form.
CSRF_FAILURE_VIEW = "apps.core.views.csrf_failure"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Content is Farsi-only (ADR-0001) — this also gives the Django admin
# chrome itself in Farsi for free, which is a bonus for the non-technical
# Content Editor, not a reintroduction of the i18n-framework decision.
LANGUAGE_CODE = "fa"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# The public address, for canonical links, Open Graph and structured data.
SITE_URL = "https://dr.safanavaiee.ir"

# Static and media files: same layout as every environment, so dev and prod
# can't drift. Edit sources in `static_dev/` (gitignored, dev only), then run
# `collectstatic` locally and commit `public/static/`. Production serves that
# committed directory through WhiteNoise, so collectstatic never runs on
# Runflare (static_dev/ isn't deployed; running it there would rewrite the
# manifest without the site's own files).
STATIC_URL = "/public/static/"
STATIC_ROOT = BASE_DIR / "public" / "static"
STATICFILES_DIRS = [BASE_DIR / "static_dev"]

# Uploads (the doctor's photo). Gitignored; on Runflare a disk is mounted at
# /app/public/media so they survive redeploys (ADR-0003). Served by Django
# itself, see config/urls.py.
MEDIA_URL = "/public/media/"
MEDIA_ROOT = BASE_DIR / "public" / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "config.storage.StaticFilesStorage"},
}


# ── Django admin theme (django-jazzmin), same setup as ArameshMusicAcademy-website ──
JAZZMIN_SETTINGS = {
    "site_title": "مدیریت سایت دکتر صفانوایی",
    "site_header": "سایت دکتر صفانوایی",
    "site_brand": "سایت دکتر صفانوایی",
    "welcome_sign": "به پنل مدیریت سایت دکتر سپیده صفانوایی خوش آمدید",
    "copyright": "دکتر سپیده صفانوایی",
    # «S» for Safanavaei, on the site's teal and gold (owner request, Stage 3 gate)
    "site_logo": "assets/img/admin-logo.svg",
    "search_model": ["conditions.ConditionTreated", "inquiries.Inquiry"],
    # Top menu: quick link to the live site
    "topmenu_links": [
        {"name": "مشاهده سایت", "url": "/", "new_window": True},
    ],
    # Order of app sections in the sidebar
    "order_with_respect_to": ["doctor", "conditions", "locations", "inquiries", "auth"],
    # FontAwesome icons per model
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "doctor": "fas fa-user-md",
        "doctor.DoctorProfile": "fas fa-user-md",
        "conditions": "fas fa-lungs",
        "conditions.ConditionTreated": "fas fa-lungs",
        "locations": "fas fa-clinic-medical",
        "locations.ClinicLocation": "fas fa-map-marker-alt",
        "inquiries": "fas fa-envelope",
        "inquiries.Inquiry": "fas fa-envelope-open-text",
    },
    "default_icon_parents": "fas fa-chevron-circle-left",
    "default_icon_children": "fas fa-circle",
    # RTL fixes, mainly the 10,000px horizontal scroll (static_dev/assets/css/admin.css)
    "custom_css": "assets/css/admin.css",
    # Keep the familiar stacked fieldsets instead of tabbed forms
    "changeform_format": "single",
    "show_ui_builder": False,
    "related_modal_active": True,
    # Load nothing from the internet, so the admin still opens when Iran's international
    # internet is cut. static_dev/vendor/bootswatch/flatly/ shadows jazzmin's flatly theme
    # with its Google Fonts @import removed; the admin falls back to system fonts.
    "use_google_fonts_cdn": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "default_theme_mode": "light",
    "sidebar_nav_flat_style": True,
    "navbar_fixed": True,
    "sidebar_fixed": True,
}
