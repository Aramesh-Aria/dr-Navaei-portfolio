from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static as static_url
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from apps.core.views import ShellPreviewView

urlpatterns = [
    path("", ShellPreviewView.as_view(), name="home"),  # TEMPORARY until Stage 4
    path("admin/", admin.site.urls),
    path(
        "favicon.ico",
        RedirectView.as_view(url=static_url("assets/img/favicon.ico"), permanent=True),
    ),
    # Uploads, served by Django whatever DEBUG is: the static() helper returns
    # nothing when DEBUG is off, and there's no separate web server on Runflare.
    re_path(r"^public/media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
