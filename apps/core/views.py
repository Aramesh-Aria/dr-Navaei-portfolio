import logging

from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView

from apps.conditions.models import ConditionTreated
from apps.doctor.models import DoctorProfile
from apps.doctor.views import credential_context
from apps.locations.models import ClinicLocation

logger = logging.getLogger(__name__)

HOME_CONDITIONS = 6


class HomeView(TemplateView):
    """`/`: the founder card, a credentials preview, the top conditions,
    the procedures and the call band."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = ConditionTreated.objects.filter(is_published=True)
        context["conditions"] = published.filter(
            category=ConditionTreated.CATEGORY_CONDITION
        )[:HOME_CONDITIONS]
        context["procedures"] = published.filter(category=ConditionTreated.CATEGORY_PROCEDURE)
        context.update(credential_context(DoctorProfile.objects.first()))
        return context


def bad_request(request, exception=None):
    """The 400 page: a request the site could not read (a broken query, a
    malformed upload). It never asks for the host, which may be what was bad."""
    return render(request, "400.html", status=400)


def permission_denied(request, exception=None):
    """The 403 page, for a page that isn't open to visitors."""
    return render(request, "403.html", status=403)


def page_not_found(request, exception=None):
    """The 404 page: the way back, the published conditions, the clinic phone."""
    conditions = ConditionTreated.objects.filter(
        is_published=True, category=ConditionTreated.CATEGORY_CONDITION
    )[:HOME_CONDITIONS]
    return render(request, "404.html", {"conditions": conditions}, status=404)


def server_error(request):
    """The 500 page. It stands alone (no base.html, no context processors),
    and reads the clinic phone only if the database answers, since the
    database may be what failed."""
    context = {}
    try:
        context["profile"] = DoctorProfile.objects.first()
        context["primary_location"] = ClinicLocation.objects.all().first()
    except Exception:
        context = {}
    try:
        html = loader.get_template("500.html").render(context)
    except Exception:
        logger.exception("The 500 page could not be rendered")
        html = "<h1>Server Error (500)</h1>"
    return HttpResponseServerError(html)


def csrf_failure(request, reason=""):
    """A form sent with an expired or missing CSRF cookie: in practice, the
    contact form left open too long."""
    return render(request, "403_csrf.html", status=403)
