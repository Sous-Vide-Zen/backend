from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField

from .models import IngredientInRecipe


class IngredientInRecipeSerializer(ModelSerializer):
    """
    Ingredients in recipe serializer
    """

    name = CharField(source="ingredient.name", max_length=100)
    unit = CharField(source="unit.name")

    class Meta:
        model = IngredientInRecipe
        fields = (
            "name",
            "unit",
            "amount",
        )

    def validate_amount(self, value):
        if value == 0:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value
