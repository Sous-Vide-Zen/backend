from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_banned")
    list_filter = ("is_admin", "is_staff", "is_banned")
    search_fields = ("username", "email")
