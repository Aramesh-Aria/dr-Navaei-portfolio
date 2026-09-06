from django.contrib import admin
from django.shortcuts import redirect

from .models import Credential, DoctorProfile


class CredentialInline(admin.TabularInline):
    model = Credential
    extra = 1
    fields = ("title", "institution", "year", "order")


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    inlines = [CredentialInline]

    def has_add_permission(self, request):
        # Singleton: only one DoctorProfile should ever exist.
        return not DoctorProfile.objects.exists()

    def changelist_view(self, request, extra_context=None):
        profile = DoctorProfile.objects.first()
        if profile is not None:
            return redirect("admin:doctor_doctorprofile_change", profile.pk)
        return super().changelist_view(request, extra_context)
