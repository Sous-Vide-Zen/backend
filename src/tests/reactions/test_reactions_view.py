import pytest
from django.contrib.contenttypes.models import ContentType

from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction


@pytest.mark.reactions
@pytest.mark.models
class TestRecipeReactionsView:
    def test_recipe_reaction_create_view(self, api_client, new_user, new_recipe):
        """
        Recipe reaction create test
        [POST] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/
        """

        slug = new_recipe.slug
        url = f"/api/v1/recipe/{slug}/reactions/"
        api_client.force_authenticate(user=new_user)

        emojies = EmojyChoice.values
        for num in range(len(emojies) - 1):
            api_client.post(url, data={"emoji": emojies[num]}, format="json")
            assert new_recipe.reactions.values("emoji")[num]["emoji"] == emojies[num]

    def test_recipe_reaction_delete_view(self, api_client, new_user, new_recipe):
        """
        Recipe reaction delete test
        [DELETE] http://127.0.0.1:8000/api/v1/recipe/{slug}/reactions/{reaction_id}
        """
        slug = new_recipe.slug
        reaction_default = Reaction.objects.create(
            author=new_user,
            object_id=new_recipe.id,
            content_type=ContentType.objects.get_for_model(new_recipe),
        )
        url = f"/api/v1/recipe/{slug}/reactions/{reaction_default.id}/"
        api_client.force_authenticate(user=new_user)

        response = api_client.delete(url)

        assert response.status_code == 204
        assert response.data == {"message": "Реакция отменена!"}


@pytest.mark.reactions
@pytest.mark.models
class TestCommentReactionsView:
    def test_comment_reaction_create_view(self, api_client, new_user, new_comment):
        """
        Comment reaction create test
        [POST] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/
        """
        id = new_comment.id
        url = f"/api/v1/comment/{id}/reactions/"
        api_client.force_authenticate(user=new_user)

        emojies = EmojyChoice.values
        for num in range(len(emojies) - 1):
            api_client.post(url, data={"emoji": emojies[num]}, format="json")
            assert new_comment.reactions.values("emoji")[num]["emoji"] == emojies[num]

    def test_comment_reaction_delete_view(self, api_client, new_user, new_comment):
        """
        Comment reaction delete test
        [DELETE] http://127.0.0.1:8000/api/v1/comment/{id}/reactions/{reaction_id}
        """
        id = new_comment.id
        reaction_default = Reaction.objects.create(
            author=new_user,
            object_id=new_comment.id,
            content_type=ContentType.objects.get_for_model(new_comment),
        )
        url = f"/api/v1/comment/{id}/reactions/{reaction_default.id}/"
        api_client.force_authenticate(user=new_user)

        response = api_client.delete(url)

        assert response.status_code == 204
        assert response.data == {"message": "Реакция отменена!"}
