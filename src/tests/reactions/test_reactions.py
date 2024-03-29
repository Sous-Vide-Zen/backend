import pytest
from django.contrib.contenttypes.models import ContentType

from src.apps.comments.models import Comment
from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe


@pytest.mark.reactions
@pytest.mark.models
class TestReactionsModel:
    def test_reaction_fields(self, new_user):
        title = "Recipe 1"
        full_text = "recipe 1 full text"

        new_recipe = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
        )
        content_type = ContentType.objects.get_for_model(Recipe)

        reaction = Reaction.objects.create(
            author=new_user,
            object_id=new_recipe.id,
            content_type=content_type,
            emoji=EmojyChoice.LIKE,
        )

        assert str(reaction) == "Like reaction by user1"
        assert reaction.emoji == EmojyChoice.LIKE.value

    def test_reaction_fields_comment(self, new_user):
        title = "Recipe 1"
        full_text = "recipe 1 full text"

        # creating recipe
        new_recipe = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
        )

        # creating comment to recipe
        new_comment = Comment.objects.create(
            author=new_user,
            recipe=new_recipe,
            text="comment 1 to recipe 1",
        )
        content_type = ContentType.objects.get_for_model(Comment)

        reaction = Reaction.objects.create(
            author=new_user,
            object_id=new_comment.id,
            content_type=content_type,
            emoji=EmojyChoice.DISLIKE,
        )

        assert str(reaction) == f"Dislike reaction by user1"
        assert reaction.emoji == EmojyChoice.DISLIKE.value
