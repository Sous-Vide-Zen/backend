import pytest
from django.db import IntegrityError

from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from django.contrib.contenttypes.models import ContentType
from src.apps.ingredients.models import Unit


@pytest.mark.reactions
@pytest.mark.models
def test_reaction_fields(new_user):
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

    assert str(reaction) == "Like by test"


# @pytest.mark.reactions
# @pytest.mark.models
# def test_reaction_wrong_object(new_user):
#     unit = Unit.objects.create(name="kg")
#     content_type = ContentType.objects.get_for_model(Unit)
#     with pytest.raises(IntegrityError):
#         reaction = Reaction.objects.create(
#             author=new_user,
#             object_id=unit.id,
#             content_type=content_type,
#             emoji=EmojyChoice.FIRE,
#         )
