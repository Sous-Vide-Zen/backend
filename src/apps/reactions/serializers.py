from rest_framework.serializers import ModelSerializer, ChoiceField, RelatedField

from .choices import EmojyChoice
from .models import Reaction
from src.apps.comments.models import Comment
from src.apps.recipes.models import Recipe
from src.base.services import count_reactions_on_objects, show_user_reactions


class RecipeReactionsListSerializer(ModelSerializer):
    """
    Retrieve reactions on recipe serializer
    """

    class Meta:
        model = Recipe
        fields = ("reactions",)

    def to_representation(self, instance):
        """
        representation
        """
        user = self.context.get("request").user
        return {
            "reactions": count_reactions_on_objects(instance),
            "user_reactions": show_user_reactions(user, instance),
        }


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
        user = self.context.get("request").user
        return {
            "reactions": count_reactions_on_objects(instance),
            "user_reactions": show_user_reactions(user, instance),
        }
