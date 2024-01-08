from src.apps.recipes.models import Recipe
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer


class FeedSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField("get_comments_count")
    views_count = serializers.SerializerMethodField("get_view_count")
    reactions_count = serializers.SerializerMethodField("get_reactions")
    tag = TagListSerializerField()
    author = serializers.CharField(source="author.username")

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "short_text",
            "author",
            "pub_date",
            "tag",
            "cooking_time",
            "comments_count",
            "views_count",
            "reactions_count",
            "tag",
        ]
        depth = 1

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_view_count(self, obj):
        return obj.views.count()

    def get_reactions(self, obj):
        return obj.reactions.count()
