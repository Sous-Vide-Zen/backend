import pytest
from src.apps.recipes.models import Recipe
from src.apps.favorite.models import Favorite


@pytest.mark.favorite
@pytest.mark.models
def test_favorite_fields(new_user):
    title = "Recipe 1"
    full_text = "recipe 1 full text"

    new_recipe = Recipe.objects.create(
        author=new_user,
        title=title,
        full_text=full_text,
        cooking_time=10,
    )

    new_favorite = Favorite(author=new_user, recipe=new_recipe)

    assert str(new_favorite) == f"{new_user.username}'s favorite recipe: {title}"
