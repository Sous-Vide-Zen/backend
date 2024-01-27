from django.conf import settings
import pytest
from src.apps.recipes.models import Recipe


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedPagination:
    page_size = settings.FEED_PAGE_SIZE

    @pytest.mark.parametrize(
        "recipes_num",
        list(range(settings.FEED_PAGE_SIZE, settings.FEED_PAGE_SIZE * 3, 3)),
    )
    def test_feed_pagination(self, api_client, new_user, recipes_num):
        title, full_text = "recipe_title", "recipe full text"
        # creating recipes
        for i in range(recipes_num):
            Recipe.objects.create(
                author=new_user,
                title=f"{title}_{i}",
                full_text=full_text,
                cooking_time=10,
            )

        # first page
        next_page_url = "/api/v1/feed/"
        recipes_seen, recipes_to_see = 0, recipes_num
        # next pages
        while recipes_seen < TestFeedPagination.page_size * (
            recipes_num // TestFeedPagination.page_size
        ):
            response = api_client.get(next_page_url)
            num_recipes = len(response.data["results"])
            recipes_seen += num_recipes
            recipes_to_see -= num_recipes
            assert num_recipes == TestFeedPagination.page_size
            next_page_url = response.data["next"]

        # last page
        if recipes_to_see:
            response = api_client.get(next_page_url)
            next_page_url = response.data["next"]
            assert next_page_url is None
            assert len(response.data["results"]) == recipes_to_see
