import pytest
from django.contrib.contenttypes.models import ContentType

from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction


@pytest.mark.reactions
@pytest.mark.models
class TestRecipeReactionsUrl:
    def test_recipe_reaction_create_url(self, api_client, new_user, new_recipe):
        """
        Recipe reaction create test
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/
        """
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/reactions/"
        api_client.force_authenticate(user=new_user)

        response_default = api_client.post(url, data={}, format="json")
        response_duplicate = api_client.post(url, data={"emoji": "Like"}, format="json")

        assert response_default.status_code == 201
        assert response_default.data == {"message": "Вы оценили рецепт!"}
        assert new_recipe.reactions.values("emoji")[0]["emoji"] == EmojyChoice.LIKE
        assert response_duplicate.status_code == 403
        assert response_duplicate.data == {
            "detail": "Вы уже поставили такую реакцию к данному рецепту"
        }

    def test_recipe_reaction_create_non_authorized(
        self, api_client, new_user, new_recipe
    ):
        """
        Recipe reaction create test for non-authorized user
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/
        """
        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/reactions/"
        response = api_client.post(url, data={"emoji": "Like"}, format="json")
        assert response.status_code == 401
        assert response.data == {"detail": "Учетные данные не были предоставлены."}

    def test_recipe_reaction_create_recipe_not_found(
        self, api_client, new_user, new_recipe
    ):
        """
        Recipe reaction create test for not found recipe
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/
        """
        url = f"/api/v1/recipe/slug-of-non-existing-recipe/reactions/"
        api_client.force_authenticate(user=new_user)
        response = api_client.post(url, data={"emoji": "Like"}, format="json")
        assert response.status_code == 404
        assert response.data == {"detail": "Страница не найдена."}

    def test_recipe_reaction_delete_url(self, api_client, new_user, new_recipe):
        """
        Recipe reaction delete test
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/{reaction_id}
        """
        reaction_default = Reaction.objects.create(
            author=new_user,
            object_id=new_recipe.id,
            content_type=ContentType.objects.get_for_model(new_recipe),
        )
        slug = new_recipe.slug
        url_reaction_not_found = f"/api/v1/recipe/{slug}/reactions/2/"
        url_recipe_not_found = (
            f"/api/v1/recipe/non-existing-recipe/reactions/{reaction_default.id}/"
        )
        url = f"/api/v1/recipe/{slug}/reactions/{reaction_default.id}/"

        response_non_authorized = api_client.delete(url)
        assert response_non_authorized.status_code == 401
        assert response_non_authorized.data == {
            "detail": "Учетные данные не были предоставлены."
        }

        api_client.force_authenticate(user=new_user)

        response_not_found_reaction = api_client.delete(url_reaction_not_found)
        assert response_not_found_reaction.status_code == 404
        assert response_not_found_reaction.data == {"detail": "Страница не найдена."}

        response_not_found_recipe = api_client.delete(url_recipe_not_found)
        assert response_not_found_recipe.status_code == 404
        assert response_not_found_recipe.data == {"detail": "Страница не найдена."}

        response = api_client.delete(url)
        assert response.status_code == 204
        assert response.data == {"message": "Реакция отменена!"}

    def test_recipe_reactions_list_url(self, api_client, new_user, new_recipe):
        """
        Recipe reaction retrieve test for any user
        [GET] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/
        """
        response = api_client.get(f"/api/v1/recipe/non-existing-recipe/reactions/")
        assert response.status_code == 404
        assert response.data == {"detail": "Страница не найдена."}
        slug = new_recipe.slug
        response = api_client.get(f"/api/v1/recipe/{slug}/reactions/")
        assert response.status_code == 200
        assert response.data == {"reactions": {}, "user_reactions": []}


@pytest.mark.reactions
@pytest.mark.models
class TestCommentReactionsUrl:
    def test_comment_reaction_create_url(self, api_client, new_user, new_comment):
        """
        Comment reaction create test
        [POST] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/
        """
        id = new_comment.id
        url = f"/api/v1/comment/{id}/reactions/"
        api_client.force_authenticate(user=new_user)

        response_default = api_client.post(url, data={}, format="json")
        response_duplicate = api_client.post(url, data={"emoji": "Like"}, format="json")
        assert response_default.status_code == 201
        assert response_default.data == {"message": "Вы оценили комментарий!"}
        assert new_comment.reactions.values("emoji")[0]["emoji"] == EmojyChoice.LIKE
        assert response_duplicate.status_code == 403
        assert response_duplicate.data == {
            "detail": "Вы уже оценили данный комментарий"
        }

    def test_comment_reaction_create_non_authorized(
        self, api_client, new_user, new_comment
    ):
        """
        Comment reaction create test for non-authorized user
        [POST] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/
        """
        id = new_comment.id
        url = f"/api/v1/comment/{id}/reactions/"
        response = api_client.post(url, data={"emoji": "Like"}, format="json")
        assert response.status_code == 401
        assert response.data == {"detail": "Учетные данные не были предоставлены."}

    def test_comment_reaction_create_comment_not_found(
        self, api_client, new_user, new_comment
    ):
        """
        Comment reaction create test for not found comment
        [POST] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/
        """
        url = f"/api/v1/comment/111/reactions/"
        api_client.force_authenticate(user=new_user)
        response = api_client.post(url, data={"emoji": "Like"}, format="json")
        assert response.status_code == 404
        assert response.data == {"detail": "Страница не найдена."}

    def test_comment_reaction_delete_url(self, api_client, new_user, new_comment):
        """
        Comment reaction delete test
        [DELETE] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/{reaction_id}
        """
        reaction_default = Reaction.objects.create(
            author=new_user,
            object_id=new_comment.id,
            content_type=ContentType.objects.get_for_model(new_comment),
        )
        id = new_comment.id
        url_reaction_not_found = f"/api/v1/comment/{id}/reactions/2/"
        url_comment_not_found = f"/api/v1/comment/111/reactions/{reaction_default.id}/"
        url = f"/api/v1/comment/{id}/reactions/{reaction_default.id}/"

        response_non_authorized = api_client.delete(url)
        assert response_non_authorized.status_code == 401
        assert response_non_authorized.data == {
            "detail": "Учетные данные не были предоставлены."
        }

        api_client.force_authenticate(user=new_user)

        response_not_found_reaction = api_client.delete(url_reaction_not_found)
        assert response_not_found_reaction.status_code == 404
        assert response_not_found_reaction.data == {"detail": "Страница не найдена."}

        response_not_found_comment = api_client.delete(url_comment_not_found)
        assert response_not_found_comment.status_code == 404
        assert response_not_found_comment.data == {"detail": "Страница не найдена."}

        response = api_client.delete(url)
        assert response.status_code == 204
        assert response.data == {"message": "Реакция отменена!"}

    def test_comment_reactions_list_url(self, api_client, new_user, new_comment):
        """
        Comment reaction retrieve test for any user
        [GET] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/
        """
        response = api_client.get(f"/api/v1/comment/111/reactions/")
        assert response.status_code == 404
        assert response.data == {"detail": "Страница не найдена."}
        id = new_comment.id
        response = api_client.get(f"/api/v1/comment/{id}/reactions/")
        assert response.status_code == 200
        assert response.data == {"reactions": {}, "user_reactions": []}
