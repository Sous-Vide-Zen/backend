from rest_framework.serializers import ModelSerializer, ChoiceField

from .choices import EmojyChoice
from .models import Reaction
from src.apps.recipes.models import Recipe
from src.apps.recipes.serializers import RecipeRetriveSerializer


class RecipeReactionRetriveSerializer(RecipeRetriveSerializer):
    """
    Retrieve reactions on recipe serializer
    """

    class Meta:
        model = Recipe
        fields = ("reactions",)


class RecipeReactionCreateSerializer(ModelSerializer):
    """
    Create reactions on recipe serializer
    """

    emoji = ChoiceField(choices=EmojyChoice.choices, default=EmojyChoice.LIKE)

    class Meta:
        model = Reaction
        fields = ("emoji",)
