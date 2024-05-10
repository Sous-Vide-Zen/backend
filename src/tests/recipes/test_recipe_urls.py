import pytest
from collections import OrderedDict
from src.apps.recipes.models import Recipe


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

    def test_retrive_recipes_not_found(self, client):
        """
        Test for retrieve recipes not found
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        assert client.get("/api/v1/recipe/not-found/").status_code == 404
        assert client.get("/api/v1/recipe/not-found/").data == {
            "detail": "Страница не найдена."
        }

    def test_create_recipe(self, api_client, new_author):
        """
        Test for create draft recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)

        assert api_client.post("/api/v1/recipe/", format="json").status_code == 201
        assert Recipe.objects.all()[0].published == False

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
        assert response.data == {"errors": "Нельзя добавить два одинаковых ингредиента"}

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
        response = api_client.post("/api/v1/recipe/", recipe_data, format="json")

        assert response.status_code == 400

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
        assert response.data == {"detail": "Учетные данные не были предоставлены."}

    def test_update_and_publish_recipe(
        self, api_client, new_author, new_recipe, recipe_data
    ):
        """
        Test for update recipe
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)

        response = api_client.patch(
            f"/api/v1/recipe/{new_recipe.slug}/", recipe_data, format="json"
        )

        assert response.status_code == 200
        assert new_recipe.published == True

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
        assert response.data == {"detail": "Учетные данные не были предоставлены."}

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
        assert response.data == {
            "detail": "У вас недостаточно прав для выполнения данного действия."
        }

    def test_delete_recipe(self, api_client, new_author, new_recipe):
        """
        Test for delete recipe
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 204
        assert response.data == {"message": "Рецепт успешно удален."}

    def test_delete_recipe_not_owner(self, api_client, new_user, new_recipe):
        """
        Test for delete recipe not owner
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_user)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 403
        assert response.data == {
            "detail": "У вас недостаточно прав для выполнения данного действия."
        }

    def test_delete_recipe_by_admin(self, api_client, app_admin, new_recipe):
        """
        Test for delete recipe
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=app_admin)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 204
        assert response.data == {"message": "Рецепт успешно удален."}
