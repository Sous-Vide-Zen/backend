from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField

from .models import IngredientInRecipe
from ...base.code_text import AMOUNT_OF_INGREDIENT_LESS_THAN_ZERO


class IngredientInRecipeSerializer(ModelSerializer):
    """
    Ingredients in recipe serializer
    """

    name = CharField(source="ingredient.name", max_length=100)
    unit = CharField(source="unit.name", max_length=30)

    class Meta:
        model = IngredientInRecipe
        fields = (
            "name",
            "unit",
            "amount",
        )

    def validate_amount(self, value):
        """
        Validate amount
        """

        if value <= 0:
            raise serializers.ValidationError(
                AMOUNT_OF_INGREDIENT_LESS_THAN_ZERO, code="amount_less_than_zero"
            )
        return value
