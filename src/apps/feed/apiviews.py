from rest_framework import viewsets
from src.apps.recipes.models import Recipe
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from .serializers import FeedSerializer


class FeedUserPagination(PageNumberPagination):
    page_size = 5


class FeedUserList(viewsets.ViewSet):
    """
    Listing all created user's posts with pagination and sorting by pub_date
    """

    def list(self, request):
        paginator = FeedUserPagination()
        user = request.user
        queryset = Recipe.objects.filter(author=user).order_by("-pub_date")
        page = paginator.paginate_queryset(queryset, request)
        serializer = FeedSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
