from django.contrib import admin
from .models import CustomUser, EmailVerification

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "is_active", "email_verified", "is_staff")
    search_fields = ("email", "full_name")
    list_filter = ("is_active", "email_verified", "is_staff")

@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_used", "created_at")
    search_fields = ("user__email",)
