from datetime import datetime

import pytest
from src.apps.recipes.models import Recipe, Category
from django.db import IntegrityError


@pytest.mark.recipes
@pytest.mark.models
def test_recipe_fields(db, django_db_setup, django_user_model):
    new_user = django_user_model.objects.create_user(
        username="test", password="changeme123", email="test@ya.ru"
    )
    new_category1 = Category.objects.create(name="cat1")
    new_category2 = Category.objects.create(name="cat2")
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


@pytest.mark.recipes
@pytest.mark.models
def test_unique_slug(db, django_db_setup, django_user_model):
    new_user = django_user_model.objects.create_user(
        username="test", password="changeme123", email="test@ya.ru"
    )
    title = "Recipe 1"
    full_text = "recipe 1 full text"
    Recipe.objects.create(
        author=new_user,
        title=title,
        full_text=full_text,
        cooking_time=10,
    )
    with pytest.raises(IntegrityError):
        Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
        )
