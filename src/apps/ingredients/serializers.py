from rest_framework.serializers import ModelSerializer, CharField

from .models import IngredientInRecipe


class IngredientInRecipeSerializer(ModelSerializer):
    """
    Ingredients in recipe serializer
    """

    name = CharField(source="ingredient.name")
    unit = CharField(source="unit.name")

    class Meta:
        model = IngredientInRecipe
        fields = (
            "name",
            "unit",
            "amount",
        )
