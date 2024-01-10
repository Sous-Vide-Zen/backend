from django.contrib import admin

from .models import Reaction


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ["author", "is_deleted", "emoji", "pub_date", "reaction_object"]
