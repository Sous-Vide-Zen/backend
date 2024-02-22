from rest_framework import serializers
from taggit.serializers import TagListSerializerField

from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from src.apps.users.serializers import AuthorInRecipeSerializer


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["author", "pub_date", "emoji"]


class FeedSerializer(serializers.ModelSerializer):
    total_comments_count = serializers.IntegerField()
    total_views_count = serializers.IntegerField()
    total_reactions_count = serializers.IntegerField()
    reactions = ReactionSerializer(many=True, read_only=True)
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
            "tag",
            "reactions",
            "activity_count",
        ]
