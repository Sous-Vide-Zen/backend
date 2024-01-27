import pytest
from django.db.utils import IntegrityError

from src.apps.favorite.models import Favorite
from src.apps.recipes.models import Recipe


@pytest.mark.favorite
@pytest.mark.models
class TestViewModel:
    def test_favorite_fields(self, new_user):
        title = "Recipe 1"
        full_text = "recipe 1 full text"

        new_recipe = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
        )

        new_favorite = Favorite.objects.create(author=new_user, recipe=new_recipe)

        assert str(new_favorite) == f"{new_user.username}'s favorite recipe: {title}"
        # check number of objects created
        assert Favorite.objects.count() == 1

    def test_favorite_creation(self, new_user):
        """
        Check that object can't be created without all required fields
        """

        with pytest.raises(IntegrityError):
            new_favorite = Favorite.objects.create(author=new_user)
