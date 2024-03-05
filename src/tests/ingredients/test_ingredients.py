import pytest

from src.apps.ingredients.models import Unit, Ingredient


@pytest.mark.django_db
class TestIngredientsModels:
    """
    Test ingredients models
    """

    def test_create_unit(self):
        """
        Test for creating unit
        """

        unit = Unit.objects.create(name="Килограмм")
        assert unit.name == "Килограмм"

    def test_search_ingredient_by_name(self):
        """
        Test for searching ingredient by name
        """

        Ingredient.objects.create(name="Перец")
        found_ingredient = Ingredient.objects.filter(name__icontains="Перец").first()
        assert found_ingredient is not None
        assert found_ingredient.name == "Перец"
