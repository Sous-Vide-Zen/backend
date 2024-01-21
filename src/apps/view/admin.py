from django.contrib import admin

from src.apps.view.models import ViewRecipes


@admin.register(ViewRecipes)
class ViewAdmin(admin.ModelAdmin):
    list_display = ["user", "recipe", "created_at"]
    list_display_links = ["user", "recipe"]
    list_filter = ["created_at"]
    search_fields = ["user", "recipe"]
