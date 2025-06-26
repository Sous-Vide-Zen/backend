from collections import OrderedDict

from src.apps.recipes.models import Recipe
import pytest

from src.apps.recipes.models import Recipe
from src.base.code_text import (
    AMOUNT_OF_DRAFTS_LESS_THAN_THREE,
    PAGE_NOT_FOUND,
    CANT_ADD_TWO_SIMILAR_INGREDIENT,
    CREDENTIALS_WERE_NOT_PROVIDED,
    DONT_HAVE_PERMISSIONS,
    RECIPE_SUCCESSFUL_DELETE,
    NAME_OF_INGREDIENT_LESS_THAN_HUNDRED_SYMBLS,
    ENTER_RECIPE_NAME_BEFORE_PUBLISHING,
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

    def test_create_draft(self, api_client, new_author):
        """
        Test for create draft recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)
        assert list(Recipe.objects.all()) == []

        response = api_client.post("/api/v1/recipe/", format="json")
        draft_recipe = Recipe.objects.all()[0]

        assert response.status_code == 201
        assert draft_recipe.published == False
        assert draft_recipe.title == "Черновик"
        assert draft_recipe.slug == f"{new_author.username}_chernovik_1"

    def test_create_more_than_three_drafts(self, api_client, new_author):
        """
        Test for create more than three drafts of recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        api_client.force_authenticate(user=new_author)
        assert list(Recipe.objects.all()) == []

        for _ in range(3):
            response = api_client.post("/api/v1/recipe/", format="json")
        draft_recipes = list(Recipe.objects.all())

        assert len(draft_recipes) == 3
        for i in range(3):
            assert str(draft_recipes[i]) == f"{new_author.username}_chernovik_{i+1}"

        fourth_draft_response = api_client.post("/api/v1/recipe/", format="json")
        assert fourth_draft_response.status_code == 400
        assert fourth_draft_response.data == AMOUNT_OF_DRAFTS_LESS_THAN_THREE

    def test_create_recipe_with_name_ingredient_more_than_100_characters(
        self, api_client, new_author, recipe_data, draft_recipe
    ):
        """
        Test for create new recipe data by updating its draft
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["ingredients"] = [{"name": "a" * 101}]

        response = api_client.patch(
            f"/api/v1/recipe/{draft_recipe.slug}/", recipe_data, format="json"
        )
        assert response.data == {
            "ingredients": [{"name": [NAME_OF_INGREDIENT_LESS_THAN_HUNDRED_SYMBLS]}]
        }
        assert response.status_code == 400

    def test_create_recipe_with_2_equal_ingredients(
        self, api_client, new_author, recipe_data, draft_recipe
    ):
        """
        Test for create new recipe data by updating its draft
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["ingredients"].append(recipe_data["ingredients"][0])
        response = api_client.patch(
            f"/api/v1/recipe/{draft_recipe.slug}/", recipe_data, format="json"
        )
        assert response.status_code == 400
        assert str(response.data[0]) == (
            f"Проверьте заполнение полей ({CANT_ADD_TWO_SIMILAR_INGREDIENT},) в поле 'ingredients'."
        )

    def test_create_recipe_with_value_ingredients_less_than_or_equal_to_zero(
        self, api_client, new_author, recipe_data, draft_recipe
    ):
        """
        Test for create new recipe data by updating its draft
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["ingredients"] = [0]
        assert (
            api_client.patch(
                f"/api/v1/recipe/{draft_recipe.slug}/", recipe_data, format="json"
            ).status_code
            == 400
        )

    def test_create_recipe_with_len_units_ingredients_less_more_than_30_characters(
        self, api_client, new_author, recipe_data, draft_recipe
    ):
        """
        Test for create new recipe data by updating its draft
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["ingredients"][0]["unit"] = ["a" * 31]
        assert (
            api_client.patch(
                f"/api/v1/recipe/{draft_recipe.slug}/", recipe_data, format="json"
            ).status_code
            == 400
        )

    def test_create_recipe_with_cooking_time_less_than_ten_minutes(
        self, api_client, new_author, recipe_data, draft_recipe
    ):
        """
        Test for create new recipe data by updating its draft
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["cooking_time"] = 9
        response = api_client.patch(
            f"/api/v1/recipe/{draft_recipe.slug}/", recipe_data, format="json"
        )

        assert response.status_code == 400

    def test_create_recipe_with_tags_name_more_than_100_characters(
        self, api_client, new_author, recipe_data, draft_recipe
    ):
        """
        Test for create new recipe data by updating its draft
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)
        recipe_data["tag"] = ["a" * 101]
        assert (
            api_client.patch(
                f"/api/v1/recipe/{draft_recipe.slug}/", recipe_data, format="json"
            ).status_code
            == 400
        )

    def test_create_recipe_not_authenticated(self, api_client, recipe_data):
        """
        Test for create draft recipe not authenticated
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        response = api_client.post("/api/v1/recipe/", recipe_data, format="json")

        assert response.status_code == 401
        assert response.data == CREDENTIALS_WERE_NOT_PROVIDED

    def test_update_draft_recipe(
        self, api_client, new_author, recipe_data, draft_recipe
    ):
        """
        Test for update draft recipe
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)

        response = api_client.patch(
            f"/api/v1/recipe/{draft_recipe.slug}/", recipe_data, format="json"
        )

        assert response.status_code == 200
        assert draft_recipe.published == False

    def test_publicate_recipe_without_reqiered_fields(
        self, api_client, new_author, draft_recipe, new_ingredient_in_recipe
    ):
        """
        Test for publicating recipe without title indicated in request data
        [POST] http://127.0.0.1:8000/api/v1/recipe/drafts/{slug}/publicate/
        """
        api_client.force_authenticate(user=new_author)

        request_data = {
            "full_text": "Published text",
            "ingredients": [
                OrderedDict(
                    [
                        ("name", new_ingredient_in_recipe.ingredient.name),
                        ("unit", new_ingredient_in_recipe.unit.name),
                        ("amount", new_ingredient_in_recipe.amount),
                    ]
                )
            ],
        }
        response = api_client.post(
            f"/api/v1/recipe/drafts/{draft_recipe.slug}/publicate/", format="json"
        )
        response = api_client.patch(
            f"/api/v1/recipe/{draft_recipe.slug}/", request_data, format="json"
        )
        response = api_client.post(
            f"/api/v1/recipe/drafts/{draft_recipe.slug}/publicate/", format="json"
        )

        assert response.status_code == 400
        assert response.data[0] == ENTER_RECIPE_NAME_BEFORE_PUBLISHING

    # def test_publicate_recipe_with_slug_in_request_data(
    #     self, api_client, new_author, draft_recipe, new_ingredient_in_recipe
    # ):
    #     """
    #     Test for publicating recipe with slug indicated in request data
    #     [POST] http://127.0.0.1:8000/api/v1/recipe/drafts/{slug}/publicate/
    #     """

    #     request_data = {
    #         "title": "Test title",
    #         "full_text": "Published text",
    #         "ingredients": [
    #             OrderedDict(
    #                 [
    #                     ("name", new_ingredient_in_recipe.ingredient.name),
    #                     ("unit", new_ingredient_in_recipe.unit.name),
    #                     ("amount", new_ingredient_in_recipe.amount),
    #                 ]
    #             )
    #         ],
    #     }

    #     api_client.force_authenticate(user=new_author)
    #     response = api_client.patch(
    #         f"/api/v1/recipe/{draft_recipe.slug}/", request_data, format="json"
    #     )

    #     request_data = {"slug": "varenye-iaitsa"}
    #     response = api_client.post(
    #         f"/api/v1/recipe/drafts/{draft_recipe.slug}/publicate/",
    #         request_data,
    #         format="json",
    #     )
    #     assert response.status_code == 200
    #     assert response.data["slug"] == "varenye-iaitsa"

    def test_publicate_recipe(
        self, api_client, new_author, draft_recipe, new_ingredient_in_recipe
    ):
        request_data = {
            "title": "Published_title",
            "full_text": "Published text",
            "ingredients": [
                OrderedDict(
                    [
                        ("name", new_ingredient_in_recipe.ingredient.name),
                        ("unit", new_ingredient_in_recipe.unit.name),
                        ("amount", new_ingredient_in_recipe.amount),
                    ]
                )
            ],
        }

        api_client.force_authenticate(user=new_author)
        response = api_client.patch(
            f"/api/v1/recipe/{draft_recipe.slug}/", request_data, format="json"
        )

        response = api_client.post(
            f"/api/v1/recipe/drafts/{draft_recipe.slug}/publicate/",
            format="json",
        )

        assert response.status_code == 200
        assert response.data["title"] == "Published_title"
        assert response.data["slug"] == "published_title"
        assert Recipe.objects.all()[0].published == True

    def test_update_published_recipe(
        self, api_client, new_author, new_recipe, recipe_data
    ):
        """
        Test for update published recipe
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

    def test_repost_recipe(self, api_client, new_user, new_recipe):
        """
        Test reposting a recipe successfully.
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/repost/
        """
        api_client.force_authenticate(user=new_user)

        response = api_client.post(f"/api/v1/recipe/{new_recipe.slug}/repost/")

        assert response.status_code == 201
        assert response.data == {"detail": "Рецепт успешно добавлен на вашу страницу."}

        # Verify reposted recipe exists
        reposted_recipe = Recipe.objects.filter(
            author=new_user, is_repost=True, original_recipe=new_recipe
        ).first()
        assert reposted_recipe is not None
        assert reposted_recipe.title == new_recipe.title
        assert reposted_recipe.author == new_user
        assert reposted_recipe.is_repost is True

    def test_repost_already_reposted_recipe(self, api_client, new_user, new_recipe):
        """
        Test reposting a recipe that has already been reposted.
        [POST] http://127.0..1:8000/api/v1/recipe/{slug}/repost/
        """
        api_client.force_authenticate(user=new_user)

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
