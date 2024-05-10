import pytest
from django.contrib.auth import get_user_model
from factory import Faker, RelatedFactoryList, Sequence, SubFactory
from factory.django import DjangoModelFactory

from src.apps.follow.models import Follow
from src.apps.ingredients.models import Ingredient
from src.apps.recipes.models import Recipe

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = Faker("email")
    password = Faker("password")
    username = Faker("user_name")


class IngredientFactory(DjangoModelFactory):
    class Meta:
        model = Ingredient

    name = Sequence(lambda n: "word #%s" % n)


class RecipeFactory(DjangoModelFactory):
    class Meta:
        model = Recipe

    author = SubFactory(UserFactory)
    title = Faker("word")
    slug = Faker("slug")
    full_text = Faker("text")
    ingredients = RelatedFactoryList(IngredientFactory, size=1)
    cooking_time = 10


class FollowFactory(DjangoModelFactory):
    class Meta:
        model = Follow

    user = SubFactory(UserFactory)
    author = SubFactory(UserFactory)


@pytest.mark.feed
@pytest.mark.api
@pytest.mark.django_db
class TestFeedUsernames:
    """
    Test Feed Usernames
    """

    def test_feed_subscriptions(self, api_client):
        """
        Only posts of author subscribed to are returned
        """

        new_user = UserFactory()
        new_user1 = UserFactory()
        new_user2 = UserFactory()

        title, full_text = "recipe", "recipe full text"
        num_recipes = 3
        for i in range(num_recipes):
            for user in [new_user, new_user1, new_user2]:
                RecipeFactory(
                    author=user,
                    title=title,
                    full_text=full_text,
                    cooking_time=10,
                    published=True,
                )

        FollowFactory(user=new_user, author=new_user1)

        api_client.force_authenticate(user=new_user)

        url = "/api/v1/feed/?filter=subscriptions"
        response = api_client.get(url)

        assert [r["author"]["username"] for r in response.data["results"]] == [
            new_user1.username
        ] * num_recipes

        url = f"/api/v1/feed/?username={new_user2.username}"
        response = api_client.get(url)
        assert [r["author"]["username"] for r in response.data["results"]] == [
            new_user2.username
        ] * num_recipes
