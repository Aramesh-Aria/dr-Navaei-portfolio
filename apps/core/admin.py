from django.contrib import admin

from apps.core.templatetags.site import fa_digits


class SiteAdminSite(admin.AdminSite):
    """The default admin site, with the unread Inquiry count in the sidebar."""

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        from apps.inquiries.models import Inquiry

        unread = Inquiry.objects.filter(is_read=False).count()
        if unread:
            for app in app_list:
                for model in app.get("models", []):
                    if model.get("object_name") == "Inquiry":
                        model["name"] = f"{model['name']} ({fa_digits(unread)})"
        return app_list
