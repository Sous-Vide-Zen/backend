from django.contrib import admin

from .models import Recipe, Category


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["id", "author", "title", "pub_date"]
    list_filter = ["pub_date", "author"]
    search_fields = ["title"]
    list_display_links = ["title"]
    prepopulated_fields = {"slug": ["title"]}
    exclude = ("short_text",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    prepopulated_fields = {"slug": ["name"]}
