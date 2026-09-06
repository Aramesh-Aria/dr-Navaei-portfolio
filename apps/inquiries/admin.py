from django.contrib import admin

from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    readonly_fields = ("name", "phone", "preferred_contact_time", "message", "created_at")

    def has_add_permission(self, request):
        # Inquiries only ever come from the public contact form (Phase 4).
        return False
