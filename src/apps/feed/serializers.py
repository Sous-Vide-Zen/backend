from rest_framework import serializers
from taggit.serializers import TagListSerializerField

from django.db.models import Count

from src.apps.recipes.models import Recipe
from src.apps.users.serializers import AuthorInRecipeSerializer


class FeedSerializer(serializers.ModelSerializer):
    """
    Reflection of Feed page with count of emojies by type in reactions field
    """

    total_comments_count = serializers.IntegerField()
    total_views_count = serializers.IntegerField()
    total_reactions_count = serializers.IntegerField()
    tag = TagListSerializerField()
    author = AuthorInRecipeSerializer(read_only=True)
    activity_count = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "short_text",
            "preview_image",
            "author",
            "pub_date",
            "tag",
            "cooking_time",
            "total_comments_count",
            "total_views_count",
            "total_reactions_count",
            "reactions",
            "activity_count",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        reactions_queryset = instance.reactions.values("emoji").annotate(
            count=Count("emoji")
        )
        representation["reactions"] = {
            reaction["emoji"]: reaction["count"] for reaction in reactions_queryset
        }
        return representation
