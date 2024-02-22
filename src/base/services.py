from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from typing import List, Type, Any, Set

from config.settings import SHORT_RECIPE_SYMBOLS
from src.apps.ingredients.models import Ingredient, Unit, IngredientInRecipe


def validate_avatar_size(value: Any) -> None:
    """Validate avatar size"""
    if value.size > 5 * 1024 * 1024:  # 5 МБ в байтах
        raise ValidationError(
            _("Размер файла слишком большой. Максимальный размер - 5 МБ.")
        )


def user_avatar_path(instance: Model, filename: str) -> str:
    """Generate filepath for user avatar"""
    return f"avatar/user_{instance.id}/{filename}"


def recipe_preview_path(instance: Model, filename: str) -> str:
    """Generate filepath for recipe preview"""
    return f"preview/recipe_{instance.slug}/{filename}"


def shorten_text(full_text: str, n: int) -> str:
    """
    Shorten text to n characters with rounding by last word
    """
    short_text = full_text[:SHORT_RECIPE_SYMBOLS]
    if len(full_text) > n and full_text[n] != "":
        short_text = short_text[: short_text.rfind(" ")]
    return short_text


def bulk_get_or_create(
    model: Type[Model], objs: List[Model], match_field: str
) -> List[Model]:
    """
    Bulk get or create objects
    """
    match_values: List[Any] = [getattr(obj, match_field) for obj in objs]
    existing_objs: List[Model] = model.objects.filter(**{f"{match_field}__in": match_values})

    existing_map: dict = {getattr(obj, match_field): obj for obj in existing_objs}

    objs_to_create: List[Model] = [
        obj for obj in objs if getattr(obj, match_field) not in existing_map
    ]

    created_objs: List[Model] = model.objects.bulk_create(objs_to_create)
    existing_map.update({getattr(obj, match_field): obj for obj in created_objs})
    return [existing_map[value] for value in match_values]


def create_ingredients_in_recipe(recipe: Model, ingredients_data: List[dict]) -> List[Model]:
    """
    Create ingredients in recipe
    """
    ingredient_names: List[str] = [data["name"] for data in ingredients_data]
    if len(ingredient_names) != len(set(ingredient_names)):
        raise ValidationError({"errors": "Нельзя добавить два одинаковых ингредиента"})

    existing_ingredients: List[str] = IngredientInRecipe.objects.filter(
        recipe=recipe, ingredient__name__in=ingredient_names
    ).values_list("ingredient__name", flat=True)
    if existing_ingredients:
        raise ValidationError(
            {"errors": "В рецепте уже есть один или несколько добавляемых ингредиентов"}
        )

    ingredient_objs: List[Ingredient] = [Ingredient(name=data["name"]) for data in ingredients_data]
    unit_names: Set[str] = {data["unit"] for data in ingredients_data}
    unit_objs: List[Unit] = [Unit(name=name) for name in unit_names]

    with transaction.atomic():
        ingredients: dict = {
            ingredient.name: ingredient
            for ingredient in bulk_get_or_create(Ingredient, ingredient_objs, "name")
        }
        units: dict = {
            unit.name: unit for unit in bulk_get_or_create(Unit, unit_objs, "name")
        }

    ingredients_in_recipe_objs: List[IngredientInRecipe] = [
        IngredientInRecipe(
            recipe=recipe,
            ingredient=ingredients[ingredient_data["name"]],
            unit=units[ingredient_data["unit"]],
            amount=ingredient_data["amount"],
        )
        for ingredient_data in ingredients_data
    ]
    IngredientInRecipe.objects.bulk_create(ingredients_in_recipe_objs)
    return ingredients_in_recipe_objs
