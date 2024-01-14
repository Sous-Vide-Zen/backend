from src.apps.recipes.models import Recipe
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from src.apps.reactions.models import Reaction


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["author", "pub_date", "emoji"]


class FeedSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    tag = TagListSerializerField()
    author = serializers.CharField(source="author.username")
    activity_count = serializers.SerializerMethodField()

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

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_views_count(self, obj):
        return obj.views.count()

    def get_reactions(self, obj):
        reactions = obj.reactions
        serializer = ReactionSerializer(reactions, many=True)
        return serializer.data

    def get_activity_count(self, obj):
        return obj.comments.count() + obj.views.count() + obj.reactions.count()
