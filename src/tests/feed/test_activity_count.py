from datetime import datetime, timedelta
import pytest
from django.utils.timezone import make_aware

from config.settings import ACTIVITY_INTERVAL
from src.apps.comments.models import Comment
from src.apps.reactions.models import Reaction
from src.apps.view.models import ViewRecipes
from src.tests.factories.factories import ReactionFactory, CommentFactory, ViewFactory


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedResponseFields:
    """
    Test activity count in one month
    """

    NUM_NEW_ACTIVITY = 20
    NUM_OLD_ACTIVITY = 10

    def test_activity_count_calculation(self, new_recipe, api_client):
        """
        Count of reactions, views, and comments are correctly calculated in activity_count
        """

        ReactionFactory.create_batch(self.NUM_NEW_ACTIVITY, object_id=new_recipe.id)
        old_reaction = ReactionFactory.create_batch(
            self.NUM_OLD_ACTIVITY, object_id=new_recipe.id
        )

        for reaction in old_reaction:
            reaction.pub_date = make_aware(
                datetime.now() - timedelta(days=ACTIVITY_INTERVAL + 1)
            )

        Reaction.objects.bulk_update(old_reaction, ["pub_date"], batch_size=100)

        url = "/api/v1/feed/?ordering=-activity_count"

        response = api_client.get(url)

        assert response.data["results"][0]["reactions_count"] == 30
        assert response.data["results"][0]["activity_count"] == 20

        ViewFactory.create_batch(self.NUM_NEW_ACTIVITY, recipe=new_recipe)
        old_view = ViewFactory.create_batch(self.NUM_OLD_ACTIVITY, recipe=new_recipe)

        for view in old_view:
            view.created_at = make_aware(
                datetime.now() - timedelta(days=ACTIVITY_INTERVAL + 1)
            )

        ViewRecipes.objects.bulk_update(old_view, ["created_at"], batch_size=100)

        response = api_client.get(url)

        assert response.data["results"][0]["views_count"] == 30
        assert response.data["results"][0]["activity_count"] == 40

        CommentFactory.create_batch(self.NUM_NEW_ACTIVITY, recipe=new_recipe)
        old_comment = CommentFactory.create_batch(
            self.NUM_OLD_ACTIVITY,
            recipe=new_recipe,
            pub_date=make_aware(datetime.now() - timedelta(days=ACTIVITY_INTERVAL + 1)),
        )

        for comment in old_comment:
            comment.pub_date = make_aware(
                datetime.now() - timedelta(days=ACTIVITY_INTERVAL + 1)
            )

        Comment.objects.bulk_update(old_comment, ["pub_date"], batch_size=100)

        response = api_client.get(url)

        assert response.data["results"][0]["comments_count"] == 30
        assert response.data["results"][0]["activity_count"] == 60
