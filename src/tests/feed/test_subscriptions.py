import pytest
from src.apps.recipes.models import Recipe
from datetime import datetime, timedelta
from src.apps.comments.models import Comment
from src.apps.follow.models import Follow


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedSubscriptions:
    def test_order_by_activity_count(
        self,
        django_user_model,
        api_client,
    ):
        """
        Only posts of author subscribed to are returned
        """
        # create token
        new_user = django_user_model.objects.create_user(
            username="test", password="changeme123", email="test@ya.ru"
        )
        response = api_client.post(
            "/api/v1/auth/jwt/create/",
            data={"password": "changeme123", "email": "test@ya.ru"},
            format="json",
        )
        token = f'Bearer {response.data["access"]}'
        # create new user1
        new_user1 = django_user_model.objects.create_user(
            username="test1", password="changeme123", email="test1@ya.ru"
        )
        # create new user2
        new_user2 = django_user_model.objects.create_user(
            username="test2", password="changeme123", email="test2@ya.ru"
        )
        title, full_text = "recipe", "recipe full text"
        # creating recipes
        num_recipes = 3
        for i in range(num_recipes):
            Recipe.objects.create(
                author=new_user,
                title=title,
                full_text=full_text,
                cooking_time=10,
            )
            Recipe.objects.create(
                author=new_user1,
                title=title,
                full_text=full_text,
                cooking_time=10,
            )

            Recipe.objects.create(
                author=new_user2,
                title=title,
                full_text=full_text,
                cooking_time=10,
            )
        # new_user follow new_user1
        Follow.objects.create(user=new_user, author=new_user1)
        # add token to request header
        api_client.credentials(HTTP_AUTHORIZATION=token)
        url = "/api/v1/feed/?filter=subscriptions"
        response = api_client.get(url)
        assert [r["author"]["username"] for r in response.data["results"]] == [
            new_user1.username
        ] * num_recipes
