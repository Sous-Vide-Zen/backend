from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import (
    ModelSerializer,
    IntegerField,
    SlugField,
)
from taggit.serializers import TagListSerializerField, TagList

from config.settings import SHORT_RECIPE_SYMBOLS
from src.apps.ingredients.serializers import IngredientInRecipeSerializer
from src.apps.recipes.models import Recipe, Category
from src.apps.users.serializers import AuthorInRecipeSerializer
from src.base.services import (
    shorten_text,
    create_ingredients_in_recipe,
    create_recipe_slug,
)


class CategorySerializer(ModelSerializer):
    """
    Category serializer
    """

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
        )


class TagSerializer(TagListSerializerField):
    """
    Tag serializer
    """

    def to_internal_value(self, data):
        # Вызов родительского метода для получения списка тегов
        tag_list = super().to_internal_value(data)

        # Проверка длины каждого тега
        for tag_name in tag_list:
            if len(tag_name) > 100:
                raise serializers.ValidationError(
                    "Максимальная длина тега - 100 символов."
                )

        return tag_list

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


class BaseRecipeSerializer(ModelSerializer):
    """
    Base recipe serializer
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

        if "full_text" in data:
            data["short_text"] = shorten_text(data["full_text"], SHORT_RECIPE_SYMBOLS)

        if "title" in data:
            data = create_recipe_slug(Recipe, data)

        return data


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
            "tag",
            "reactions_count",
            "views_count",
            "category",
            "cooking_time",
            "pub_date",
            "updated_at",
        )


class RecipeCreateSerializer(BaseRecipeSerializer):
    """
    Create recipe serializer
    """

    class Meta(BaseRecipeSerializer.Meta):
        fields = BaseRecipeSerializer.Meta.fields

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


class RecipeUpdateSerializer(BaseRecipeSerializer):
    """
    Update recipe serializer
    """

    slug = SlugField(read_only=True)

    class Meta(BaseRecipeSerializer.Meta):
        fields = BaseRecipeSerializer.Meta.fields

    def update(self, instance, validated_data):
        """
        Update recipe
        """
        if timezone.now() - instance.pub_date > timedelta(days=1):
            raise PermissionDenied(
                "Обновление рецепта возможно только в течение суток после создания."
            )

        tags_data = validated_data.pop("tag", [])
        ingredients_data = (
            self.initial_data["ingredients"]
            if "ingredients" in self.initial_data
            else None
        )
        validated_data.pop("ingredients", [])
        category_data = validated_data.pop("category", [])

        if tags_data:
            instance.tag.set(tags_data)
        if category_data:
            instance.category.set(category_data)
        if ingredients_data:
            instance.ingredients.clear()
            ingredients_instance = create_ingredients_in_recipe(
                instance, ingredients_data
            )
            if ingredients_instance:
                instance.ingredients.set(ingredients_instance)

        return super().update(instance, validated_data)
