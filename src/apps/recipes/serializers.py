from django.db import transaction
from django.db.models import Count
from django.utils.text import slugify
from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
    IntegerField,
)
from taggit.serializers import TagListSerializerField, TagList
from unidecode import unidecode

from src.apps.ingredients.serializers import IngredientInRecipeSerializer
from src.apps.recipes.models import Recipe, Category
from src.apps.users.serializers import AuthorInRecipeSerializer
from src.base.services import shorten_text, create_ingredients_in_recipe


class CategorySerializer(ModelSerializer):
    """
    Category serializer
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(TagListSerializerField):
    """
    Tag serializer
    """

    def to_representation(self, value):
        """
        Convert the input value to its representation. If the input value is not an instance of TagList, it is converted to a list of dictionaries containing the name and slug of each tag. If the input value is already an instance of TagList, it is returned as is.

        Parameters:
        - value: The input value to be converted

        Returns:
        - The converted representation of the input value
        """
        if not isinstance(value, TagList):
            if not isinstance(value, list):
                if self.order_by:
                    tags = value.all().order_by(*self.order_by)
                else:
                    tags = value.all()
                value = [{"name": tag.name, "slug": tag.slug} for tag in tags]
            value = TagList(value, pretty_print=self.pretty_print)

        return value


class RecipeRetriveSerializer(ModelSerializer):
    """
    Recipe serializer
    """

    ingredients = IngredientInRecipeSerializer(many=True)
    tag = TagSerializer(required=False)
    author = AuthorInRecipeSerializer(read_only=True)
    category = CategorySerializer(many=True, required=False)
    reactions_count = IntegerField(read_only=True)
    views_count = IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "title",
            "slug",
            "author",
            "preview_image",
            "ingredients",
            "full_text",
            "reactions",
            "tag",
            "reactions_count",
            "views_count",
            "category",
            "cooking_time",
            "pub_date",
            "updated_at",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        reactions_queryset = instance.reactions.values("emoji").annotate(
            count=Count("emoji")
        )
        representation["reactions"] = {
            reaction["emoji"]: reaction["count"] for reaction in reactions_queryset
        }
        return representation


class RecipeCreateSerializer(ModelSerializer):
    """
    Create recipe serializer
    """

    author = HiddenField(default=CurrentUserDefault())
    ingredients = IngredientInRecipeSerializer(many=True)
    tag = TagSerializer(required=False)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "title",
            "slug",
            "preview_image",
            "ingredients",
            "full_text",
            "tag",
            "category",
            "cooking_time",
            "pub_date",
            "updated_at",
        )

    def validate(self, data):
        """
        Validate data
        """
        data["short_text"] = shorten_text(data["full_text"], 100)

        with transaction.atomic():
            same_recipes = Recipe.objects.filter(title=data["title"]).count()
            slug_str = unidecode(
                f"{data['title']}_{same_recipes + 1}" if same_recipes else data["title"]
            )
            data["slug"] = slugify(slug_str)

            if Recipe.objects.filter(slug=data["slug"]).exists():
                raise ValidationError("A recipe with this slug already exists.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        """Create recipe"""
        tags_data = validated_data.pop("tag", [])
        ingredients_data = self.initial_data["ingredients"]
        validated_data.pop("ingredients", [])
        category_data = validated_data.pop("category", [])

        recipe = Recipe.objects.create(**validated_data)

        if tags_data:
            recipe.tag.set(tags_data)
        if category_data:
            recipe.category.set(category_data)

        ingredients_instance = create_ingredients_in_recipe(recipe, ingredients_data)

        if ingredients_instance:
            recipe.ingredients.set(ingredients_instance)
        return recipe
