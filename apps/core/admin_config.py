from django.contrib.admin.apps import AdminConfig


class SiteAdminConfig(AdminConfig):
    """Replaces `django.contrib.admin` in INSTALLED_APPS (adds the unread Inquiry count)."""

    default_site = "apps.core.admin.SiteAdminSite"
