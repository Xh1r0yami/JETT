from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "company", "salary", "created_at")
    search_fields = ("title", "company__name")
    list_filter = ("company",)
