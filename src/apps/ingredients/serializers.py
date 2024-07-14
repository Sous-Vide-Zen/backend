from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField

from src.base.code_text import (
    AMOUNT_OF_INGREDIENT_LESS_THAN_ONE,
    MAX_COUNT_OF_INGREDIENT,
)
from .models import IngredientInRecipe


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
        Validating amount for min(1) and max(1000) count.
        """

        if value <= 0:
            raise serializers.ValidationError(
                AMOUNT_OF_INGREDIENT_LESS_THAN_ONE, code="amount_less_than_one"
            )
        if value > 1000:
            raise serializers.ValidationError(
                MAX_COUNT_OF_INGREDIENT, code="no_more_than_1000"
            )
        return value
