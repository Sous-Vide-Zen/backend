import pytest
from django.core.management import call_command
from django.utils import timezone
from django.utils.text import slugify
from rest_framework.test import APIClient

from src.apps.ingredients.models import Ingredient, Unit, IngredientInRecipe
from src.apps.recipes.models import Recipe, Category


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
    return f'Bearer {response.data["access"]}'


@pytest.fixture(scope="function")
def app_admin(django_user_model):
    """
    Create new user
    """

    return django_user_model.objects.create_user(
        username="admin", password="changeme123", email="admin@ya.ru", is_staff=True
    )


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
        pub_date=timezone.now(),
        updated_at=timezone.now(),
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


@pytest.fixture(scope="function")
def new_ingredient_in_recipe(new_recipe, new_ingredient, new_unit):
    """
    Create new ingredient in recipe
    """

    ingredient_in_recipe = IngredientInRecipe.objects.create(
        recipe=new_recipe, ingredient=new_ingredient, unit=new_unit, amount=1
    )
    return ingredient_in_recipe


@pytest.fixture(scope="function")
def category_1():
    """
    Create new category
    """

    category = Category.objects.create(name="Рыба", slug="fish")
    return category


@pytest.fixture(scope="function")
def category_2():
    """
    Create new category
    """

    category = Category.objects.create(name="Мясо", slug="meat")
    return category


@pytest.fixture(scope="function")
def category_3():
    """
    Create new category
    """

    category = Category.objects.create(name="Овощи", slug="vegetables")
    return category


@pytest.fixture(scope="function")
def recipe_data(category_1, category_2, category_3):
    """
    Create recipe data
    """

    return {
        "title": "Вареные яйца",
        "ingredients": [
            {"name": "Яйца", "unit": "Шт", "amount": 3},
            {"name": "Волда", "unit": "литр", "amount": 1},
        ],
        "full_text": """Вареные яйца - это простое и полезное блюдо, которое можно приготовить за несколько минут. 
                        Вот рецепт вареных яиц: \nНалейте в кастрюлю холодную воду и поставьте на сильный огонь. 
                        \nОпустите в воду яйца и доведите до кипения.\nКак только вода закипит, уменьшите огонь и 
                        варите яйца в зависимости от желаемой степени прожарки:\n3-4 минуты для яиц в мешочек 
                        (мягких)\n5-6 минут для яиц всмятку (средних)\n7-8 минут для яиц вкрутую (твердых)\nСлейте 
                        горячую воду и охладите яйца под холодной водой или в ледяной воде.\nОчистите яйца от 
                        скорлупы и подавайте по вкусу: с солью, перцем, майонезом, сметаной, зеленью, хлебом и т.д.
                        \nНадеюсь, вам понравится этот рецепт.""",
        "tag": ["Яйца", "Вода", "Варка"],
        "category": [category_1.id, category_2.id, category_3.id],
        "cooking_time": 10,
    }
