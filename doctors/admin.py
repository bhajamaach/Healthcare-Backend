from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'specialization', 'created_at']
    search_fields = ['name', 'email', 'specialization', 'license_number']
    list_filter = ['specialization', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
