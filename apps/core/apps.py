from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Site-wide public plumbing: the shell's context, template filters and
    HTML caching. Owns no models."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"
    verbose_name = "سایت"
