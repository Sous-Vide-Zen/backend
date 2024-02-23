import pytest
from django.core.management import call_command
from django.utils.text import slugify
from rest_framework.test import APIClient

from src.apps.ingredients.models import Ingredient, Unit
from src.apps.recipes.models import Recipe


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Django DB setup.
    """

    with django_db_blocker.unblock():
        call_command("migrate")


@pytest.fixture
def api_client():
    """
    APIClient fixture
    """

    return APIClient()


@pytest.fixture
def create_token(api_client, django_user_model):
    """
    Create token
    """

    django_user_model.objects.create_user(
        username="test", password="changeme123", email="test@ya.ru"
    )
    response = api_client.post(
        "/api/v1/auth/jwt/create/",
        data={"password": "changeme123", "email": "test@ya.ru"},
        format="json",
    )
    print(f'Bearer {response.data["access"]}')
    return f'Bearer {response.data["access"]}'


@pytest.fixture
def new_author(django_user_model):
    """
    Create new author
    """

    return django_user_model.objects.create_user(
        username="test2", password="changeme123", email="test2@ya.ru"
    )


@pytest.fixture(scope="function")
def new_user(django_user_model):
    """
    Create new user
    """

    return django_user_model.objects.create_user(
        username="test", password="changeme123", email="test@ya.ru"
    )


@pytest.fixture(scope="function")
def new_recipe(new_author, new_ingredient, new_unit):
    """
    Create new recipe
    """

    recipe = Recipe.objects.create(
        author=new_author,
        title="Test Recipe",
        slug=slugify("Test Recipe"),
        full_text="This is a test recipe full text.",
        short_text="Test short text",
        cooking_time=30,
    )
    return recipe


@pytest.fixture(scope="function")
def new_ingredient():
    """
    Create new ingredient
    """

    ingredient = Ingredient.objects.create(name="Яйцо")
    return ingredient


@pytest.fixture(scope="function")
def new_unit():
    """
    Create new unit
    """

    unit = Unit.objects.create(name="Штука")
    return unit
