from datetime import datetime, timedelta

import pytest
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import make_aware
from factory import Faker, LazyAttribute, Sequence, SubFactory, SelfAttribute
from factory.django import DjangoModelFactory

from config.settings import ACTIVITY_INTERVAL
from src.apps.comments.models import Comment
from src.apps.reactions.choices import EmojyChoice
from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from src.apps.view.models import ViewRecipes


class UserFactory(DjangoModelFactory):
    class Meta:
        model = "users.CustomUser"

    email = Faker("email")
    username = Faker("user_name")
    password = Faker("password")


class ReactionFactory(DjangoModelFactory):
    class Meta:
        model = "reactions.Reaction"

    author = SubFactory(UserFactory)
    object_id = SelfAttribute("recipe.id")
    content_type = LazyAttribute(lambda _: ContentType.objects.get_for_model(Recipe))
    emoji = Faker("random_element", elements=EmojyChoice)


class ViewFactory(DjangoModelFactory):
    class Meta:
        model = "view.ViewRecipes"

    user = Sequence(lambda n: f"test_user_{n}")
    recipe = SelfAttribute("recipe.id")


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = "comments.Comment"

    author = SubFactory(UserFactory)
    recipe = SelfAttribute("recipe.id")


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
        old_reaction = ReactionFactory.create_batch(self.NUM_OLD_ACTIVITY, object_id=new_recipe.id)

        for reaction in old_reaction:
            reaction.pub_date = make_aware(datetime.now() - timedelta(days=ACTIVITY_INTERVAL + 1))

        Reaction.objects.bulk_update(old_reaction, ["pub_date"], batch_size=100)

        url = "/api/v1/feed/?ordering=-activity_count"

        response = api_client.get(url)

        assert response.data["results"][0]["total_reactions_count"] == 30
        assert response.data["results"][0]["activity_count"] == 20

        ViewFactory.create_batch(self.NUM_NEW_ACTIVITY, recipe=new_recipe)
        old_view = ViewFactory.create_batch(self.NUM_OLD_ACTIVITY, recipe=new_recipe)

        for view in old_view:
            view.created_at = make_aware(datetime.now() - timedelta(days=ACTIVITY_INTERVAL + 1))

        ViewRecipes.objects.bulk_update(old_view, ["created_at"], batch_size=100)

        response = api_client.get(url)

        assert response.data["results"][0]["total_views_count"] == 30
        assert response.data["results"][0]["activity_count"] == 40

        CommentFactory.create_batch(self.NUM_NEW_ACTIVITY, recipe=new_recipe)
        old_comment = CommentFactory.create_batch(self.NUM_OLD_ACTIVITY, recipe=new_recipe, pub_date=make_aware(datetime.now() - timedelta(days=ACTIVITY_INTERVAL + 1)))

        for comment in old_comment:
            comment.pub_date = make_aware(datetime.now() - timedelta(days=ACTIVITY_INTERVAL + 1))

        Comment.objects.bulk_update(old_comment, ["pub_date"], batch_size=100)

        response = api_client.get(url)

        assert response.data["results"][0]["total_comments_count"] == 30
        assert response.data["results"][0]["activity_count"] == 60
