from rest_framework import serializers
from taggit.serializers import TagListSerializerField

from src.apps.reactions.models import Reaction
from src.apps.recipes.models import Recipe
from src.apps.users.models import CustomUser


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["author", "pub_date", "emoji"]


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "avatar"]


class FeedSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField()
    views_count = serializers.IntegerField()
    reactions = ReactionSerializer(many=True, read_only=True)
    tag = TagListSerializerField()
    author = AuthorSerializer()
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
            "comments_count",
            "views_count",
            "reactions",
            "tag",
            "reactions",
            "activity_count",
        ]
