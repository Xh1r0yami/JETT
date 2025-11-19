from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "job", "user", "status", "applied_at")
    search_fields = ("job__title", "user__full_name")
    list_filter = ("status",)
