from django.views.generic import TemplateView

from apps.conditions.models import ConditionTreated
from apps.doctor.models import DoctorProfile
from apps.doctor.views import credential_context

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
