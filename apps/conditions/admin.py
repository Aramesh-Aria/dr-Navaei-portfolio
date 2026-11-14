from django.contrib import admin

from .models import ConditionTreated


@admin.register(ConditionTreated)
class ConditionTreatedAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "slug", "is_published", "order")
    list_editable = ("is_published", "order")
    list_filter = ("category",)
    search_fields = ("title", "short_description")
    # Not prepopulated from `title`: title is Farsi, slug must stay Latin
    # (see docs/plan.md URL structure) — Django's slugify() would mangle it.
