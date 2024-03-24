import pytest
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from src.apps.comments.models import Comment
from src.apps.view.models import ViewRecipes
import random
from config.settings import ACTIVITY_INTERVAL
from django.utils.timezone import make_aware


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedResponseFields:
    """
    Test activity count in one month
    """

    def test_activity_count_calculation(self, new_user, api_client, django_user_model):
        """
        Count of reactions, views, and comments are correctly calculated in activity_count
        """

        title, full_text = "recipe", "recipe full text"
        last_month_start = make_aware(
            datetime.now() - timedelta(days=ACTIVITY_INTERVAL)
        )

        new_recipe = Recipe.objects.create(
            author=new_user,
            title=title,
            full_text=full_text,
            cooking_time=10,
            slug=f"recipe",
        )
        users = [
            django_user_model.objects.create_user(
                username=f"user{i}", email=f"testemail{i}@gmail.com", password="test"
            )
            for i in range(random.randint(10, 20))
        ]

        content_type = ContentType.objects.get_for_model(Recipe)
        for user in users:
            for choice in EmojyChoice:
                Reaction.objects.create(
                    author=user,
                    object_id=new_recipe.id,
                    content_type=content_type,
                    emoji=choice,
                )

        for _ in range(random.randint(10, 100)):
            Comment.objects.create(
                author=new_user,
                recipe=new_recipe,
                text="Test Comment",
                pub_date=last_month_start,
            )

        for _ in range(random.randint(10, 100)):
            ViewRecipes.objects.create(
                recipe=new_recipe,
                user=new_user,
                created_at=last_month_start,
            )

        url = "/api/v1/feed/?ordering=-activity_count"
        response = api_client.get(url)

        assert response.status_code == 200

        for result in response.data["results"]:

            activity_count = (
                result["total_comments_count"]
                + result["total_views_count"]
                + result["total_reactions_count"]
            )
            assert result["activity_count"] == activity_count
