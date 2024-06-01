from datetime import timedelta

import pytest
from django.utils import timezone

from src.base.code_text import (
    RECIPE_CAN_BE_EDIT_WITHIN_FIRST_DAY,
)
from src.apps.recipes.serializers import RecipeRetriveSerializer
from tests.factories.recipes.recipe_serializers_factory import (
    get_recipe_data,
    get_create_data,
    get_update_data,
)


@pytest.mark.django_db
@pytest.mark.api
class TestRecipeSerializers:
    """
    TestRecipeSerializers:
    RecipeRetrieveSerializer
    RecipeCreateSerializer
    RecipeUpdateSerializer
    """

    def test_retrieve_recipe_serializer(self, request, new_recipe, new_user):
        """
        Test for retrive recipe
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        recipe_data = get_recipe_data()
        request.user = new_user
        serializer = RecipeRetriveSerializer(new_recipe, context={"request": request})
        serializer_data = serializer.data.copy()
        serializer_data.pop("pub_date", None)
        serializer_data.pop("updated_at", None)
        assert serializer_data == recipe_data

    def test_create_recipe_serializer(self, api_client, new_author, recipe_data):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """
        example_data, example_response = get_create_data()

        api_client.force_authenticate(user=new_author)
        recipe = api_client.post("/api/v1/recipe/", example_data, format="json")
        recipe.data.pop("pub_date")
        recipe.data.pop("updated_at")

        assert recipe.data["tag"]

        recipe.data.pop("tag")
        example_response.pop("tag")

        assert recipe.data == example_response

    def test_update_recipe_serializer(self, api_client, new_author, new_recipe):
        """
        Test for update recipe
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)
        patch_url = f"/api/v1/recipe/{new_recipe.slug}/"

        example_data = get_update_data()

        assert new_recipe.slug == "test-recipe"
        print(example_data.get("title"))

        response = api_client.patch(
            f"{patch_url}", data=dict(title=example_data.get("title")), format="json"
        )

        assert response.data["title"] == example_data.get("title")
        assert response.data["slug"] == example_data.get("slug")

        new_url = f"/api/v1/recipe/{response.data['slug']}/"

        response = api_client.patch(
            f"{new_url}",
            data=dict(cooking_time=example_data.get("cooking_time")),
            format="json",
        )
        assert response.data["cooking_time"] == example_data.get("cooking_time")
        assert response.data["slug"] == example_data.get("slug")

        response = api_client.patch(
            f"{new_url}",
            data=dict(full_text=example_data.get("full_text")),
            format="json",
        )
        assert response.data["full_text"] == example_data.get("full_text")
        assert response.data["slug"] == example_data.get("slug")

        response = api_client.patch(
            f"{new_url}",
            data=dict(ingredients=example_data.get("ingredients")),
            format="json",
        )
        assert response.data["ingredients"] == example_data.get("ingredients")
        assert response.data["slug"] == example_data.get("slug")

        response = api_client.patch(
            f"{new_url}", data=dict(tag=example_data.get("tag")), format="json"
        )
        expected_tags = {
            ("Горячий", "goriachii"),
            ("вода", "voda"),
            ("сахар", "sakhar"),
        }
        response_tags_set = {(tag["name"], tag["slug"]) for tag in response.data["tag"]}
        assert (
            response_tags_set == expected_tags
        ), "Теги в ответе не соответствуют ожидаемым."

    def test_recipe_update_once_per_day(self, api_client, new_author, new_recipe):
        """
        Test for update recipe once per day
        """

        update_data = {
            "full_text": "Updated recipe full text",
        }

        api_client.force_authenticate(user=new_author)
        url = f"/api/v1/recipe/{new_recipe.slug}/"

        response = api_client.patch(url, data=update_data, format="json")

        assert response.status_code == 200

        new_recipe.pub_date = timezone.now() - timedelta(days=1)
        new_recipe.save()

        response = api_client.patch(url, data=update_data, format="json")
        assert response.status_code == 403
        assert response.data == RECIPE_CAN_BE_EDIT_WITHIN_FIRST_DAY
