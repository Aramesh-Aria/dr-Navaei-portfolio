from django.views.generic import TemplateView

from .models import DoctorProfile


def credential_context(profile):
    """Credentials split the way every page shows them: those with an
    institution turn as flip cards, the rest are static rows. `current` is
    the latest card (her present post), for the founder card's caption."""
    if not profile:
        return {"cards": [], "rows": [], "current": None}
    credentials = list(profile.credentials.all())
    cards = [c for c in credentials if c.institution]
    rows = [c for c in credentials if not c.institution]
    current = max(cards, key=lambda c: (c.year or 0, c.order), default=None)
    return {"cards": cards, "rows": rows, "current": current}


class AboutView(TemplateView):
    """`/about/`: the portrait, the full bio and every credential."""

    template_name = "doctor/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(credential_context(DoctorProfile.objects.first()))
        return context
