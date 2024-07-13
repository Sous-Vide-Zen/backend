from src.apps.follow.models import Follow
from django.contrib.auth import get_user_model
from factory import RelatedFactoryList
from src.apps.ingredients.models import Ingredient
from django.contrib.contenttypes.models import ContentType
from factory import Faker, LazyAttribute, Sequence, SubFactory, SelfAttribute
from factory.django import DjangoModelFactory
from src.apps.reactions.choices import EmojyChoice
from src.apps.recipes.models import Recipe

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """
    User factory.

    Generate an email, password and a username.
    """

    class Meta:
        model = User

    email = Faker("email")
    password = Faker("password")
    username = Faker("user_name")


class FollowFactory(DjangoModelFactory):
    """
    Follow factory.

    Generates a Follow instance, associating a user with an author.
    """

    class Meta:
        model = Follow

    user = SubFactory(UserFactory)
    author = SubFactory(UserFactory)


class ReactionFactory(DjangoModelFactory):
    """
    Reaction factory.

    Generate an author, object_id, content_type and emoji.
    """

    class Meta:
        model = "reactions.Reaction"

    author = SubFactory(UserFactory)
    object_id = SelfAttribute("recipe.id")
    content_type = LazyAttribute(lambda _: ContentType.objects.get_for_model(Recipe))
    emoji = Faker("random_element", elements=EmojyChoice)


class ViewFactory(DjangoModelFactory):
    """
    View factory.

    Generate a user and recipe.
    """

    class Meta:
        model = "view.ViewRecipes"

    user = Sequence(lambda n: f"test_user_{n}")
    recipe = SelfAttribute("recipe.id")


class CommentFactory(DjangoModelFactory):
    """
    Comment factory.

    Generates an author and associates the comment with a recipe.
    """

    class Meta:
        model = "comments.Comment"

    author = SubFactory(UserFactory)
    recipe = SelfAttribute("recipe.id")


class IngredientFactory(DjangoModelFactory):
    """
    Ingredient factory.

    Generates a unique name for each ingredient.
    """

    class Meta:
        model = Ingredient

    name = Sequence(lambda n: "word #%s" % n)


class RecipeFactory(DjangoModelFactory):
    """
    Recipe factory.

    Generates a recipe with an author, title, slug, full text, ingredients list,
    and cooking time.
    """

    class Meta:
        model = Recipe

    author = SubFactory(UserFactory)
    title = Faker("word")
    slug = Faker("slug")
    full_text = Faker("text")
    ingredients = RelatedFactoryList(IngredientFactory, size=1)
    cooking_time = 10
