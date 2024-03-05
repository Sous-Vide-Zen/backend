import pytest
from django.db import IntegrityError

from src.apps.recipes.models import Recipe, Category


@pytest.mark.recipes
@pytest.mark.models
class TestRecipeModel:
    """
    Test Recipe model
    """

    def test_recipe_fields(self, new_user):
        """
        Test Recipe model fields
        """

        new_category1 = Category.objects.create(name="category 1", slug="category-1")
        new_category2 = Category.objects.create(name="category 2", slug="category-2")
        title = "Recipe 1"
        full_text = "recipe 1 full text"
        slug = "recipe-for-test"

        new_recipe = Recipe.objects.create(
            author=new_user,
            title=title,
            slug=slug,
            full_text=full_text,
            cooking_time=10,
        )
        new_recipe.category.add(new_category1, new_category2)
        assert str(new_recipe) == slug
        assert new_recipe.slug == "recipe-for-test"
        assert new_category1.slug == "category-1"

    def test_unique_slug(self, new_user):
        """
        Test that two recipes with same slug can't be created
        """

        title = "Recipe 1"
        full_text = "recipe 1 full text"
        r1 = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
            slug="recipe-1",
        )

        r2 = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
            slug="recipe-2",
        )
        with pytest.raises(IntegrityError):
            Recipe.objects.filter(id=r2.id).update(slug=r1.slug)

    def test_cooking_time(self, new_user):
        """
        Test that cooking_time can't be negative
        """

        title = "Recipe 1"
        full_text = "recipe 1 full text"
        cooking_time = -1

        with pytest.raises(IntegrityError):
            Recipe.objects.create(
                author=new_user,
                title=title,
                full_text=full_text,
                cooking_time=cooking_time,
            )
