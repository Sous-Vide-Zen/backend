import pytest
from rest_framework.test import APIClient
from src.apps.recipes.models import Recipe
from datetime import datetime, timedelta
from src.apps.comments.models import Comment


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedSorting:
    def test_order_by_activity_count(self, api_client, new_user):
        """
        Should be sorted by activity_count desc
        """
        title, full_text = "recipe", "recipe full text"
        expected_activity_count_list = [4, 3, 2, 1, 0]
        # creating recipes
        for i in range(5):
            new_recipe = Recipe.objects.create(
                author=new_user,
                title=title,
                full_text=full_text,
                cooking_time=10,
                slug=f"recipe-{i}",
            )
            for j in range(i):
                # creating comment to recipe
                Comment.objects.create(
                    author=new_user,
                    recipe=new_recipe,
                    text=f"comment {j} to recipe {i}",
                )

        url = "/api/v1/feed/?ordering=-activity_count"
        response = api_client.get(url)
        activity_count_list = [r["activity_count"] for r in response.data["results"]]
        assert activity_count_list == expected_activity_count_list

        url = "/api/v1/feed/?ordering=activity_count"
        response = api_client.get(url)
        activity_count_list = [r["activity_count"] for r in response.data["results"]]
        assert activity_count_list == expected_activity_count_list[::-1]

    def test_order_by_pub_date(self, api_client, new_user):
        title, full_text = "recipe_title", "recipe full text"
        # creating recipes
        for i in range(5):
            new_recipe = Recipe.objects.create(
                author=new_user,
                title=f"{title}_{i}",
                full_text=full_text,
                cooking_time=10,
            )
            new_recipe.pub_date = datetime.now() - timedelta(days=i)
            new_recipe.save()

        url = "/api/v1/feed/"
        response = api_client.get(url)
        pub_date_list = [r["pub_date"] for r in response.data["results"]]
        # check that dates are sorted from latest to earliest
        assert pub_date_list == sorted(pub_date_list, reverse=True)
