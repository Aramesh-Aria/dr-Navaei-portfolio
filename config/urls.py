from django.conf import settings
from django.contrib import admin
from django.templatetags.static import static as static_url
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

from apps.conditions.views import ConditionDetailView, ConditionListView
from apps.core.views import HomeView
from apps.doctor.views import AboutView
from apps.inquiries.views import ContactView
from apps.locations.views import LocationsView

handler400 = "apps.core.views.bad_request"
handler403 = "apps.core.views.permission_denied"
handler404 = "apps.core.views.page_not_found"
handler500 = "apps.core.views.server_error"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("conditions/", ConditionListView.as_view(), name="conditions"),
    path("conditions/<slug:slug>/", ConditionDetailView.as_view(), name="condition"),
    path("locations/", LocationsView.as_view(), name="locations"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("captcha/", include("captcha.urls")),
    path("admin/", admin.site.urls),
    path(
        "favicon.ico",
        RedirectView.as_view(url=static_url("assets/img/favicon.ico"), permanent=True),
    ),
    # Uploads, served by Django whatever DEBUG is: the static() helper returns
    # nothing when DEBUG is off, and there's no separate web server on Runflare.
    re_path(r"^public/media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
