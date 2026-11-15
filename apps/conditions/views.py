from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.core.templatetags.site import body_sections

from .models import ConditionTreated


class ConditionListView(TemplateView):
    """`/conditions/`: Conditions Treated and Procedures Performed as two
    labelled groups, published rows only."""

    template_name = "conditions/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["conditions"] = ConditionTreated.objects.conditions()
        context["procedures"] = ConditionTreated.objects.procedures()
        return context


class ConditionDetailView(TemplateView):
    """`/conditions/<slug>/`: one Condition Treated or Procedure Performed,
    in Mayo Clinic's order. An unpublished slug is a 404.

    `toc` (the "on this page" index) lists the body's `## ` sections, and is
    empty unless there are at least two of them."""

    template_name = "conditions/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = get_object_or_404(ConditionTreated.objects.published(), slug=kwargs["slug"])
        sections = body_sections(item.body)
        headed = [s for s in sections if s["heading"]]
        context.update({
            "item": item,
            "is_procedure": item.category == ConditionTreated.CATEGORY_PROCEDURE,
            "sections": sections,
            "toc": headed if len(headed) >= 2 else [],
        })
        return context
