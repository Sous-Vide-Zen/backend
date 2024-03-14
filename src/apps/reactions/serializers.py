from rest_framework.serializers import ModelSerializer, ChoiceField

from .choices import EmojyChoice
from .models import Reaction
from src.apps.comments.models import Comment
from src.apps.recipes.models import Recipe
from src.apps.recipes.serializers import RecipeRetriveSerializer
from src.base.services import count_reactions_on_objects


class RecipeReactionsListSerializer(RecipeRetriveSerializer):
    """
    Retrieve reactions on recipe serializer
    """

    class Meta:
        model = Recipe
        fields = ("reactions",)


class ReactionCreateSerializer(ModelSerializer):
    """
    Create reactions on recipe serializer
    """

    emoji = ChoiceField(choices=EmojyChoice.choices, default=EmojyChoice.LIKE)

    class Meta:
        model = Reaction
        fields = ("emoji",)


class CommentReactionsListSerializer(ModelSerializer):
    """
    Retrieve reactions on comment serializer
    """

    class Meta:
        model = Comment
        fields = ("reactions",)

    def to_representation(self, instance):
        super().to_representation(instance)
        return {"reactions": count_reactions_on_objects(instance)}
