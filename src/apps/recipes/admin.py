from django.contrib import admin
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["author", "title", "pub_date"]
    prepopulated_fields = {"slug": ["title"]}
    exclude = ("short_text",)
