from django.conf import settings
import pytest
from src.apps.recipes.models import Recipe


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedPagination:
    def test_feed_pagination(self, api_client, new_user):
        page_size = settings.FEED_PAGE_SIZE
        title, full_text = "recipe_title", "recipe full text"
        # creating recipes
        recipes_num = int(page_size * 3.5)
        for i in range(recipes_num):
            Recipe.objects.create(
                author=new_user,
                title=f"{title}_{i}",
                full_text=full_text,
                cooking_time=10,
            )

        # first page
        url = "/api/v1/feed/"
        response = api_client.get(url)
        recipes_seen, recipes_to_see = 0, recipes_num
        # next pages
        while recipes_seen < page_size * (recipes_num // page_size):
            num_recipes = len(response.data["results"])
            assert num_recipes == page_size
            next_page_url = response.data["next"]
            response = api_client.get(next_page_url)
            recipes_seen += num_recipes
            recipes_to_see -= num_recipes
        # last page
        assert response.data["next"] is None
        assert len(response.data["results"]) == recipes_to_see
