from django.contrib import admin

from .models import Ingredient, Unit, IngredientInRecipe


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    pass
