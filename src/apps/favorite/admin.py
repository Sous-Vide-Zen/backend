from django.contrib import admin

from src.apps.favorite.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Class for displaying admin panel for favorites.

     Attrs:
    • list_display (list[str]): list of fields to be displayed.
    • list_filter (list[str]): list of fields by which you can sort.
    • search_fields (list[str]): list of fields by which you can do search.
    • list_display_links (list[str]): List of reference fields that can be used to
    navigate to this object.
    • readonly_fields (list[str]): list of fields that you cant edit.
    """

    list_display = ["id", "recipe", "author", "pub_date"]
    list_filter = ["pub_date", "author"]
    search_fields = ["recipe"]
    list_display_links = ["id", "recipe"]
    readonly_fields = ["pub_date"]
