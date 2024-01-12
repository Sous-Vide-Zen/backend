from rest_framework import viewsets
from src.apps.recipes.models import Recipe
from rest_framework.response import Response
from .serializers import FeedSerializer


class FeedUserList(viewsets.ViewSet):
    """
    Listing all created user's posts
    """

    def list(self, request):
        user = request.user
        queryset = Recipe.objects.filter(author=user)
        serializer = FeedSerializer(queryset, many=True)
        return Response(serializer.data)
