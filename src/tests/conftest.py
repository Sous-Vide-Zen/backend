import pytest
from django.core.management import call_command
from django.utils.text import slugify
from rest_framework.test import APIClient

from src.apps.ingredients.models import Ingredient, Unit
from src.apps.recipes.models import Recipe


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("migrate")


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_token(api_client, django_user_model):
    django_user_model.objects.create_user(
        username="test", password="changeme123", email="test@ya.ru"
    )
    response = api_client.post(
        "/auth/jwt/create/",
        data={"password": "changeme123", "email": "test@ya.ru"},
        format="json",
    )
    print(f'Bearer {response.data["access"]}')
    return f'Bearer {response.data["access"]}'


@pytest.fixture(scope="function")
def new_user(django_user_model):
    return django_user_model.objects.create_user(
        username="test", password="changeme123", email="test@ya.ru"
    )


@pytest.fixture(scope="function")
def new_recipe(new_user):
    recipe = Recipe.objects.create(
        author=new_user,
        title="Test Recipe",
        slug=slugify("Test Recipe"),
        full_text="This is a test recipe full text.",
        short_text="Test short text",
        cooking_time=30,
    )
    return recipe


@pytest.fixture(scope="function")
def new_ingredient():
    # Создаем единицу измерения для ингредиента
    unit = Unit.objects.create(name="Штука")
    # Создаем ингредиент и добавляем единицу измерения к нему
    ingredient = Ingredient.objects.create(name="Яйцо")
    ingredient.units.add(unit)
    return ingredient
