import pytest

from src.apps.ingredients.models import Unit, Ingredient, IngredientInRecipe


@pytest.mark.django_db
class TestIngredientsModels:
    def test_create_unit(self):
        # Тестирование создания единицы измерения
        unit = Unit.objects.create(name="Килограмм")
        assert unit.name == "Килограмм"

    def test_create_ingredient_with_units(self, new_ingredient):
        # Тестирование создания ингредиента с единицами измерения
        assert new_ingredient.units.filter(name="Штука").exists()

    def test_add_ingredient_to_recipe(self, new_recipe, new_ingredient):
        # Тестирование добавления ингредиента в рецепт
        ingredient_in_recipe = IngredientInRecipe.objects.create(
            ingredient=new_ingredient,
            recipe=new_recipe,
            unit=new_ingredient.units.first(),
            amount=3,
        )
        assert ingredient_in_recipe.ingredient == new_ingredient
        assert ingredient_in_recipe.recipe == new_recipe
        assert ingredient_in_recipe.unit == new_ingredient.units.first()
        assert ingredient_in_recipe.amount == 3

    def test_search_ingredient_by_name(self):
        # Создание ингредиента
        Ingredient.objects.create(name="Перец")
        # Поиск созданного ингредиента по названию
        found_ingredient = Ingredient.objects.filter(name__icontains="Перец").first()
        assert found_ingredient is not None
        assert found_ingredient.name == "Перец"
