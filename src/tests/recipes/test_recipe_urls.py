import pytest


@pytest.mark.django_db
@pytest.mark.api
class TestRecipeUrls:
    """
    Test recipe urls
    """

    @pytest.fixture(scope="function")
    def recipe_data(self, category_1, category_2, category_3):
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

    def test_retrieve_recipes(self, client, new_recipe):
        """
        Test for retrieve recipes
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        slug_new_recipe = new_recipe.slug
        assert client.get(f"/api/v1/recipe/{slug_new_recipe}/").status_code == 200

    def test_retrive_recipes_not_found(self, client):
        """
        Test for retrieve recipes not found
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        assert client.get("/api/v1/recipe/not-found/").status_code == 404
        assert client.get("/api/v1/recipe/not-found/").data == {"detail": "Not found."}

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

    def test_create_recipe_not_authenticated(self, api_client, recipe_data):
        """
        Test for create recipe not authenticated
        [POST] http://127.0.0.1:8000/api/v1/recipe/
        """

        response = api_client.post("/api/v1/recipe/", recipe_data, format="json")

        assert response.status_code == 401
        assert response.data == {
            "detail": "Authentication credentials were not provided."
        }

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

    def test_update_recipe_by_admin(self, api_client, app_admin, new_recipe, recipe_data):
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
        assert response.data == {
            "detail": "Authentication credentials were not provided."
        }

    def test_update_recipe_not_owner(self, api_client, new_user, new_recipe, recipe_data):
        """
        Test for update recipe not owner
        [PATCH] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_user)

        response = api_client.patch(
            f"/api/v1/recipe/{new_recipe.slug}/", recipe_data, format="json"
        )

        assert response.status_code == 403
        assert response.data == {"detail": "You do not have permission to perform this action."}

    def test_delete_recipe(self, api_client, new_author, new_recipe):
        """
        Test for delete recipe
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_author)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 204
        assert response.data == {"message": "Рецепт успешно удален"}

    def test_delete_recipe_not_owner(self, api_client, new_user, new_recipe):
        """
        Test for delete recipe not owner
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=new_user)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 403
        assert response.data == {"detail": "You do not have permission to perform this action."}

    def test_delete_recipe_by_admin(self, api_client, app_admin, new_recipe):
        """
        Test for delete recipe
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/
        """

        api_client.force_authenticate(user=app_admin)

        response = api_client.delete(f"/api/v1/recipe/{new_recipe.slug}/")

        assert response.status_code == 204
        assert response.data == {"message": "Рецепт успешно удален"}