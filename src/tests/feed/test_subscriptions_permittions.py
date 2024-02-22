import pytest
from django.contrib.contenttypes.models import ContentType

from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe


@pytest.mark.feed
@pytest.mark.api
class TestFeedSubscripitonsPermittions:
    def test_subscriptions_list_permittions(
        self,
        new_user,
        api_client,
    ):
        """
        Subscriptions list is available only for authenticated users
        """

        title = "Recipe 1"
        full_text = "recipe 1 full text"

        new_recipe = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
        )

        url = "/api/v1/feed/?filter=subscriptions"
        response = api_client.get(url)

        assert response.status_code == 401
