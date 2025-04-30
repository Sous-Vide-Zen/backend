from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import CurrentUserDefault, HiddenField
from rest_framework.serializers import IntegerField
from rest_framework.serializers import ModelSerializer, SlugField
from taggit.serializers import TagListSerializerField, TagList

from src.apps.ingredients.serializers import IngredientInRecipeSerializer
from src.apps.recipes.models import Recipe, Category
from src.apps.users.serializers import AuthorInRecipeSerializer
from src.base.code_text import RECIPE_CAN_BE_EDIT_WITHIN_FIRST_DAY
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
        Convert the input value to its representation. If the input value is
        not an instance of TagList, it is converted to a list of dictionaries
        containing the name and slug of each tag. If the input value is
        already an instance of TagList, it is returned as is.

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


class DraftSerializer(ModelSerializer):
    """
    Draft recipe serializer
    """

    draft_title = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ("draft_title", "id", "slug")

    def get_draft_title(self, obj):
        return f"{obj.title} от {obj.pub_date.date()}"


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
            "title",
            "slug",
            "author",
            "preview_image",
            "ingredients",
            "full_text",
            "tag",
            "category",
            "cooking_time",
            "pub_date",
            "updated_at",
        )
        read_only_fields = ("pub_date", "updated_at")

    def validate(self, data):
        """
        Validate data
        """
        if "full_text" in data:
            data["short_text"] = shorten_text(
                data["full_text"], settings.SHORT_RECIPE_SYMBOLS
            )

        return data


class BaseRecipeListSerializer(ModelSerializer):
    """
    Base serializer for list of recipes
    """

    author = AuthorInRecipeSerializer(read_only=True)
    tag = TagSerializer(read_only=True)
    comments_count = IntegerField(read_only=True)
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
            "short_text",
            "tag",
            "comments_count",
            "reactions_count",
            "views_count",
            "cooking_time",
            "pub_date",
        )


class RecipeRetrieveSerializer(BaseRecipeSerializer):
    """
    Recipe serializer
    """

    author = AuthorInRecipeSerializer(read_only=True)
    category = CategorySerializer(many=True, required=False)
    reactions_count = IntegerField(read_only=True)
    views_count = IntegerField(read_only=True)

    class Meta(BaseRecipeSerializer.Meta):
        fields = BaseRecipeSerializer.Meta.fields + (
            "reactions_count",
            "views_count",
            "updated_at",
        )


class RecipePublicateSerializer(BaseRecipeSerializer):
    """
    Publicate recipe serializer
    """

    ingredients = IngredientInRecipeSerializer(many=True, read_only=True)

    class Meta(BaseRecipeSerializer.Meta):
        fields = BaseRecipeSerializer.Meta.fields + ("published",)


class RecipeUpdateSerializer(BaseRecipeSerializer):
    """
    Update recipe serializer
    """

    slug = SlugField(read_only=True)
    cooking_time = serializers.IntegerField(max_value=60 * 24, min_value=10)

    class Meta(BaseRecipeSerializer.Meta):
        fields = BaseRecipeSerializer.Meta.fields

    def update(self, instance, validated_data):
        """
        Update recipe
        """
        if instance.published and timezone.now() - instance.pub_date > timedelta(
            days=1
        ):
            raise PermissionDenied(
                RECIPE_CAN_BE_EDIT_WITHIN_FIRST_DAY, code="restriction_per_day"
            )
        if instance.published and "title" in validated_data:
            validated_data = create_recipe_slug(Recipe, validated_data)

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
