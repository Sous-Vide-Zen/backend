from collections import OrderedDict

import pytest

from src.apps.recipes.models import Recipe
from src.base.code_text import (
    PAGE_NOT_FOUND,
    CANT_ADD_TWO_SIMILAR_INGREDIENT,
    CREDENTIALS_WERE_NOT_PROVIDED,
    DONT_HAVE_PERMISSIONS,
    RECIPE_SUCCESSFUL_DELETE,
)


@pytest.mark.django_db
@pytest.mark.api
class TestRecipeUrls:
    """
    Test recipe urls
    """

    def test_retrieve_recipes(self, client, new_recipe):
        """
        Test for retrieve recipes
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        slug_new_recipe = new_recipe.slug
        recipe_data = {
            "id": 1,
            "title": "Test Recipe",
            "slug": "test-recipe",
            "author": OrderedDict(
                [
                    ("id", 1),
                    ("username", "user1"),
                    ("display_name", None),
                    ("avatar", None),
                ]
            ),
            "preview_image": None,
            "ingredients": [],
            "full_text": "This is a test recipe full text.",
            "tag": [],
            "category": [],
            "cooking_time": 30,
            "reactions_count": 0,
            "views_count": 0,
        }
        response = client.get(f"/api/v1/recipe/{slug_new_recipe}/")
        assert response.status_code == 200

        response_data = response.data.copy()
        response_data.pop("pub_date", None)
        response_data.pop("updated_at", None)
        assert response_data == recipe_data

    def test_retrieve_recipes_not_found(self, client):
        """
        Test for retrieve recipes not found
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        assert client.get("/api/v1/recipe/not-found/").status_code == 404
        assert client.get("/api/v1/recipe/not-found/").data == PAGE_NOT_FOUND

    def test_create_recipe(self, api_client, new_author, recipe_data):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)

        assert (
            api_client.post("/api/v1/recipe/", recipe_data, format="json").status_code
            == 201
        )

    def test_create_recipe_with_name_ingredient_more_than_100_characters(
        self, api_client, new_author, recipe_data
    ):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["ingredients"] = ["a" * 101]
        assert (
            api_client.post("/api/v1/recipe/", recipe_data, format="json").status_code
            == 400
        )

    def test_create_recipe_with_2_equal_ingredients(
        self, api_client, new_author, recipe_data
    ):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["ingredients"].append(recipe_data["ingredients"][0])
        response = api_client.post("/api/v1/recipe/", recipe_data, format="json")
        assert response.status_code == 400
        assert response.data == CANT_ADD_TWO_SIMILAR_INGREDIENT

    def test_create_recipe_if_slug_exists(self, api_client, new_author, recipe_data):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        slug = "varenye-iaitsa"
        api_client.force_authenticate(user=new_author)
        response = api_client.post("/api/v1/recipe/", recipe_data, format="json")
        assert response.status_code == 201
        assert response.data["slug"] == slug

        response = api_client.post("/api/v1/recipe/", recipe_data, format="json")
        assert response.status_code == 201
        assert response.data["slug"] == slug + "_2"

        response = api_client.post("/api/v1/recipe/", recipe_data, format="json")
        assert response.status_code == 201
        assert response.data["slug"] == slug + "_3"

    def test_create_recipe_with_value_ingredients_less_than_or_equal_to_zero(
        self, api_client, new_author, recipe_data
    ):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["ingredients"] = [0]
        assert (
            api_client.post("/api/v1/recipe/", recipe_data, format="json").status_code
            == 400
        )

    def test_create_recipe_with_len_units_ingredients_less_more_than_30_characters(
        self, api_client, new_author, recipe_data
    ):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["ingredients"][0]["unit"] = ["a" * 31]
        assert (
            api_client.post("/api/v1/recipe/", recipe_data, format="json").status_code
            == 400
        )

    def test_create_recipe_with_cooking_time_less_than_ten_minutes(
        self, api_client, new_author, recipe_data
    ):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["cooking_time"] = 9
        assert (
            api_client.post("/api/v1/recipe/", recipe_data, format="json").status_code
            == 400
        )

    def test_create_recipe_with_tags_name_more_than_100_characters(
        self, api_client, new_author, recipe_data
    ):
        """
        Test for create recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["tag"] = ["a" * 101]
        assert (
            api_client.post("/api/v1/recipe/", recipe_data, format="json").status_code
            == 400
        )

    def test_create_recipe_not_authenticated(self, api_client, recipe_data):
        """
        Test for create recipe not authenticated
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        response = api_client.post("/api/v1/recipe/", recipe_data, format="json")

        assert response.status_code == 401
        assert response.data == CREDENTIALS_WERE_NOT_PROVIDED

    def test_update_recipe(self, api_client, new_author, new_recipe, recipe_data):
        """
        Test for update recipe
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)

        response = api_client.patch(
            f"/api/v1/recipe/{new_recipe.slug}/", recipe_data, format="json"
        )

        assert response.status_code == 200

    def test_update_recipe_by_admin(
        self, api_client, app_admin, new_recipe, recipe_data
    ):
        """
        Test for update recipe
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=app_admin)

        response = api_client.patch(
            f"/api/v1/recipe/{new_recipe.slug}/", recipe_data, format="json"
        )

        assert response.status_code == 200

    def test_update_recipe_not_authenticated(self, api_client, new_recipe, recipe_data):
        """
        Test for update recipe not authenticated
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        response = api_client.patch(
            f"/api/v1/recipe/{new_recipe.slug}/", recipe_data, format="json"
        )

        assert response.status_code == 401
        assert response.data == CREDENTIALS_WERE_NOT_PROVIDED

    def test_update_recipe_not_owner(
        self, api_client, new_user, new_recipe, recipe_data
    ):
        """
        Test for update recipe not owner
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_user)

        response = api_client.patch(
            f"/api/v1/recipe/{new_recipe.slug}/", recipe_data, format="json"
        )

        assert response.status_code == 403
        assert response.data == DONT_HAVE_PERMISSIONS

    def test_delete_recipe(self, api_client, new_author, new_recipe):
        """
        Test for delete recipe
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 204
        assert response.data == RECIPE_SUCCESSFUL_DELETE

    def test_delete_recipe_not_owner(self, api_client, new_user, new_recipe):
        """
        Test for delete recipe not owner
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_user)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 403
        assert response.data == DONT_HAVE_PERMISSIONS

    def test_delete_recipe_by_admin(self, api_client, app_admin, new_recipe):
        """
        Test for delete recipe
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=app_admin)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 204
        assert response.data == RECIPE_SUCCESSFUL_DELETE

    def test_repost_recipe(self, api_client, new_author, new_recipe):
        """
        Test reposting a recipe successfully.
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/repost/
        """
        api_client.force_authenticate(user=new_author)

        response = api_client.post(f"/api/v1/recipe/{new_recipe.slug}/repost/")

        assert response.status_code == 201
        assert response.data == {"detail": "Рецепт успешно добавлен на вашу страницу."}

        # Verify reposted recipe exists
        reposted_recipe = Recipe.objects.filter(
            author=new_author, is_repost=True, slug__startswith=new_recipe.slug
        ).first()
        assert reposted_recipe is not None
        assert reposted_recipe.title == new_recipe.title
        assert reposted_recipe.author == new_author
        assert reposted_recipe.is_repost is True

    def test_repost_already_reposted_recipe(self, api_client, new_author, new_recipe):
        """
        Test reposting a recipe that has already been reposted.
        [POST] http://127.0..1:8000/api/v1/recipe/{slug}/repost/
        """
        api_client.force_authenticate(user=new_author)

        # First repost
        api_client.post(f"/api/v1/recipe/{new_recipe.slug}/repost/")

        # Attempt to repost again
        response = api_client.post(f"/api/v1/recipe/{new_recipe.slug}/repost/")

        assert response.status_code == 400
        assert response.data == {"detail": "Вы уже поделились этим рецептом."}

    def test_repost_recipe_unauthenticated(self, api_client, new_recipe):
        """
        Test reposting a recipe without authentication.
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/repost/
        """
        response = api_client.post(f"/api/v1/recipe/{new_recipe.slug}/repost/")

        assert response.status_code == 401
        assert response.data == {"detail": "Учетные данные не были предоставлены."}

    def test_repost_nonexistent_recipe(self, api_client, new_author):
        """
        Test reposting a non-existent recipe.
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/repost/
        """
        api_client.force_authenticate(user=new_author)

        response = api_client.post("/api/v1/recipe/nonexistent-slug/repost/")

        assert response.status_code == 404
        assert response.data == {"detail": "Страница не найдена."}
