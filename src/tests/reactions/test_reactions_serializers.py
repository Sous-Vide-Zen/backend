import pytest
from django.contrib.contenttypes.models import ContentType

from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction
from src.apps.reactions.serializers import (
    CommentReactionsListSerializer,
    ReactionCreateSerializer,
    RecipeReactionsListSerializer,
)


@pytest.mark.reactions
@pytest.mark.models
class TestRecipeReactionsSerializer:
    def test_recipe_reaction_create_serializer(self, new_user, new_recipe):
        """
        Recipe reaction create serializer test
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/
        """
        example_data = {"emoji": "Like"}
        reaction = Reaction.objects.create(
            author=new_user,
            object_id=new_recipe.id,
            emoji=EmojyChoice.LIKE,
            content_type=ContentType.objects.get_for_model(new_recipe),
        )
        serializer = ReactionCreateSerializer(reaction)
        assert serializer.data == example_data

    def test_recipe_reactions_list_serializer(self, new_user, new_recipe):
        """
        Recipe reaction retrieve serializer test
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/
        """
        for emoji in EmojyChoice:
            Reaction.objects.create(
                emoji=emoji.value,
                object_id=new_recipe.id,
                author=new_user,
                content_type=ContentType.objects.get_for_model(new_recipe),
            )
        reactions_data = dict({"reactions": dict.fromkeys(EmojyChoice.values, 1)})
        serializer = RecipeReactionsListSerializer(new_recipe)
        serializer_data = serializer.data.copy()

        assert serializer_data == reactions_data


@pytest.mark.reactions
@pytest.mark.models
class TestCommentReactionsSerializer:
    def test_comment_reaction_create_serializer(self, new_user, new_comment):
        """
        Comment reaction create serializer test
        [POST] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/
        """
        example_data = {"emoji": "Like"}
        reaction = Reaction.objects.create(
            author=new_user,
            object_id=new_comment.id,
            emoji=EmojyChoice.LIKE,
            content_type=ContentType.objects.get_for_model(new_comment),
        )
        serializer = ReactionCreateSerializer(reaction)
        assert serializer.data == example_data

    def test_comment_reactions_list_serializer(self, new_user, new_comment):
        """
        Comment reaction retrieve serializer test
        [GET] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/
        """
        for emoji in EmojyChoice:
            Reaction.objects.create(
                emoji=emoji.value,
                object_id=new_comment.id,
                author=new_user,
                content_type=ContentType.objects.get_for_model(new_comment),
            )
        reactions_data = dict({"reactions": dict.fromkeys(EmojyChoice.values, 1)})
        serializer = CommentReactionsListSerializer(new_comment)
        serializer_data = serializer.data.copy()

        assert serializer_data == reactions_data
