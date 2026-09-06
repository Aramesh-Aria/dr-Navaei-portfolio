from django.contrib import admin

from .models import ClinicLocation


@admin.register(ClinicLocation)
class ClinicLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "order")
    list_editable = ("order",)
