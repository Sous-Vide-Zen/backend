from datetime import datetime

import pytest
from src.apps.recipes.models import Recipe, Category
from django.db import IntegrityError
from django.core.exceptions import ValidationError


@pytest.mark.recipes
@pytest.mark.models
def test_recipe_fields(new_user):
    new_category1 = Category.objects.create(name="category 1")
    new_category2 = Category.objects.create(name="category 2")
    title = "Recipe 1"
    full_text = "recipe 1 full text"

    new_recipe = Recipe.objects.create(
        author=new_user,
        title=title,
        full_text=full_text,
        cooking_time=10,
    )
    new_recipe.category.add(new_category1, new_category2)
    assert str(new_recipe) == title
    assert new_recipe.short_text == full_text
    assert new_recipe.slug == "recipe-1"
    # test category
    assert new_category1.slug == "category-1"


@pytest.mark.recipes
@pytest.mark.models
def test_unique_slug(new_user):
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
    )

    r2 = Recipe.objects.create(
        author=new_user,
        title=title,
        full_text=full_text,
        cooking_time=10,
        slug="recipe-1",
    )
    with pytest.raises(IntegrityError):
        Recipe.objects.filter(id=r2.id).update(slug=r1.slug)


@pytest.mark.recipes
@pytest.mark.models
def test_cooking_time(new_user):
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


@pytest.mark.recipes
@pytest.mark.models
def test_same_titles(new_user):
    title = "Recipe 1"
    full_text = "recipe 1 full text"
    r1 = Recipe.objects.create(
        author=new_user,
        title=title,
        full_text=full_text,
        cooking_time=10,
    )

    r2 = Recipe.objects.create(
        author=new_user,
        title=title,
        full_text=full_text,
        cooking_time=10,
    )

    assert r1.title == r2.title
