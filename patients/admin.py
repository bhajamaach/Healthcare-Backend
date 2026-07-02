from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'user', 'created_at']
    search_fields = ['name', 'email', 'user__email']
    list_filter = ['created_at', 'user']
    readonly_fields = ['created_at', 'updated_at']
