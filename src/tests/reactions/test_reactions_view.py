import uuid

import pytest
from django.contrib.contenttypes.models import ContentType

from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from src.base.code_text import (
    SUCCESSFUL_APPRECIATED_COMMENT,
    REACTION_CANCELLED,
    SUCCESSFUL_APPRECIATED_RECIPE,
)


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

    def test_existing_recipe_reaction_create_view(
        self, api_client, new_user, new_recipe
    ):
        slug = new_recipe.slug
        reaction_default = Reaction.objects.create(
            author=new_user,
            object_id=new_recipe.id,
            content_type=ContentType.objects.get_for_model(new_recipe),
            is_deleted=True,
        )
        url = f"/api/v1/recipe/{slug}/reactions/"
        api_client.force_authenticate(user=new_user)
        response = api_client.post(url, data={"emoji": EmojyChoice.LIKE}, format="json")
        reaction_default.refresh_from_db()
        assert reaction_default.is_deleted == False
        assert response.status_code == 201
        assert response.data == SUCCESSFUL_APPRECIATED_RECIPE

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
        reaction_default.refresh_from_db()

        assert reaction_default.is_deleted == True
        assert response.status_code == 204
        assert response.data == REACTION_CANCELLED

    @pytest.fixture
    def original_recipe(self, new_user):
        return Recipe.objects.create(
            author=new_user,
            title="Original Recipe",
            slug="original-recipe",
            full_text="Original recipe full text",
            short_text="Original recipe short text",
            cooking_time=30,
            is_repost=False,
        )

    @pytest.fixture
    def repost_with_uuid(self, new_user, original_recipe):
        return Recipe.objects.create(
            author=new_user,
            title="Repost Recipe",
            slug=f"{original_recipe.slug}-{uuid.uuid4().hex[:8]}",
            full_text="Repost recipe full text",
            short_text="Repost recipe short text",
            cooking_time=30,
            is_repost=True,
        )

    @pytest.fixture
    def repost_without_uuid(self, new_user, original_recipe):
        return Recipe.objects.create(
            author=new_user,
            title="Invalid Repost",
            slug="original-recipe-slug",
            full_text="Invalid repost full text",
            short_text="Invalid repost short text",
            cooking_time=30,
            is_repost=True,
        )

    def test_reaction_on_repost_creates_on_original(
        self, api_client, new_user, repost_with_uuid, original_recipe
    ):
        api_client.force_authenticate(new_user)

        response = api_client.post(
            f"/api/v1/recipe/{repost_with_uuid.slug}/reactions/",
            {"emoji": EmojyChoice.LIKE},
        )

        assert response.status_code == 201
        assert Reaction.objects.filter(object_id=repost_with_uuid.id).count() == 1
        assert Reaction.objects.filter(object_id=original_recipe.id).count() == 1

    # def test_reaction_on_repost_without_uuid_does_not_create(
    #     self, api_client, new_user, repost_without_uuid, original_recipe
    # ):
    #     api_client.force_authenticate(new_user)

    #     response = api_client.post(
    #         f"/api/v1/recipe/{repost_without_uuid.slug}/reactions/",
    #         {"emoji": EmojyChoice.LIKE},
    #     )

    #     assert response.status_code == 201
    #     assert Reaction.objects.filter(object_id=repost_without_uuid.id).count() == 0
    #     assert Reaction.objects.filter(object_id=original_recipe.id).count() == 0
    #     assert original_recipe.id == repost_without_uuid.id


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

    def test_existing_comment_reaction_create_view(
        self, api_client, new_user, new_comment
    ):
        id = new_comment.id
        reaction_default = Reaction.objects.create(
            author=new_user,
            object_id=id,
            content_type=ContentType.objects.get_for_model(new_comment),
            is_deleted=True,
        )
        url = f"/api/v1/comment/{id}/reactions/"
        api_client.force_authenticate(user=new_user)
        response = api_client.post(url, data={"emoji": EmojyChoice.LIKE}, format="json")
        reaction_default.refresh_from_db()

        assert reaction_default.is_deleted == False
        assert response.status_code == 201
        assert response.data == SUCCESSFUL_APPRECIATED_COMMENT

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
        reaction_default.refresh_from_db()

        assert reaction_default.is_deleted == True
        assert response.status_code == 204
        assert response.data == REACTION_CANCELLED
